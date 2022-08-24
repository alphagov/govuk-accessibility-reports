class AttachmentLinkAccessibilityInfo:
    def __init__(self, attachment_links, inaccurate_pdf_download_text=False, no_format_description=False, no_size_description=False):
        self.attachment_links = attachment_links
        self.inaccurate_pdf_download_text = inaccurate_pdf_download_text
        self.no_format_description = no_format_description
        self.no_size_description = no_size_description

    def attachment_links(self):
        return self.attachment_links

    def has_attachment_links(self):
        return len(self.attachment_links) > 0

    def has_inaccurate_pdf_download_text(self):
        return self.inaccurate_pdf_download_text

    def has_no_format_description(self):
        return self.no_format_description

    def has_no_size_description(self):
        return self.no_size_description

    def is_valid(self):
        if self.has_attachment_links() == False:
            return True
        return not self.has_inaccurate_pdf_download_text() and not self.has_no_format_description() and not self.has_no_size_description()
