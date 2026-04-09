"""
Parameter Optimization Framework for csaggio_trade
Systematically tests different parameter combinations to find optimal settings.
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, as_completed

from csaggio_trade.config.presets import TradingConfig, MEAN_REVERSION_CONSERVATIVE, MEAN_REVERSION_AGGRESSIVE, MEAN_REVERSION_BALANCED
from csaggio_trade.strategies.mean_reversion import MeanReversionStrategy
from csaggio_trade.data.loader import DataLoader
from csaggio_trade.indicators.builder import IndicatorBuilder
from csaggio_trade.risk.manager import RiskManager
from csaggio_trade.core.execution import ExecutionEngine
from csaggio_trade.core.portfolio import Portfolio
from csaggio_trade.core.reporter import Reporter
from csaggio_trade.core.backtester import Backtester
from csaggio_trade.core.slippage import FixedSlippageModel
from csaggio_trade.core.commission import PercentageCommissionModel
from csaggio_trade.core.metrics import Metrics
from csaggio_trade.logger import setup_logging

logger = logging.getLogger(__name__)

@dataclass
class OptimizationResult:
    """Container for optimization results."""
    config: Dict[str, Any]
    asset: str
    pnl: float
    profit_pct: float
    win_rate: float
    expectancy: float
    max_dd: float
    profit_factor: float
    sharpe: float
    sortino: float
    total_trades: int
    score: float  # Composite score for ranking

class ParameterOptimizer:
    """
    Systematic parameter optimization for trading strategies.
    Tests different parameter combinations and ranks results.
    """

    def __init__(self, data_path: str, output_dir: str = "optimization_results"):
        """
        Initialize optimizer.

        Args:
            data_path: Path to CSV data file
            output_dir: Directory to save optimization results
        """
        self.data_path = data_path
        self.asset_name = Path(data_path).stem
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Load data once
        loader = DataLoader(path=data_path, parser=lambda df: df)
        self.df = loader.load()

        # Prepare indicators once
        indicators = IndicatorBuilder(atr_period=14, rsi_period=14, zscore_period=20)
        self.df = indicators(self.df)

        logger.info(f"Optimizer initialized for {self.asset_name} with {len(self.df)} data points")

    def optimize_strategy_presets(self, risk_preset: str = "moderate",
                                execution_preset: str = "realistic") -> List[OptimizationResult]:
        """
        Test all strategy presets for a given risk/execution configuration.

        Args:
            risk_preset: Risk management preset
            execution_preset: Execution cost preset

        Returns:
            List of optimization results sorted by score
        """
        logger.info(f"Testing strategy presets for {self.asset_name} (risk: {risk_preset}, exec: {execution_preset})")

        strategy_configs = [
            ("conservative", "conservative"),
            ("balanced", "balanced"),
            ("aggressive", "aggressive"),
        ]

        results = []

        for preset_name, strategy_preset in strategy_configs:
            try:
                config = TradingConfig(
                    strategy_preset=strategy_preset,
                    risk_preset=risk_preset,
                    execution_preset=execution_preset,
                    asset_class=None  # Don't override with asset class for preset comparison
                )

                result = self._run_single_backtest(config)
                result.config["strategy_preset"] = preset_name  # Store preset name for reference
                results.append(result)

                logger.info(f"  {preset_name}: PnL={result.pnl:.2f}, WinRate={result.win_rate:.1%}, Sharpe={result.sharpe:.2f}, Score={result.score:.2f}")

            except Exception as e:
                logger.error(f"Failed to test {preset_name}: {str(e)}")
                continue

        # Sort by composite score
        results.sort(key=lambda x: x.score, reverse=True)

        # Save results
        self._save_results(results, f"strategy_presets_{risk_preset}_{execution_preset}.csv")

        return results

    def optimize_risk_presets(self, strategy_preset: str = "balanced",
                            execution_preset: str = "realistic") -> List[OptimizationResult]:
        """
        Test all risk presets for a given strategy/execution configuration.
        """
        logger.info(f"Testing risk presets for {self.asset_name} (strategy: {strategy_preset}, exec: {execution_preset})")

        risk_configs = ["conservative", "moderate", "aggressive"]
        results = []

        for risk_preset in risk_configs:
            try:
                config = TradingConfig(
                    strategy_preset=strategy_preset,
                    risk_preset=risk_preset,
                    execution_preset=execution_preset,
                    asset_class=self._detect_asset_class()
                )

                result = self._run_single_backtest(config)
                results.append(result)

                logger.info(f"  {risk_preset}: PnL={result.pnl:.2f}, MaxDD={result.max_dd:.1%}, Sharpe={result.sharpe:.2f}")

            except Exception as e:
                logger.error(f"Failed to test {risk_preset}: {str(e)}")
                continue

        results.sort(key=lambda x: x.score, reverse=True)
        self._save_results(results, f"risk_presets_{strategy_preset}_{execution_preset}.csv")

        return results

    def optimize_z_score_parameters(self, base_config: TradingConfig,
                                 z_entry_range: List[float] = None,
                                 z_exit_range: List[float] = None) -> List[OptimizationResult]:
        """
        Optimize Z-score entry and exit parameters.

        Args:
            base_config: Base configuration to modify
            z_entry_range: List of Z-score entry values to test (negative for long, positive for short)
            z_exit_range: List of Z-score exit values to test
        """
        if z_entry_range is None:
            z_entry_range = [-3.0, -2.5, -2.0, -1.5]
        if z_exit_range is None:
            z_exit_range = [0.2, 0.4, 0.6, 0.8]

        logger.info(f"Optimizing Z-score parameters for {self.asset_name}")
        logger.info(f"Testing {len(z_entry_range)} entry values × {len(z_exit_range)} exit values = {len(z_entry_range) * len(z_exit_range)} combinations")

        results = []

        for z_entry in z_entry_range:
            for z_exit in z_exit_range:
                try:
                    # Create modified config
                    config_dict = base_config.get_all_params()
                    config_dict["z_entry_long"] = z_entry
                    config_dict["z_entry_short"] = -z_entry  # Symmetric
                    config_dict["z_exit"] = z_exit

                    # Create result object manually since we modified the dict
                    result = self._run_backtest_with_params(config_dict)
                    results.append(result)

                except Exception as e:
                    logger.error(f"Failed Z-score combo (entry={z_entry}, exit={z_exit}): {str(e)}")
                    continue

        results.sort(key=lambda x: x.score, reverse=True)
        self._save_results(results, "z_score_optimization.csv")

        # Log top 5 results
        logger.info("Top 5 Z-score combinations:")
        for i, result in enumerate(results[:5]):
            logger.info(f"  {i+1}. Entry={result.config['z_entry_long']:.1f}, Exit={result.config['z_exit']:.1f}, Score={result.score:.2f}")

        return results

    def _run_single_backtest(self, config: TradingConfig) -> OptimizationResult:
        """Run a single backtest with given configuration."""
        params = config.get_all_params()
        return self._run_backtest_with_params(params)

    def _run_backtest_with_params(self, params: Dict[str, Any]) -> OptimizationResult:
        """Run backtest with raw parameter dictionary."""
        # Create strategy
        strategy_params = {k: v for k, v in params.items()
                          if k in ["z_entry_long", "z_entry_short", "z_exit", "rsi_long_max",
                                 "rsi_short_min", "ema_period", "atr_filter", "tp_atr", "sl_atr"]}
        strategy = MeanReversionStrategy(**strategy_params)
        df = strategy.prepare_data(self.df.copy())

        # Create risk manager
        risk = RiskManager(
            risk_per_trade=params["risk_per_trade"],
            account_size=2000,
            atr_multiplier=2,
            leverage=params["leverage"],
            max_drawdown_stop=params["max_drawdown_stop"]
        )

        # Create execution
        execution = ExecutionEngine(
            risk_manager=risk,
            slippage_model=FixedSlippageModel(slippage_pips=params["slippage_fixed"] * 10000),
            commission_model=PercentageCommissionModel(commission_rate=params["commission_per_lot"] / 100)
        )

        # Run backtest
        portfolio = Portfolio(initial_equity=2000, execution=execution)
        reporter = Reporter()
        bt = Backtester(df, strategy, execution, portfolio, reporter)

        results, trade_log = bt.run()
        m = Metrics(results)

        # Calculate composite score (higher = better)
        # Weight: Sharpe (40%), Profit Factor (30%), Win Rate (20%), Max DD penalty (10%)
        score = (
            m.sharpe() * 0.4 +
            min(m.profit_factor(), 3.0) * 0.3 +  # Cap profit factor at 3
            m.win_rate() * 0.2 -
            abs(m.max_drawdown()[0]) * 0.1  # Penalty for drawdown
        )

        return OptimizationResult(
            config=params,
            asset=self.asset_name,
            pnl=m.pnl(),
            profit_pct=m.profit_percent(),
            win_rate=m.win_rate(),
            expectancy=m.expectancy(),
            max_dd=m.max_drawdown()[0],
            profit_factor=m.profit_factor(),
            sharpe=m.sharpe(),
            sortino=m.sortino(),
            total_trades=len(results),
            score=score
        )

    def _detect_asset_class(self) -> Optional[str]:
        """Detect asset class based on filename."""
        asset_lower = self.asset_name.lower()
        if any(x in asset_lower for x in ['xau', 'xag']):
            return "metals"
        elif any(x in asset_lower for x in ['jpy', 'eur', 'gbp', 'aud', 'nzd', 'cad', 'chf']):
            return "forex"
        else:
            return None  # Use default

    def _save_results(self, results: List[OptimizationResult], filename: str):
        """Save optimization results to CSV."""
        data = []
        for result in results:
            row = {
                "asset": result.asset,
                "score": result.score,
                "pnl": result.pnl,
                "profit_pct": result.profit_pct,
                "win_rate": result.win_rate,
                "expectancy": result.expectancy,
                "max_dd": result.max_dd,
                "profit_factor": result.profit_factor,
                "sharpe": result.sharpe,
                "sortino": result.sortino,
                "total_trades": result.total_trades,
            }
            # Add config parameters
            row.update(result.config)
            data.append(row)

        df = pd.DataFrame(data)
        output_path = self.output_dir / filename
        df.to_csv(output_path, index=False)
        logger.info(f"Saved {len(results)} results to {output_path}")

def run_optimization_campaign(data_folder: str, output_dir: str = "optimization_results"):
    """
    Run comprehensive optimization campaign across all assets.

    Args:
        data_folder: Path to folder containing CSV data files
        output_dir: Directory to save results
    """
    setup_logging()
    logger.info("🚀 Starting optimization campaign")

    data_path = Path(data_folder)
    csv_files = list(data_path.glob("*.csv"))

    if not csv_files:
        logger.error("❌ No CSV files found")
        return

    logger.info(f"📁 Found {len(csv_files)} assets to optimize")

    all_results = []

    for csv_file in csv_files[:3]:  # Limit to first 3 for testing
        logger.info(f"\n🔄 Optimizing {csv_file.stem}")

        try:
            optimizer = ParameterOptimizer(str(csv_file), output_dir)

            # Test strategy presets
            strategy_results = optimizer.optimize_strategy_presets()
            all_results.extend(strategy_results)

            # Test risk presets with best strategy
            if strategy_results:
                best_strategy = strategy_results[0].config.get("strategy_preset", "balanced")
                risk_results = optimizer.optimize_risk_presets(best_strategy)
                all_results.extend(risk_results)

        except Exception as e:
            logger.error(f"❌ Failed to optimize {csv_file.stem}: {str(e)}")
            continue

    # Save summary
    if all_results:
        summary_data = [{
            "asset": r.asset,
            "config_type": "strategy" if "strategy_preset" in r.config else "risk",
            "preset": r.config.get("strategy_preset") or r.config.get("risk_preset"),
            "score": r.score,
            "pnl": r.pnl,
            "sharpe": r.sharpe,
            "win_rate": r.win_rate,
            "max_dd": r.max_dd
        } for r in all_results]

        summary_df = pd.DataFrame(summary_data)
        summary_path = Path(output_dir) / "optimization_summary.csv"
        summary_df.to_csv(summary_path, index=False)

        logger.info(f"✅ Optimization campaign complete. Summary saved to {summary_path}")

        # Log top performers
        top_performers = sorted(all_results, key=lambda x: x.score, reverse=True)[:10]
        logger.info("🏆 Top 10 performing configurations:")
        for i, result in enumerate(top_performers, 1):
            logger.info(f"  {i}. {result.asset} - Score: {result.score:.2f}, PnL: {result.pnl:.2f}")

if __name__ == "__main__":
    # Example usage
    run_optimization_campaign("csaggio_trade/data/raw")