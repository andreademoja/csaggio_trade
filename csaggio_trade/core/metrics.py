import pandas as pd
import numpy as np

class Metrics:
    def __init__(self, results):
        self.df = pd.DataFrame(results)
        self.equity = self.df["equity"]

    def pnl(self):
        return self.equity.iloc[-1] - self.equity.iloc[0]

    def deposit(self):
        return self.equity.iloc[0]

    def max_drawdown(self):
        roll_max = self.equity.cummax()
        drawdown = self.equity / roll_max - 1
        max_dd = drawdown.min()
        dd_equity = self.equity.iloc[drawdown.idxmin()]
        return max_dd, dd_equity

    def profit_factor(self):
        # calcolo dei trade
        trades = self._extract_trades()
        gains = trades[trades > 0].sum()
        losses = -trades[trades < 0].sum()
        if losses == 0:
            return np.inf
        return gains / losses

    def win_rate(self):
        trades = self._extract_trades()
        wins = (trades > 0).sum()
        total = len(trades)
        return wins / total if total > 0 else 0

    def sharpe(self, risk_free=0):
        returns = self.equity.pct_change().dropna()
        if returns.std() == 0:
            return 0
        return (returns.mean() - risk_free) / returns.std() * np.sqrt(252)

    def sortino(self, risk_free=0):
        returns = self.equity.pct_change().dropna()
        downside = returns[returns < 0]
        if downside.std() == 0:
            return 0
        return (returns.mean() - risk_free) / downside.std() * np.sqrt(252)

    def expectancy(self):
        trades = self._extract_trades()
        if len(trades) == 0:
            return 0
        return trades.mean()

    def _extract_trades(self):
        """ Estrae i PnL dei trade dal file results """
        trades = []
        prev_equity = self.equity.iloc[0]

        for eq in self.equity:
            if eq != prev_equity:
                trades.append(eq - prev_equity)
                prev_equity = eq

        return pd.Series(trades)
    
    def profit_percent(self):
        return (self.pnl() / self.deposit()) * 100

    def months(self):
        df = self.df.copy()
        df["t"] = pd.to_datetime(df["t"])
        start = df["t"].min()
        end = df["t"].max()
        return (end.year - start.year) * 12 + (end.month - start.month) + 1