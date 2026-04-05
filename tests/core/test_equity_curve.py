import pandas as pd
from csaggio_trade.core.equity_curve import EquityCurve

def test_equity_curve_generates_dataframe():
    results = [
        {"t": 0, "equity": 10000},
        {"t": 1, "equity": 10500},
        {"t": 2, "equity": 10200},
    ]

    ec = EquityCurve(results)
    df = ec.to_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["t", "equity"]
    assert len(df) == 3
    assert df["equity"].iloc[1] == 10500

def test_equity_curve_plot_saves_file(tmp_path):
    results = [
        {"t": 0, "equity": 10000},
        {"t": 1, "equity": 10500},
        {"t": 2, "equity": 10200},
    ]

    ec = EquityCurve(results)
    output_file = tmp_path / "equity.png"

    ec.plot(output_file)

    assert output_file.exists()
    assert output_file.stat().st_size > 0
