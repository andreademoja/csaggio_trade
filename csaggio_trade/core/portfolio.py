import logging

class Portfolio:
    def __init__(self, initial_equity):
        self.equity = initial_equity
        self.position_size = 0
        self.position_side = None
        self.entry_price = None
        self.last_price = None
        self.open_price = None  # Prezzo apertura del periodo
        self.last_tick_price = None  # Prezzo ultimo tick
        self.current_atr = 0
        self.logger = logging.getLogger(__name__)

    def update(self, t, row, orders, commission_model=None):
        self.open_price = row.get("open", row.get("close"))
        self.last_price = row["close"]
        self.last_tick_price = row["close"]
        price = row["close"]

        for order in orders:
            action = order["action"]
            self.current_atr = row.get("atr", None)

            # Apertura posizione
            if order["action"] == "open":
                self.position_side = order["side"]
                self.position_size = order["size"]
                # Use slippage-adjusted open price if present
                self.entry_price = order.get("open_price", price)
                # Deduct commission on open
                if commission_model is not None:
                    commission = commission_model.calculate_commission(self.position_size, self.entry_price)
                    self.equity -= commission

            # Chiusura totale
            elif action == "close_all":
                if self.position_size != 0:
                    # Use slippage-adjusted exit price if present
                    exit_price = order.get("exit_price", price)
                    pnl = self._calculate_pnl(exit_price)
                    self.equity += pnl
                    # Deduct commission on close
                    if commission_model is not None:
                        commission = commission_model.calculate_commission(self.position_size, exit_price)
                        self.equity -= commission
                self.position_size = 0
                self.position_side = None
                self.entry_price = None

    def _calculate_pnl(self, price):
        if self.position_side == "long":
            return (price - self.entry_price) * self.position_size
        elif self.position_side == "short":
            return (self.entry_price - price) * self.position_size
        return 0

    def get_atr(self):
        return self.current_atr