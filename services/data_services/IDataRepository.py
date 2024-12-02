from abc import ABC, abstractmethod
from services.data_services.market_data import MarketData

class IDataRepository(ABC):
    @abstractmethod
    def fetch_data(self, symbol: str) -> MarketData:
        """Fetch stock data."""
        pass