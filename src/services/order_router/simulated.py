# custom imports
from .base import BaseOrderRouter
from src.services.events import FillEvent



class SimulatedOrderRouter(BaseOrderRouter):
    '''
    The SimulatedOrderRouter simply converts orders into
    fill objects without executing them in the market.
    '''

    def __init__(self, bars, event_q):
        self.bars = bars
        self.event_q = event_q


    def execute_order(self, event):
        # get closing price and commissions
        price = self.bars.get_latest_close(event.symbol, n=1)[-1]
        commission = self.calc_commission(event.quantity, price)

        # send simulated fill event
        fill_evt = FillEvent(
            event.strategy_id, event.trade_id, event.desc, event.symbol, event.direction, event.quantity,
            price, commission
        )
        self.event_q.append(fill_evt)


    def calc_commission(self, quantity, price):
        '''
        Calculate trading fees using 3.33 bps.
        '''
        return quantity * price * 0.000333


    def calc_slippage(self):
        pass
