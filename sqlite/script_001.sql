
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
    mean_performance real not null,
    mean_time real not null,
    count real not null,
    count_win real not null,
    pct_win real not null,
    pct_win real not null,
    win_mean_performance real not null,
    loss_mean_performance real not null,
    sharpe real not null
);


create table if not exists tb_trades (
    id text primary key,
    date text not null,
    strategy_id text not null,
    trade_id text not null,
    type text not null,
    symbol text not null,
    direction text not null,
    quantity text not null,
    price text not null,
    commission text not null
);
