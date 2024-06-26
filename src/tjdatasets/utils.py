import pandas as pd
import re

from pathlib import Path

# DEFAULT_PUNCTUATION = string.punctuation + '—”“ªº°'
# DEFAULT_PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\]^`{|}~' + '—”“ªº°'
DEFAULT_PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\]^`{|}~—”“ªº°'

PATTERN_REMOVE_EXTRA_SPACE = re.compile(r'\s+')
PATTERN_REMOVE_SPECIAL_CHARS = re.compile(r"[\[\]—\*]+")
TABLE_REMOVE_LOWER_ACCENTS = str.maketrans('áàãâäéèêëóòõôöíìîïúùüç', 'aaaaaeeeeoooooiiiiuuuc')
TABLE_REMOVE_UPPER_ACCENTS = str.maketrans('ÁÀÃÂÄÉÈÊËÓÒÕÔÖÍÌÎÏÚÙÜÇ', 'AAAAAEEEEOOOOOIIIIUUUC')
TABLE_REMOVE_ACCENTS = str.maketrans('áàãâäéèêëóòõôöíìîïúùüçÁÀÃÂÄÉÈÊËÓÒÕÔÖÍÌÎÏÚÙÜÇ', 'aaaaaeeeeoooooiiiiuuucAAAAAEEEEOOOOOIIIIUUUC')

## https://www.stj.jus.br/docs_internet/revista/eletronica/stj-revista-eletronica-2021_263_2_capAbreviaturaseSiglas.pdf
STANDART_EXPRESSIONS = {
    # Referente a pessoas
    r'exmo\.?s?\.?(\s)' : r'excelentissimo\g<1>',
    r'rel\.' : r'relator',
    r'min\.' : r'ministro',
    
    # abreviações comuns em textos jurídicos
    r'c\.(?=\s+\w+)' : r'colendo ',
    r'dje\.?\s+(?=\d+)' :  r'diario_justica_uniao ',
    r'dje\.?\s+(?=\d+)' :  r'diario_justica_eletronico ',
    r'(?:\W+)j\.\s*?\d{1,2}[\.\/]\d{1,2}[\.\/]\d{2,4}' : r'_DATA_JULGAMENTO_',
    r'(\W+)p\.?\s*(?=\d+)' : r'\g<1>pagina_',
    r'(\W+)r\.(\W+)' : r'\g<1>respeitavel\g<2>',
    r'(\W+)t\.(\W+)' : r'\g<1>turma\g<2>',
    r'fls(?=\.?\s+\d+)'  : r'_folha_',
    r'fl(?=\.?\s+\d+)' :  r'_folha_',
    r'v\.\s{0,1}u\.' : r'votacao_unamime',
    r"arts?\.?\s+([\d\w-]+)" : r"artigo_\g<1>",
    r"artigo\s+([\d\w-]+)" : r"artigo_\g<1>",
    r"§\s?(\d+)" : r"parágrafo_\g<1>",
    r'inc\.? ' : r'inciso ',
    r'§{1,2}\s*(?=[\d])' : r'paragrafo ',
    r'(\W+)lc(\W+)' : r'\g<1>lei_complementar\g<2>',

    # expressões em latim
    r'erga\s+omnes' : r'erga_omnes ',
    r'quantum\s+exequendum' : r'quantum_exequendum',
    r'quantum\s+debeatur' : r'quantum_debeatur',
    r'habeas\s+corpus' : r'habeas_corpus',
    r'(\W+)hc(\W+)' : r'\g<1>habeas_corpus\g<2>',

    r'(\W+)idec(\W+)' : r'\g<1>instituto_brasileiro_defesa_consumidor\g<2>',
    r'(\W+)stj(\W+)' : r'\g<1>superior_tribunal_justica\g<2>',
    r'superior\s+tribunal\s+(?:de\s+)?justi(?:ç|c)a' : r'superior_tribunal_justica',
    r'(\W+)stf(\W+)' : r'supremo_tribunal_federal',
    r'supremo\s+tribunal\s+federal' : r'supremo_tribunal_federal',
    r'(\W+?)s(?:a|ã)o\s+paulo(\W+?)' : r'\g<1>sao_paulo\g<2>',
    r'(\W+)sp(\W+)' : r'\g<1>sao_paulo\g<2>',
    r'(\W+)ac(\W+)' : r'\g<1>apelacao_civel\g<2>',
    r'(\W+)adm(\W+)' : r'\g<1>administrativo\g<2>',
    r'(\W+)ag(\W+)' : r'\g<1>agravo_de_instrumento\g<2>',
    r'(\W+)agrg(\W+)' : r'\g<1>agravo_regimental\g<2>',
    r'(\W+)ai(\W+)' : r'\g<1>arguicao_de_inconstitucionalidade\g<2>',
    r'(\W+)adpf(\W+)' : r'\g<1>arguicao_de_descumprimento_de_preceito_fundamental\g<2>',
    # r'(\W+)ana(\W+)' : r' agencia_nacional_de_águas ',
    r'(\W+)anatel(\W+)' : r'\g<1>agencia_nacional_telecomunicacoes\g<2>',
    r'(\W+)aneel(\W+)' : r'\g<1>agencia_nacional_energia_eletrica\g<2>',
    r'(\W+)apn(\W+)' : r'\g<1>acao_penal\g<2>',
    r'(\W+)acp(\W+)' : r'\g<1>acao_civil_publica\g<2>',
    r"a(?:ç|c)(?:ã|a)o\s+c(?:i|í)vil\s+p(?:ú|u)blica" : r"acao_civil_publica",
    # '(\W+)ar(\W+)' : r'\g<1>ação rescisória\g<2>',
    r'(\W+)cat(\W+)' : r'\g<1>conflito_de_atribuicoes\g<2>',
    # r'(\W+)cc(\W+)' : r'\g<1>código civil\g<2>',
    # r'(\W+)cc(\W+)' : r'\g<1>conflito de competência\g<2>',
    r'c(?:ó|o)digo\s+c(?:í|i)vil' : r'codigo_civil',
    r'(\W+)ccm(\W+)' : r'\g<1>codigo_comercial\g<2>',
    r'c(?:ó|o)digo\s+comercial' : r'codigo_comercial',
    r'(\W+)cm(\W+)' : r'\g<1>comercial\g<2>',
    r'(\W+)cne(\W+)' : r'\g<1>conselho_nacional_de_educacao_com_comunicacao\g<2>',
    r'(\W+)cef(\W+)' : r'\g<1>caixa_economica_federal\g<2>',
    r'caixa\s+econ(?:ô|o)mica\s+federal' : r'caixa_economica_federal',
    r'(\W+)fcvs(\W+)' : r'\g<1>fundo_de_compensacao_de_variacoes_salariais\g<2>',
    r'(\W+)cpc(\W+)' : r'\g<1>codigo_processo_civil\g<2>',
    r'c(?:ó|o)digo\s+(?:de\s+)?processo\s+c(?:i|í)vil' : r'codigo_processo_civil',
    r'(\W+)cdc(\W+)' : r'\g<1>codigo_defesa_consumidor\g<2>',
    r'c(?:o|ó)digo\s+(?:de\s*?)?defesa\s+(?:do\s+)?consumidor' : r'codigo_defesa_consumidor',
    r'(\W+)cp(\W+)' : r'\g<1>codigo_penal\g<2>',
    r'c(?:ó|o)digo\s+penal' : r'codigo_penal',
    r'(\W+)cpp(\W+)' : r'\g<1>codigo_processo_penal\g<2>',
    r'c(?:ó|o)digo\s+(?:de\s+)?processo\s+penal' : r'codigo_processo_penal',
    r'(\W+)cr(\W+)' : r'\g<1>carta_rogatoria\g<2>',
    r'(\W+)cri(\W+)' : r'\g<1>carta_rogatoria_impugnada\g<2>',
    r'(\W+)ct(\W+)' : r'\g<1>codigo_transito_brasileiro\g<2>',
    r'c(?:ó|o)digo\s+(?:de\s+)?tr(?:â|a)nsito\s+brasileiro' : r'codigo_transito_brasileiro',
    r'(\W+)ctn(\W+)' : r'\g<1>codigo_tributario_nacional\g<2>',
    r'c(?:ó|o)digo\s+(?:de\s+)?tribut(?:á|a)rio\s+nacional' : r'codigo_tributario_nacional',
    r'(\W+)cv(\W+)' : r'\g<1>civil\g<2>',
    r'minist(?:e|é)rio\s+p(?:u|ú)blico' : r'ministerio_publico ',
    # '(\W+)d(\W+)' : r\g<1> decreto\g<2>',
    # '(\W+)dl(\W+)' :\g<1>r' decreto-lei\g<2>',
    r'(\W+)dnaee(\W+)' : r'\g<1>departamento_nacional_aguas_energia_eletrica\g<2>',
    # r'(\W+)e(\W+)' : r\g<1>ementário da jurisprudência do superior tribunal de justiça\g<2>',
    r'(\W+)eac(\W+)' : r'\g<1>embargos_infringentes_em_apelacao_civel\g<2>',
    r'(\W+)ear(\W+)' : r'\g<1>embargos_infringentes_em_acao_rescisoria\g<2>',
    r'(\W+)eag(\W+)' : r'\g<1>embargos_de_divergencia_no_agravo\g<2>',
    r'(\W+)ec(\W+)' : r'\g<1>emenda_constitucional\g<2>',
    r'(\W+)eca(\W+)' : r'\g<1>estatuto_da_crianca_e_do_adolescente\g<2>',
    r'(\W+)edcl(\W+)' : r'\g<1>embargos_de_declaracao\g<2>',
    r'(\W+)ejstj(\W+)' : r'\g<1>ementario_da_jurisprudencia_do_superior_tribunal_de_justica\g<2>',
    r'(\W+)el(\W+)' : r'\g<1>eleitoral\g<2>',
    r'(\W+)eresp(\W+)' : r'\g<1>embargos_de_divergencia_em_recurso_especial\g<2>',
    r'(\W+)erms(\W+)' : r'\g<1>embargos_infringentes_no_recurso_em_mandado_de_segurança\g<2>',
    r'(\W+)eximp(\W+)' : r'\g<1>excecao_de_impedimento\g<2>',
    r'(\W+)exsusp(\W+) ' : r'\g<1>excecao_de_suspeicao\g<2>',
    r'(\W+)exverd(\W+)' : r'\g<1>excecao_da_verdade\g<2>',
    r'(\W+)execar(\W+)' : r'\g<1>execucao_em_acao_rescisoria\g<2>',
    r'(\W+)execmc(\W+)' : r'\g<1>execucao_em_medida_cautelar\g<2>',
    r'(\W+)execms(\W+)' : r'\g<1>execucao_em_mandado_de_segurança\g<2>',
    r'(\W+)hse(\W+)' : r'\g<1>homologacao_de_sentenca_estrangeira\g<2>',
    r'(\W+)idc(\W+)' : r'\g<1>incidente_de_deslocamento_de_competencia\g<2>',
    r'(\W+)iexecc(\W+)' : r'\g<1>incidente_de_execucao\g<2>',
    r'(\W+)if(\W+)' : r'\g<1>intervencao_federal\g<2>',
    r'(\W+)ij(\W+)' : r'\g<1>interpelacao_judicial\g<2>',
    r'(\W+)inq(\W+)' : r'\g<1>inquerito\g<2>',
    r'(\W+)ipva(\W+)' : r'\g<1>imposto_sobre_a_propriedade_de_veiculos_automotores\g<2>',
    r'(\W+)iuj(\W+)' : r'\g<1>incidente_de_uniformizacao_de_jurisprudencia\g<2>',
    r'(\W+)lcp(\W+)' : r'\g<1>lei_das_contravencoes_penais\g<2>',
    r'(\W+)loman(\W+)' : r'\g<1>lei_organica_da_magistratura\g<2>',
    r'(\W+)lonmp(\W+)' : r'\g<1>lei_organica_nacional_do_ministerio_publico\g<2>',
    r'(\W+)mc(\W+)' : r'\g<1>medida_cautelar\g<2>',
    r'(\W+)mc(\W+)' : r'\g<1>ministerio_das_comunicacoes\g<2>',
    r'(\W+)mi(\W+)' : r'\g<1>mandado_de_injuncao\g<2>',
    r'(\W+)ms(\W+)' : r'\g<1>mandado_de_seguranca\g<2>',
    r'(\W+)nc(\W+)' : r'\g<1>noticia_crime\g<2>',
    r'(\W+)pa(\W+)' : r'\g<1>processo_administrativo\g<2>',
    r'(\W+)pet(\W+)' : r'\g<1>peticao\g<2>',
    r'(\W+)pext(\W+)' : r'\g<1>pedido_de_extensao\g<2>',
    r'(\W+)pn(\W+)' : r'\g<1>penal\g<2>',
    r'(\W+)prc(\W+)' : r'\g<1>precatorio\g<2>',
    r'(\W+)prcv(\W+)' : r'\g<1>processual_civil\g<2>',
    r'(\W+)prpn(\W+)' : r'\g<1>processual_penal\g<2>',
    r'(\W+)pv(\W+)' : r'\g<1>previdenciario\g<2>',
    r'(\W+)qo(\W+)' : r'\g<1>questao_de_ordem\g<2>',
    r'(\W+)rcl(\W+)' : r'\g<1>reclamacao\g<2>',
    r'(\W+)rd(\W+)' : r'\g<1>reconsideracao_de_despacho\g<2>',
    r'(\W+)re(\W+)' : r'\g<1>recurso_extraordinario\g<2>',
    r'(\W+)resp(\W+)' : r'\g<1>recurso_especial\g<2>',
    r'(\W+)rhc(\W+)' : r'\g<1>recurso_em_habeas_corpus\g<2>',
    r'(\W+)rmi(\W+)' : r'\g<1>recurso_em_mandado_de_injuncao\g<2>',
    r'(\W+)rms(\W+)' : r'\g<1>recurso_em_mandado_de_seguranca\g<2>',
    r'(\W+)ro(\W+)' : r'\g<1>recurso_ordinario\g<2>',
    r'(\W+)rp(\W+)' : r'\g<1>representacao\g<2>',
    r'(\W+)rtj(\W+)' : r'\g<1>revista_trimestral_jurisprudencia\g<2>',
    r'(\W+)ristj(\W+)' : r'\g<1>regimento_interno_superior_tribunal_justica\g<2>',
    r'(\W+)rstj(\W+)' : r'\g<1>revista_do_superior_tribunal_de_justica\g<2>',
    r'(\W+)rvcr(\W+)' : r'\g<1>revisao_criminal\g<2>',
    r'(\W+)saf(\W+)' : r'\g<1>secretaria_de_administração_federal\g<2>',
    r'(\W+)sd(\W+)' : r'\g<1>sindicancia\g<2>',
    r'(\W+)sec(\W+)' : r'\g<1>sentenca_estrangeira_contestada\g<2>',
    r'(\W+)sf(\W+)' : r'\g<1>senado_federal\g<2>',
    r'senado(?:\s+federal)?' : r'senado_federal',
    r'(\W+)sl(\W+)' : r'\g<1>suspensao_de_liminar\g<2>',
    r'(\W+)sls(\W+) ' : r'\g<1>suspensao_de_liminar_e_de_sentenca\g<2>',
    r'(\W+)ss(\W+) ' : r'\g<1>suspensao_de_seguranca\g<2>',
    r'(\W+)sta(\W+)' : r'\g<1>suspensao_de_tutela_antecipada\g<2>',
    r'(\W+)tr(\W+)' : r'\g<1>trabalho\g<2>',
    r'(\W+)trbt(\W+)' : r'\g<1>tributario\g<2>',
    r'http\S+' : r'_url_',

    # Tipos de Legislação
    r"(lei)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>",
    r"(lei)\s+(complementar)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>_\g<3>",
    r"(lei)\s+(federal|estadual)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>_\g<3>",
    r"(decreto-Lei)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>",
    r"(decreto)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>",
    r"(decreto)\s+(federal|estadual)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>_\g<3>",
    r"(resolução)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>",
    r"(portaria)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>",
    r"(s(?:ú|u)mula)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>",
    r"(s(?:ú|u)mula)\s+(vinculante)\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"\g<1>_\g<2>_\g<3>",
    r"voto\s+(?:n[\.º°]{0,2}\s+)?([\d\.\/-]+)" : r"_registro_juridico_",
    r"medida\s+provis(?:ó|o)ria\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"medida_provisoria_\g<1>",
    r"mp\s+(?:n[\.º°]{0,2}\s+)?([\d\/\.-]+)" : r"medida_provisoria_\g<1>",
    
    # Processo 
    r"\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}" : r"_registro_juridico_", # Possível formato para número de processo
    r"registro:?\s*?\d{1,4}\.\d{5,10}" : r"_registro_juridico_",  # Possível formato para código de registro
    r"R\$\s{0,1}[\d\,\.]+" : r"_valor_monetario_", # Possível formato de dinheiro (real)
    r"\d{1,2}[\.\/]\d{1,2}[\.\/]\d{2,4}" : r"_data_", # Possível formato de data
    r"(\w+)\/(\w+)" : r"\g<1>_\g<2>",
    r"([a-zA-Z]+)(\d+)" : r"\g<1> \g<2>", # captura qualquer palavra seguida de número e acrescenta um espaço
    r"[\d\,\.]+\s{0,1}\%" : r"_porcentagem_",
    r"(\d)\.(\d)" : r"\g<1>\g<2>", # Se observar um ponto no meio de dois números, unir os números

    # Customizáveis (podem ser retiradas no futuro)
     r'(19|20)(\d{2})' : r'(\g<1>\g<2>)',
    r'\d+(?=\s)' : r'_numero_',
    r'\d+$' : r'_numero_'
}

# https://github.com/explosion/spaCy/blob/master/spacy/lang/pt/stop_words.py
STOP_WORDS_SPACY = {
    'a', 'acerca', 'ademais', 'adeus', 'agora', 'ainda', 'algo', 'algumas', 'alguns', 'ali', 'além', 
    'ambas', 'ambos', 'antes', 'ao', 'aos', 'apenas', 'apoia', 'apoio', 'apontar', 'após', 'aquela', 
    'aquelas', 'aquele', 'aqueles', 'aqui', 'aquilo', 'as', 'assim', 'através', 'atrás', 'até', 'aí', 
    'baixo', 'bastante', 'bem', 'boa', 'bom', 'breve', 'cada', 'caminho', 'catorze', 'cedo', 'cento', 
    'certamente', 'certeza', 'cima', 'cinco', 'coisa', 'com', 'como', 'comprida', 'comprido', 
    'conhecida', 'conhecido', 'conselho', 'contra', 'contudo', 'corrente', 'cuja', 'cujo', 'custa', 
    'cá', 'da', 'daquela', 'daquele', 'dar', 'das', 'de', 'debaixo', 'demais', 'dentro', 'depois', 
    'des', 'desde', 'dessa', 'desse', 'desta', 'deste', 'deve', 'devem', 'deverá', 'dez', 'dezanove', 
    'dezasseis', 'dezassete', 'dezoito', 'diante', 'direita', 'disso', 'diz', 'dizem', 'dizer', 'do', 
    'dois', 'dos', 'doze', 'duas', 'dá', 'dão', 'e', 'ela', 'elas', 'ele', 'eles', 'em', 'embora', 
    'enquanto', 'entre', 'então', 'era', 'essa', 'essas', 'esse', 'esses', 'esta', 'estado', 'estar', 
    'estará', 'estas', 'estava', 'este', 'estes', 'esteve', 'estive', 'estivemos', 'estiveram', 
    'estiveste', 'estivestes', 'estou', 'está', 'estás', 'estão', 'eu', 'eventual', 'exemplo', 
    'falta', 'fará', 'favor', 'faz', 'fazeis', 'fazem', 'fazemos', 'fazer', 'fazes', 'fazia', 
    'faço', 'fez', 'fim', 'final', 'foi', 'fomos', 'for', 'fora', 'foram', 'forma', 'foste', 
    'fostes', 'fui', 'geral', 'grande', 'grandes', 'grupo', 'inclusive', 'iniciar', 'inicio', 
    'ir', 'irá', 'isso', 'isto', 'já', 'lado', 'lhe', 'ligado', 'local', 'logo', 'longe', 'lugar', 
    'lá', 'maior', 'maioria', 'maiorias', 'mais', 'mal', 'mas', 'me', 'meio', 'menor', 'menos', 
    'meses', 'mesmo', 'meu', 'meus', 'mil', 'minha', 'minhas', 'momento', 'muito', 'muitos', 
    'máximo', 'mês', 'na', 'nada', 'naquela', 'naquele', 'nas', 'nem', 'nenhuma', 'nessa', 'nesse', 
    'nesta', 'neste', 'no', 'nos', 'nossa', 'nossas', 'nosso', 'nossos', 'nova', 'novas', 'nove', 
    'novo', 'novos', 'num', 'numa', 'nunca', 'nuns', 'não', 'nível', 'nós', 'número', 'números', 
    'o', 'obrigada', 'obrigado', 'oitava', 'oitavo', 'oito', 'onde', 'ontem', 'onze', 'ora', 'os', 
    'ou', 'outra', 'outras', 'outros', 'para', 'parece', 'parte', 'partir', 'pegar', 'pela', 'pelas', 
    'pelo', 'pelos', 'perto', 'pode', 'podem', 'poder', 'poderá', 'podia', 'pois', 'ponto', 'pontos', 
    'por', 'porquanto', 'porque', 'porquê', 'portanto', 'porém', 'posição', 'possivelmente', 'posso', 
    'possível', 'pouca', 'pouco', 'povo', 'primeira', 'primeiro', 'próprio', 'próxima', 'próximo', 
    'puderam', 'pôde', 'põe', 'põem', 'quais', 'qual', 'qualquer', 'quando', 'quanto', 'quarta', 
    'quarto', 'quatro', 'que', 'quem', 'quer', 'querem', 'quero', 'questão', 'quieta', 'quieto', 
    'quinta', 'quinto', 'quinze', 'quê', 'relação', 'sabe', 'saber', 'se', 'segunda', 'segundo', 'sei', 
    'seis', 'sem', 'sempre', 'ser', 'seria', 'sete', 'seu', 'seus', 'sexta', 'sexto', 'sim', 'sistema', 
    'sob', 'sobre', 'sois', 'somente', 'somos', 'sou', 'sua', 'suas', 'são', 'sétima', 'sétimo', 'só', 
    'tais', 'tal', 'talvez', 'também', 'tanta', 'tanto', 'tarde', 'te', 'tem', 'temos', 'tempo', 
    'tendes', 'tenho', 'tens', 'tentar', 'tentaram', 'tente', 'tentei', 'ter', 'terceira', 'terceiro', 
    'teu', 'teus', 'teve', 'tipo', 'tive', 'tivemos', 'tiveram', 'tiveste', 'tivestes', 'toda', 'todas', 
    'todo', 'todos', 'treze', 'três', 'tu', 'tua', 'tuas', 'tudo', 'tão', 'têm', 'um', 'uma', 'umas', 
    'uns', 'usa', 'usar', 'vai', 'vais', 'valor', 'veja', 'vem', 'vens', 'ver', 'vez', 'vezes', 'vinda', 
    'vindo', 'vinte', 'você', 'vocês', 'vos', 'vossa', 'vossas', 'vosso', 'vossos', 'vários', 'vão', 
    'vêm', 'vós', 'zero', 'à', 'às', 'área', 'é', 'és', 'último'
}

JUR_STOPWORDS = {
    'acordo', 'acórdão', 'ano', 'ação', 'caso', 'civil', 'coletiva', 'competência', 'contrato', 
    'direito', 'especial', 'federal', 'feito', 'grifamos', 'interesse', 'judiciário', 'julgamento', 
    'justiça', 'medida', 'ministro', 'paulo', 'prescrição', 'proferida', 'pública', 'recurso', 
    'relator', 'sentença', 'superior', 'suspensão', 'taxa', 'tribunal'
}

CUSTO_STOPWORDS = STOP_WORDS_SPACY.union(JUR_STOPWORDS)

# Movimento temas
MOVS_TEMAS = {
  "85721" : "S1039",
  "85738" : "S1101",
  "85714" : "S1033",
  "85696" : "S1015",
  "85568" : "S0929",
  "80355" : "0381",
  "85556" : "S0744",
  "80551" : "0837",
  "85609" : "S0948",
  "85629" : "S0958",
  "80718" : "1011",
  "85697" : "S1016",
  "85755" : "S1069",
  "80822" : "1127",
  "85820" : "S1137"
}

STR_MOVS_CODE = "85721;85738;85714;85696;85568;80355;85556;80551;85609;85629;80718;85697;85755;80822;85820"
MOVS_CODE = STR_MOVS_CODE.split(';')

TEMAS_MOVS = {v: k for k, v in MOVS_TEMAS.items()}


def define_label_column(df : pd.DataFrame, 
                        column_codes='codigos_movimentos_temas', 
                        column_label='temas',
                        sep=';'):

    codes_as_list = df[column_codes].str.split(sep)
    condition = lambda code : code in MOVS_TEMAS
    selected_codes = codes_as_list.apply(lambda codes : list(filter(condition, codes)))
    df[column_label] = selected_codes.apply(lambda codes : [MOVS_TEMAS[c] for c in codes]).apply(tuple)

    return df

def save_as_parquet(df : pd.DataFrame, filepath : Path):
    ''' Auxiliary function to save dataframe with parquet extension.

    `.to_parquet` method requeries columns names as strings.
    However, after the vectorization, it's build a dataframe where
    the columns names are integers, ranging from 0 to `max_features - 1`.
    Then, to fix that, we map the columns names with `.rename`.
    The dict comprehension builds a map between the olds names and the new ones.
    '''
    df.rename(columns={ k : str(k) for k in df.columns}, inplace=True)
    df.to_parquet(filepath, compression='gzip', index=False)