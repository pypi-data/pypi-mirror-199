from ic_toolkit_edd.beta.arquivo_s3 import ArquivoS3


class InputTextConfig(ArquivoS3):
    def __init__(self, bucket: str, prefix: str, filename: str, version_id=None, main=False, parser=None):
        super().__init__(bucket, prefix, filename, version_id)
        self.options = {
            'parser-pipeline': 'false',
        }
        self.main = main
        self.parser = parser

    @property
    def main(self):
        return 'type' in self.options

    @main.setter
    def main(self, value):
        if value:
            self.options.update({'type': 'MAIN'})
        else:
            self.options.pop('type', None)

    @property
    def parser(self):
        return self.options['parser']

    @parser.setter
    def parser(self, value):
        self.options['parser'] = value

    @property
    def dict(self):
        return {
            'bucket': self.bucket,
            'prefix': self.prefix,
            'filename': self.filename,
            'options': self.options,
        }
