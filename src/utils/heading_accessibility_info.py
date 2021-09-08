class HeadingAccessibilityInfo:
    def __init__(self, headings, duplicate_h1s=False, bad_ordering=False, no_headings=False, wrong_start=False):
        self.headings = headings
        self.duplicate_h1s = duplicate_h1s
        self.bad_ordering = bad_ordering
        self.no_headings = no_headings
        self.wrong_start = wrong_start

    def heading_order(self):
        return self.headings

    def has_duplicate_h1s(self):
        return self.duplicate_h1s

    def has_bad_ordering(self):
        return self.bad_ordering

    def has_no_headings(self):
        return self.no_headings

    def has_wrong_start(self):
        return self.wrong_start

    def is_valid(self):
        return not self.has_duplicate_h1s() and not self.has_bad_ordering() and not self.has_no_headings() and not self.has_wrong_start()
