import json
import yaml
from yaml.loader import SafeLoader


def json_open(path: str) -> dict:
    '''
    Method opens json file
    :param path: path to file
    :return: dict
    '''
    with open(path, 'r') as f:
        return json.load(f)


def sql_open(path: str) -> "sql":
    '''
    Method returns SQL query
    :param path: path to file
    :return: sql
    '''
    with open(path, 'r') as f:
        return f.read()


def yaml_open(path: str) -> dict:
    '''
    Method returns yaml loaded into dict
    :param path: path to file
    :return: dict
    '''
    with open(path, 'r') as f:
        return yaml.load(f, Loader=SafeLoader)


def txt_open(path: str) -> list:
    '''
    Method returns list of strings based on txt
    :param path: path to txt file
    :return: list
    '''
    with open(path, 'r') as f:
        return [line.rstrip() for line in f]