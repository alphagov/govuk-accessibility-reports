from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException
from src.report_generators.base_report_generator import BaseReportGenerator

import pandas as pd


class NonEnglishDocsReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ["base_path", "primary_publishing_organisation", "text", "text_languages", "detected_as_english"]

    @property
    def filename(self):
        return "non_english_docs_report.csv"

    def process_page(self, content_item, html):
        if pd.isna(content_item['text']):
            return [content_item['base_path'], content_item['text'], [], content_item.get('detected_as_english',
                                                                                          default=False)]
        # extract primary publishing organisation
        primary_publishing_organisation = self.__primary_org(content_item['organisations'])

        content_item['text'] = str(content_item['text'])

        content_item['text_lang'] = self.detect_languages(content_item['text'])
        languages_dict = dict([(language.lang, language.prob) for language in content_item['text_lang']])

        if 'en' in languages_dict and languages_dict['en'] > 0.5:
            content_item['detected_as_english'] = True

        return [content_item['base_path'],
                primary_publishing_organisation,
                content_item['text'],
                content_item['text_lang'],
                content_item.get('detected_as_english', default=False)]

    def detect_languages(self, text):
        """Detects language of a text, moving onto next text if an error is thrown

        :param text: A string to detect the language of
        :return: A list returning the language detected and confidence score associated to it

        """
        try:
            return detect_langs(text)
        except LangDetectException:
            return []

    @staticmethod
    def __primary_org(content_item_orgs) -> str:
        # Parses Content Item list of Organisations, extracts the Primary Publishing Organisation
        #  and returns its title.
        #  Falls back to first Organisation if there is no Primary Publishing Organisation.
        #
        # Structure of `orgs` would look like:
        # {
        #     'organisations': [
        #         ('b548a09f-8b35-4104-89f4-f1a40bf3136d', 'Department for Work and Pensions', 'D10')
        #     ],
        #     'primary_publishing_organisation': [
        #         ('b548a09f-8b35-4104-89f4-f1a40bf3136d', 'Department for Work and Pensions', 'D10')
        #     ]
        # }

        primary = None
        orgs = ast.literal_eval(content_item_orgs)

        try:
            if orgs is not None:
                primary = (orgs.get('primary_publishing_organisation'))[0][1]
            if primary is None:
                primary = (orgs.get('organisations'))[0][1]
        except TypeError:
            primary = "NO ORG"

        return primary
