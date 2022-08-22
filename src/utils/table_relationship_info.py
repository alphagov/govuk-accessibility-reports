class TableRelationshipInfo:
    def __init__(self, table_mentions, attachments, table_in_document=False):
        self.table_mentions = table_mentions
        self.attachments = attachments
        self.table_in_document = table_in_document

    def table_mentions(self):
        return self.table_mentions

    def has_mention_of_table(self):
        return len(self.table_mentions) > 0

    def has_table_in_document(self):
        return self.table_in_document

    def has_possible_table_attachment(self):
        return len(self.attachments) > 0

    def is_valid(self):
        if self.has_table_in_document() == True:
            return True
        return not self.has_mention_of_table()
