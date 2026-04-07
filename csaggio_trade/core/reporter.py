from csaggio_trade.core.trade_log import TradeLog

class Reporter:
    def __init__(self):
        self.events = []
        self.trade_log = TradeLog()

    def record(self, t, row, portfolio, orders):
        self.events.append({
            "t": t,
            "price": row["close"],
            "equity": portfolio.equity
        })

        price = row["close"]

        for order in orders:
            pos_size = getattr(portfolio, "position_size", 0)
            pos_side = getattr(portfolio, "position_side", None)
            entry = getattr(portfolio, "entry_price", None)

            if order["action"] == "close_all" and pos_size > 0:
                # Usa il prezzo di chiusura del tick come prezzo exit
                # Se non è la prima chiusura, usa row["close"]
                exit_price = row["open"]  # Prezzo apertura tick successivo (exit price)
                pnl = 0
                if entry is not None:
                    if pos_side == "long":
                        pnl = (exit_price - entry) * pos_size
                    else:  # short
                        pnl = (entry - exit_price) * pos_size

                self.trade_log.record(
                    t=t,
                    side=pos_side,
                    size=pos_size,
                    entry=entry,
                    exit=exit_price,
                    pnl=pnl
                )

    def finalize(self):
        return self.events

