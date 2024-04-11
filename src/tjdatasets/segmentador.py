
import pandas as pd
import re

from collections import defaultdict
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

abbreviations = {
    'ap',   # apelação
    'apel', # apelação
    'art',  # artigo
    'arts', # artigos
    'c',    # colendo
    'cc',   # combinado com c.c. ou código do consumidor
    'des',  # desembargador
    'dir',  # direito
    'dje',  # diário da justiça eletrônico
    'dr',   # doutor
    'eg',   # egrégio
    'exmo', # excelentíssimo
    'exmos',# excelentíssimos 
    'fl',   # folha
    'fls',  # folhas
    'inc',  # inciso
    'j',    # julgado em
    'min',  # ministro
    'mm',   # meritíssimo
    'pag',  # página
    'priv', # privado em camara do direito privado
    'rel',  # relator
    'resp', # recurso especial
    'u',    # votação unânime
    'v',    # votação unânime
    'vol'   # volume
}

SEGMENT_EXPRESSIONS = {
    'lei' : [
        '[\\s,]lei[\\s,]', 
        's[úu]mula', 
        'artigo', 
        'c[óo]digo'
    ],
    'fato' : [
        'aduz',
        'afirma',
        'argumenta',
        'assever',
        'constata-se',
        'deduz',
        'esclarece',
        'laudo',
        'no caso',
        'per[íi]cia',
        'prova',
        'sustenta',
        'trata\\-se'
    ],
    'decisao' : [
        'absolv',
        'acolhimento',
        'acordam',
        'arquive',
        'celeb.{1,10}acordo',
        'conced',
        'conden',
        'dar.{,10}provimento',
        'determino',
        'expeça',
        'extingo',
        'proced.ncia',
        'procedente',
        'provido',
        'provimento',
        'homolog.{1,10}acordo'
    ],
    'pedido' : [
        '[\\s,]pede[\\s,]',
        '[\\s,]pedido[\\s,]',
        'pleitea',
        'pretende',
        'seja condenado',
        'seja deferido',
        '[\\s,]solicita[\\s,]']
}

punkt_param = PunktParameters()
punkt_param.abbrev_types = abbreviations

_tokenizer = PunktSentenceTokenizer(punkt_param)

def sentence_tokenize(text):
    return _tokenizer.tokenize(text)


class Segmentador(BaseEstimator, TransformerMixin):
    '''
    '''
    def __init__(self,
                 segment_name=None,
                 sentence_sep=' ',
                 safe_dtypes=False):
        
        assert segment_name in SEGMENT_EXPRESSIONS.keys(), f'O nome do segmento precisa ser um dos seguintes: lei, fato, decisao, pedido'

        self.segment_name = segment_name
        self.safe_dtypes = safe_dtypes
        self.column_sentence = f"segmento_{segment_name}"
        self.sentence_sep = sentence_sep
        self.mapping_dtypes = defaultdict(lambda : 'object',  # default
                     numero_processo='category',
                     id_documento='category',
                     conteudo='string',
                     formatado='string',
                     codigos_movimentos_temas='string')

    def fit(self, X):
        return self

    def transform(self, df):
        column_sentence = self.column_sentence
        if self.safe_dtypes:
            columns_dtypes = {column: df[column].dtype for column in df.columns}
            columns_dtypes.update(self.mapping_dtypes)
        else:
            columns_dtypes = self.mapping_dtypes
        # change columns dtype for optimization purposes
        df = df.astype(columns_dtypes)

        frame = df[['numero_processo', 'id_documento']].copy()
        frame[column_sentence] = df['formatado'].apply(sentence_tokenize)
        frame = frame.explode(column_sentence)
        frame['contains'] = False
        # for segment in SEGMENT_EXPRESSIONS.keys():
        #     frame['contains'] = False

        for expression in SEGMENT_EXPRESSIONS[self.segment_name]:
            frame['contains'] = frame['contains'] | frame[column_sentence].str.contains(expression, regex=True, flags=re.I)
        
        frame = (frame
                    .groupby(['contains', 'numero_processo'])
                    .agg({column_sentence: lambda values: f'{self.sentence_sep}'.join(values)})
                    .loc[True] )
        
        frame = pd.merge(df['numero_processo'], frame, how='left', left_on='numero_processo', right_index=True)

        return frame
