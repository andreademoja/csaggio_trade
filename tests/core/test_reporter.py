import pandas as pd
from csaggio_trade.core.reporter import Reporter

def test_reporter_records_and_finalizes():
    reporter = Reporter()

    # Dummy portfolio
    class DummyPortfolio:
        def __init__(self, equity):
            self.equity = equity

    # Dummy row
    row = pd.Series({"close": 1.2000})

    # Registriamo due eventi
    reporter.record(t=0, row=row, portfolio=DummyPortfolio(10000), orders=[{"action": "open"}])
    reporter.record(t=1, row=row, portfolio=DummyPortfolio(10100), orders=[{"action": "close_all"}])

    result = reporter.finalize()

    # Deve essere una lista di dict
    assert isinstance(result, list)
    assert len(result) == 2

    # Controlliamo i campi
    assert result[0]["t"] == 0
    assert result[0]["equity"] == 10000
    assert result[1]["equity"] == 10100
