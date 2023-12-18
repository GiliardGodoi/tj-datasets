from .utils import remove_header, remove_footer, STOP_WORDS_SPACY
import re
import string
from typing import List
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import RSLPStemmer

DEFAULT_PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\]^`{|}~' + '—”“ªº°'

## https://www.stj.jus.br/docs_internet/revista/eletronica/stj-revista-eletronica-2021_263_2_capAbreviaturaseSiglas.pdf
EXPRESSIONS = {
    r'exmo\.?s?\.?(\s)' : r'excelentíssimo\g<1>',
    r'(\W+)n\.(\W+)' : r'',
    r'(\W+)c\.(\W+)' : r'\g<1>colendo\g<2>',
    r'dje\.?\s+(?=\d+)' :  r'diário_justiça_união ',
    r'dje\.?\s+(?=\d+)' :  r'diário_justiça_eletrônico ',
    r'(\W+)j\.(\W+)' : r'\g<1>julgado\g<2>',
    r'(\W+)p\.?\s*(?=\d+)' : r'\g<1>página_',
    r'(\W+)r\.(\W+)' : r'\g<1>respeitável\g<2>',
    r'(\W+)t\.(\W+)' : r'\g<1>turma\g<2>',
    r'(\W+)fls\.?\d+(\W+)'  : r'\g<1>_FOLHA_NUMERO_\g<2>',
    r'(\W+)fls\.?\d+(\W+)' :  r'\g<1>_FOLHA_NUMERO_\g<2>',
    r'v\.\s*u\.' : r'votação unâmime',
    r'rel\.?\s+' : r'relator ',
    r'min\.?\s+' : r'ministro ',
    r'\sidec\s ' : r' instituto_brasileiro_de_defesa_do_consumidor ',
    r'art\.? ' : r'artigo ',
    r'arts\.? ' : r'artigos ',
    r'inc\.? ' : r'inciso ',
    r'§{1,2}\s*(?=[\d])' : r'parágrafo ',
    r'ministério público' : r'ministério_público ',
    r'ministerio público' : r'ministério_público ',
    r'código processo civil' : r'código_processo_civil  ',
    r'código de defesa do consumidor' : r'código_defesa_consumidor ',
    r'(\W+)lc(\W+)' : r'\g<1>lei_complementar\g<2>',
    r'erga omnes' : r'erga_omnes ',
    r'ação civil publica' : r'ação_civil_publica ',
    r'stj' : r'superior_tribunal_de_justiça ',
    r'stf' : r'supremo_tribunal_federal ',
    r'(\W+)são\s+paulo(\W+)' : r'\g<1>são_paulo\g<2>',
    r'(\W+)sp(\W+)' : r'\g<1>são_paulo\g<2>',
    r'(\W+)ac(\W+)' : r'\g<1>apelação_cível\g<2>',
    r'(\W+)adm(\W+)' : r'\g<1>administrativo\g<2>',
    r'(\W+)ag(\W+)' : r'\g<1>agravo_de_instrumento\g<2>',
    r'(\W+)agrg(\W+)' : r'\g<1>agravo_regimental\g<2>',
    r'(\W+)ai(\W+)' : r'\g<1>arguição_de_inconstitucionalidade\g<2>',
    r'(\W+)adpf(\W+)' : r'\g<1>arguição_de_descumprimento_de_preceito_fundamental\g<2>',
    # r'(\W+)ana(\W+)' : r' agência_nacional_de_águas ',
    r'(\W+)anatel(\W+)' : r'\g<1>agência_nacional_de_telecomunicações\g<2>',
    r'(\W+)aneel(\W+)' : r'\g<1>agência_nacional_de_energia_elétrica\g<2>',
    r'(\W+)apn(\W+)' : r'\g<1>ação_penal\g<2>',
    # '(\W+)ar(\W+)' : r'\g<1>ação rescisória\g<2>',
    r'(\W+)cat(\W+)' : r'\g<1>conflito_de_atribuições\g<2>',
    # r'(\W+)cc(\W+)' : r'\g<1>código civil\g<2>',
    # r'(\W+)cc(\W+)' : r'\g<1>conflito de competência\g<2>',
    r'(\W+)ccm(\W+)' : r'\g<1>código_comercial\g<2>',
    r'(\W+)cm(\W+)' : r'\g<1>comercial\g<2>',
    r'(\W+)cne(\W+)' : r'\g<1>conselho_nacional_de_educação_com_comunicação\g<2>',
    r'(\W+)cef(\W+)' : r'\g<1>caixa_econômica_federal\g<2>',
    r'(\W+)fcvs(\W+)' : r'\g<1>fundo_de_compensação_de_variações_salariais\g<2>',
    r'(\W+)cp(\W+)' : r'\g<1>código_penal\g<2>',
    r'(\W+)cpc(\W+)' : r'\g<1>código_de_processo_civil\g<2>',
    # r'(\W+)cdc(\W+)' : r'\g<1>código_de_proteção_e_defesa_do_consumidor\g<2>',
    r'(\W+)cdc(\W+)' : r'\g<1>código_defesa_consumidor\g<2>',
    r'(\W+)cpp(\W+)' : r'\g<1>código_de_processo_penal\g<2>',
    r'(\W+)cr(\W+)' : r'\g<1>carta_rogatória\g<2>',
    r'(\W+)cri(\W+)' : r'\g<1>carta_rogatória_impugnada\g<2>',
    r'(\W+)ct(\W+)' : r'\g<1>código_de_trânsito_brasileiro\g<2>',
    r'(\W+)ctn(\W+)' : r'\g<1>código_tributário_nacional\g<2>',
    r'(\W+)cv(\W+)' : r'\g<1>civil\g<2>',
    # '(\W+)d(\W+)' : r\g<1> decreto\g<2>',
    # '(\W+)dl(\W+)' :\g<1>r' decreto-lei\g<2>',
    r'(\W+)dnaee(\W+)' : r'\g<1>departamento_nacional_de_águas_e_energia_elétrica\g<2>',
    # r'(\W+)e(\W+)' : r\g<1>ementário da jurisprudência do superior tribunal de justiça\g<2>',
    r'(\W+)eac(\W+)' : r'\g<1>embargos_infringentes_em_apelação_cível\g<2>',
    r'(\W+)ear(\W+)' : r'\g<1>embargos_infringentes_em_ação rescisória\g<2>',
    r'(\W+)eag(\W+)' : r'\g<1>embargos_de_divergência_no_agravo\g<2>',
    r'(\W+)ec(\W+)' : r'\g<1>emenda_constitucional\g<2>',
    r'(\W+)eca(\W+)' : r'\g<1>estatuto_da_criança_e_do_adolescente\g<2>',
    r'(\W+)edcl(\W+)' : r'\g<1>embargos_de_declaração\g<2>',
    r'(\W+)ejstj(\W+)' : r'\g<1>ementário_da_jurisprudência_do_superior_tribunal_de_justiça\g<2>',
    r'(\W+)el(\W+)' : r'\g<1>eleitoral\g<2>',
    r'(\W+)eresp(\W+)' : r'\g<1>embargos_de_divergência_em_recurso_especial\g<2>',
    r'(\W+)erms(\W+)' : r'\g<1>embargos_infringentes_no_recurso_em_mandado_de_segurança\g<2>',
    r'(\W+)eximp(\W+)' : r'\g<1>exceção_de_impedimento\g<2>',
    r'(\W+)exsusp(\W+) ' : r'\g<1>exceção_de_suspeição\g<2>',
    r'(\W+)exverd(\W+)' : r'\g<1>exceção_da_verdade\g<2>',
    r'(\W+)execar(\W+)' : r'\g<1>execução_em_ação_rescisória\g<2>',
    r'(\W+)execmc(\W+)' : r'\g<1>execução_em_medida_cautelar\g<2>',
    r'(\W+)execms(\W+)' : r'\g<1>execução_em_mandado_de_segurança\g<2>',
    r'(\W+)hc(\W+)' : r'\g<1>habeas_corpus\g<2>',
    r'(\W+)habeas\s+corpus(\W+)' : r'\g<1>habeas_corpus\g<2>',
    r'(\W+)hse(\W+)' : r'\g<1>homologação_de_sentença_estrangeira\g<2>',
    r'(\W+)idc(\W+)' : r'\g<1>incidente_de_deslocamento_de_competência\g<2>',
    r'(\W+)iexecc(\W+)' : r'\g<1>incidente_de_execução\g<2>',
    r'(\W+)if(\W+)' : r'\g<1>intervenção_federal\g<2>',
    r'(\W+)ij(\W+)' : r'\g<1>interpelação_judicial\g<2>',
    r'(\W+)inq(\W+)' : r'\g<1>inquérito\g<2>',
    r'(\W+)ipva(\W+)' : r'\g<1>imposto_sobre_a_propriedade_de_veículos_automotores\g<2>',
    r'(\W+)iuj(\W+)' : r'\g<1>incidente_de_uniformização_de_jurisprudência\g<2>',
    r'(\W+)lcp(\W+)' : r'\g<1>lei_das_contravenções_penais\g<2>',
    r'(\W+)loman(\W+)' : r'\g<1>lei_orgânica_da_magistratura\g<2>',
    r'(\W+)lonmp(\W+)' : r'\g<1>lei_orgânica_nacional_do_ministério_público\g<2>',
    r'(\W+)mc(\W+)' : r'\g<1>medida_cautelar\g<2>',
    r'(\W+)mc(\W+)' : r'\g<1>ministério_das_comunicações\g<2>',
    r'(\W+)mi(\W+)' : r'\g<1>mandado_de_injunção\g<2>',
    r'(\W+)ms(\W+)' : r'\g<1>mandado_de_segurança\g<2>',
    r'(\W+)nc(\W+)' : r'\g<1>notícia_crime\g<2>',
    r'(\W+)pa(\W+)' : r'\g<1>processo_administrativo\g<2>',
    r'(\W+)pet(\W+)' : r'\g<1>petição\g<2>',
    r'(\W+)pext(\W+)' : r'\g<1>pedido_de_extensão\g<2>',
    r'(\W+)pn(\W+)' : r'\g<1>penal\g<2>',
    r'(\W+)prc(\W+)' : r'\g<1>precatório\g<2>',
    r'(\W+)prcv(\W+)' : r'\g<1>processual_civil\g<2>',
    r'(\W+)prpn(\W+)' : r'\g<1>processual_penal\g<2>',
    r'(\W+)pv(\W+)' : r'\g<1>previdenciário\g<2>',
    r'(\W+)qo(\W+)' : r'\g<1>questão_de_ordem\g<2>',
    r'(\W+)rcl(\W+)' : r'\g<1>reclamação\g<2>',
    r'(\W+)rd(\W+)' : r'\g<1>reconsideração_de_despacho\g<2>',
    r'(\W+)re(\W+)' : r'\g<1>recurso_extraordinário\g<2>',
    r'(\W+)resp(\W+)' : r'\g<1>recurso_especial\g<2>',
    r'(\W+)rhc(\W+)' : r'\g<1>recurso_em_habeas_corpus\g<2>',
    r'(\W+)rmi(\W+)' : r'\g<1>recurso_em_mandado_de_injunção\g<2>',
    r'(\W+)rms(\W+)' : r'\g<1>recurso_em_mandado_de_segurança\g<2>',
    r'(\W+)ro(\W+)' : r'\g<1>recurso_ordinário\g<2>',
    r'(\W+)rp(\W+)' : r'\g<1>representação\g<2>',
    r'(\W+)rtj(\W+)' : r'\g<1>revista_trimestral_de_jurisprudência\g<2>',
    r'(\W+)ristj(\W+)' : r'\g<1>regimento_interno superior_tribunal_justiça\g<2>',
    r'(\W+)rstj(\W+)' : r'\g<1>revista_do_superior_tribunal_de_justiça\g<2>',
    r'(\W+)rvcr(\W+)' : r'\g<1>revisão_criminal\g<2>',
    r'(\W+)saf(\W+)' : r'\g<1>secretaria_de_administração_federal\g<2>',
    r'(\W+)sd(\W+)' : r'\g<1>sindicância\g<2>',
    r'(\W+)sec(\W+)' : r'\g<1>sentença_estrangeira_contestada\g<2>',
    r'(\W+)sf(\W+)' : r'\g<1>senado_federal\g<2>',
    r'(\W+)sl(\W+)' : r'\g<1>suspensão_de_liminar\g<2>',
    r'(\W+)sls(\W+) ' : r'\g<1>suspensão_de_liminar_e_de_sentença\g<2>',
    r'(\W+)ss(\W+) ' : r'\g<1>suspensão_de_segurança\g<2>',
    r'(\W+)sta(\W+)' : r'\g<1>suspensão_de_tutela_antecipada\g<2>',
    r'(\W+)tr(\W+)' : r'\g<1>trabalho\g<2>',
    r'(\W+)trbt(\W+)' : r'\g<1>tributário\g<2>',
    r'http\S+' : r'<URL>'
}


def remove_noise_from_header(text : str) -> str:
    doc = list()
    for page in re.split(r'\x0c', text):
        page = re.sub(r'^(.*?)(PODER JUDICIÁRIO)', 'PODER JUDICIÁRIO', page, flags=re.DOTALL)
        page = re.sub(r'PODER JUDICIÁRIO.*?TRIBUNAL DE JUSTIÇA', 'PODER JUDICIÁRIO\nTRIBUNAL DE JUSTIÇA', page, flags=re.DOTALL)
        doc.append(page)

    return '\x0c'.join(doc)


def remove_stopwords(tokens : List[str], stopwords=STOP_WORDS_SPACY) -> List[str]:
    if not type(tokens) is list:
        raise TypeError(f"tokens should be a list of strings, but received a {type(tokens)}.\nConsider apply a tokenization before.")
    
    if type(stopwords) is list:
        stopwords = set(stopwords)

    return [token for token in tokens if token not in stopwords]


def remove_short_words(tokens: List, min_lenght=3) -> List[str]:
    if not type(tokens) is list:
        raise TypeError(f"tokens should be a list of strings, but received a {type(tokens)}.\nConsider apply a tokenization before.")
    return [token for token in tokens if len(token) > min_lenght]


def remove_word_stress(text : str) -> str:
    '''
    Remove word stress from lowercasa words.
    '''
    # https://www.w3schools.com/python/ref_string_maketrans.asp
    return text.translate(
            str.maketrans('áàãâäéèêëóòõôöíìîïúùüç', 'aaaaaeeeeoooooiiiiuuuc')
        )


def remove_punctuation(text : str, punctuation=DEFAULT_PUNCTUATION) -> str:
    return text.translate(
        str.maketrans(punctuation, len(punctuation) * ' ')
    )


def regularize_expressions(text : str, mapper=EXPRESSIONS) -> str:
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


def stemmerize(tokens : List[str]) -> list :
    if type(tokens) is str:
        raise TypeError("Tokens should be a list of strings")
    
    stemmer = RSLPStemmer()
    return [stemmer.stem(token) for token in tokens]
    
def naive_sentence_segmenter(text: str) -> List[str]:
    return re.split(r'\. ', text)
