import pandas as pd
from csaggio_trade.strategies.mean_reversion import MeanReversionStrategy

def test_mean_reversion_generates_long_signal():
    df = pd.DataFrame({
        "zscore": [-3.0],
        "rsi": [20]
    })

    strategy = MeanReversionStrategy(
        z_entry_long=-2.0,
        z_entry_short=2.0,
        z_exit=0.5,
        rsi_long_max=30,
        rsi_short_min=70,
        regime_filter=None
    )

    signals = strategy.generate_signals(0, df.iloc[0])
    assert len(signals) == 1
    assert signals[0]["side"] == "long"
    assert signals[0]["action"] == "open"


def test_mean_reversion_generates_short_signal():
    df = pd.DataFrame({
        "zscore": [3.0],
        "rsi": [80]
    })

    strategy = MeanReversionStrategy(
        z_entry_long=-2.0,
        z_entry_short=2.0,
        z_exit=0.5,
        rsi_long_max=30,
        rsi_short_min=70,
        regime_filter=None
    )

    signals = strategy.generate_signals(0, df.iloc[0])
    assert len(signals) == 1
    assert signals[0]["side"] == "short"
    assert signals[0]["action"] == "open"


def test_mean_reversion_generates_exit_signal():
    df = pd.DataFrame({
        "zscore": [0.1],
        "rsi": [50]
    })

    strategy = MeanReversionStrategy(
        z_entry_long=-2.0,
        z_entry_short=2.0,
        z_exit=0.5,
        rsi_long_max=30,
        rsi_short_min=70,
        regime_filter=None
    )

    signals = strategy.generate_signals(0, df.iloc[0])
    assert len(signals) == 1
    assert signals[0]["action"] == "close_all"
