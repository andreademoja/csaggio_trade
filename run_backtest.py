from csaggio_trade.data.loader import DataLoader
from csaggio_trade.indicators.builder import IndicatorBuilder
from csaggio_trade.strategies.mean_reversion import MeanReversionStrategy
from csaggio_trade.risk.manager import RiskManager
from csaggio_trade.core.execution import ExecutionEngine
from csaggio_trade.core.slippage import FixedSlippageModel
from csaggio_trade.core.commission import PercentageCommissionModel
from csaggio_trade.core.portfolio import Portfolio
from csaggio_trade.core.reporter import Reporter
from csaggio_trade.core.backtester import Backtester

import pandas as pd
import logging
# Logging setup
from csaggio_trade.logger import setup_logging

setup_logging(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🚀 Avvio backtest csaggio_trade")

logger = logging.getLogger(__name__)



# -------------------------
# MULTI-ASSET BACKTEST
# -------------------------
import os
from glob import glob
from csaggio_trade.core.metrics import Metrics
from csaggio_trade.core.equity_curve import EquityCurve
from csaggio_trade.core.drawdown_curve import DrawdownCurve

raw_dir = "csaggio_trade/data/raw"
asset_files = sorted([f for f in glob(os.path.join(raw_dir, "*.csv"))])

summary = []
for asset_path in asset_files:
    asset_name = os.path.splitext(os.path.basename(asset_path))[0]
    print(f"\n=== Backtest {asset_name} ===")
    try:
        loader = DataLoader(path=asset_path, parser=lambda df: df)
        indicators = IndicatorBuilder(atr_period=14, rsi_period=14, zscore_period=20)
        strategy = MeanReversionStrategy(
            z_entry_long=-2.0,
            z_entry_short=2.0,
            z_exit=1.0,
            rsi_long_max=30,
            rsi_short_min=70,
            regime_filter=None
        )
        risk = RiskManager(
            risk_per_trade=0.01,
            account_size=2000,
            atr_multiplier=2,
            leverage=500
        )
        slippage = FixedSlippageModel(slippage_pips=0.5)
        commission = PercentageCommissionModel(commission_rate=0.001)
        execution = ExecutionEngine(
            risk_manager=risk,
            slippage_model=slippage,
            commission_model=commission
        )
        portfolio = Portfolio(initial_equity=2000)
        reporter = Reporter()
        df = loader.load()
        df = indicators(df)
        df = strategy.prepare_data(df)
        bt = Backtester(df, strategy, execution, portfolio, reporter)
        results, trade_log = bt.run()
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
        summary.append({
            "Asset": asset_name,
            #"Deposit": deposit,
            "PnL": pnl,
            "Profit %": profit_pct,
            #"Win Rate": win_rate,
            #"Expectancy": expectancy,
            "Months": months,
            "Max DD": max_dd,
            "Equity at Max DD": dd_equity,
            #"Profit Factor": profit_factor,
            #"Sharpe": sharpe,
            #"Sortino": sortino,
            "Final Equity": portfolio.equity,
            "Num Events": len(results)
        })
        # Save results for each asset
        pd.DataFrame(results).to_csv(f"results/backtest_results_{asset_name}.csv", index=False)
        trade_log.save(f"results/trade_log_{asset_name}.csv")
        EquityCurve(results).plot(f"results/equity_curve_{asset_name}.png")
        DrawdownCurve(results).plot(f"results/drawdown_curve_{asset_name}.png")
    except Exception as e:
        print(f"Errore nel backtest di {asset_name}: {e}")

# Print summary table
print("\n================= SUMMARY =================")
import tabulate
print(tabulate.tabulate(summary, headers="keys", floatfmt=".2f"))

