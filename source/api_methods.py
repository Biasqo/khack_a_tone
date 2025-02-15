import requests
import uuid


def get_model_data(url: str, payload: dict | str, headers: dict, method: str) -> tuple:
    '''
    Method gets response data
    :param url: url
    :param payload: payload
    :param headers: headers dict
    :param method:
    :return:
    '''
    response = requests.request(method, url, headers=headers, data=payload, verify=False)
    return response, response.status_code


def get_uuid() -> str:
    '''
    Method generates uuid
    :return: uuid str
    '''
    return str(uuid.uuid4())
