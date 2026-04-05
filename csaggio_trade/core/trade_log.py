import pandas as pd

class TradeLog:
    def __init__(self):
        self.trades = []

    def record(self, t, side, size, entry, exit, pnl):
        self.trades.append({
            "t": t,
            "side": side,
            "size": size,
            "entry": entry,
            "exit": exit,
            "pnl": pnl
        })

    def to_dataframe(self):
        return pd.DataFrame(self.trades)

    def save(self, path):
        df = self.to_dataframe()
        df.to_csv(path, index=False)
