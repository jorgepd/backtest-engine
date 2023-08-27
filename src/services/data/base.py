# imports
from abc import ABC, abstractmethod



class BaseDataHandler(ABC):
    '''
    The DataHandler class is supposed to provide an interface to access
    market data.
    '''

    @abstractmethod
    def get_latest_bars(self, symbol, n=1):
        raise NotImplementedError('Should implement get_latest_bars()')

    @abstractmethod
    def update_bars(self):
        raise NotImplementedError('Should implement update_bars()')

