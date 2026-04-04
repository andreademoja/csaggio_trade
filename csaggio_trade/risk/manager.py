class RiskManager:
    def __init__(self, risk_per_trade, account_size, atr_multiplier):
        self.risk_per_trade = risk_per_trade
        self.account_size = account_size
        self.atr_multiplier = atr_multiplier

    def size(self, t, signal, portfolio):
        # capitale da rischiare
        risk_amount = self.risk_per_trade * self.account_size

        # distanza dello stop basata su ATR
        atr = portfolio.get_atr()
        stop_distance = atr * self.atr_multiplier

        # size = rischio / stop_distance
        size = risk_amount / stop_distance
        return size
