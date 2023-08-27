# imports
import pandas as pd
from sqlalchemy import text

# custom imports
from config import engine
from helper import try_catch




@try_catch
def select(ticker=None):
    query = f'''
    select *
    from tb_ohlc
    where 1 = 1
    '''

    if ticker is not None:
        query += f' and ticker = \'{ticker}\''

    df = pd.read_sql(query, con=engine)
    return df


@try_catch
def insert(df):
    df.to_sql('tb_ohlc', con=engine, if_exists='append', index=False)


@try_catch
def delete(ticker):
    query = f'''
    delete from tb_ohlc
    where ticker = '{ticker}'
    '''
    with engine.begin() as conn:
        r = conn.execute(text(query))
