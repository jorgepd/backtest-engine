# imports
import pandas as pd
from sqlalchemy import text

# custom imports
from config import bt_engine
from .helper import try_catch



@try_catch
def select(id=None):
    query = f'''
    select *
    from tb_metrics
    where 1 = 1
    '''

    if id is not None:
        query += f' and strat_id = \'{id}\''

    df = pd.read_sql(query, con=bt_engine)
    return df


@try_catch
def insert(df):
    df.to_sql('tb_metrics', con=bt_engine, if_exists='append', index=False)


@try_catch
def delete(id):
    query = f'''
    delete from tb_metrics
    where strat_id = '{id}'
    '''
    with bt_engine.begin() as conn:
        r = conn.execute(text(query))
