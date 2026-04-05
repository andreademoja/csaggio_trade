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
            try:
                signals = self.strategy.generate_signals(t, row, self.portfolio)
            except TypeError:
                # Strategia legacy (usata nei test)
                signals = self.strategy.generate_signals(t, row)

            orders = self.execution.process_signals(t, signals, self.portfolio)

            # 1) PRIMA registro cosa sta succedendo (con la posizione ancora "viva")
            self.reporter.record(t, row, self.portfolio, orders)

            # 2) POI aggiorno il portfolio (chiusure, PnL, reset, ecc.)
            self.portfolio.update(t, row, orders)

        events = self.reporter.finalize()

        # Se il reporter ha un trade_log (runtime reale), restituiscilo
        # Se non ce l’ha (DummyReporter nei test), restituisci solo events
        trade_log = getattr(self.reporter, "trade_log", None)

        if trade_log is None:
            return events
        else:
            return events, trade_log
