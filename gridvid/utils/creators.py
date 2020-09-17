from datetime import datetime

def create_unique_name(prefix:str = None, suffix:str = None) -> str:
    '''
        Generate a filename using the current date and time
    '''
    if prefix is None:
        prefix = ''
    elif prefix[-1] != '_':
        prefix += '_'

    if suffix is None:
        suffix = ''
    elif suffix[0] != '_':
        suffix = '_' + suffix

    datetime_str = f'{datetime.now():%m_%d_%Y_%H_%M_%S_%f}'
    filename = f'{prefix}{datetime_str}{suffix}'
    return filename
