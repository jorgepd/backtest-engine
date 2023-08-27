
create table if not exists tb_backtest_info (
    id text primary key,
    name text not null
);


create table if not exists tb_backtest_portfolio_relation (
    id integer primary key,
    backtest_id text not null,
    portfolio_id text not null
);


create table if not exists tb_portfolio_strategy_relation (
    id integer primary key,
    portfolio_id text not null,
    strategy_id text not null
);


create table if not exists tb_strategy_parameters (
    id text primary key,
    desc text not null
);


create table if not exists tb_metrics (
    id integer primary key,
    msg text not null
);


create table if not exists tb_trades (
    id text primary key,
    strategy_id text not null
);


create table if not exists tb_holdings (
    id integer primary key,
    portfolio_id text not null
);

