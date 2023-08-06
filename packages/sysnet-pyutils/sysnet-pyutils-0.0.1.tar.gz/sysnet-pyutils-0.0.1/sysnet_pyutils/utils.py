import logging
import os
import secrets
import traceback
import uuid
from pathlib import Path
from urllib.parse import quote

import dateutil.parser
import pytz
import yaml


def get_project_root() -> Path:
    r = Path(__file__).parent.parent
    return os.path.abspath(r)


TZ = os.getenv('TZ', 'Europe/Prague')
ROOT_DIR = get_project_root()  # This is your Project Root
CONFIG_DIR = os.getenv('CONFIG_DIRECTORY', os.path.join(ROOT_DIR, 'conf'))
CONFIG_FILE_NAME = os.getenv('CONFIG_FILE_NAME', 'config.yml')
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE_NAME)


def init_config(config_dictionary=None):
    """
    Inicializace configurace. Pokud je konfigurace uložena v souboru, natáhne se z něj. Jinak se vytvoří a uloží.

    :param config_dictionary: Slovník iniciální konfigurace
    :return: Uložená konfigurace
    """
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as yamlfile:
            out = yaml.load(yamlfile, Loader=yaml.FullLoader)
            logging.info('Configuration loaded')
        return out
    if config_dictionary is None:
        logging.error('Config is empty')
        config_dictionary = {}
    store_config(config_dictionary)
    return config_dictionary


def store_config(config):
    """
    Uložit konfiguraci

    :param config:  Uloží slovník s konfigurací do souboru
    :return:
    """
    with open(CONFIG_FILE_PATH, 'w') as yamlfile:
        yaml.dump(config, yamlfile)
    logging.info('Configuration stored')
    return True


def delete_config():
    """
    Odstraní soubor s konfigurací

    :return:
    """
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)
        return True
    else:
        logging.error('Configuration file does not exist')
        return False


def url_safe(url):
    """
    Upraví URL, aby beobsahovalo nepovolené znaky

    :param url: Vstupní URL
    :return: Upravené URL
    """
    return quote(url, safe='/:?=&')


def who_am_i():
    """
    Vrátí název funkce

    :return:
    """
    stack = traceback.extract_stack()
    file_name, code_line, func_name, text = stack[-2]
    return func_name


def unique_list(list1):
    """
    Vyřadí opakující se položky ze seznamu

    :param list1:
    :return:
    """
    if not isinstance(list1, list):
        return list1
    out = []
    for x in list1:
        if x not in out:
            out.append(x)
    return out


def init_api_keys(agenda='main', amount=4):
    """
    Vygeneruje klíče pro API

    :param agenda: Název agendy, pro kterou se klíče generují
    :param amount: Počet vygenerovaných klíčů
    :return: seznam vygenerovaných klíčů
    """
    out = []
    for i in range(amount):
        out.append(next_api_key('{} {}'.format(agenda, i + 1)))
    return out


def next_uuid(uuid_type=1):
    """
    Vygeneruje UUID

    :param uuid_type: Lze použít pouze typ 1 nebo 4
    :return: uuid
    """
    if uuid_type == 1:
        out = uuid.uuid1()
    else:
        out = uuid.uuid4()
    return out


def next_api_key(name, length=16):
    """
    Vygeneruje slovník API key {<API Key>: <name>}

    :param name:    Název API klíče
    :param length:  Dělka API klíče
    :return:    Slovník {<API Key>: <name>}
    """
    out = {generate_api_key(length=length): name}
    return out


def generate_api_key(length: int):
    """
    vygeneruje API klíč

    :param length: Dělka API klíče
    :return: API Key
    """
    return secrets.token_urlsafe(length)


def iso_to_local_datetime(isodate):
    """
    ISO string datum do lokálního datetime

    :param isodate: Textové datum v ISO
    :return: lokální datetime
    """
    if isodate is None:
        return None
    local_tz = pytz.timezone(TZ)
    ts = dateutil.parser.parse(isodate)
    out = ts.astimezone(local_tz)
    return out


def convert_hex_to_int(id_hex):
    """
    KOnvertuje hex string na int

    :param id_hex:  Hexadecimální string
    :return: int
    """
    id_int = int(id_hex, base=16)
    return id_int


CONFIG = init_config()
