# imports
import sqlalchemy
import logging
from logging import config as log_config
import yaml


def create_logger():
    conf_dict = yaml.load(open('logging.conf'), Loader=yaml.FullLoader)
    log_config.dictConfig(conf_dict)
    return logging.getLogger()


logger = create_logger()
bt_engine = sqlalchemy.create_engine('sqlite:///sqlite/database.db')
market_data_engine = sqlalchemy.create_engine('sqlite:///sqlite/market_data.db')
