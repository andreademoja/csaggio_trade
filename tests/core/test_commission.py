import pytest
from csaggio_trade.core.commission import PercentageCommissionModel


class TestPercentageCommissionModel:
    def test_init(self):
        """Test PercentageCommissionModel initialization."""
        model = PercentageCommissionModel(commission_rate=0.001)
        assert model.commission_rate == 0.001

    def test_init_default(self):
        """Test PercentageCommissionModel with default rate."""
        model = PercentageCommissionModel()
        assert model.commission_rate == 0.001

    def test_calculate_commission(self):
        """Test commission calculation."""
        model = PercentageCommissionModel(commission_rate=0.001)  # 0.1%
        size = 1000.0
        price = 100.0
        commission = model.calculate_commission(size, price)
        expected = 1000.0 * 100.0 * 0.001  # 1.0
        assert commission == expected

    def test_calculate_commission_zero_rate(self):
        """Test commission with zero rate."""
        model = PercentageCommissionModel(commission_rate=0.0)
        size = 1000.0
        price = 100.0
        commission = model.calculate_commission(size, price)
        assert commission == 0.0

    def test_calculate_commission_different_values(self):
        """Test commission with different size and price."""
        model = PercentageCommissionModel(commission_rate=0.002)  # 0.2%
        size = 500.0
        price = 50.0
        commission = model.calculate_commission(size, price)
        expected = 500.0 * 50.0 * 0.002  # 0.5
        assert commission == expected