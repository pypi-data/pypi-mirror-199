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


def config_init(config=None):
    """
    Inicializace configurace. Pokud je konfigurace uložena v souboru, natáhne se z něj. Jinak se vytvoří a uloží.

    :param config: Slovník iniciální konfigurace
    :return: Uložená konfigurace
    """
    out = {}
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as yamlfile:
            out = yaml.load(yamlfile, Loader=yaml.FullLoader)
            logging.info('Configuration loaded')
        if bool(out):
            return out
    if config is None:
        logging.warning('Configuration is empty')
        config = {}
    config_store(config)
    return config


def config_store(config):
    """
    Uložit konfiguraci

    :param config:  Uloží slovník s konfigurací do souboru
    :return:
    """
    with open(CONFIG_FILE_PATH, 'w') as yamlfile:
        yaml.dump(config, yamlfile)
    logging.info('Configuration stored')
    return True


def config_delete():
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


def config_replace(config):
    """
    Nahradí konfigurační soubor novým obsahem

    :param config:
    :return:
    """
    config_delete()
    return config_init(config=config)


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


def api_keys_init(agenda='main', amount=4):
    """
    Vygeneruje klíče pro API

    :param agenda: Název agendy, pro kterou se klíče generují
    :param amount: Počet vygenerovaných klíčů
    :return: seznam vygenerovaných klíčů
    """
    out = []
    for i in range(amount):
        out.append(api_key_next('{} {}'.format(agenda, i + 1)))
    return out


def uuid_next(uuid_type=1):
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


def api_key_next(name, length=16):
    """
    Vygeneruje slovník API key {<API Key>: <name>}

    :param name:    Název API klíče
    :param length:  Dělka API klíče
    :return:    Slovník {<API Key>: <name>}
    """
    out = {api_key_generate(length=length): name}
    return out


def api_key_generate(length: int):
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


CONFIG = config_init()
