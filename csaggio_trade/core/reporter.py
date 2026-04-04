class Reporter:
    def __init__(self):
        self.events = []

    def record(self, t, row, portfolio, orders):
        self.events.append({
            "t": t,
            "price": row["close"],
            "equity": portfolio.equity,
            "orders": orders
        })

    def finalize(self):
        return self.events
