import configparser
from .logger import logger

parser = configparser.ConfigParser()
try:
    parser.read(filenames='setting.ini', encoding='utf-8')
except configparser.ParsingError:
    logger.error('Config setting.ini parser error!')
else:
    dbParser = parser['DB']
    baseParser = parser['BASE']
    alertParser = parser['ALERT']
