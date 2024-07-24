import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

from .fragmentador import (
  identifica_nome_relator,
  identifica_decisao,
  identifica_voto_relator,
  identifica_relatorio_voto,
  identifica_fundamentacao_voto,
  identifica_voto_divergente,
)

from .preprocessing import (
    remove_noise_from_header,
    remove_header,
    remove_footer,
    remove_punctuation,
    regularize_expressions,
    remove_special_case_words,
)

from .utils import (CUSTO_STOPWORDS,
                    DEFAULT_PUNCTUATION,
                    PATTERN_REMOVE_EXTRA_SPACE,
                    PATTERN_REMOVE_SPECIAL_CHARS,
                    STANDART_EXPRESSIONS,
                    TABLE_REMOVE_LOWER_ACCENTS)

def _check_input_type(X, column_text) -> pd.Series:
  if type(X) is pd.Series:
      documents = X
  elif type(X) is pd.DataFrame:
    documents = X[column_text]
  else:
    raise TypeError(f'Expected pd.Series or pd.DataFrame, but received {type(X)}')

  return documents

class PreProcessamentoLimpo(BaseEstimator, TransformerMixin):
  '''Pré-processamento Limpo

  Converte o texto para o formato 'Limpo'

  São aplicadas as seguintes operações:
    - Remove ruído do cabeçalho e rodapé
    - Remove cabeçalho
    - Remove rodapé
    - Remove caracteres em branco duplos (espaços em branco)
    - Remove caracteres em branco do início e fim do documento (.strip)


  Recebe como parâmetro um pandas DataFrame ou um pandas Series.

  Retorna um pandas Series com os documentos (textos) formatados.
  '''

  def __init__(self, column_text='conteudo'):
    '''Inicializa a classe.

    Parâmetros:
      column_text: quando um pd.DataFrame é passado como entrada, define a coluna que contém os documentos a serem processados.
    '''
    self.column_text = column_text

  def fit(self, X, y=None):
    return self

  def transform(self, X):
    '''Aplica as operações para conversão do texto para o formato Limpo'''

    documents = _check_input_type(X, self.column_text)

    result = (documents
              .apply(remove_noise_from_header)
              .apply(remove_header)
              .apply(remove_footer)
              .str.replace(PATTERN_REMOVE_EXTRA_SPACE, ' ', regex=True) # substituí caracteres em branco duplos por um espaço simples, inclusive quebra de página \x0c
              .str.strip() # remove espaço em branco no começo e no final do texto
              )

    return result

class PreProcessamentoNormalizado(BaseEstimator, TransformerMixin):
  '''Pré-processamento Normalizado

  Converte o texto para o formato 'Normalizado'

  São aplicadas as seguintes operações:
    - Converte para letras minúsculas
    - Remove o acento das palavras
    - Regulariza expressões    (definidas em STANDART_EXPRESSIONS)
    - Remove pontuação gráfica (definidas em  DEFAULT_PUNCTUATION)
    - Remove alguns casos especiais de palavras:
        - stopwords
        - palavras com comprimento mínimo ou menor (min_length é definido por padrão como 3)
        - Porém tenta preservar algumas palavras definidas em words_do_not_remove

  Recebe como parâmetro um pandas DataFrame ou um pandas Series.

  Retorna um pandas Series com os documentos (textos) formatados.
  '''

  def __init__(self, column_text='formatado'):
    '''Inicializa a classe.

    Parâmetros:
      column_text: quando um pd.DataFrame é passado como entrada, define a coluna que contém os documentos a serem processados.
    '''
    self.column_text = column_text

    self.words_do_not_remove = {'nao', 'lei', 'ato',
                                'reu', 'mes', 'ano',
                                'dia', 'reu', 'quo', 'jus'}

  def fit(self, X, y=None):
    return self

  def transform(self, X):
    '''
    '''
    documents = _check_input_type(X, self.column_text)

    result = (documents
              .str.lower()
              .str.translate(TABLE_REMOVE_LOWER_ACCENTS)
              .apply(regularize_expressions, mapper=STANDART_EXPRESSIONS)
              .apply(remove_punctuation, punctuation=DEFAULT_PUNCTUATION)
              .apply(remove_special_case_words,
                     stopwords=CUSTO_STOPWORDS,
                     spare_words=self.words_do_not_remove,
                     min_length=3)
              .str.strip() # remove espaço em branco no começo e no final do texto
            )

    return result

