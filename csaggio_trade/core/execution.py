import logging
class ExecutionEngine:
    def __init__(self, risk_manager, slippage_model=None, commission_model=None):
        self.risk_manager = risk_manager
        self.slippage_model = slippage_model
        self.commission_model = commission_model

    def process_signals(self, t, signals, portfolio, row=None):
        orders = []
        price = None
        if row is not None:
            price = row.get("close", None)

        for signal in signals:
            if signal == "close" and portfolio.position_size == 0:
                return []
            action = signal["action"]

            # Caso 1: chiusura totale
            if action == "close_all":
                # Apply slippage to exit price if possible
                exit_price = price
                if self.slippage_model and price is not None and portfolio.position_side:
                    exit_price = self.slippage_model.apply_slippage(
                        price, portfolio.position_side, "close_all"
                    )
                orders.append({"action": "close_all", "exit_price": exit_price})
                continue

            # Caso 2: apertura long/short
            side = signal["side"]
            size = self.risk_manager.size(t, signal, portfolio)
            open_price = price
            if self.slippage_model and price is not None:
                open_price = self.slippage_model.apply_slippage(price, side, "open")
            order = {
                "action": action,
                "side": side,
                "size": size,
                "open_price": open_price
            }
            orders.append(order)
        return orders
