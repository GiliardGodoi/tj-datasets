import re
import pandas as pd

from .preprocessing import (
    remove_noise_from_header, 
    remove_header, 
    remove_footer
)

def limpo(df : pd.DataFrame, content='conteudo', formatted='formatado') -> pd.DataFrame :
    '''Remoção de cabeçalhos e rodapé, remoção de quebra de páginas, quebra de linha
    tabulação, e espaços duplos (substituí por um espaço simples).

    Mantém no texto: letras maiúsculas e minúsculas, números, pontuação e acentuação.
    '''
    df[formatted] = (df[content]
                    .apply(remove_noise_from_header)
                    .apply(remove_header)
                    .apply(remove_footer)
                    .apply(lambda t: re.sub(r'\x0c', '', t)) # remove caracter de quebra de linha
                    .apply(lambda t: re.sub(r'\s+', ' ', t)) # remove caracteres em branco
                    .apply(lambda t: t.strip() ) # remove espaço em branco do começo e final do texto
            )
    return df