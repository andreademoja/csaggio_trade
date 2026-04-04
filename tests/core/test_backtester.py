import pandas as pd
from csaggio_trade.core.backtester import Backtester

class DummyData:
    def __init__(self):
        self.df = pd.DataFrame({"price": [1, 2, 3]}, index=[1, 2, 3])

    def iter_rows(self):
        for t, row in self.df.iterrows():
            yield t, row

class DummyStrategy:
    def generate_signals(self, t, row):
        return [{"action": "test"}]

class DummyExecution:
    def process_signals(self, t, signals, portfolio):
        return signals

class DummyPortfolio:
    def update(self, t, row, orders):
        pass

class DummyReporter:
    def __init__(self):
        self.events = []

    def record(self, t, row, portfolio, orders):
        self.events.append((t, orders))

    def finalize(self):
        return self.events

def test_backtester_runs():
    bt = Backtester(
        data_handler=DummyData(),
        strategy=DummyStrategy(),
        execution_engine=DummyExecution(),
        portfolio=DummyPortfolio(),
        reporter=DummyReporter()
    )

    result = bt.run()

    assert len(result) == 3
    assert result[0][1][0]["action"] == "test"
