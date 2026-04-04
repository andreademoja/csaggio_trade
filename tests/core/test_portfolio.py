import pandas as pd
from csaggio_trade.core.portfolio import Portfolio

def test_portfolio_opens_and_closes_positions():
    portfolio = Portfolio(initial_equity=10000)

    # Dummy price row
    row = pd.Series({"close": 1.2000})

    # Ordine di apertura long
    order_open = {
        "action": "open",
        "side": "long",
        "size": 10000
    }

    portfolio.update(t=0, row=row, orders=[order_open])

    assert portfolio.position_size == 10000
    assert portfolio.position_side == "long"
    assert portfolio.entry_price == 1.2000

    # Prezzo cambia
    row2 = pd.Series({"close": 1.2100})

    # Ordine di chiusura
    order_close = {"action": "close_all"}

    portfolio.update(t=1, row=row2, orders=[order_close])

    # PnL: (1.2100 - 1.2000) * 10000 = 100
    assert portfolio.equity == 10100
    assert portfolio.position_size == 0
    assert portfolio.position_side is None
    assert portfolio.entry_price is None
