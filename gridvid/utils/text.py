'''
    For quick and simple text formatting, such as bold, italic, and more.
'''

def bold(string:str) -> str:
    '''
        Converts the given string to bold.
    '''
    return f'\033[1m{string}'

def italic(string:str) -> str:
    '''
        Converts the given string to italic.
    '''
    return f'\033[3m{string}'

def norm() -> str:
    '''
        Returns the text style to normal.
    '''
    return '\033[0m'
