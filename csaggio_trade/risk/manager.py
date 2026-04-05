import pandas as pd

class RiskManager:
    def __init__(self, risk_per_trade, account_size, atr_multiplier, leverage=500):
        self.risk_per_trade = risk_per_trade
        self.account_size = account_size
        self.atr_multiplier = atr_multiplier
        self.leverage = leverage

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

        # Size basata sul rischio ATR
        raw_size = risk_amount / stop_distance

        # Size massima consentita dalla leva
        # margine richiesto = (size * price) / leverage
        # size_max = (equity * leverage) / price
        price = getattr(portfolio, "last_price", None)
        if price is None or price == 0:
            return raw_size

        max_size_by_leverage = (self.account_size * self.leverage) / price

        # La size finale è la min tra sizing ATR e sizing massimo consentito dalla leva
        final_size = min(raw_size, max_size_by_leverage)

        return final_size
