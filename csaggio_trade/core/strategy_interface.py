from abc import ABC, abstractmethod
from typing import List, Dict, Any

class StrategyInterface(ABC):
    """
    Abstract Base Class defining the interface for all trading strategies.
    All concrete strategies must inherit from this class and implement 
    the required methods.
    """

    def __init__(self, parameters: Dict[str, Any]):
        """
        Initializes the strategy with specific parameters (e.g., lookback period, threshold).
        :param parameters: Dictionary containing configuration parameters.
        """
        self.parameters = parameters

    @abstractmethod
    def initialize(self, initial_data: List[Dict[str, float]]) -> None:
        """
        Initializes the strategy using the initial historical data provided 
        (e.g., calculating initial indicators).
        :param initial_data: A list of historical data points (e.g., OHLCV data).
        """
        pass

    @abstractmethod
    def calculate_signal(self, current_data_point: Dict[str, float], historical_data: List[Dict[str, float]]) -> str:
        """
        Analyzes the current data point against historical context to generate a trading signal.
        
        :param current_data_point: The latest data point (e.g., the closing price).
        :param historical_data: The historical context needed for calculations.
        :return: A string signal: "BUY", "SELL", or "HOLD".
        """
        pass

    @abstractmethod
    def get_trade_parameters(self, signal: str) -> Dict[str, Any]:
        """
        Calculates specific trade parameters (e.g., target price, stop-loss level) 
        based on the generated signal.
        
        :param signal: The signal received from calculate_signal ("BUY", "SELL", "HOLD").
        :return: A dictionary containing trade details.
        """
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__} initialized with parameters: {self.parameters}"