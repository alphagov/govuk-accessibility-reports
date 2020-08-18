import os
import yaml


class FileReader:

    @staticmethod
    def read_file_as_string(filepath):
        """(str) -> str
        Opens the file at filepath for reading, removing /n
        before rejoining separate lines with " " separator.
        """
        with open(filepath, 'r') as file:
            lines = " ".join(line.strip("\n") for line in file)
        return lines

    @staticmethod
    def read_yaml(filename):
        with open(
                os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '..', 'config', filename),
                'r') as f:
            return yaml.safe_load(f)
