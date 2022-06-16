from collections import namedtuple


def process_callback_data(data: str) -> namedtuple:
    '''
    Callback data must be in format: 
    "%action%(required) %data%(optional) %search filter%(optional) %other%(optional)"
    '''

    processed_data = namedtuple('processed_data', 'action data filter other')
    data = data.split()
    try:
        processed_data.action = data[0]
    except:
        raise AttributeError('Callback is empty!')
    try:
        processed_data.data = data[1]
    except:
        processed_data.data = None
    try:
        processed_data.filter = data[2]
    except:
        processed_data.filter = None
    try:
        processed_data.id_1 = data[3]
    except:
        processed_data.other = None
    try:
        processed_data.id_2 = data[4]
    except:
        processed_data.other = None

    return processed_data
