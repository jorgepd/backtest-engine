# imports
from abc import ABC, abstractmethod



class BaseStrategy(ABC):
    '''
    The Strategy class is supposed to provide an interface
    to generate trading signals for the system.
    '''

    @abstractmethod
    def calc_signals(self, event):
        raise NotImplementedError('Should implement calc_signals()')
