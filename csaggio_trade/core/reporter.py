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
                pnl = 0
                if entry is not None:
                    pnl = (row["close"] - entry) * pos_size if pos_side == "long" else (entry - row["close"]) * pos_size

                self.trade_log.record(
                    t=t,
                    side=pos_side,
                    size=pos_size,
                    entry=entry,
                    exit=row["close"],
                    pnl=pnl
                )

    def finalize(self):
        return self.events

