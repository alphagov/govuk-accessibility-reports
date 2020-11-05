from src.report_generators.base_report_generator import BaseReportGenerator
from bs4 import BeautifulSoup
import json
import boto3
import boto3.session
from datetime import datetime
import time
from ast import literal_eval

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
        if EntityReportGenerator.is_mainstream(content_item) == False:
            return []
        print(f"Get entities {content_item['base_path']}")
        text = EntityReportGenerator.extract_texts(html)
        start_time = time.time()
        entities, govner_version = EntityReportGenerator.get_entities(text)
        print(f"Got entities {content_item['base_path']}, time {time.time() - start_time}")
        return [content_item['base_path'], entities, datetime.now(), govner_version]

    @staticmethod
    def is_mainstream(content_item):
        # Content that is mainstream; where primary publisher is GDS and pubishing app is 'publisher'
        if content_item["publishing_app"] != "publisher":
            return False
        organisations = literal_eval(content_item['organisations'])
        for primary_publishing_organisation in organisations["primary_publishing_organisation"]:
            # "OT1056" is id of GDS
            if primary_publishing_organisation[2] == "OT1056":
                return True
        return False

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
            EndpointName="govner-endpoint",
            ContentType="application/json",
            Accept="application/json",
            Body= json.dumps({"text": text}),
        )
        response = json.loads(response['Body'].read())
        return [response['results']['entities'], response['results']['govner_version']]

