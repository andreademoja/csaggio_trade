import pandas as pd
from csaggio_trade.core.trade_log import TradeLog

def test_trade_log_records_trades():
    tl = TradeLog()

    tl.record(
        t="2020-01-01",
        side="long",
        size=1.0,
        entry=100,
        exit=110,
        pnl=10
    )

    df = tl.to_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["side"] == "long"
    assert df.iloc[0]["pnl"] == 10

def test_trade_log_saves_csv(tmp_path):
    tl = TradeLog()

    tl.record(
        t="2020-01-01",
        side="short",
        size=2.0,
        entry=200,
        exit=180,
        pnl=20
    )

    output_file = tmp_path / "trades.csv"
    tl.save(output_file)

    assert output_file.exists()
    assert output_file.stat().st_size > 0
