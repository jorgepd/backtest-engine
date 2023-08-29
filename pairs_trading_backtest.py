# imports
from collections import deque
from tqdm import tqdm
import pandas as pd
import numpy as np
import itertools
import time

# custom imports
from config import logger
from src.services import utils
from src.services.main import main_loop
from src.services.data import HistoricDataHandler
from src.services.portfolio import NaivePortfolio
from src.services.order_router import SimulatedOrderRouter
from src.services.strategy import PairsTradingStrategy
from src.services.metrics import calc_statistics


# start
start_time = time.time()
bt_name = 'nasdaq_top10'
logger.info(f'Backtest name: {bt_name}')
utils.clean_backtest_data(bt_name)

# generate all parameter combinations
symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'META', 'TSLA', 'AVGO', 'GOOGL', 'PEP', 'ADBE']
symbols = ['AAPL', 'MSFT']
pairs = itertools.combinations(symbols, 2)
pairs = list(pairs)

_ = 0.1
type = ['LONG', 'SHORT']
lookbacks = np.arange(60, 300+_, 20)
entries = np.arange(1, 3+_, 0.25)
exits = np.arange(-0.5, 0.5+_, 0.25)

lookbacks = [100, 120]
entries = [1, 2]
exits = [0, 0.5]
parm = itertools.product(type, pairs, lookbacks, entries, exits)
parm = list(parm)
logger.info(f'Number of backtest configurations: {len(parm)}')

# loading historic data
logger.info('Loading data...')
bars = HistoricDataHandler(symbols)
logger.info('Finished loading data')

# iter over combinations
logger.info(f'Estimated time is {len(parm)*2/60:.2f} minutes')
for p in tqdm(parm):
    # declare components
    event_q = deque()
    bars.new_instance(event_q)
    port = NaivePortfolio(bars, event_q)
    broker = SimulatedOrderRouter(bars, event_q)
    strat = PairsTradingStrategy(bt_name, bars, event_q, p[0], p[1][0], p[1][1], p[2], p[3], p[4], 50000)

    # execute
    main_loop(bars, event_q, port, broker, [strat])

    # metrics
    calc_statistics(strat.strat_id, port.trades, pd.DataFrame(port.all_holdings))
