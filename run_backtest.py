from csaggio_trade.data.loader import DataLoader
from csaggio_trade.indicators.builder import IndicatorBuilder
from csaggio_trade.strategies.mean_reversion import MeanReversionStrategy
from csaggio_trade.risk.manager import RiskManager
from csaggio_trade.core.execution import ExecutionEngine
from csaggio_trade.core.portfolio import Portfolio
from csaggio_trade.core.reporter import Reporter
from csaggio_trade.core.backtester import Backtester

import pandas as pd

# -------------------------
# 1. Loader
# -------------------------
loader = DataLoader(
    path="csaggio_trade/data/raw/EURUSD.csv",
    parser=lambda df: df  # per ora nessun parser custom
)

# -------------------------
# 2. Indicator Builder
# -------------------------
indicators = IndicatorBuilder(
    atr_period=14,
    rsi_period=14,
    zscore_period=20
)

# -------------------------
# 3. Strategy
# -------------------------
strategy = MeanReversionStrategy(
    z_entry_long=-2.0,
    z_entry_short=2.0,
    z_exit=0.5,
    rsi_long_max=30,
    rsi_short_min=70,
    regime_filter=None
)

# -------------------------
# 4. Risk Manager
# -------------------------
risk = RiskManager(
    risk_per_trade=0.01,
    account_size=2000,
    atr_multiplier=2
)

# -------------------------
# 5. Execution Engine
# -------------------------
execution = ExecutionEngine(
    risk_manager=risk,
    slippage_model=None,
    commission_model=None
)

# -------------------------
# 6. Portfolio
# -------------------------
portfolio = Portfolio(initial_equity=2000)

# -------------------------
# 7. Reporter
# -------------------------
reporter = Reporter()

# -------------------------
# 8. Backtest
# -------------------------
df = loader.load()
df = indicators(df)
df = strategy.prepare_data(df)

bt = Backtester(
    df,
    strategy,
    execution,
    portfolio,
    reporter
)

results = bt.run()

from csaggio_trade.core.metrics import Metrics

m = Metrics(results)

pnl = m.pnl()
deposit = m.deposit()
max_dd, dd_equity = m.max_drawdown()
profit_factor = m.profit_factor()
win_rate = m.win_rate()
sharpe = m.sharpe()
sortino = m.sortino()
expectancy = m.expectancy()
profit_pct = m.profit_percent()
months = m.months()

# -------------------------
# 9. Output finale
# -------------------------
print("Backtest completato.")
print("\n--- PERFORMANCE METRICS ---")
print(f"Deposit: {deposit:.2f}")
print(f"PnL: {pnl:.2f}")
print(f"Profit %: {profit_pct:.2f}%")
print(f"Win Rate: {win_rate:.2%}")
print(f"Expectancy per trade: {expectancy:.2f}")
print(f"Mesi di backtest: {months}")
print(f"Max Drawdown: {max_dd:.2%}")
print(f"Equity at Max DD: {dd_equity:.2f}")
print(f"Profit Factor: {profit_factor:.2f}")
print(f"Sharpe Ratio: {sharpe:.2f}")
print(f"Sortino Ratio: {sortino:.2f}")
print(f"Equity finale: {portfolio.equity}")
print(f"Numero eventi registrati: {len(results)}")

# Salva i risultati:
pd.DataFrame(results).to_csv("results/backtest_results.csv", index=False)
print("Risultati salvati in backtest_results.csv")
