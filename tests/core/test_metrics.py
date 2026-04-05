import pandas as pd
from csaggio_trade.core.metrics import Metrics

def test_metrics_basic():
    # equity fittizia
    results = [
        {"equity": 10000},
        {"equity": 10500},
        {"equity": 10200},
        {"equity": 11000},
    ]

    m = Metrics(results)

    # PnL
    assert m.pnl() == 1000
    assert m.deposit() == 10000

    # Max Drawdown
    max_dd, dd_equity = m.max_drawdown()
    # equity: 10000 → 10500 → 10200 → 11000
    # drawdown max = (10200 / 10500 - 1) = -2.857%
    assert round(max_dd, 4) == round((10200/10500 - 1), 4)
    assert dd_equity == 10200

def test_metrics_profit_factor_and_win_rate():
    results = [
        {"equity": 10000},
        {"equity": 10200},  # +200
        {"equity": 9900},   # -300
        {"equity": 10300},  # +400
    ]

    m = Metrics(results)

    # trades: +200, -300, +400
    assert m.win_rate() == 2/3
    assert m.profit_factor() == (200 + 400) / 300

def test_metrics_expectancy():
    results = [
        {"equity": 10000},
        {"equity": 10100},  # +100
        {"equity": 10050},  # -50
        {"equity": 10200},  # +150
    ]

    m = Metrics(results)

    # expectancy = mean([100, -50, 150]) = 66.66
    assert round(m.expectancy(), 2) == 66.67

def test_profit_percent():
    results = [
        {"equity": 10000},
        {"equity": 15000},
    ]
    m = Metrics(results)
    assert m.profit_percent() == 50.0

def test_months():
    results = [
        {"t": "2020-01-01", "equity": 10000},
        {"t": "2020-03-15", "equity": 11000},
    ]
    m = Metrics(results)
    assert m.months() == 3
