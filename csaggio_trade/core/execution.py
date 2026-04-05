class ExecutionEngine:
    def __init__(self, risk_manager, slippage_model=None, commission_model=None):
        self.risk_manager = risk_manager
        self.slippage_model = slippage_model
        self.commission_model = commission_model

    def process_signals(self, t, signals, portfolio):
        orders = []

        for signal in signals:
            if signal == "close" and portfolio.position_size == 0:
                return []   # non chiudere se non c’è nulla da chiudere
            
            action = signal["action"]

            # Caso 1: chiusura totale
            if action == "close_all":
                orders.append({"action": "close_all"})
                continue

            # Caso 2: apertura long/short
            side = signal["side"]
            size = self.risk_manager.size(t, signal, portfolio)

            order = {
                "action": action,
                "side": side,
                "size": size
            }

            orders.append(order)

        return orders
