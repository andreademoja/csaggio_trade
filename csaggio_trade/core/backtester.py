import logging
class Backtester:
    def __init__(self, data_handler, strategy, execution_engine, portfolio, reporter):
        self.data = data_handler
        self.strategy = strategy
        self.execution = execution_engine
        self.portfolio = portfolio
        self.reporter = reporter
        self.logger = logging.getLogger(__name__)

    def run(self):
        # Supporta sia pandas (iterrows) che dummy nei test (iter_rows)
        if hasattr(self.data, "iterrows"):
            iterator = self.data.iterrows()
        elif hasattr(self.data, "iter_rows"):
            iterator = self.data.iter_rows()
        else:
            raise AttributeError("Data object must implement iterrows() or iter_rows()")



        initial_equity = self.portfolio.equity
        min_equity = initial_equity * 0.5

        stop_index = None
        stopped = False
        for idx, (t, row) in enumerate(iterator):
            if stopped:
                break
            if self.portfolio.equity <= min_equity:
                self.logger.info(f"Max loss reached: equity={self.portfolio.equity:.2f} <= {min_equity:.2f}. Stopping backtest.")
                stop_index = idx
                stopped = True
                break
            try:
                signals = self.strategy.generate_signals(t, row, self.portfolio)
            except TypeError:
                signals = self.strategy.generate_signals(t, row)

            orders = self.execution.process_signals(t, signals, self.portfolio, row=row)
            self.reporter.record(t, row, self.portfolio, orders)
            self.portfolio.update(t, row, orders, commission_model=getattr(self.execution, 'commission_model', None))

        # After stop, strictly truncate all results/events and prevent further updates
        events = self.reporter.finalize()
        if stop_index is not None:
            events = events[:stop_index+1]
            if hasattr(self.reporter, "trade_log") and hasattr(self.reporter.trade_log, "trades"):
                self.reporter.trade_log.trades = self.reporter.trade_log.trades[:stop_index+1]
            # Debug prints for diagnostics
            print("[DEBUG] Backtest stopped early at stop_index:", stop_index)
            print("[DEBUG] Length of truncated events:", len(events))
            print("[DEBUG] Last 3 events:", events[-3:] if len(events) >= 3 else events)
            print("[DEBUG] Final portfolio equity:", self.portfolio.equity)
            if len(events) > 0:
                print("[DEBUG] Last event equity:", events[-1]["equity"])

        trade_log = getattr(self.reporter, "trade_log", None)
        if trade_log is None:
            return events
        else:
            return events, trade_log
