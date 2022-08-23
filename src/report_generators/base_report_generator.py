from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from src.helpers.preprocess_text import extract_subtext

import re

class BaseReportGenerator(ABC):

    @property
    @abstractmethod
    def filename(self):
        return ''

    @property
    @abstractmethod
    def headers(self):
        return []

    @abstractmethod
    def process_page(self, content_item, html):
        pass

    def post_process_report(self):
        pass

    def base_headers(self):
        return ["base_path",
                "primary_publishing_organisation",
                "publishing_app",
                "document_type",
                "schema_type",
                "first_published_at",
                "public_updated_at",
                "status"]

    def base_columns(self, content_item, html):
        content_item["primary_publishing_organisation"] = extract_subtext(text=content_item["organisations"],
                                                                          key="primary_publishing_organisation",
                                                                          index=1)
        content_item["schema_name"] = ""
        soup = BeautifulSoup(html, "html5lib")
        schema_element = soup.head.find("meta", attrs={"name":"govuk:schema-name"})
        if schema_element != None:
            content_item["schema_name"] = schema_element["content"]

        regex = re.compile("^This was published under the", re.IGNORECASE)
        historical_box = soup.body.find("span", attrs={"class":"gem-c-notice__title govuk-notification-banner__heading"}, text=regex)

        content_item["status"] = "published"
        if content_item["withdrawn"] == "TRUE":
            content_item["status"] = "withdrawn"
        elif historical_box != None:
            content_item["status"] = "historical"

        return [content_item["base_path"],
                ", ".join(content_item["primary_publishing_organisation"]),
                content_item["publishing_app"],
                content_item["document_type"],
                content_item["schema_name"],
                content_item["first_published_at"],
                content_item["public_updated_at"],
                content_item["status"]]
