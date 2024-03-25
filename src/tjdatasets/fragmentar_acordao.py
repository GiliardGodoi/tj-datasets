import re
from dataclasses import dataclass

@dataclass
class Result:
    name : str
    text : str
    re : str = None
    rule : int = -1
    span : tuple = (-1, -1)

    def start(self):
        return self.span[0]

    def end(self):
        return self.span[1]

def find_by_rules(text, patterns):
    result = (None, -1)
    for id_rule, pattern in enumerate(patterns, start=1):
        re_match = pattern.search(text)
        if re_match is not None:
            result = (re_match, id_rule)
            break
    return result

patterns_relator = [
    r'data\s+do\s+julgamento\s+por\s+extenso\s+n.o\s+informado\W+([\w\s\.\']+?)(?:\s+desembargador.)?\W+relator',
    r"de[\s\w]+de\s+\d{4}\W+(?:assinatura\s+eletr.nica|assinatura\s+digital)?\W*([\w\s\.\']{5,50}?)\W+(?:relator.|desembargador.|presidente|assinatura\s+eletr.nica|assinatura\s+digital)",
    r"de\s+\w+\s+de\s+\d{4}\W+([\w\s\.\']{5,50}?)\W+(?:relator.|desembargador.|presidente|assinatura\s+eletr.nica|assinatura\s+digital)",
    r"de\s+\w+\s+de\s+\d{4}\W+([\w\s\.\'\-]+)\D+relatora?",
    r"de\s+\w+\s+de\s+\d{4}\W+([\w\s\.\']+)relatora?",
    r"s.o\s*paulo,\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4}\W*(\w+\s*\w+).*?relator",
    r'data\s+do\s+julgamento\s+por\s+extenso\s+n.o\s+informado\W+([\w\s\.\']+)\D+relatora?',
    r"de[\s\w]+de\s+\d{4}\W+(\w+\s+\w+)",
]

patterns_relator = [re.compile(pattern, flags=re.M | re.I) for pattern in patterns_relator ]

PATTERN_REMOVE_EXTRA_SPACE = re.compile(r'\s+')

PATTERN_REMOVE_SPECIAL_CHARS = re.compile(r"[\[\]—\*\(\)\\/?+\-]+")

PATTERN_REMOVE_HEADER_NOISE = r'(?:poder.*?judiciario.*?tribunal.*?justica|tribunal.*?justica.*?poder.*?judiciario)(?:.*?estado)?(?:.*?sao.*?paulo)?'

PATTERN_REMOVE_SMALL_WORDS = r'\b\w{1,2}\b'

PATTERN_REMOVE_NUMBER = r'\b[\d]+\b'

def identifica_nome_relator(text, patterns=patterns_relator, page_sep='\x0c'):
    result = None
    re_match, rule_id = find_by_rules(text, patterns=patterns)
    if rule_id == -1 :
        result = Result(
            name='nome_relator',
            text=None,
            rule=rule_id,
        )
    else:
        nome_relator = re_match.group(1)
        
        if len(nome_relator) > 50 :
            nome_relator = re.sub(PATTERN_REMOVE_HEADER_NOISE, ' ', nome_relator)
            nome_relator = re.sub(PATTERN_REMOVE_NUMBER, ' ', nome_relator)
            nome_relator = re.sub(PATTERN_REMOVE_SMALL_WORDS, ' ', nome_relator)

        nome_relator = re.sub(PATTERN_REMOVE_EXTRA_SPACE, ' ', nome_relator)
        nome_relator = nome_relator.strip()

        result = Result(
            name='nome_relator',
            text=nome_relator,
            re=re_match.re,
            rule=rule_id,
            span=re_match.span(0) # pegar toda a string
        )

    return result

pattern_decisao_acordao = [
    r"decisao\s?:?([\W\w]+?)\s+?(?:o\s*|\d\s*)?julgamento\W+teve",
    r"decisao\s?:?([\W\w]+?)\s+(?:o\s*)?julgamento",
    r"nte\s[decisao\s-]{7,9}:?([\W\w]+?)\s+?(?:o\s*|\d\s*)?[julgamento\s-]{10,12}\W+teve",
]

pattern_decisao_acordao = [ re.compile(p, flags=re.M|re.I) for p in pattern_decisao_acordao ]

