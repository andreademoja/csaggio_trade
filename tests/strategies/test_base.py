import pandas as pd
import pytest
import tempfile
import os
from csaggio_trade.strategies.base import DataLoader


class TestDataLoader:
    def test_init(self):
        """Test DataLoader initialization."""
        loader = DataLoader(path="dummy.csv", parser=lambda df: df)
        assert loader.path == "dummy.csv"
        assert callable(loader.parser)

    def test_load_csv(self, tmp_path):
        """Test loading a CSV file."""
        # Create a temporary CSV file
        csv_content = """date,open,high,low,close,volume
2023-01-01,100,105,95,102,1000
2023-01-02,102,107,98,105,1100"""
        
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        loader = DataLoader(path=str(csv_file), parser=lambda df: df)
        df = loader.load()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ['open', 'high', 'low', 'close', 'volume']
        assert df.iloc[0]['close'] == 102

    def test_load_with_parser(self, tmp_path):
        """Test loading with a custom parser."""
        csv_content = """date,price
2023-01-01,100
2023-01-02,102"""
        
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        def custom_parser(df):
            df['parsed'] = df['price'] * 2
            return df
        
        loader = DataLoader(path=str(csv_file), parser=custom_parser)
        df = loader.load()
        
        assert 'parsed' in df.columns
        assert df.iloc[0]['parsed'] == 200

    def test_load_nonexistent_file(self):
        """Test loading a nonexistent file raises error."""
        loader = DataLoader(path="nonexistent.csv", parser=lambda df: df)
        with pytest.raises(FileNotFoundError):
            loader.load()