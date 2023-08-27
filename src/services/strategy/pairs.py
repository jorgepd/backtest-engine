# imports
from numba import jit
import pandas as pd
import numpy as np
import uuid

# custom imports
from .base import BaseStrategy
from src.services.events import OrderEvent
from src.db import strategy_db



class PairsTradingStrategy(BaseStrategy):
    '''
    A pairs trading strategy that trades on mean reversion.
    '''

    def __init__(self, bt_name, bars, event_q, type, symbol_A, symbol_B, lookback, entry_mult, exit_mult, order_size):
        '''
        Parameters:
        bars - DataHandler with bars data
        event_q - event queue
        type - 'LONG' or 'SHORT'
        symbol_A - symbol A
        symbol_B - symbol B
        lookback - lookback size
        entry_mult - std multiplier for entry point
        exit_mult - std multiplier for exit point
        order_size - maximum position order size
        '''

        # TODO:
        # move generic properties to BaseStrategy

        # properties
        self.strategy_id = str(uuid.uuid4())
        self.bars = bars
        self.event_q = event_q

        # save info
        strategy_db.insert(pd.DataFrame({
            'strat_id': [self.strategy_id],
            'backtest_name': [bt_name],
            'type': [type],
            'symbol_A': [symbol_A],
            'symbol_B': [symbol_B],
            'lookback': [lookback],
            'entry_mult': [entry_mult],
            'exit_mult': [exit_mult],
            'order_size': [order_size]
        }))

        # strategy specific properties
        self.trade_id = None
        self.type = type.upper()
        self.symbol_A = symbol_A.upper()
        self.symbol_B = symbol_B.upper()
        self.lookback = lookback
        self.entry_mult = entry_mult
        self.exit_mult = exit_mult
        self.order_size = order_size

        # always use long positions
        if self.type == 'SHORT':
            self.symbol_A, self.symbol_B = self.symbol_B, self.symbol_A


    def calc_signals(self):
        '''
        Method that uses Bollinger Bands to generate entry and
        exit signals on the asset pair.
        '''

        # compute spread
        close_A = self.bars.get_latest_close(self.symbol_A, self.lookback)
        close_B = self.bars.get_latest_close(self.symbol_B, self.lookback)
        spread = close_A / close_B
        if len(spread) < self.lookback:
            return

        # send entry signals
        limit, _, _ = _calc_BB(spread, self.entry_mult, 0.01)
        if (
            (self.trade_id is None)
            and (spread[-1] < limit)
        ):
            # calc quantities
            self.quantity_A = _calc_quantity(self.order_size, close_A[-1])
            self.quantity_B = _calc_quantity(self.order_size, close_B[-1])

            # break if financials differ by more than 5%
            fin_A = self.quantity_A * close_A[-1]
            fin_B = self.quantity_B * close_B[-1]
            if (abs(fin_A - fin_B) / min(fin_A, fin_B) >= 0.05):
                return

            # send orders
            self.trade_id = str(uuid.uuid4())
            self.event_q.append(OrderEvent(self.strategy_id, self.trade_id, 'ENTRY', self.symbol_A, 'BUY', self.quantity_A))
            self.event_q.append(OrderEvent(self.strategy_id, self.trade_id, 'ENTRY', self.symbol_B, 'SELL', self.quantity_B))

        # send exit signals, no minimum deviation
        limit, _, _ = _calc_BB(spread, self.exit_mult)
        if (
            (self.trade_id is not None)
            and (spread[-1] > limit)
        ):
            self.event_q.append(OrderEvent(self.strategy_id, self.trade_id, 'EXIT', self.symbol_A, 'SELL', self.quantity_A))
            self.event_q.append(OrderEvent(self.strategy_id, self.trade_id, 'EXIT', self.symbol_B, 'BUY', self.quantity_B))
            self.trade_id = None


@jit(nopython=True)
def _calc_BB(spread, std_mult, min_deviation=0.0):
    '''
    Calculates Bollinger Bands. If std is lower than min_deviation,
    use min_deviation instead.

    Parameters:
    spread - pair spread
    std_mult - number of std's to push the bands away from the mean
    min_deviation - minimum deviation as a percentage of the mean
    '''

    # metrics
    mean = np.mean(spread)
    std_calc = np.std(spread)

    # bands
    std_min = min_deviation * mean
    std = std_mult * max(std_calc, std_min)
    upper_B = mean + std
    lower_B = mean - std

    return lower_B, mean, upper_B


@jit(nopython=True)
def _calc_quantity(order_size, price, batch_size=1):
    '''
    Calculates asset max quantity for a given order size.
    Rounds that number to its nearest batch size.
    '''
    quantity = order_size / price
    quantity = round(quantity / batch_size) * batch_size
    return quantity
