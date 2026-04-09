import pandas as pd
import pytest
from unittest.mock import Mock, patch
from csaggio_trade.core.engine import Engine


class TestEngine:
    def test_init(self):
        """Test Engine initialization."""
        mock_loader = Mock()
        mock_strategy = Mock()
        mock_execution = Mock()
        mock_portfolio = Mock()
        mock_reporter = Mock()
        
        engine = Engine(mock_loader, mock_strategy, mock_execution, mock_portfolio, mock_reporter)
        
        assert engine.loader == mock_loader
        assert engine.strategy == mock_strategy
        assert engine.execution == mock_execution
        assert engine.portfolio == mock_portfolio
        assert engine.reporter == mock_reporter

    @patch('csaggio_trade.core.backtester.Backtester')
    def test_run(self, mock_backtester_class):
        """Test Engine run method."""
        # Mock data
        mock_data = pd.DataFrame({"close": [100, 101, 102]})
        
        # Mocks
        mock_loader = Mock()
        mock_loader.load.return_value = mock_data
        
        mock_strategy = Mock()
        mock_strategy.prepare_data.return_value = mock_data
        
        mock_execution = Mock()
        mock_portfolio = Mock()
        mock_reporter = Mock()
        
        # Mock backtester instance
        mock_backtester_instance = Mock()
        mock_backtester_instance.run.return_value = ("results", "trade_log")
        mock_backtester_class.return_value = mock_backtester_instance
        
        engine = Engine(mock_loader, mock_strategy, mock_execution, mock_portfolio, mock_reporter)
        result = engine.run()
        
        # Verify calls
        mock_loader.load.assert_called_once()
        mock_strategy.prepare_data.assert_called_once_with(mock_data)
        mock_backtester_class.assert_called_once_with(
            mock_data, mock_strategy, mock_execution, mock_portfolio, mock_reporter
        )
        mock_backtester_instance.run.assert_called_once()
        
        assert result == ("results", "trade_log")