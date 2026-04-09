import logging
import os
import pytest
from pathlib import Path

from csaggio_trade.logger import setup_logging, get_logger, logger


class TestSetupLogging:
    def test_setup_logging_creates_logs_directory(self, tmp_path):
        """Test that setup_logging creates the logs directory if it doesn't exist."""
        log_dir = tmp_path / "logs"
        setup_logging(level=logging.INFO, log_dir=log_dir)
        assert log_dir.exists()
        assert log_dir.is_dir()

    def test_setup_logging_configures_handlers(self):
        """Test that setup_logging configures console and file handlers."""
        test_logger = setup_logging(level=logging.DEBUG)
        
        # Check that root logger has handlers (since basicConfig adds to root)
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) >= 2  # At least console and file
        
        # Check handler types
        handler_types = [type(h).__name__ for h in root_logger.handlers]
        assert "StreamHandler" in handler_types
        assert "FileHandler" in handler_types

    def test_setup_logging_sets_levels(self):
        """Test that setup_logging sets the correct logging level."""
        test_logger = setup_logging(level=logging.ERROR)
        assert test_logger.level == logging.ERROR
        
        # Test with different level
        test_logger = setup_logging(level=logging.DEBUG)
        assert test_logger.level == logging.DEBUG

    def test_setup_logging_file_output(self, tmp_path):
        """Test that logs are written to file."""
        log_dir = tmp_path / "logs"
        test_logger = setup_logging(level=logging.INFO, log_dir=log_dir)
        test_logger.info("Test file log message")
        log_file = log_dir / "csaggio_trade.log"
        assert log_file.exists()
        content = log_file.read_text(encoding='utf-8')
        assert "Test file log message" in content


class TestGetLogger:
    def test_get_logger_without_name(self):
        """Test get_logger without name returns default logger."""
        test_logger = get_logger()
        assert test_logger.name == "csaggio_trade"

    def test_get_logger_with_name(self):
        """Test get_logger with name returns named logger."""
        test_logger = get_logger("test_module")
        assert test_logger.name == "csaggio_trade.test_module"

    def test_logger_instance(self):
        """Test that the default logger instance is properly configured."""
        assert logger.name == "csaggio_trade"
        assert isinstance(logger, logging.Logger)


class TestBackwardCompatibility:
    def test_get_package_logger(self):
        """Test backward compatibility function."""
        from csaggio_trade.logger import get_package_logger
        test_logger = get_package_logger()
        assert test_logger.name == "csaggio_trade"

    def test_get_module_logger(self):
        """Test backward compatibility function."""
        from csaggio_trade.logger import get_module_logger
        test_logger = get_module_logger("compat")
        assert test_logger.name == "csaggio_trade.compat"