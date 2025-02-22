import pickle
import os

def create_cache(system_data: list, path: str, user_id: str) -> None:
    '''
    Method creates cache if it is not created
    :param system_data: system data
    :param path: path to .pkl file
    :param user_id: username
    :return: None
    '''
    if not os.path.exists(f'{path}{user_id}.pkl'):
        with open(f'{path}{user_id}.pkl', 'wb') as file:
            pickle.dump(system_data, file)
    else:
        pass

def load_cache(path: str, user_id: str) -> list:
    '''
    Method loades cache .pkl
    :param path: path to pickle
    :param user_id: username
    :return: list
    '''
    try:
        with open(f'{path}{user_id}.pkl', 'rb') as f:
            data = pickle.load(f)
    except EOFError:
        data = []
    return data

def cache_messages(data: list, path: str, user_id: str) -> None:
    '''
    Method saves cached messages
    :param data: data
    :param path: path to cache
    :param user_id: username
    :return: None
    '''
    with open(f'{path}{user_id}.pkl', 'wb') as f:
        pickle.dump(data, f)
        f.close()

def remove_cache(system_data: list, path: str, user_id: str) -> None:
    '''
    Method removes cache
    :param system_data: system data
    :param path: path to cache
    :param user_id: username
    :return: None
    '''
    if os.path.exists(f'{path}{user_id}.pkl'):
        with open(f'{path}{user_id}.pkl', 'wb') as file:
            file.truncate(0)
            pickle.dump(system_data, file)
            file.close()