# imports
from abc import ABC, abstractmethod



class BaseOrderRouter(ABC):
    '''
    The OrderRouter class handles the interaction between
    orders and its execution in the market, returning the
    corresponding 'Fill' objects.
    '''

    @abstractmethod
    def execute_order(self, event):
        raise NotImplementedError('Should implement execute_order()')

