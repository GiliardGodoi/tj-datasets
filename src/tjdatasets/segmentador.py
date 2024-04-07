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