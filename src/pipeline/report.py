class Report:

    def __init__(self, report):
        self.report = report

    @property
    def name(self):
        return self.report['name']

    @property
    def filename(self):
        return self.report['filename']

    @property
    def klass(self):
        return self.report['class']

    @property
    def skip(self):
        return self.report['skip']
