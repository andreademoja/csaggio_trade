import pandas as pd

class RiskManager:
    def __init__(self, risk_per_trade, account_size, atr_multiplier):
        self.risk_per_trade = risk_per_trade
        self.account_size = account_size
        self.atr_multiplier = atr_multiplier

    def size(self, t, signal, portfolio):
        # capitale da rischiare
        risk_amount = self.risk_per_trade * self.account_size

        # ATR corrente
        atr = portfolio.get_atr()

        # Se ATR non è disponibile o è zero → NON apriamo posizioni
        if atr is None or atr == 0 or pd.isna(atr):
            return 0

        stop_distance = atr * self.atr_multiplier

        # Se stop_distance è zero → NON apriamo posizioni
        if stop_distance == 0:
            return 0

        size = risk_amount / stop_distance
        return size

