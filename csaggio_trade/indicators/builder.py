import pandas as pd

class IndicatorBuilder:
    def __init__(self, atr_period, rsi_period, zscore_period):
        self.atr_period = atr_period
        self.rsi_period = rsi_period
        self.zscore_period = zscore_period

    def __call__(self, df):
        df = df.copy()
        df["atr"] = self._atr(df, self.atr_period)
        df["rsi"] = self._rsi(df["close"], self.rsi_period)
        df["zscore"] = self._zscore(df["close"], self.zscore_period)
        return df

    # ---------------------------
    # ATR
    # ---------------------------
    def _atr(self, df, period):
        high_low = df["high"] - df["low"]
        high_close = (df["high"] - df["close"].shift()).abs()
        low_close = (df["low"] - df["close"].shift()).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    # ---------------------------
    # RSI
    # ---------------------------
    def _rsi(self, series, period):
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    # ---------------------------
    # Z-SCORE
    # ---------------------------
    def _zscore(self, series, period):
        mean = series.rolling(period).mean()
        std = series.rolling(period).std()
        return (series - mean) / std
