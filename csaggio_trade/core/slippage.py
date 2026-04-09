class FixedSlippageModel:
    def __init__(self, slippage_pips=0.5):  # 0.5 USD for gold
        self.slippage_pips = slippage_pips

    def apply_slippage(self, price, side, action):
        if action == "open":
            if side == "long":
                return price + self.slippage_pips
            elif side == "short":
                return price - self.slippage_pips
        elif action == "close_all":
            if side == "long":
                return price - self.slippage_pips
            elif side == "short":
                return price + self.slippage_pips
        return price