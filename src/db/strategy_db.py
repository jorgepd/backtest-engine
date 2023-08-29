# imports
import pandas as pd
from sqlalchemy import text

# custom imports
from config import bt_engine
from .helper import try_catch



@try_catch
def select(bt_name=None, strat_id=None):
    query = f'''
    select *
    from tb_strategy_parameters
    where 1 = 1
    '''

    if bt_name is not None:
        query += f' and backtest_name = \'{bt_name}\''

    if strat_id is not None:
        query += f' and strat_id = \'{strat_id}\''

    df = pd.read_sql(query, con=bt_engine)
    return df


@try_catch
def insert(df):
    df.to_sql('tb_strategy_parameters', con=bt_engine, if_exists='append', index=False)


@try_catch
def delete(bt_name=None, strat_id=None):
    query = f'''
    delete from tb_strategy_parameters
    where 1 = 1
    '''

    if bt_name is not None:
        query += f' and backtest_name = \'{bt_name}\''

    if strat_id is not None:
        query += f' and strat_id = \'{strat_id}\''

    with bt_engine.begin() as conn:
        r = conn.execute(text(query))
