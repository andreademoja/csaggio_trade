import pandas as pd
from csaggio_trade.indicators.builder import IndicatorBuilder

def test_indicator_builder_adds_indicators():
    # 1) DataFrame di test
    df = pd.DataFrame({
        "high": [10, 11, 12, 13, 14],
        "low":  [ 9, 10, 11, 12, 13],
        "close":[ 9.5, 10.5, 11.5, 12.5, 13.5]
    })

    # 2) Parametri (nessun numero hard-coded nel modulo)
    params = {
        "atr_period": 3,
        "rsi_period": 2,
        "zscore_period": 3
    }

    # 3) Builder
    builder = IndicatorBuilder(**params)

    # 4) Applichiamo gli indicatori
    out = builder(df)

    # 5) Asserzioni
    assert "atr" in out.columns
    assert "rsi" in out.columns
    assert "zscore" in out.columns

    # Controlliamo che non siano tutti NaN
    assert out["atr"].notna().sum() > 0
    assert out["rsi"].notna().sum() > 0
    assert out["zscore"].notna().sum() > 0
