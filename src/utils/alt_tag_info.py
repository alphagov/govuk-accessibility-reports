from dataclasses import dataclass

@dataclass
class AltTagInfo:
    def __init__(self, has_images=False, missing_alt_tags=False, alt_tags_empty=False, alt_tags_double_quotes=False, alt_tags_filename=False):
        self.has_images = has_images
        self.missing_alt_tags = missing_alt_tags
        self.alt_tags_empty = alt_tags_empty
        self.alt_tags_double_quotes = alt_tags_double_quotes
        self.alt_tags_filename = alt_tags_filename

    def includes_images(self):
        return self.has_images

    def missing_tags(self):
        return self.missing_alt_tags

    def tags_empty(self):
        return self.alt_tags_empty

    def tags_double_quotes(self):
        return self.alt_tags_double_quotes

    def tags_filename(self):
        return self.alt_tags_filename

    def is_valid(self):
        if self.includes_images() and (self.missing_tags() or self.tags_empty() or self.tags_double_quotes() or self.tags_filename()):
            return False
        return True
