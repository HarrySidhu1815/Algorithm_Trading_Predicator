from abc import ABC, abstractmethod
import pandas as pd
from services.data_services.market_data import MarketData

class IDataRepository(ABC):
    # @abstractmethod
    # def store_data(self, symbol: str, data: pd.DataFrame) -> None:
    #     """Store stock data."""
    #     pass

    @abstractmethod
    def fetch_data(self, symbol: str) -> MarketData:
        """Fetch stock data."""
        pass