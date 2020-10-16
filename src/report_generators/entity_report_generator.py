from src.report_generators.base_report_generator import BaseReportGenerator
from bs4 import BeautifulSoup
import json
import boto3
import boto3.session
from datetime import datetime
import time

class EntityReportGenerator(BaseReportGenerator):

    @staticmethod
    def headers():
        return ['base_path',
                'entities',
                'updated_at',
                'govner_version',
                ]

    @staticmethod
    def filename():
        return "entity_report.csv"

    @staticmethod
    def process_page(content_item, html):
        print(f"Get entities {content_item['base_path']}")
        text = EntityReportGenerator.extract_texts(html)
        start_time = time.time()
        entities, govner_version = EntityReportGenerator.get_entities(text)
        print(f"Got entities {content_item['base_path']}, time {time.time() - start_time}")
        entities = []
        govner_version = 1
        return [content_item['base_path'], entities, datetime.now(), govner_version]

    @staticmethod
    def extract_texts(html):
        soup = BeautifulSoup(html, 'html.parser')
        for tag in ['b', 'i', 'u', 'a', 'abbr']:
            for match in soup.findAll(tag):
                match.replaceWithChildren()
                # If we don't extract them, the old tags stick
                # around and mess up the soup.strings call
        [x.extract() for x in soup.findAll('script')]
        soup = BeautifulSoup(str(soup), 'html.parser')
        return ". ".join(list(soup.strings))

    @staticmethod
    def get_entities(text):
        sagemaker_client = boto3.session.Session().client('sagemaker-runtime', 'eu-west-1')
        response = sagemaker_client.invoke_endpoint(
            EndpointName="govner",
            ContentType="application/json",
            Accept="application/json",
            Body= json.dumps({"text": text}),
        )
        response = json.loads(response['Body'].read())
        return [response['results']['entities'], response['results']['govner_version']]

