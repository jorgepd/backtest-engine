
create table if not exists tb_strategy_parameters (
    strat_id text primary key,
    backtest_name text not null,
    type text not null,
    symbol_A text not null,
    symbol_B text not null,
    lookback real not null,
    entry_mult real not null,
    exit_mult real not null,
    order_size real not null
);


create table if not exists tb_metrics (
    strat_id text primary key,
    mean_performance real null,
    mean_time real null,
    count real null,
    count_win real null,
    pct_win real null,
    win_mean_performance real null,
    loss_mean_performance real null,
    sharpe real null
);


create table if not exists tb_trades (
    id integer primary key,
    strat_id text not null,
    trade_id text not null,
    datetime text not null,
    type text not null,
    symbol text not null,
    direction text not null,
    quantity real not null,
    price real not null,
    commission real
);
