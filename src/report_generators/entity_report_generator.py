from src.report_generators.base_report_generator import BaseReportGenerator
from bs4 import BeautifulSoup
import json
import boto3
from datetime import datetime

class EntityReportGenerator(BaseReportGenerator):
    @property
    def headers(self):
        return ['base_path',
                'entities',
                'updated_at'
                'govner_version',
                ]

    @property
    def filename(self):
        return "entity_report.csv"

    def process_page(self, content_item, html):
        text = self._extract_texts(html)
        entities, govner_version = self._get_entities(text)
        return content_item["base_path"], entities, datetime.now(), govner_version

    def _extract_texts(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for tag in ['b', 'i', 'u', 'a', 'abbr']:
            for match in soup.findAll(tag):
                match.replaceWithChildren()
                # If we don't extract them, the old tags stick
                # around and mess up the soup.strings call
        [x.extract() for x in soup.findAll('script')]
        soup = BeautifulSoup(str(soup), 'html.parser')
        return ". ".join(list(soup.strings))

    def _get_entities(self, text):
        sagemaker_client = boto3.client('sagemaker-runtime', 'eu-west-1')
        endpoint_name = "govner"
        content_type = "application/json"
        accept = "application/json"
        payload = json.dumps({"text": text})
        response = sagemaker_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType=content_type,
            Accept=accept,
            Body=payload
        )
        response = json.loads(response['Body'].read())
        return [response['results'], response['govner_version']]
