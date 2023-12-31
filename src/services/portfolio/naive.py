# imports
import pandas as pd

# custom imports
from .base import BasePortfolio
from src.db import trades_db



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
        trade = pd.DataFrame({
            'strat_id': [event.strategy_id],
            'trade_id': [event.trade_id],
            'datetime': [self.bars.get_latest_date()],
            'type': [event.desc],
            'symbol': [event.symbol],
            'direction': [event.direction],
            'quantity': [event.quantity],
            'price': [event.price],
            'commission': [event.commission]
        })
        self.trades = pd.concat([self.trades, trade])


    def close_positions(self):
        self.trades = self.trades[:-2]
        # base case
        if self.trades.empty:
            return self.trades

        # already closed
        last_trade = self.trades.iloc[-1]
        if last_trade['type'] == 'EXIT':
            return self.trades

        # close last trades
        exit_trades = self.trades.iloc[-2:].copy()
        exit_trades['type'] = 'EXIT'
        exit_trades['direction'] = exit_trades['direction'].apply(lambda x: 'BUY' if x == 'SELL' else 'SELL')
        exit_trades['price'] = exit_trades.apply(lambda x: self.bars.get_latest_close(x['symbol'], n=1)[-1], axis=1)
        self.trades = pd.concat([self.trades, exit_trades])

        # save trades
        trades_db.insert(self.trades)
