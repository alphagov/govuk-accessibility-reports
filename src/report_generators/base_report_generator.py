from abc import ABC, abstractmethod


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
