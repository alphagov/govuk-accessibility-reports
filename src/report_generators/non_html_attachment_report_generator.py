from src.report_generators.base_report_generator import BaseReportGenerator
from src.helpers.preprocess_text import extract_links_from_html
from src.helpers.preprocess_text import extract_from_path
from src.helpers.preprocess_text import extract_subtext

import os
import ast
import re

from bs4 import BeautifulSoup
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
        return "non_html_page_report.csv"

    def process_page(self, content_item, html):

        content_item['primary_publishing_organisation'] = extract_subtext(text=content_item['organisations'],
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
        content_item['attachment_url_three'] = self.extract_attachment_smart(text=content_item['details'])

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

    def extract_attachment_smart(self, text):
        """
        Extracts all 'attachments' from 'nodes' section of GOV.UK pages.
        Mainly for pages where we have simple smart answers.
        e.g. https://www.gov.uk/api/content/student-finance-forms

        :param text: String of the HTML code for GOV.UK page being passed in
        :return: list of all the attachment links that were extracted from GOV.UK page
        """

        try:
            # simple smart answers are nested within the 'nodes' part of HTML code
            text = ast.literal_eval(text)
            text = text.get('nodes')

            # extract links
            list_body = []
            for txt in text:
                if txt.get('body'):
                    for _, value in txt.items():
                        links = str(value)
                        soup = BeautifulSoup(links, 'html5lib')
                        links = [link.get('href') for link in soup.findAll('a', href=True)]
                        list_body.append(links)
                else:
                    continue

            # remove empty lists
            list_body = [x for x in list_body if x]
            # un-nest lists in list
            list_body = [item for sublist in list_body for item in sublist]
            # remove duplicate links
            list_body = list(dict.fromkeys(list_body))

            # extract only attachment links
            list_attachments = []
            for link in list_body:
                if not os.path.splitext(link)[1] == '':
                    list_attachments.append(link)

            return list_attachments

        except (ValueError, TypeError):
            return []
