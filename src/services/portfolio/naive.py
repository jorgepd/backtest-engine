# imports
import pandas as pd

# custom imports
from .base import BasePortfolio



class NaivePortfolio(BasePortfolio):
    '''
    The NaivePortfolio class is designed to simply send orders
    to the broker blindly, without much interaction
    '''

    def __init__(self, bars, event_q, w=100000.0):
        self.bars = bars
        self.event_q = event_q
        self.w = w
        self.symbol_ls = bars.symbol_ls

        self.all_positions = []
        self.current_positions = self._construct_empty_dict()

        self.all_holdings = []
        self.current_holdings = self._construct_empty_dict()
        self.current_holdings['cash'] = w
        self.current_holdings['total'] = w
        self.current_holdings['commission'] = 0.0

        self.trades = pd.DataFrame()


    def update_timeindex(self):
        # update positions
        cur_pos = self.current_positions.copy()
        cur_pos['datetime'] = self.bars.get_latest_date()
        self.all_positions.append(cur_pos)

        # update holdings
        self.current_holdings['total'] = self.current_holdings['cash']
        for s in self.symbol_ls:
            close = self.bars.get_latest_close(s, n=1)[-1]
            mkt_v = self.current_positions[s] * close
            self.current_holdings[s] = mkt_v
            self.current_holdings['total'] += mkt_v

        cur_hold = self.current_holdings.copy()
        cur_hold['datetime'] = self.bars.get_latest_date()
        self.all_holdings.append(cur_hold)


    def update_signal(self, event):
        pass


    def update_fill(self, event):
        self._update_positions_from_fill(event)
        self._update_holdings_from_fill(event)
        self._record_trade(event)


    def _construct_empty_dict(self):
        return dict ( (s, 0.0) for s in self.symbol_ls)


    def _fill_direction(self, event):
        return 1 if event.direction == 'BUY' else -1


    def _update_positions_from_fill(self, event):
        fill_dir = self._fill_direction(event)
        self.current_positions[event.symbol] += fill_dir * event.quantity


    def _update_holdings_from_fill(self, event):
        fill_dir = self._fill_direction(event)
        cost = fill_dir * event.price * event.quantity
        self.current_holdings[event.symbol] += cost
        self.current_holdings['commission'] += event.commission
        self.current_holdings['cash'] -= (cost + event.commission)
        self.all_holdings[-1]['total'] -= event.commission


    def _record_trade(self, event):
        pass
