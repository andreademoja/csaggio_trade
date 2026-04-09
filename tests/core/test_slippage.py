import pytest
from csaggio_trade.core.slippage import FixedSlippageModel


class TestFixedSlippageModel:
    def test_init(self):
        """Test FixedSlippageModel initialization."""
        model = FixedSlippageModel(slippage_pips=0.5)
        assert model.slippage_pips == 0.5

    def test_init_default(self):
        """Test FixedSlippageModel with default slippage."""
        model = FixedSlippageModel()
        assert model.slippage_pips == 0.5

    def test_apply_slippage_open_long(self):
        """Test slippage application for opening long position."""
        model = FixedSlippageModel(slippage_pips=0.5)
        price = 100.0
        result = model.apply_slippage(price, "long", "open")
        assert result == 100.5

    def test_apply_slippage_open_short(self):
        """Test slippage application for opening short position."""
        model = FixedSlippageModel(slippage_pips=0.5)
        price = 100.0
        result = model.apply_slippage(price, "short", "open")
        assert result == 99.5

    def test_apply_slippage_close_long(self):
        """Test slippage application for closing long position."""
        model = FixedSlippageModel(slippage_pips=0.5)
        price = 100.0
        result = model.apply_slippage(price, "long", "close_all")
        assert result == 99.5

    def test_apply_slippage_close_short(self):
        """Test slippage application for closing short position."""
        model = FixedSlippageModel(slippage_pips=0.5)
        price = 100.0
        result = model.apply_slippage(price, "short", "close_all")
        assert result == 100.5

    def test_apply_slippage_invalid_action(self):
        """Test slippage application with invalid action returns original price."""
        model = FixedSlippageModel(slippage_pips=0.5)
        price = 100.0
        result = model.apply_slippage(price, "long", "invalid")
        assert result == 100.0

    def test_apply_slippage_zero_slippage(self):
        """Test with zero slippage."""
        model = FixedSlippageModel(slippage_pips=0.0)
        price = 100.0
        result = model.apply_slippage(price, "long", "open")
        assert result == 100.0