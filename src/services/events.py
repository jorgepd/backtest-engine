# imports
from abc import ABC



class Event(ABC):
    '''
    The Event class is supposed to provide an interface
    to system events.
    '''
    pass


class MarketEvent(Event):
    def __init__(self):
        self.type = 'MARKET'


class SignalEvent(Event):
    def __init__(self):
        self.type = 'SIGNAL'


class OrderEvent(Event):
    def __init__(self, strategy_id, trade_id, desc, symbol, direction, quantity):
        self.type = 'ORDER'
        self.strategy_id = strategy_id
        self.trade_id = trade_id
        self.desc = desc
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity


class FillEvent(Event):
    def __init__(self, strategy_id, trade_id, desc, symbol, direction, quantity, price, commission=0):
        self.type = 'FILL'
        self.strategy_id = strategy_id
        self.trade_id = trade_id
        self.desc = desc
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity
        self.price = price
        self.commission = commission
