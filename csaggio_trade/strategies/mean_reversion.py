class MeanReversionStrategy:
    def __init__(
        self,
        z_entry_long,
        z_entry_short,
        z_exit,
        rsi_long_max,
        rsi_short_min,
        regime_filter=None
    ):
        self.z_entry_long = z_entry_long
        self.z_entry_short = z_entry_short
        self.z_exit = z_exit
        self.rsi_long_max = rsi_long_max
        self.rsi_short_min = rsi_short_min
        self.regime_filter = regime_filter

    def prepare_data(self, df):
        return df

    def generate_signals(self, t, row):
        signals = []

        # Regime filter (se presente)
        if self.regime_filter is not None:
            if not self.regime_filter.allow_trade(row):
                return signals

        z = row["zscore"]
        rsi = row["rsi"]

        # Entry long
        if z <= self.z_entry_long and rsi <= self.rsi_long_max:
            signals.append({"side": "long", "action": "open"})
            return signals

        # Entry short
        if z >= self.z_entry_short and rsi >= self.rsi_short_min:
            signals.append({"side": "short", "action": "open"})
            return signals

        # Exit
        if abs(z) <= self.z_exit:
            signals.append({"action": "close_all"})
            return signals

        return signals
