import re
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

from .preprocessing import (
    remove_noise_from_header, 
    remove_header, 
    remove_footer,
    remove_punctuation,
    remove_word_stress,
    # remove_stopwords,
    # remove_short_words,
    remove_short_and_stop_words,
    regularize_expressions,
    # tokenizer,
    # regex_tokenizer,
    # lemmatize,
    # stemmerize,
)

from .utils import (JUR_EXPRESSIONS, 
                    LEG_EXPRESSIONS, 
                    DEFAULT_PUNCTUATION,
                    STOP_WORDS_SPACY)

class PreprocessamentoLimpo(BaseEstimator, TransformerMixin):
  
  def __init__(self, content='conteudo'):
    '''Inicializa a classe.

    Parâmetros:
      target: define a coluna alvo, que contém os documentos a serem processados.
      transformed: define a coluna que será gerada
    '''
    self.target = content

  def fit(self, X, y=None):
    return self
  
  def transform(self, X):
    '''
    '''
    if type(X) is pd.Series:
      documents = X
    elif type(X) is pd.DataFrame:
      documents = X[self.content]
    else:
      raise TypeError(f'Expected pd.Series or pd.DataFrame, but received {type(X)}')

    result = (documents
              .apply(remove_noise_from_header)
              .apply(remove_header)
              .apply(remove_footer)
              .apply(lambda t: re.sub(r'\x0c', '', t)) # remove caracter de quebra de linha
              .apply(lambda t: re.sub(r'\s+', ' ', t)) # remove caracteres em branco
              .apply(lambda t: t.strip()) # remove espaço em branco no começo e no final do texto
              )

    return result

class PreprocessamentoNormalizado(BaseEstimator, TransformerMixin):
  
  def __init__(self, content='conteudo'):
    '''Inicializa a classe.

    Parâmetros:
      target: define a coluna alvo, que contém os documentos a serem processados.
      transformed: define a coluna que será gerada
    '''
    self.target = content

  def fit(self, X, y=None):
    return self
  
  def transform(self, X):
    '''
    '''
    if type(X) is pd.Series:
      documents = X
    elif type(X) is pd.DataFrame:
      documents = X[self.content]
    else:
      raise TypeError(f'Expected pd.Series or pd.DataFrame, but received {type(X)}')

    result = (documents
              .apply(remove_noise_from_header)
              .apply(remove_header)
              .apply(remove_footer)
              .apply(lambda t: re.sub(r'\x0c', '', t)) # remove caracter de quebra de linha
              .apply(lambda t: re.sub(r'\s+', ' ', t)) # remove caracteres em branco
              .apply(lambda t: t.strip()) # remove espaço em branco no começo e no final do texto
              .apply(regularize_expressions, mapper=LEG_EXPRESSIONS)
              .apply(regularize_expressions, mapper=JUR_EXPRESSIONS)
              .apply(lambda t: t.lower()) # transforma as palavras em minusculas
              .apply(remove_word_stress)
              .apply(remove_punctuation, punctuation=DEFAULT_PUNCTUATION)
              .apply(remove_short_and_stop_words, stopwords=STOP_WORDS_SPACY, min_length=3)
              )

    return result