def identifica_decisao(text):
    # Lógica para extrair a decisao
    result = None
    re_match, rule_id = find_by_rules(text, patterns=pattern_decisao_acordao)
    if rule_id == -1 :
        result = Result(
            name='decisao_acordao',
            text=None,
            rule=rule_id,
        )
    else:
        result = Result(
            name='decisao_acordao',
            text=re_match.group(1),
            re=re_match.re,
            rule=rule_id,
            span=re_match.span(1)
        )

    return result

def identifica_voto_relator(text, relator : Result, page_sep='\x0c'):
    result = None
    if (relator is None) or (relator.rule < 0):
        pages = text.split(page_sep) # bad smell
        first_page = pages[0] if len(pages) >= 1 else ''
        result = Result(
            name='voto_relator',
            text=text[len(first_page):],
            rule = -1,
            span=(len(first_page), len(text))
        )
        return result

    nome = relator.text.strip()
    primeiro_caso = nome.strip()[::-1]
    primeiro_caso = r'[\w\s]*?'.join(primeiro_caso.split())

    # segundo caso considera que pode haver espaço inadvertidos 
    # entre as letras de um nome ENI O
    segundo_caso = nome.strip()[::-1]
    segundo_caso = r'[\W\w]*?'.join([
       r'\s*'.join(list(n)) for n in segundo_caso.split()
    ])

    inv_pattern_ultimo_nome_relator = [
        rf'a?rotaler(?:\s+a?rodagrabmesed|\s+\.?sed)?[\w\s]*?{primeiro_caso}',
        rf'odavirp\s*?otierid\s*?ed\s*?o..es\s*?ad\s*?etnediserp[\w\s]*?{primeiro_caso}',

        rf'a?rotaler(?:\s+a?rodagrabmesed|\s+\.?sed)?[\w\s]*?{segundo_caso}',
        rf'odavirp\s*?otierid\s*?ed\s*?o..es\s*?ad\s*?etnediserp[\w\s]*?{segundo_caso}'
    ]

    inv_text = text[::-1]
    for rule_id, pattern in enumerate(inv_pattern_ultimo_nome_relator, start=1):
        inv_pattern = re.compile(pattern, flags=re.M|re.I)
        re_match = inv_pattern.search(inv_text)
        if re_match is not None:
            start = len(text) - re_match.end()
            end = len(text) - re_match.start()
            if relator.end() < end:
                result = Result(
                    name='voto_relator',
                    text=text[relator.end() : end],
                    re=re_match.re,
                    rule=rule_id,
                    span=(relator.end(), end))
                break
            else :
                result = Result(
                    name='voto_relator',
                    text=text[relator.end():],
                    rule=-(rule_id + 100),
                    span=(relator.end(), len(text))
                )
    else:
        # this block will be executed only if the for...loop never encouters
        # the break statement
        result = Result(
            name='voto_relator',
            text=text[relator.end():],
            rule = -2,
            span=(relator.end(), len(text))
        )

    return result

patterns_relatorio = [
    r"e\s*o\s*relat.rio\.?",                        # é o relatório.
    r"(?:e\s*o\s*)*breve\s*relat.\.?",              # é o breve relatório # breve relato
    r"(?:e\s*o|este\s*o)*\s*relat.rio\s*do\s*essencial\.?",
                                                  # é o relatório do essencial
                                                  # Relatório do essencial
                                                  # Este o relatório do essencial.

    r"e\s+a\s+s.ntese\s+do\s+essencial\.?",       # é a síntese do essencial
    r"(?:e\s*o|este\s*o)*\s*relat.rio(?:\s*do)?\s*necess.rio\.?",
                                                    # É o relatório do necessário.
                                                    # Relatório do necessário.
                                                    # Este o relatório do necessário.
                                                    # Este o relatório necessário.
    r"e\s*.\s*?\s*suma(?:\s*do)?\s*necess.rio\.?", # É a suma do necessário.
    r"e\s*a\s+s.ntese(?:\s+do)*\s+necess.ri.\.?",
                                                 # É a sintese do necessário
                                                 # É a síntese necessária.
    r"(?:e\s*o|este\s*o)\s*resumo(?:\s*do)?\s*essencial\.?",
                                                  # É o resumo do essencial
                                                  # Este o resumo do essencial
    r"e\s*como\s*relato\.",                       # É como relato.
    r"e\s+o\s+que\s+importa\s+ser\s+relatado\.?", # É o que importa ser relatado
    r"tempestiva\W+preparada.*?respondida\.",     # Tempestiva, preparada e respondida.
    r"tempestivo\W+respondido.*?isento de preparo.*?\.", # tempestivo, respondido e isento de preparo
    r"recurso\s*regularmente\s*processado", # Recurso regularmente processado
]

