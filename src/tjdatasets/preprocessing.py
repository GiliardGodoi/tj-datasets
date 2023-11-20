import re
import string
from typing import List
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import RSLPStemmer

abbreviations = {
    r'r\.' : r'respeitável ',
    r'fl\. (?=\d)'  : r'folha_',
    r'fls\. (?=\d)' :  r'folha_',
    r'v\.u\.' : r'votação_unâmime '
}

acronyms = {
    r'rel ' : r'relator ',
    r'min ' : r'ministro ',
    r'resp ' : r'recurso_especial ',
    r' idec ' : r' instituto_brasileiro_de_defesa_do_consumidor ',
    r'art ' : r'artigo ',
    r'arts ' : r'artigos ',
    r'inc ' : r'inciso ',
    r'§ ' : r'parágrafo ',
    r'ministério público' : r'ministério_público ',
    r'ministerio público' : r'ministério_público ',
    r'código processo civil' : r'código_processo_civil  ',
    r'cpd ' : r'código_processo_civil ',
    r'código de defesa do consumidor' : r'código_defesa_consumidor ',
    r'cdc ' : r'código_defesa_consumidor ',
    r' lc ' : r' lei_complementar ',
    r'erga omnes' : r'erga_omnes ',
    r'ação civil publica' : r'ação_civil_publica ',
    r'stj' : r'superior_tribunal_de_justiça ',
    r'stf' : r'supremo_tribunal_federal ',
    r' são paulo ' : r' são_paulo ',
    r' sp ' : r' são_paulo ',
    r' ac ' : r' apelação_cível ',
    r' adm ' : r' administrativo ',
    r' ag ' : r' agravo_de_instrumento ',
    r' agrg ' : r' agravo_regimental ',
    r' ai ' : r' argüição_de_inconstitucionalidade ',
    # r' ana ' : r' agência_nacional_de_águas ',
    r' anatel ' : r' agência_nacional_de_telecomunicações ',
    r' aneel ' : r' agência_nacional_de_energia_elétrica ',
    r' apn ' : r' ação_penal ',
    # r' ar ' : r' ação rescisória ',
    r' cat ' : r' conflito_de_atribuições ',
    # r'cc ' : r'código civil ',
    # r'cc ' : r'conflito de competência ',
    r' ccm ' : r' código_comercial ',
    r' cm ' : r' comercial ',
    r' cne ' : r' conselho_nacional_de_educação_com_comunicação ',
    r' cef ' : r' caixa_econômica_federal  ',
    r' fcvs ' : r' fundo_de_compensação_de_variações_salariais ',
    r' cp ' : r' código_penal ',
    r' cpc ' : r' código_de_processo_civil ',
    r' cdc ' : r' código_de_proteção_e_defesa_do_consumidor ',
    r' cpp ' : r' código_de_processo_penal ',
    r' cr ' : r' carta_rogatória ',
    r' cri ' : r' carta_rogatória_impugnada ',
    r' ct ' : r' código_de_trânsito_brasileiro ',
    r' ctn' : r' código_tributário_nacional ',
    r' cv ' : r' civil ',
    # r' d ' : r' decreto ',
    # r' dl ' : r' decreto-lei ',
    r' dnaee' : r' departamento_nacional_de_águas_e_energia_elétrica ',
    # r' e ' : r' ementário da jurisprudência do superior tribunal de justiça ',
    r' eac ' : r'embargos_infringentes_em_apelação_cível ',
    r' ear ' : r' embargos_infringentes_em_ação rescisória ',
    r' eag ' : r' embargos_de_divergência_no_agravo ',
    r' ec ' : r' emenda_constitucional ',
    r' eca ' : r' estatuto_da_criança_e_do_adolescente ',
    r' edcl ' : r' embargos_de_declaração ',
    r' ejstj ' : r' ementário_da_jurisprudência_do_superior_tribunal_de_justiça ',
    r' el ' : r' eleitoral ',
    r' eresp ' : r' embargos_de_divergência_em_recurso_especial ',
    r' erms ' : r' embargos_infringentes_no_recurso_em_mandado_de_segurança ',
    r' eximp ' : r' exceção_de_impedimento ',
    r' exsusp  ' : r' exceção_de_suspeição ',
    r' exverd ' : r' exceção_da_verdade ',
    r' execar ' : r' execução_em_ação_rescisória ',
    r' execmc ' : r' execução_em_medida_cautelar ',
    r' execms ' : r' execução_em_mandado_de_segurança ',
    r'fcvs' : r'fundo_de_compensação_de_variações_valariais ',
    r' hc ' : r' habeas_corpus ',
    r' habeas corpus ' : r' habeas_corpus ',
    r' hse ' : r' homologação_de_sentença_estrangeira ',
    r' idc ' : r' incidente_de_deslocamento_de_competência ',
    r' iexecc ' : r' incidente_de_execução ',
    r' if ' : r' intervenção_federal ',
    r' ij ' : r' interpelação_judicial ',
    r' inq ' : r' inquérito ',
    r' ipva ' : r' imposto_sobre_a_propriedade_de_veículos_automotores ',
    r' iuj ' : r' incidente_de_uniformização_de_jurisprudência ',
    r' lcp ' : r' lei_das_contravenções_penais ',
    r' loman ' : r' lei_orgânica_da_magistratura ',
    r' lonmp ' : r' lei_orgânica_nacional_do_ministério_público ',
    r' mc ' : r' medida_cautelar ',
    r' mc ' : r' ministério_das_comunicações ',
    r' mi ' : r' mandado_de_injunção ',
    r' ms ' : r' mandado_de_segurança ',
    r' nc ' : r' notícia_crime ',
    r' pa ' : r' processo_administrativo  ',
    r' pet ' : r' petição  ',
    r' pext ' : r' pedido_de_extensão ',
    r' pn ' : r' penal ',
    r' prc ' : r' precatório ',
    r' prcv ' : r'processual_civil ',
    r' prpn ' : r' processual_penal ',
    r' pv ' : r' previdenciário ',
    r' qo ' : r' questão_de_ordem ',
    r' rcl ' : r' reclamação ',
    r' rd ' : r' reconsideração_de_despacho ',
    r' re ' : r' recurso_extraordinário ',
    r' resp ' : r' recurso_especial ',
    r' rhc ' : r' recurso_em_habeas_corpus ',
    r' rmi ' : r' recurso_em_mandado_de_injunção ',
    r' rms ' : r' recurso_em_mandado_de_segurança ',
    r' ro ' : r' recurso_ordinário ',
    r' rp ' : r' representação ',
    r' rtj ' : r' revista_trimestral_de_jurisprudência ',
    r' rstj ' : r' revista_do_superior_tribunal_de_justiça ',
    r' rvcr ' : r' revisão_criminal ',
    r' saf ' : r' secretaria_de_administração_federal ',
    r' sd ' : r' sindicância ',
    r' sec ' : r' sentença_estrangeira_contestada ',
    r' sf ' : r' senado_federal ',
    r' sl ' : r' suspensão_de_liminar ',
    r' sls  ' : r' suspensão_de_liminar_e_de_sentença ' ,
    r' ss  ' : r' suspensão_de_segurança ',
    r' sta ' : r' suspensão_de_tutela_antecipada ',
    r' tr ' : r' trabalho ',
    r' trbt ' : r' tributário ',
    r'http\S+' : r'<URL>'
}


def remove_word_stress(text : str) -> str:
    '''
    Remove word stress from lowercasa words.
    '''
    # https://www.w3schools.com/python/ref_string_maketrans.asp
    return text.translate(
            str.maketrans('áàãâäéèêëóòõôöíìîïúùüç', 'aaaaaeeeeoooooiiiiuuuc')
        )


def remove_punctuation_text(text : str) -> str:
    return text.translate(
        str.maketrans(string.punctuation, len(string.punctuation)* ' ')
    )


def regularize_abbreviations(text : str, abbreviations=abbreviations) -> str:

    for old_str, new_str in abbreviations.items():
        text = re.sub(old_str, new_str, text, flags = re.MULTILINE | re.IGNORECASE)

    return text


def regularize_expressions(text : str, mapper=acronyms) -> str:
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


def stemmerize(tokens : List[str], model) -> list :
    stemmer = RSLPStemmer()
    return [stemmer.stem(token) for token in tokens]
    

