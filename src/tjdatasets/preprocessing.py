import re
from typing import List
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import RSLPStemmer

from .utils import (CUSTO_STOPWORDS, 
                    STANDART_EXPRESSIONS,
                    DEFAULT_PUNCTUATION, TABLE_REMOVE_LOWER_ACCENTS)

def detect_header(s1, s2, minHeaderLen=15):
    """
    Identifica como header o texto que se repete no início de páginas seguidas
    """
    i = 0
    n1 = len(s1)
    n2 = len(s2)
    j = minHeaderLen
    while j < n1:
        seq = s1[i:j]
        k = s2.find(seq)
        if k != -1:
            k += minHeaderLen
            while j < n1 and k < n2 and s1[j] == s2[k]:
                j += 1
                k += 1
            return s1[i:j]
        i += 1
        j += 1
    return ""


def detect_footer(s1, s2, minFooterLen=15):
    """
    Identifica como footer o texto que se repete no final de páginas seguidas
    """
    n1 = len(s1)
    i = n1 - minFooterLen
    j = n1
    while i >= 0:
        seq = s1[i:j]
        k = s2.rfind(seq)
        if k != -1:
            i -= 1
            k -= 1
            while i >= 0 and k >= 0 and s1[i] == s2[k]:
                i -= 1
                k -= 1
            footer = s1[(i + 1) : j]
            res = re.search(r"\n\s*\n", footer)
            if res:
                return footer[res.start() :]
            return ""
        i -= 1
        j -= 1
    return ""


def remove_header_footer(text, pageSep="\x0c", maxHeaderLen=200, maxFooterLen=200):
    """
    Remove cabeçalho e rodapé do texto, baseado na igualdade destes entre páginas.
    As páginas devem ter separador, que será removido no fim do processo.
    """
    v = re.split(pageSep, text)
    pattern = ""
    numPages = len(v)
    for i in range(numPages):
        if i + 1 < numPages:
            page0 = "".join([c for c in v[i] if c != " " and c != "\n"])
            page1 = "".join([c for c in v[i + 1] if c != " " and c != "\n"])
            end0 = maxHeaderLen
            end1 = maxHeaderLen
            if end0 > len(page0):
                end0 = len(page0)
            if end1 > len(page1):
                end1 = len(page1)
            header = detect_header(page0[:end0], page1[:end1])
            if header:
                pattern = r"\s*".join(header)
        if pattern:
            try:
                res = re.search(pattern, v[i])
                if res and res.end() < maxHeaderLen:
                    v[i] = v[i][res.end() :]
            except:
                pass
    pattern = ""
    for i in range(numPages):
        if i + 1 < numPages:
            page0 = "".join([c for c in v[i] if c != " "])
            page1 = "".join([c for c in v[i + 1] if c != " "])
            begin0 = len(page0) - maxFooterLen
            begin1 = len(page1) - maxFooterLen
            if begin0 < 0:
                begin0 = 0
            if begin1 < 0:
                begin1 = 0
            footer = detect_footer(page0[begin0:], page1[begin1:])
            if footer:
                footer = footer.strip()
                pattern = r"\s*".join(footer)
        if pattern:
            try:
                iter_res = re.finditer(pattern, v[i])
                res = [m for m in iter_res]
                if len(res) > 0:
                    if len(v[i]) - res[-1].start() < maxFooterLen:
                        v[i] = v[i][: res[-1].start()]
            except:
                pass
    return f"{pageSep}".join(v)


def remove_header(text, pageSep="\x0c", maxLen=200):
    """
    Remove apenas o cabeçalho do texto, baseado na igualdade entre duas páginas.
    """
    pages = re.split(pageSep, text)
    pattern = ""
    numPages = len(pages)
    for i in range(numPages):
        if i + 1 < numPages:
            page0 = "".join([c for c in pages[i] if c != " " and c != "\n"])
            page1 = "".join([c for c in pages[i + 1] if c != " " and c != "\n"])
            end0 = maxLen
            end1 = maxLen
            if end0 > len(page0):
                end0 = len(page0)
            if end1 > len(page1):
                end1 = len(page1)
            header = detect_header(page0[:end0], page1[:end1])
            if header:
                pattern = r"\s*".join(header)
        if pattern:
            try:
                res = re.search(pattern, pages[i])
                if res and res.end() < maxLen:
                    pages[i] = pages[i][res.end() :]
            except:
                pass

    return f"{pageSep}".join(pages)


