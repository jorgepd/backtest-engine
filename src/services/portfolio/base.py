# imports
from abc import ABC, abstractmethod



class BasePortfolio(ABC):
    '''
    The Portfolio class handles the positioning of the
    strategies, it also keep tabs on position holdings
    and trades executed.
    '''

    @abstractmethod
    def update_signal(self, event):
        raise NotImplementedError('Should implement update_signal()')

    @abstractmethod
    def update_fill(self, event):
        raise NotImplementedError('Should implement update_fill()')
