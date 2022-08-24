from dataclasses import dataclass

@dataclass
class AltTagInfo:
    def __init__(self, has_images=False, missing_alt_tags=False, alt_tags_empty=False, alt_tags_double_quotes=False, alt_tags_filename=False):
        self.has_images = has_images
        self.missing_alt_tags = missing_alt_tags
        self.alt_tags_empty = alt_tags_empty
        self.alt_tags_double_quotes = alt_tags_double_quotes
        self.alt_tags_filename = alt_tags_filename

    def has_images(self):
        return self.has_images

    def missing_alt_tags(self):
        return self.missing_alt_tags

    def alt_tags_empty(self):
        return self.alt_tags_empty

    def alt_tags_double_quotes(self):
        return self.alt_tags_double_quotes

    def alt_tags_filename(self):
        return self.alt_tags_filename

    def is_valid(self):
        if self.has_images() and (self.missing_alt_tags() or self.alt_tags_empty() or self.alt_tags_double_quotes() or self.alt_tags_filename()):
            return False
        return True
