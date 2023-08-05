import logging
from html import unescape

import deepl
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.utils.html import strip_tags
from django.utils.translation import gettext as _

from ..cms.utils.translation_utils import mt_is_permitted

logger = logging.getLogger(__name__)


class DeepLApi:
    """
    DeepL API to auto translate selected posts.
    """

    def __init__(self):
        """
        Initialize the DeepL client
        """
        self.translator = deepl.Translator(settings.DEEPL_AUTH_KEY)
        self.translatable_attributes = ["title", "content", "meta_description"]

    @staticmethod
    def check_availability(request, target_language):
        """
        This function checks, if the selected language is supported by DeepL

        :param request: request that was sent to the server
        :type request: ~django.http.HttpRequest

        :param target_language: transmitted target language
        :type target_language: ~integreat_cms.cms.models.languages.language.Language

        :return: true or false
        :rtype: bool
        """
        deepl_config = apps.get_app_config("deepl_api")
        source_language = request.region.get_source_language(target_language.slug)
        return (
            source_language
            and source_language.slug in deepl_config.supported_source_languages
            and (
                target_language.slug in deepl_config.supported_target_languages
                or target_language.bcp47_tag.lower()
                in deepl_config.supported_target_languages
            )
        )

    def get_target_language_key(self, target_language):
        """
        This function decides the correct target language key

        :param target_language: the target language
        :type target_language: ~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation

        :return: target_language_key which is 2 characters long for all languages except English and Portugese where the BCP tag is transmitted
        :rtype: str
        """
        deepl_config = apps.get_app_config("deepl_api")
        for code in [target_language.slug, target_language.bcp47_tag]:
            if code.lower() in deepl_config.supported_target_languages:
                return code
        return None

    def check_usage(self, region, source_translation):
        """
        This function checks if the attempted translation would exceed the region's word limit

        :param region: region for which to check usage
        :type region: ~integreat_cms.cms.models.regions.region.Region

        :param source_translation: single content object
        :type source_translation: ~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation

        :return: translation would exceed limit, region budget, attempted translation word count
        :rtype: (bool, int, int)
        """
        # Gather content to be translated and calculate total word count
        attributes = [
            getattr(source_translation, attr, None)
            for attr in self.translatable_attributes
        ]
        content_to_translate = [
            unescape(strip_tags(attr)) for attr in attributes if attr
        ]

        content_to_translate = " ".join(content_to_translate)
        for char in "-;:,;!?\n":
            content_to_translate = content_to_translate.replace(char, " ")
        word_count = len(content_to_translate.split())

        # Check if translation would exceed DeepL usage limit
        region.refresh_from_db()
        # Allow up to DEEPL_SOFT_MARGIN more words than the actual limit
        word_count_leeway = max(1, word_count - settings.DEEPL_SOFT_MARGIN)
        translation_exceeds_limit = region.deepl_budget_remaining < word_count_leeway

        return (translation_exceeds_limit, word_count)

    # pylint: disable=too-many-locals
    def deepl_translation(self, request, content_objects, language_slug, form_class):
        """
        This functions gets the translation from DeepL

        :param request: passed request
        :type request: ~django.http.HttpRequest

        :param content_objects: passed content objects
        :type content_objects: ~django.db.models.query.QuerySet [ ~integreat_cms.cms.models.abstract_content_model.AbstractContentModel ]

        :param language_slug: current GUI language slug
        :type language_slug: str

        :param form_class: passed Form class of content type
        :type form_class: ~integreat_cms.cms.forms.custom_content_model_form.CustomContentModelForm
        """
        # Re-select the region from db to prevent simultaneous
        # requests exceeding the DeepL usage limit

        with transaction.atomic():
            region = (
                apps.get_model("cms", "Region")
                .objects.select_for_update()
                .get(id=request.region.id)
            )
            # Get target language
            target_language = region.get_language_or_404(language_slug)
            source_language = region.get_source_language(language_slug)

            if content_objects and not mt_is_permitted(
                region,
                request.user,
                type(content_objects[0])._meta.default_related_name,
                language_slug,
            ):
                messages.error(
                    request,
                    _(
                        'Machine translations are disabled for content type "{}", language "{}" or the current user.'
                    ).format(
                        type(content_objects[0])._meta.verbose_name.title(),
                        target_language,
                    ),
                )
                return

            target_language_key = self.get_target_language_key(target_language)

            for content_object in content_objects:
                source_translation = content_object.get_translation(
                    source_language.slug
                )
                if not source_translation:
                    messages.error(
                        request,
                        _('No source translation could be found for {} "{}".').format(
                            type(content_object)._meta.verbose_name.title(),
                            content_object.best_translation.title,
                        ),
                    )
                    continue

                existing_target_translation = content_object.get_translation(
                    target_language.slug
                )

                # Before translating, check if translation would exceed usage limit
                (
                    translation_exceeds_limit,
                    word_count,
                ) = self.check_usage(region, source_translation)
                if translation_exceeds_limit:
                    messages.error(
                        request,
                        _(
                            "Translation from {} to {} not possible: translation of {} words would exceed the remaining budget of {} words."
                        ).format(
                            source_language,
                            target_language,
                            word_count,
                            region.deepl_budget_remaining,
                        ),
                    )
                    continue

                data = {
                    "status": existing_target_translation.status
                    if existing_target_translation
                    else source_translation.status,
                    "machine_translated": True,
                }

                for attr in self.translatable_attributes:
                    # Only translate existing, non-empty attributes
                    if hasattr(source_translation, attr) and getattr(
                        source_translation, attr
                    ):
                        # data has to be unescaped for DeepL to recognize Umlaute
                        data[attr] = self.translator.translate_text(
                            unescape(getattr(source_translation, attr)),
                            source_lang=source_language.slug,
                            target_lang=target_language_key,
                            tag_handling="html",
                        )

                content_translation_form = form_class(
                    data=data,
                    instance=existing_target_translation,
                    additional_instance_attributes={
                        "creator": request.user,
                        "language": target_language,
                        source_translation.foreign_field(): content_object,
                    },
                )
                # Validate event translation
                if content_translation_form.is_valid():
                    content_translation_form.save()
                    logger.debug(
                        "Successfully translated for: %r",
                        content_translation_form.instance,
                    )
                    messages.success(
                        request,
                        _('{} "{}" has successfully been translated ({} ➜ {}).').format(
                            type(content_object)._meta.verbose_name.title(),
                            source_translation.title,
                            source_language,
                            target_language,
                        ),
                    )
                else:
                    logger.error(
                        "Automatic translation for %r could not be created because of %r",
                        content_object,
                        content_translation_form.errors,
                    )
                    messages.error(
                        request,
                        _('{} "{}" could not be translated automatically.').format(
                            type(content_object)._meta.verbose_name.title(),
                            source_translation.title,
                        ),
                    )

                # Update remaining DeepL usage for the region
                region.deepl_budget_used += word_count
                region.save()

    def deepl_translate_to_languages(
        self, request, source_object, target_languages, form_class
    ):
        """
        This function iterates over all descendants of a source language
        and invokes a translation of a single source object into each of
        those languages.

        :param request: passed request
        :type request: ~django.http.HttpRequest

        :param source_object: passed content object
        :type source_object: ~integreat_cms.cms.models.abstract_content_model.AbstractContentModel

        :param target_languages: The target languages into which to translate
        :type target_languages: ~django.db.models.query.QuerySet [ ~integreat_cms.cms.models.languages.language.Language ]

        :param form_class: passed Form class of content type
        :type form_class: ~integreat_cms.cms.forms.custom_content_model_form.CustomContentModelForm
        """
        for language in target_languages:
            if self.check_availability(request, language):
                self.deepl_translation(
                    request,
                    [source_object],
                    language.slug,
                    form_class,
                )
