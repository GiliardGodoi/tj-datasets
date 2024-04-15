
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
        r'[\s,]lei[\s,]', 
        r's[úu]mula', 
        r'artigo', 
        r'c[óo]digo'
    ],
    'fato' : [
        r'aduz',
        r'afirma',
        r'argumenta',
        r'assever',
        r'constata-se',
        r'deduz',
        r'esclarece',
        r'laudo',
        r'no caso',
        r'per[íi]cia',
        r'prova',
        r'sustenta',
        r'trata-se'
    ],
    'decisao' : [
        r'absolv',
        r'acolhimento',
        r'acordam',
        r'arquive',
        r'celeb.{1,10}acordo',
        r'conced',
        r'conden',
        r'dar.{,10}provimento',
        r'determino',
        r'expeça',
        r'extingo',
        r'proced.ncia',
        r'procedente',
        r'provido',
        r'provimento',
        r'homolog.{1,10}acordo'
    ],
    'pedido' : [
        r'[\s,]pede[\s,]',
        r'[\s,]pedido[\s,]',
        r'pleitea',
        r'pretende',
        r'seja condenado',
        r'seja deferido',
        r'[\s,]solicita[\s,]'
    ]
}

punkt_param = PunktParameters()
punkt_param.abbrev_types = abbreviations

_tokenizer = PunktSentenceTokenizer(punkt_param)

def __sentence_tokenize(text):
    return _tokenizer.tokenize(text)

def __segmentar(frame: pd.DataFrame, segment_name: str, column_senteces: str):
    '''
    '''
    column_segment = f'segmento_{segment_name}'
    frame['contains'] = False

    for expression in SEGMENT_EXPRESSIONS[segment_name]:
            # pandas, assim como Python, suporta algo chamado short-circuit evaluation
            frame['contains'] = frame['contains'] | frame[column_senteces].str.contains(expression, regex=True, flags=re.I)
        
    return (frame.loc[lambda x: x['contains'] == True]
                .groupby(['numero_processo'])
                .agg({column_senteces: lambda values: ' '.join(values)})
                .rename(columns={column_senteces : column_segment })
            )

def obter_todos_segmentos(df : pd.DataFrame):
    '''
    '''
    columns_dtypes = {column: df[column].dtype for column in df.columns}
    columns_dtypes.update(dict(numero_processo='category',
                                    id_documento='category',
                                    conteudo='string',
                                    formatado='string',
                                    codigos_movimentos_temas='string')
                        )
    df = df.astype(columns_dtypes)

    # Essa é a parte do código que mais demora para executar
    frame = df[['numero_processo', 'id_documento']].copy()
    frame['sentences'] = df['formatado'].apply(__sentence_tokenize)
    frame = frame.explode('sentences')

    segmento_lei     = __segmentar(frame, segment_name='lei', column_senteces='sentences')
    segmento_fato    = __segmentar(frame, segment_name='fato', column_senteces='sentences')
    segmento_decisao = __segmentar(frame, segment_name='decisao', column_senteces='sentences')
    segmento_pedido  = __segmentar(frame, segment_name='pedido', column_senteces='sentences')
    
    result = pd.merge(df['numero_processo'], segmento_lei, how='left', left_on='numero_processo', right_index=True)
    result = pd.merge(result, segmento_fato, how='left', left_on='numero_processo', right_index=True)
    result = pd.merge(result, segmento_decisao, how='left', left_on='numero_processo', right_index=True)
    result = pd.merge(result, segmento_pedido, how='left', left_on='numero_processo', right_index=True)

    return result


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
        self.column_segment = f"segmento_{segment_name}"
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
        '''
        '''
        column_segment = self.column_segment

        # Os tipos das colunas são alterados para efeito de otimização
        # numero_processo é transformado de string para category, por exemplo
        if self.safe_dtypes:
            columns_dtypes = {column: df[column].dtype for column in df.columns}
            columns_dtypes.update(self.mapping_dtypes)
        else:
            columns_dtypes = self.mapping_dtypes
        # change columns dtype for optimization purposes
        df = df.astype(columns_dtypes)

        frame = df[['numero_processo', 'id_documento']].copy()
        # Essa ainda é a parte mais lenta do código
        # primeiro separamos o documentos em frases
        # setence_tokenize retorna uma lista de frases
        frame[column_segment] = df['formatado'].apply(__sentence_tokenize)
        # .explode transforma cada item da lista uma nova linha
        # de um novo dataframe
        frame = frame.explode(column_segment)
        frame['contains'] = False

        for expression in SEGMENT_EXPRESSIONS[self.segment_name]:
            # pandas, assim como Python, suporta algo chamado short-circuit evaluation
            frame['contains'] = frame['contains'] | frame[column_segment].str.contains(expression, regex=True, flags=re.I)
        
        frame = (frame.loc[lambda x: x['contains'] == True]
                    .groupby(['numero_processo'])
                    .agg({column_segment: lambda values: ' '.join(values)})
                )
        
        frame = pd.merge(df['numero_processo'], frame, how='left', left_on='numero_processo', right_index=True)

        return frame
