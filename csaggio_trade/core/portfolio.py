class Portfolio:
    def __init__(self, initial_equity):
        self.equity = initial_equity
        self.position_size = 0
        self.position_side = None
        self.entry_price = None

    def update(self, t, row, orders):
        price = row["close"]

        for order in orders:
            action = order["action"]

            # Apertura posizione
            if action == "open":
                self.position_side = order["side"]
                self.position_size = order["size"]
                self.entry_price = price

            # Chiusura totale
            elif action == "close_all":
                if self.position_size != 0:
                    pnl = self._calculate_pnl(price)
                    self.equity += pnl

                # Reset posizione
                self.position_size = 0
                self.position_side = None
                self.entry_price = None

    def _calculate_pnl(self, price):
        if self.position_side == "long":
            return (price - self.entry_price) * self.position_size
        elif self.position_side == "short":
            return (self.entry_price - price) * self.position_size
        return 0
