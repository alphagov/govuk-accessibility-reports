from src.report_generators.base_report_generator import BaseReportGenerator
from src.helpers.preprocess_text import extract_links_from_html
from src.helpers.preprocess_text import extract_attachment_smart
from src.helpers.preprocess_text import extract_from_path

import ast
import re

import pandas as pd


class NonHtmlAttachmentReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ["base_path",
                "primary_publishing_organisation",
                "publishing_app",
                "document_type",
                "first_published_at",
                "attachment_path"]

    @property
    def filename(self):
        return "test_non_html_page_report.csv"

    def process_page(self, content_item, html):

        content_item['primary_publishing_organisation'] = self.extract_subtext(text=content_item['organisations'],
                                                                               key='primary_publishing_organisation',
                                                                               index=1)

        # ignore cases we do not want to return
        publishers = ["publisher", "service-manual-publisher", "specialist-publisher", "travel-advice-publisher"]
        if not content_item['publishing_app'] in publishers:
            return []

        attachments = (".chm|.csv|.diff|.doc|.docx|.dot|.dxf|.eps|"
                       + ".gif|.gml|.ics|.jpg|.kml|.odp|.ods|.odt|.pdf|"
                       + ".png|.ppt|.pptx|.ps|.rdf|.ris|.rtf|.sch|.txt|"
                       + ".vcf|.wsdl|.xls|.xlsm|.xlsx|.xlt|.xml|.xsd|.xslt|"
                       + ".zip")
        if not any(re.findall(pattern=attachments, string=content_item['details'])):
            return []

        if pd.isna(content_item['details']):
            return []

        # extract attachment url
        # each method gives different results
        # need both methods to capture different ways attachments can be on webpage
        content_item['attachment_url_one'] = extract_links_from_html(text=content_item['details'])
        content_item['attachment_url_two'] = self.extract_attachment(text=content_item['details'],
                                                                     element='url')
        content_item['attachment_url_three'] = extract_attachment_smart(text=content_item['details'])

        # combine two lists
        content_item['attachment_path'] = content_item['attachment_url_one'] \
                                          + content_item['attachment_url_two'] \
                                          + content_item['attachment_url_three']
        # remove duplicates
        content_item['attachment_path'] = list(dict.fromkeys(content_item['attachment_path']))

        # extract file extension from attachment url
        content_item['attachment_ext'] = extract_from_path(data=content_item['attachment_path'],
                                                           part='ext')

        # return only pages with attachments by ignoring empty lists
        if not content_item['attachment_ext']:
            return []
        else:
            return [content_item['base_path'],
                    content_item['primary_publishing_organisation'],
                    content_item['publishing_app'],
                    content_item['document_type'],
                    content_item['first_published_at'],
                    content_item['attachment_path']]

    def extract_subtext(self, text, key, index=0):
        """
        Extracts the value of a key within a dictionary masquerading as a string

        :param text: A string that's in the format of a dictionary
        :param key: The name of the key you want to extract the associated value from
        :param index: The index of specific value if you extracted more than one value from the key
        :return: the extracted value of the key
        """
        try:

            # convert to dictionary
            dictionary = ast.literal_eval(text)

            # extract value of key entered from dictionary
            list_keys = list(map(lambda x: x[index], dictionary.get(key, {})))

            return list_keys
        except (ValueError, SyntaxError):
            return []

    def extract_attachment(self, text, element):
        """
        Extracts all the 'attachments' from a specified 'section' from GOV.UK pages

        :param text: String of the HTML code for the GOV.UK page being passed in
        :param element: The `element` within `section` part of HTML code to extract the contents of e.g. 'title', 'url'
        :return: list of all the attachment 'element' that were extracted from GOV.UK page
        """

        try:
            text = ast.literal_eval(text)
            text = text.get('attachments')

            text = list(map(lambda x: x[element], text))
            return text

        except (ValueError, TypeError):
            return []
