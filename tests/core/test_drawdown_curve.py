import pandas as pd
from csaggio_trade.core.drawdown_curve import DrawdownCurve

def test_drawdown_curve_dataframe():
    results = [
        {"t": 0, "equity": 10000},
        {"t": 1, "equity": 10500},
        {"t": 2, "equity": 10200},
    ]

    dc = DrawdownCurve(results)
    df = dc.to_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["t", "drawdown"]
    assert len(df) == 3
    assert df["drawdown"].iloc[2] < 0  # drawdown negativo

def test_drawdown_curve_plot(tmp_path):
    results = [
        {"t": 0, "equity": 10000},
        {"t": 1, "equity": 10500},
        {"t": 2, "equity": 10200},
    ]

    dc = DrawdownCurve(results)
    output_file = tmp_path / "drawdown.png"

    dc.plot(output_file)

    assert output_file.exists()
    assert output_file.stat().st_size > 0
