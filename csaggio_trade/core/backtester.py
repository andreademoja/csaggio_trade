class Backtester:
    def __init__(self, data_handler, strategy, execution_engine, portfolio, reporter):
        self.data = data_handler
        self.strategy = strategy
        self.execution = execution_engine
        self.portfolio = portfolio
        self.reporter = reporter

    def run(self):
        for t, row in self.data.iter_rows():
            signals = self.strategy.generate_signals(t, row)
            orders = self.execution.process_signals(t, signals, self.portfolio)
            self.portfolio.update(t, row, orders)
            self.reporter.record(t, row, self.portfolio, orders)

        return self.reporter.finalize()
