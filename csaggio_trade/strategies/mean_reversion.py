class MeanReversionStrategy:
    def __init__(
        self,
        z_entry_long=-2.5,
        z_entry_short=2.5,
        z_exit=0.8,
        rsi_long_max=25,
        rsi_short_min=75,
        ema_period=100,
        atr_filter=0.0004,
        tp_atr=1.0,
        sl_atr=1.5,
        regime_filter=None
    ):
        self.z_entry_long = z_entry_long
        self.z_entry_short = z_entry_short
        self.z_exit = z_exit
        self.rsi_long_max = rsi_long_max
        self.rsi_short_min = rsi_short_min
        self.ema_period = ema_period
        self.atr_filter = atr_filter
        self.tp_atr = tp_atr
        self.sl_atr = sl_atr
        self.regime_filter = regime_filter

    def prepare_data(self, df):
        df["ema"] = df["close"].ewm(span=self.ema_period).mean()
        df["bb_mid"] = df["close"].rolling(20).mean()
        df["bb_std"] = df["close"].rolling(20).std()
        df["bb_upper"] = df["bb_mid"] + 2 * df["bb_std"]
        df["bb_lower"] = df["bb_mid"] - 2 * df["bb_std"]
        return df

    def generate_signals(self, t, row, portfolio=None):
        signals = []

        # Compatibilità con i test
        if portfolio is None:
            z = row["zscore"]
            rsi = row["rsi"]
            if z <= self.z_entry_long and rsi <= self.rsi_long_max:
                return [{"side": "long", "action": "open"}]
            if z >= self.z_entry_short and rsi >= self.rsi_short_min:
                return [{"side": "short", "action": "open"}]
            if abs(z) <= self.z_exit:
                return [{"action": "close_all"}]
            return []

        # ============================
        # 0) Regime filter
        # ============================
        if self.regime_filter is not None:
            if not self.regime_filter.allow_trade(row):
                return signals

        z = row["zscore"]
        rsi = row["rsi"]
        atr = row["atr"]
        price = row["close"]

        # ============================
        # 1) NO POSITION → ENTRY LOGIC
        # ============================
        if portfolio.position_side is None:

            # Filtro volatilità (mercato troppo piatto)
            if atr < price * self.atr_filter:
                return signals

            # Filtro trend (EMA50)
            above_ema = price > row["ema"]
            below_ema = price < row["ema"]

            # Filtro Bollinger (estensione)
            near_lower_band = price <= row["bb_lower"]
            near_upper_band = price >= row["bb_upper"]

            # Entry long
            if (
                z <= self.z_entry_long
                and rsi <= self.rsi_long_max
                and above_ema
                and near_lower_band
            ):
                signals.append({"side": "long", "action": "open"})
                return signals

            # Entry short
            if (
                z >= self.z_entry_short
                and rsi >= self.rsi_short_min
                and below_ema
                and near_upper_band
            ):
                signals.append({"side": "short", "action": "open"})
                return signals

            return signals

        # ============================
        # 2) POSITION OPEN → EXIT LOGIC
        # ============================

        entry = portfolio.entry_price
        side = portfolio.position_side

        # --- Exit 1: Take Profit ATR ---
        if side == "long" and price >= entry + self.tp_atr * atr:
            signals.append({"action": "close_all"})
            return signals

        if side == "short" and price <= entry - self.tp_atr * atr:
            signals.append({"action": "close_all"})
            return signals

        # --- Exit 2: Stop Loss ATR ---
        if side == "long" and price <= entry - self.sl_atr * atr:
            signals.append({"action": "close_all"})
            return signals

        if side == "short" and price >= entry + self.sl_atr * atr:
            signals.append({"action": "close_all"})
            return signals

        # --- Exit 3: ritorno verso la media ---
        if abs(z) <= self.z_exit:
            signals.append({"action": "close_all"})
            return signals

        # --- Exit 4: inversione RSI ---
        if side == "long" and rsi > 55:
            signals.append({"action": "close_all"})
            return signals

        if side == "short" and rsi < 45:
            signals.append({"action": "close_all"})
            return signals

        # --- Exit 5: segnale opposto ---
        if side == "long" and z >= self.z_entry_short:
            signals.append({"action": "close_all"})
            return signals

        if side == "short" and z <= self.z_entry_long:
            signals.append({"action": "close_all"})
            return signals

        return signals
