# custom imports
from config import logger



def try_catch(fn):
    '''
    Decorator to be used as a try catch block, only to
    standardize error logging.
    '''
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.error(e)

    return wrapper

