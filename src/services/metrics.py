# imports
import pandas as pd



def calc_statistics(trades):
    # group trades
    trades['quantity'] = trades.apply(lambda x: x['quantity'] * (-1 if x['direction'] == 'BUY' else 1), axis=1)
    trades['total'] = trades['quantity'] * trades['price']
    trades = trades.groupby('trade_id').agg({
        # trade performance
        'total': 'sum',

        # trade time, in minutes
        'date': lambda x: (max(x) - min(x)).total_seconds() / 60
    })

    # statistics
    mean_performance = trades['total'].mean()
    mean_time = trades['date'].mean()
    count = len(trades)
    count_win = sum(trades['total'] > 0)
    pct_win = count_win / count
    win_mean_performance = trades.loc[trades['total'] > 0]['total'].mean()
    loss_mean_performance = trades.loc[trades['total'] < 0]['total'].mean()

    # save statistics
    pass
