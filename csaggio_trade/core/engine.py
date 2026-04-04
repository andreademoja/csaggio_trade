class Engine:
    def __init__(self, loader, strategy, execution, portfolio, reporter):
        self.loader = loader
        self.strategy = strategy
        self.execution = execution
        self.portfolio = portfolio
        self.reporter = reporter

    def run(self):
        data = self.loader.load()
        data = self.strategy.prepare_data(data)

        from .backtester import Backtester
        bt = Backtester(data, self.strategy, self.execution, self.portfolio, self.reporter)
        return bt.run()
