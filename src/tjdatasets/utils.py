# import string

# DEFAULT_PUNCTUATION = string.punctuation + '—”“ªº°'
# DEFAULT_PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\]^`{|}~' + '—”“ªº°'
DEFAULT_PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\]^`{|}~—”“ªº°'


## https://www.stj.jus.br/docs_internet/revista/eletronica/stj-revista-eletronica-2021_263_2_capAbreviaturaseSiglas.pdf
JUR_EXPRESSIONS = {
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
    r'(\W+)fl\.?\d+(\W+)' :  r'\g<1>_FOLHA_NUMERO_\g<2>',
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
    r'http\S+' : r'_URL_'
}

LEG_EXPRESSIONS = {
    r"(Lei)\s+n?[\.º°]?\s?([\d\.\/]+)" : r"\g<1>_\g<2>",
    r"(Lei)\s+(Complementar)\s+n?[\.º°]?\s?([\d\.\/]+)" : r"\g<1>_\g<2>_\g<3>",
    r"(Lei)\s+(Federal|Estadual)\s+n?[\.º°]?\s?([\d\.\/]+)" : r"\g<1>_\g<2>_\g<3>",
    r"(Decreto-Lei)\s+n?[\.º°]?\s?([\d\.\/]+)" : r"\g<1>_\g<2>",
    r"(Decreto)\s+n?[\.º°]?\s?([\d\.\/]+)" : r"\g<1>_\g<2>",
    r"(Decreto)\s+(Federal|Estadual)\s+n?[\.º°]?\s?([\d\.\/]+)" : r"\g<1>_\g<2>",
    r"(Resolução)\s+n?[\.º°]?\s?([\d\.\/]+)" : r"\g<1>_\g<2>",
    r"(Portaria)\s+n?[\.º°]?\s?([\d\.\/]+)" : r"\g<1>_\g<2>",
    r"(Súmula)\s+n?[\.º°]?\s?([\d\.\/]+)" : r"\g<1>_\g<2>",
    r"(Súmula)\s+(vinculante)\s+n?[\.º°]?\s?([\d\.\/-]+)" : r"\g<1>_\g<2>_\g<3>",
    r"(Medida)\s+(Provisória)\s+n?[\.º°]?\s?([\d\.\/-]+)" : r"\g<1>_\g<2>_\g<3>",
    r"(Voto)\s+n?[\.º°]?\s?([\d\.\/-]+)" : r"_REGISTRO_VOTO_",
    r"MP\s+([\d\/\.-]+)" : r"Medida_Provisória_\g<1>",
    r"art\.?\s+([\d\w-]+)" : r"artigo_\g<1>",
    r"artigo\s+([\d\w-]+)" : r"artigo_\g<1>",
    r"§\s?(\d+)" : r"parágrafo_\g<1>",
    r"c\.c\." : "combinado com",
    r"\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}" : r"_REGISTRO_JURIDICO_", # Possível formato para número de processo
    r"\d{4}\.\d{10}" : r"_REGISTRO_JURIDICO_",  # Possível formato para código de registro
    r"R\$\s*[\d\,\.]+" : r"_VALOR_MONETARIO_", # Possível formato de dinheiro (real)
    r"\d{1,2}\.\d{1,2}\.\d{2,4}" : r"_DATA_", # Possível formato de data
    r"\d{1,2}\/\d{1,2}\/\d{2,4}" : r"_DATA_", # Possível formato de data
    r"(\w+)\/(\w+)" : r"\g<1>_\g<2>",
    r"([a-zA-Z]+)(\d+)" : r"\g<1> \g<2>", # captura qualquer palavra seguida de número e acrescenta um espaço
    r"\d+\s*\%" : "_PORCENTAGEM_",
    r"(\d)\.(\d)" : r"\g<1>\g<2>", # Se observar um ponto no meio de dois números, unir os números
}


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

JUR_STOPWORDS = {
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