def remove_footer(text, pageSep="\x0c", maxLen=200):
    """
    Remove apenas o rodapé do texto, baseado na igualdade entre páginas.
    """
    pages = re.split(pageSep, text)
    pattern = ""
    numPages = len(pages)

    for i in range(numPages):
        if i + 1 < numPages:
            page0 = "".join([c for c in pages[i] if c != " "])
            page1 = "".join([c for c in pages[i + 1] if c != " "])
            begin0 = len(page0) - maxLen
            begin1 = len(page1) - maxLen
            if begin0 < 0:
                begin0 = 0
            if begin1 < 0:
                begin1 = 0
            footer = detect_footer(page0[begin0:], page1[begin1:])
            if footer:
                footer = footer.strip()
                pattern = r"\s*".join(footer)
        if pattern:
            try:
                iter_res = re.finditer(pattern, pages[i])
                res = [m for m in iter_res]
                if len(res) > 0:
                    if len(pages[i]) - res[-1].start() < maxLen:
                        pages[i] = pages[i][: res[-1].start()]
            except:
                pass

    return f"{pageSep}".join(pages)


def remove_noise_from_header(text : str) -> str:
    doc = list()
    for page in re.split(r'\x0c', text):
        page = re.sub(r'^(.*?)(PODER JUDICIÁRIO)', 'PODER JUDICIÁRIO', page, flags=re.DOTALL)
        page = re.sub(r'PODER JUDICIÁRIO.*?TRIBUNAL DE JUSTIÇA', 'PODER JUDICIÁRIO\nTRIBUNAL DE JUSTIÇA', page, flags=re.DOTALL)
        doc.append(page)

    return '\x0c'.join(doc)


def remove_stopwords(tokens : List[str], stopwords=CUSTO_STOPWORDS) -> List[str]:
    if not type(tokens) is list:
        raise TypeError(f"tokens should be a list of strings, but received a {type(tokens)}.\nConsider apply a tokenization before.")
    
    if type(stopwords) is list:
        stopwords = set(stopwords)

    return [token for token in tokens if token not in stopwords]


def remove_short_words(tokens: List, min_lenght=3) -> List[str]:
    if not type(tokens) is list:
        raise TypeError(f"tokens should be a list of strings, but received a {type(tokens)}.\nConsider apply a tokenization before.")
    return [token for token in tokens if len(token) > min_lenght]


def remove_short_and_stop_words(text: str, 
                                stopwords=CUSTO_STOPWORDS, 
                                min_length=3,
                                tokenizer=word_tokenize):

    tokens = [
        token
        for token in tokenizer(text)
        if (len(token) > min_length) and (token not in stopwords)
    ]

    return " ".join(tokens)

def remove_special_case_words(text: str,
                              stopwords: set = CUSTO_STOPWORDS,
                              spare_words: set = {},
                              min_length: int = 3,
                              tokenizer: callable = word_tokenize,
                              ):
    ''' Remove tokens (palavras):
        - menores ou igual a min_length
        - sejam consideradas stop words

    Contudo, preserva algumas palavras presente em spare_words.
    '''
    tokens = [
        token
        for token in tokenizer(text)
        if ((len(token) > min_length) and (token not in stopwords)) \
            or (token in spare_words)
    ]

    return " ".join(tokens)

def remove_word_stress(text : str, upper_case=False) -> str:
    '''Remove caracteres com acento.

    Referência: <https://www.w3schools.com/python/ref_string_maketrans.asp>
    '''
    if upper_case:
        raise NotImplementedError()
    else :
        TABLE = TABLE_REMOVE_LOWER_ACCENTS
    
    return text.translate(TABLE)


def remove_punctuation(text : str, punctuation=DEFAULT_PUNCTUATION) -> str:
    return text.translate(
        str.maketrans(punctuation, len(punctuation) * ' ')
    )


def regularize_expressions(text : str, mapper=STANDART_EXPRESSIONS) -> str:
    for pattern, replace in mapper.items():
        text = re.sub(pattern, replace, text, flags = re.MULTILINE | re.IGNORECASE)

    return text


def tokenizer(text : str) -> list:
    return [str(token) for token in word_tokenize(text)]


def regex_tokenizer(text : str, tokenizer_func=RegexpTokenizer(r"\S+")) -> List[str]:
    return tokenizer_func.tokenize(text)


def lemmatize(text : str, model) -> list :
    document = model(text)
    lemmatized = [str(token.lemma_) for token in document]
    return lemmatized


def stemmerize(tokens : List[str], stemmer=RSLPStemmer()) -> list :
    if type(tokens) is str:
        raise TypeError("Tokens should be a list of strings")

    return [stemmer.stem(token) for token in tokens]
