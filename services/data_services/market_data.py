import pandas as pd

class MarketData:
    def __init__(self, symbol: str, data: list):
        # Initialize a MarketData object.
        # :param symbol: MarketData symbol (e.g., 'AAPL', 'GOOGL').
        # :param data: List of historical data dictionaries.
        
        self.symbol = symbol
        self.data = pd.DataFrame(data)

    def __str__(self):
        return f"MarketData({self.symbol}, {len(self.data)} records)"
    
    def __repr__(self):
        return f"MarketData(symbol={self.symbol}, data_shape={self.data.shape})"