from utils import remove_header_footer


def remove_word_stress(text : str):
    '''
    Remove words accents.
    '''
    return text.translate(
            str.maketrans('áàãâäéèêëóòõôöíìîïúùüç', 'aaaaaeeeeoooooiiiiuuuc')
        )