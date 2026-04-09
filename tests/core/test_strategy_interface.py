import pytest
from abc import ABC
from csaggio_trade.core.strategy_interface import StrategyInterface


class TestStrategyInterface:
    def test_strategy_interface_is_abc(self):
        """Test that StrategyInterface is an Abstract Base Class."""
        assert issubclass(StrategyInterface, ABC)

    def test_strategy_interface_init(self):
        """Test that StrategyInterface cannot be instantiated directly."""
        with pytest.raises(TypeError):
            StrategyInterface({})

    def test_abstract_methods(self):
        """Test that StrategyInterface has the required abstract methods."""
        abstract_methods = [
            'initialize',
            'calculate_signal',
            'get_trade_parameters'
        ]
        
        for method in abstract_methods:
            assert hasattr(StrategyInterface, method)
            # Check if it's abstract (hard to test directly, but we can check it raises NotImplementedError)

    def test_str_method(self):
        """Test the __str__ method (though it can't be called on abstract class)."""
        # Since we can't instantiate, we'll test with a mock subclass
        class MockStrategy(StrategyInterface):
            def initialize(self, initial_data):
                pass
            
            def calculate_signal(self, current_data_point, historical_data):
                return "HOLD"
            
            def get_trade_parameters(self, signal):
                return {}

        strategy = MockStrategy({"test": "param"})
        assert "MockStrategy" in str(strategy)
        assert "param" in str(strategy)

    def test_parameters_storage(self):
        """Test that parameters are stored correctly in a concrete subclass."""
        class MockStrategy(StrategyInterface):
            def initialize(self, initial_data):
                pass
            
            def calculate_signal(self, current_data_point, historical_data):
                return "HOLD"
            
            def get_trade_parameters(self, signal):
                return {}

        params = {"z_entry": -2.0, "z_exit": 0.5}
        strategy = MockStrategy(params)
        assert strategy.parameters == params