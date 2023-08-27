# imports
import numpy as np
import pandas as pd
from functools import reduce

# custom imports
from .base import BaseDataHandler
from src.services.events import MarketEvent
from src.db import market_data


class HistoricDataHandler(BaseDataHandler):

    def __init__(self, symbol_ls):
        self.symbol_ls = symbol_ls
        self.symbol_data = {}
        self.date_ix = []
        self.latest_point = 0

        self._load_data()


    def _load_data(self):
        # get data
        for s in self.symbol_ls:
            self.symbol_data[s] = market_data.select([s])
        
        # create combined index
        comb_index = reduce(pd.Index.union, (df.index for df in self.symbol_data.values()))
        self.date_ix = np.array(comb_index)

        for s in self.symbol_ls:
            # reindex data
            self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index, method='ffill')

            # restruct data as np array
            df = self.symbol_data[s]
            self.symbol_data[s] = [
                df['open'].to_numpy(np.float64),
                df['high'].to_numpy(np.float64),
                df['low'].to_numpy(np.float64),
                df['close'].to_numpy(np.float64),
                df['volume'].to_numpy(np.float64),
            ]


    def new_instance(self, event_queue):
        self.event_queue = event_queue
        self.latest_point = 0


    def update_bars(self):
        # add new data point
        self.latest_point += 1
        if self.latest_point >= len(self.date_ix):
            raise StopIteration

        # send market event
        self.event_queue.append(MarketEvent())


    def get_latest_date(self):
        return self.date_ix[self.latest_point]


    def get_latest_bars(self, symbol, n=1):
        pass


    def get_latest_close(self, symbol, n=1):
        bars = self.symbol_data[symbol]
        close = bars[3][:self.latest_point]
        return close[-int(n):]
