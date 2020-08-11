from src.utils.file_reader import FileReader
from src.pipeline.report import Report


class RunnerConfig:

    def __init__(self, config_file_path):
        self.config_file = FileReader.read_yaml(config_file_path)

    @property
    def turbo_mode(self):
        return self.config_file['settings']['turbo_mode']

    @property
    def html_content_dir_path(self):
        return self.config_file['settings']['html_content_dir_path']

    @property
    def preprocessed_content_store_path(self):
        return self.config_file['settings']['preprocessed_content_store_path']

    @property
    def content_item_batch_size(self):
        return self.config_file['settings']['content_item_batch_size']

    @property
    def csv_writer_buffer_size(self):
        return self.config_file['settings']['csv_writer_buffer_size']

    @property
    def reports(self):
        return [Report(report_yaml) for report_yaml in self.config_file['reports']]

    @property
    def total_content_items(self):
        return self.config_file['settings']['total_content_items']

    def __str__(self):
        return f"""-----------------------------------------------------------------------
Running with the following settings:

html_content_dir_path:\t{self.html_content_dir_path}
preprocessed_content_store_path:\t{self.preprocessed_content_store_path}
content_item_batch_size:\t{self.content_item_batch_size}
csv_writer_buffer_size:\t{self.csv_writer_buffer_size}
total_content_items:\t{self.total_content_items}
-----------------------------------------------------------------------"""
