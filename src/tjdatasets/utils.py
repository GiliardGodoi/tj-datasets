import re

def detect_header(s1, s2, minHeaderLen=15):
    '''
    Identifica como header o texto que se repete no início de páginas seguidas
    '''
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
    '''
    Identifica como footer o texto que se repete no final de páginas seguidas
    '''
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
    '''
    Remove cabeçalho e rodapé do texto, baseado na igualdade destes entre páginas.
    As páginas devem ter separador, que será removido no fim do processo.
    '''
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
    return " ".join(v)


legal_stop_words = {
    'grifamos', 'tribunal', 'paulo', 'julgamento', 
    'justiça', 'judiciário', 'superior', 'ação', 
    'civil', 'pública', 'relator', 'feito','ano', 
    'medida', 'interesse','recurso', 'especial',
    'direito','caso','federal', 'competência',
    'sentença','ministro', 'coletiva', 'taxa','acordo',
    'contrato', 'proferida', 'suspensão', 'prescrição'
}