patterns_relatorio = [
    re.compile(p, flags=re.M|re.I) for p in patterns_relatorio
]

def identifica_relatorio_voto(text, voto_relator : Result):
    result = None
    re_match, rule_id = find_by_rules(voto_relator.text, patterns=patterns_relatorio)

    if rule_id != -1:
        start, end = voto_relator.start(), voto_relator.start() + re_match.end()

    result = Result(
        name='relatorio',
        text=text[start: end] if rule_id != -1 else None,
        rule=rule_id,
        re= re_match.re if rule_id != -1 else None,
        span=(start, end) if rule_id != -1 else (-1, -1)
    )
    return result

def identifica_fundamentacao_voto(text, voto : Result, relatorio : Result):
    result = None
    if (relatorio.rule < 0) and (voto.rule > 0):
        result = Result(
            name='fundamentacao',
            text=None,
            rule=-1,
        )
    elif (relatorio.rule < 0) and (voto.rule < 0):
        result = Result(
            name='fundamentacao',
            text=None,
             rule=-3,
        )
    elif (relatorio.rule > 0) and (voto.rule < 0):
        # verificar que
        # se não conseguimos identificar apropriadamente o voto do relator
        # tudo da segunda página para frente (excluíndo a folha de rosto)
        # por padrão vai ser considerado o voto do relator,
        # eventualmente a declaração de voto divergente.
        result = Result(
            name='fundamentacao',
            text=text[relatorio.end(): voto.end()],
            rule=-2,
            span=(relatorio.end(), voto.end())
        )
    else:
        result = Result(
            name='fundamentacao',
            text=text[relatorio.end() : voto.end()],
            rule=1,
            span=(relatorio.end(), voto.end())
        )

    return result

def identifica_se_decisao_unamime(decisao_acordao : Result):
    if decisao_acordao.rule == -1:
        return None

    text = decisao_acordao.text.lower()
    return  ('v. u.' in text) \
            or ('v.u.' in text) \
            or ('votação unânime' in text) \
            or ('votacao unanime' in text)

def identifica_voto_divergente(text, voto_relator : Result, decisao : Result):
    '''
    Ainda dá para melhorar a lógica dessa função.
    '''

    if (voto_relator.rule < 0) or (decisao.rule < 0):
        return Result(
                name='voto_divergente',
                text=None,
                rule=-1
            )
    eh_decisao_unanime = identifica_se_decisao_unamime(decisao)
    if eh_decisao_unanime:
        return Result(
                name='voto_divergente',
                text=None,
                rule=0
            )

    result = Result(
        name='voto_divergente',
        text=text[voto_relator.end(): ],
        span=(voto_relator.end(), len(text)),
        rule=1
    )

    return result

def obter_fundamento_decisao(texto : str) -> str :
    
    relator = identifica_nome_relator(texto)
    # decisao = identifica_decisao(texto)
    voto    = identifica_voto_relator(texto, relator)
    relatorio = identifica_relatorio_voto(texto, voto)
    fundamentacao = identifica_fundamentacao_voto(texto, voto, relatorio)

    # por padrão, retorna o texto completo do documento
    texto_resposta = texto 

    # em caso de sucesso rule > 0
    if fundamentacao.rule > 0 :
        texto_resposta = fundamentacao.text
    elif voto.rule > 0 :
        texto_resposta = voto.text
    
    return texto_resposta

def processa_acordao(row, text_column='formatado'):
    text = row[text_column]

    relator = identifica_nome_relator(text)

    decisao = identifica_decisao(text)
    eh_decisao_unanime = identifica_se_decisao_unamime(decisao)

    voto = identifica_voto_relator(text, relator)

    relatorio = identifica_relatorio_voto(text, voto)

    fundamentacao = identifica_fundamentacao_voto(text, voto, relatorio)

    divergente = identifica_voto_divergente(text, voto, decisao)

    return {
        relator.name : relator.text,
        f"{relator.name}_regra" : relator.rule,

        decisao.name : decisao.text,
        f"{decisao.name}_regra" : decisao.rule,
        'decisao_unanime' : eh_decisao_unanime,

        voto.name : voto.text,
        f"{voto.name}_regra" : voto.rule,

        relatorio.name : relatorio.text,
        f"{relatorio.name}_regra" : relatorio.rule,

        fundamentacao.name : fundamentacao.text,
        f"{fundamentacao.name}_regra" : fundamentacao.rule,

        divergente.name : divergente.text,
        f"{divergente.name}_regra" : divergente.rule,
    }
