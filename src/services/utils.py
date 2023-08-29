# imports
import pandas as pd

# custom imports
from config import logger
from src.db import strategy_db, trades_db, metrics_db



def clean_backtest_data(bt_name):
    logger.info('Cleaning backtest data...')
    df = strategy_db.select(bt_name=bt_name)

    for strat in df['strat_id']:
        trades_db.delete(strat)
        metrics_db.delete(strat)
    strategy_db.delete(bt_name=bt_name)
