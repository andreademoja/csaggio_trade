import pytest
from csaggio_trade.config.presets import (
    FOREX_MEAN_REVERSION,
    STOCKS_MEAN_REVERSION_PRESET,
    METALS_MEAN_REVERSION_PRESET,
    COMMODITIES_MEAN_REVERSION_PRESET
)


class TestPresets:
    def test_forex_mean_reversion_is_dict(self):
        """Test that FOREX_MEAN_REVERSION is a dictionary."""
        assert isinstance(FOREX_MEAN_REVERSION, dict)

    def test_forex_mean_reversion_has_required_keys(self):
        """Test that FOREX_MEAN_REVERSION has all required keys."""
        required_keys = [
            "z_entry_long", "z_entry_short", "z_exit",
            "rsi_long_max", "rsi_short_min", "atr_period", "risk_per_trade"
        ]
        for key in required_keys:
            assert key in FOREX_MEAN_REVERSION

    def test_forex_mean_reversion_values_types(self):
        """Test that FOREX_MEAN_REVERSION values have correct types."""
        assert isinstance(FOREX_MEAN_REVERSION["z_entry_long"], (int, float))
        assert isinstance(FOREX_MEAN_REVERSION["z_entry_short"], (int, float))
        assert isinstance(FOREX_MEAN_REVERSION["z_exit"], (int, float))
        assert isinstance(FOREX_MEAN_REVERSION["rsi_long_max"], (int, float))
        assert isinstance(FOREX_MEAN_REVERSION["rsi_short_min"], (int, float))
        assert isinstance(FOREX_MEAN_REVERSION["atr_period"], int)
        assert isinstance(FOREX_MEAN_REVERSION["risk_per_trade"], (int, float))

    def test_stocks_mean_reversion_exists(self):
        """Test that STOCKS_MEAN_REVERSION_PRESET exists."""
        # Note: This preset appears to be a placeholder
        assert 'STOCKS_MEAN_REVERSION_PRESET' in globals()

    def test_metals_mean_reversion_exists(self):
        """Test that METALS_MEAN_REVERSION_PRESET exists."""
        # Note: This preset appears to be a placeholder
        assert 'METALS_MEAN_REVERSION_PRESET' in globals()

    def test_commodities_mean_reversion_exists(self):
        """Test that COMMODITIES_MEAN_REVERSION_PRESET exists."""
        # Note: This preset appears to be a placeholder
        assert 'COMMODITIES_MEAN_REVERSION_PRESET' in globals()