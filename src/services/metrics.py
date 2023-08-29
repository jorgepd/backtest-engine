# imports
import pandas as pd

# custom imports
from src.db import metrics_db, trades_db



def calc_statistics(strat_id, trades=None, holdings=None):
    # get trades
    if trades is None:
        trades = trades_db.select(strat_id)

    if trades.empty:
        return

    # group trades
    trades['datetime'] = pd.to_datetime(trades['datetime'])
    trades['quantity'] = trades.apply(lambda x: x['quantity'] * (-1 if x['direction'] == 'BUY' else 1), axis=1)
    trades['total'] = trades['quantity'] * trades['price']
    trades = trades.groupby('trade_id').agg({
        # trade performance
        'total': 'sum',

        # trade time, in minutes
        'datetime': lambda x: (max(x) - min(x)).total_seconds() / 60
    })

    # statistics
    mean_performance = trades['total'].mean()
    mean_time = trades['datetime'].mean()
    count = len(trades)
    count_win = sum(trades['total'] > 0)
    pct_win = count_win / count
    win_mean_performance = trades.loc[trades['total'] > 0]['total'].mean()
    loss_mean_performance = trades.loc[trades['total'] < 0]['total'].mean()
    sharpe = 0

    # TODO:
    # recreate holdings when not present
    if holdings is not None:
        # sharpe ratio
        ev = holdings['total'].iloc[-1] - holdings['total'].iloc[0]
        std = holdings['total'].std()
        sharpe = ev / std


    # save statistics
    metrics_db.insert(pd.DataFrame({
        'strat_id': [strat_id],
        'mean_performance': [mean_performance],
        'mean_time': [mean_time],
        'count': [count],
        'count_win': [count_win],
        'pct_win': [pct_win],
        'win_mean_performance': [win_mean_performance],
        'loss_mean_performance': [loss_mean_performance],
        'sharpe': [sharpe]
    }))


def calc_sharpe():
    pass

def calc_drawdown():
    pass
