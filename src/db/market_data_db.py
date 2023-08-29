# imports
import pandas as pd
from sqlalchemy import text

# custom imports
from config import market_data_engine
from .helper import try_catch



@try_catch
def select(ticker_ls=[]):
    query = f'''
    select *
    from tb_ohlc
    where 1 = 1
    '''

    if ticker_ls:
        ls = '\', \''.join(ticker_ls)
        query += f' and ticker in (\'{ls}\')'

    query += ' order by date asc'
    df = pd.read_sql(query, con=market_data_engine)
    df = df.set_index('date')
    return df
