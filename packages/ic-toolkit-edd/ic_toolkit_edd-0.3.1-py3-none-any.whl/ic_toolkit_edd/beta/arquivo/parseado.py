from ic_toolkit_edd.beta.arquivo.abstract import ArquivoAbstract


class ArquivoParseado(ArquivoAbstract):
    @property
    def id_arquivo_parseado(self):
        return self.id_arquivo

    @property
    def __query__(self):
        return '''
            select
                ap.s3_bucket as `bucket`,
                ap.caminho_s3 as `prefix`,
                ap.nome_arquivo as `filename`,
                ap.*
            from upload.arquivo_parseado ap
            where
                ap.id_arquivo_parseado = %(id_arquivo)s
            ;
        '''
