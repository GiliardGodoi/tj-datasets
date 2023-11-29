import re


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


STOP_WORDS_SPACY = {
    "custa",
    "outros",
    "oitavo",
    "estás",
    "novos",
    "relação",
    "como",
    "dez",
    "faço",
    "quê",
    "tive",
    "ele",
    "não",
    "até",
    "falta",
    "logo",
    "saber",
    "grupo",
    "faz",
    "tentar",
    "meus",
    "ambos",
    "nas",
    "ir",
    "inclusive",
    "fostes",
    "sistema",
    "naquele",
    "possível",
    "toda",
    "desde",
    "certeza",
    "estava",
    "nove",
    "estes",
    "mil",
    "ao",
    "seis",
    "são",
    "apoio",
    "está",
    "bem",
    "vens",
    "quinto",
    "porquê",
    "através",
    "às",
    "em",
    "diante",
    "des",
    "iniciar",
    "ser",
    "pode",
    "tu",
    "poderá",
    "tentei",
    "novas",
    "quer",
    "tal",
    "aí",
    "uma",
    "conhecida",
    "põe",
    "área",
    "quieta",
    "a",
    "fazia",
    "coisa",
    "dezoito",
    "tanta",
    "nossa",
    "tivestes",
    "treze",
    "poder",
    "de",
    "umas",
    "menor",
    "vêm",
    "mais",
    "corrente",
    "usar",
    "deve",
    "estou",
    "dois",
    "diz",
    "estiveram",
    "quinze",
    "quem",
    "ali",
    "sete",
    "fomos",
    "quarto",
    "seria",
    "querem",
    "ainda",
    "atrás",
    "sou",
    "lugar",
    "dá",
    "qualquer",
    "bom",
    "favor",
    "maiorias",
    "todos",
    "o",
    "sétima",
    "já",
    "ou",
    "pôde",
    "ambas",
    "dizem",
    "conhecido",
    "eu",
    "onde",
    "meio",
    "pelo",
    "esse",
    "aquela",
    "veja",
    "tipo",
    "estado",
    "ter",
    "tentaram",
    "quatro",
    "do",
    "quais",
    "fazer",
    "próxima",
    "neste",
    "tem",
    "tiveram",
    "elas",
    "antes",
    "outras",
    "só",
    "eles",
    "com",
    "obrigado",
    "apoia",
    "também",
    "debaixo",
    "forma",
    "dezanove",
    "maior",
    "aquilo",
    "longe",
    "por",
    "quinta",
    "ademais",
    "fazem",
    "tiveste",
    "esses",
    "seu",
    "numa",
    "onze",
    "zero",
    "no",
    "pelos",
    "que",
    "questão",
    "cá",
    "fui",
    "mesmo",
    "menos",
    "era",
    "após",
    "muito",
    "cuja",
    "sob",
    "maioria",
    "puderam",
    "sempre",
    "aquelas",
    "pelas",
    "vez",
    "e",
    "nossos",
    "segundo",
    "povo",
    "máximo",
    "tente",
    "local",
    "tuas",
    "vinte",
    "contudo",
    "este",
    "primeira",
    "mês",
    "minhas",
    "os",
    "parte",
    "oito",
    "próximo",
    "nessa",
    "isto",
    "se",
    "aos",
    "porque",
    "sim",
    "cento",
    "aqueles",
    "entre",
    "vinda",
    "vossas",
    "lhe",
    "pouco",
    "terceiro",
    "adeus",
    "podia",
    "sobre",
    "suas",
    "fez",
    "tais",
    "comprida",
    "todas",
    "duas",
    "pontos",
    "baixo",
    "primeiro",
    "ligado",
    "sois",
    "foi",
    "vosso",
    "vossa",
    "estão",
    "nesta",
    "porquanto",
    "dezasseis",
    "estará",
    "dão",
    "final",
    "último",
    "estas",
    "esta",
    "temos",
    "pois",
    "agora",
    "nesse",
    "alguns",
    "outra",
    "certamente",
    "nos",
    "oitava",
    "tanto",
    "tendes",
    "das",
    "apontar",
    "essa",
    "parece",
    "da",
    "fazes",
    "nível",
    "meu",
    "vossos",
    "demais",
    "mal",
    "nem",
    "pela",
    "bastante",
    "somente",
    "estar",
    "cada",
    "minha",
    "podem",
    "foste",
    "nosso",
    "tens",
    "dizer",
    "todo",
    "assim",
    "você",
    "têm",
    "conselho",
    "esteve",
    "lá",
    "fará",
    "tarde",
    "és",
    "põem",
    "pegar",
    "cujo",
    "muitos",
    "tudo",
    "tempo",
    "obrigada",
    "sem",
    "dos",
    "portanto",
    "aqui",
    "vem",
    "pouca",
    "estivestes",
    "fazeis",
    "número",
    "mas",
    "nossas",
    "devem",
    "vocês",
    "sua",
    "posição",
    "tua",
    "depois",
    "dentro",
    "ontem",
    "talvez",
    "teu",
    "vezes",
    "breve",
    "perto",
    "grande",
    "momento",
    "segunda",
    "porém",
    "ela",
    "tivemos",
    "cedo",
    "daquele",
    "vários",
    "vindo",
    "nuns",
    "daquela",
    "quieto",
    "somos",
    "catorze",
    "novo",
    "caminho",
    "direita",
    "à",
    "possivelmente",
    "estiveste",
    "meses",
    "além",
    "deverá",
    "dar",
    "doze",
    "sétimo",
    "três",
    "algo",
    "naquela",
    "geral",
    "fazemos",
    "tenho",
    "para",
    "irá",
    "nenhuma",
    "essas",
    "estivemos",
    "cima",
    "ora",
    "fora",
    "nova",
    "desta",
    "inicio",
    "ponto",
    "ver",
    "vais",
    "sei",
    "exemplo",
    "nunca",
    "usa",
    "partir",
    "números",
    "grandes",
    "isso",
    "contra",
    "valor",
    "disso",
    "estive",
    "nada",
    "apenas",
    "posso",
    "enquanto",
    "teus",
    "dezassete",
    "desse",
    "seus",
    "eventual",
    "te",
    "dessa",
    "é",
    "um",
    "as",
    "for",
    "tão",
    "quero",
    "quando",
    "próprio",
    "quarta",
    "foram",
    "me",
    "quanto",
    "na",
    "boa",
    "então",
    "vai",
    "lado",
    "qual",
    "acerca",
    "cinco",
    "sabe",
    "num",
    "sexto",
    "comprido",
    "embora",
    "vós",
    "vão",
    "vos",
    "aquele",
    "fim",
    "deste",
    "algumas",
    "uns",
    "nós",
    "terceira",
    "sexta",
    "teve",
}

legal_stop_words = {
    "grifamos",
    "tribunal",
    "paulo",
    "julgamento",
    "justiça",
    "judiciário",
    "superior",
    "ação",
    "civil",
    "pública",
    "relator",
    "feito",
    "ano",
    "medida",
    "interesse",
    "recurso",
    "especial",
    "direito",
    "caso",
    "federal",
    "competência",
    "sentença",
    "ministro",
    "coletiva",
    "taxa",
    "acordo",
    "contrato",
    "proferida",
    "suspensão",
    "prescrição",
}
