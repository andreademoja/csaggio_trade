class Backtester:
    def __init__(self, data_handler, strategy, execution_engine, portfolio, reporter):
        self.data = data_handler
        self.strategy = strategy
        self.execution = execution_engine
        self.portfolio = portfolio
        self.reporter = reporter

    def run(self):
        # Supporta sia pandas (iterrows) che dummy nei test (iter_rows)
        if hasattr(self.data, "iterrows"):
            iterator = self.data.iterrows()
        elif hasattr(self.data, "iter_rows"):
            iterator = self.data.iter_rows()
        else:
            raise AttributeError("Data object must implement iterrows() or iter_rows()")

        for t, row in iterator:
            signals = self.strategy.generate_signals(t, row)
            orders = self.execution.process_signals(t, signals, self.portfolio)
            self.portfolio.update(t, row, orders)
            self.reporter.record(t, row, self.portfolio, orders)


        return self.reporter.finalize()
