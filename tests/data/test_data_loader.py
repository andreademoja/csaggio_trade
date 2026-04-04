import pandas as pd
from csaggio_trade.data.loader import DataLoader

def test_loader_reads_csv_and_applies_parser(tmp_path):
    # 1) Creiamo un CSV temporaneo
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "timestamp,price\n"
        "2024-01-01 00:00:00,1.2345\n"
        "2024-01-01 01:00:00,1.2350\n"
    )

    # 2) Parser di test (identità)
    def parser(df):
        df["price_times_two"] = df["price"] * 2
        return df

    # 3) Loader
    loader = DataLoader(path=str(csv_file), parser=parser)

    # 4) Carichiamo i dati
    df = loader.load()

    # 5) Asserzioni
    assert isinstance(df, pd.DataFrame)
    assert "price" in df.columns
    assert "price_times_two" in df.columns
    assert df.iloc[0]["price"] == 1.2345
    assert df.iloc[0]["price_times_two"] == 2.469