class ProcessamentoFundamentacao(BaseEstimator, TransformerMixin):

  def __init__(self,
               column_text='conteudo',
               as_dataframe=False):
    '''Inicializa a classe.

    Parâmetros:
      column_text: quando um pd.DataFrame é passado como entrada, define a coluna que contém os documentos a serem processados.
    '''
    self.column_text = column_text
    self.as_dataframe = as_dataframe

  def fit(self, X, y=None):
    return self

  def transform(self, X, y=None):
    '''
    '''
    documents = _check_input_type(X, self.column_text)

    documents = (documents.str.replace(PATTERN_REMOVE_SPECIAL_CHARS, ' ', regex=True)
                          .str.replace(PATTERN_REMOVE_EXTRA_SPACE, ' ', regex=True)
                          .str.lower()
                          .str.translate(TABLE_REMOVE_LOWER_ACCENTS) )

    results = (documents
               .apply(self._get_fundamentacao)
               .apply(pd.Series)
               )

    if not self.as_dataframe:
      results = results['texto']

    return results


  def _get_fundamentacao(self, texto):

    relator = identifica_nome_relator(texto)
    voto    = identifica_voto_relator(texto, relator)
    relatorio = identifica_relatorio_voto(texto, voto)
    fundamentacao = identifica_fundamentacao_voto(texto, voto, relatorio)

    # por padrão, retorna o texto completo do documento
    fragmento_texto = texto
    fragmento_nome  = 'conteudo_original'
    fragmento_span  = (0, len(texto))

    # em caso de sucesso rule > 0
    if fundamentacao.rule > 0 :
        fragmento_texto = fundamentacao.text
        fragmento_nome  = fundamentacao.name
        fragmento_span  = fundamentacao.span
    elif voto.rule > 0 :
        fragmento_texto = voto.text
        fragmento_nome  = voto.name
        fragmento_span  = voto.span

    return {'texto' : fragmento_texto,
            'fragmento_nome' : fragmento_nome,
            'fragmento_span' : fragmento_span }


class ProcessamentoVotoRelator(BaseEstimator, TransformerMixin):

  def __init__(self,
               column_text='conteudo',
               as_dataframe=False):

    self.column_text = column_text
    self.as_dataframe = as_dataframe

  def fit(self, X, y=None):
    return self

  def transform(self, X, y=None, *args):
    '''
    '''
    documents = _check_input_type(X, self.column_text)

    documents = (documents.str.replace(PATTERN_REMOVE_SPECIAL_CHARS, ' ', regex=True)
                          .str.replace(PATTERN_REMOVE_EXTRA_SPACE, ' ', regex=True)
                          .str.lower()
                          .str.translate(TABLE_REMOVE_LOWER_ACCENTS) )

    results = (documents
               .apply(self._get_voto_relator)
               .apply(pd.Series)
              )

    if not self.as_dataframe:
      results = results['texto']

    return results

  def _get_voto_relator(self, texto):
    relator = identifica_nome_relator(texto)
    voto    = identifica_voto_relator(texto, relator)

    if voto.rule > 0:
      fragmento_texto = voto.text
      fragmento_nome  = voto.name
      fragmento_span  = voto.span
    else :
      fragmento_texto = texto
      fragmento_nome  = 'conteudo_original'
      fragmento_span  = (0, len(texto))

    return {'texto' : fragmento_texto,
            'fragmento_nome' : fragmento_nome,
            'fragmento_span' : fragmento_span }
