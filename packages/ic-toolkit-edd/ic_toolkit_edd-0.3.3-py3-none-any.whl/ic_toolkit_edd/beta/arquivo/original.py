from ic_toolkit_edd.beta.arquivo.abstract import ArquivoAbstract


class ArquivoOriginal(ArquivoAbstract):
    @property
    def id_arquivo_original(self):
        return self.id_arquivo

    @property
    def __query__(self):
        return '''
            select
                ao.s3_bucket as `bucket`,
                ao.caminho_s3 as `prefix`,
                ao.nome_arquivo as `filename`,
                ao.*
            from upload.arquivo_original ao
            where
                ao.id_arquivo_original = %(id_arquivo)s
            ;
        '''
