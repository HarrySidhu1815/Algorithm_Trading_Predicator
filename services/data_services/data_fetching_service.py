from core.observer import EventObserver
from core.observer import EventPublisher
from typing import Any
from other import events
import pandas as pd


class DataFetchingService(EventObserver):
    def __init__(self, repository: Any, publisher: EventPublisher):
        self.repository = repository
        self.publisher = publisher

    def on_event(self, event: Any) -> None:
        if self.is_interested_in(event):
            print(f"[DataFetchingService] Fetching data for multiple sources")
            
            symbol = event['symbol']
            
            # Fetch stock data directly from MongoDB
            stock = self.repository.fetch_data(symbol)
            stock_data = stock.data[['Date', 'Close']].rename(columns={'Close': 'Stock_Value'})

            # Fetch data from repository
            treasury_data = self.fetch_treasury_data()
            indices_data = self.fetch_indices_data()
            commodities_data = self.fetch_commodities_data()

            # Publish the fetched data for downstream services
            self.publisher.publish({
                'type': 'DATA_FETCHED',
                'symbol': symbol,
                'stock_data': stock_data,
                'treasury_data': treasury_data,
                'indices_data': indices_data,
                'commodities_data': commodities_data
            })

    def is_interested_in(self, event: Any) -> bool:
        return event.get('type') == events.START_PROCESS

    def fetch_treasury_data(self) -> pd.DataFrame:
        """Fetch treasury bond data."""
        print("[DataFetchingService] Fetching treasury bond data")
        twovx = self.repository.fetch_data('2YearTreasuryBond')  # 2-year bond
        fvx = self.repository.fetch_data('5yearTreasuryBond')      # 5-year bond
        tvx = self.repository.fetch_data('10yearTreasuryBond')      # 10-year bond

        # Extract Date and Close columns for each dataset
        twovx_data = twovx.data[['Date', 'Close']].rename(columns={'Close': '2Y_Bond'})
        fvx_data = fvx.data[['Date', 'Close']].rename(columns={'Close': '5Y_Bond'})
        tvx_data = tvx.data[['Date', 'Close']].rename(columns={'Close': '10Y_Bond'})

        # Merge the dataframes on the 'Date' column
        treasury_data = pd.merge(twovx_data, fvx_data, on='Date', how='outer')
        treasury_data = pd.merge(treasury_data, tvx_data, on='Date', how='outer')
        return treasury_data

    def fetch_indices_data(self) -> pd.DataFrame:
        """Fetch stock indices data."""
        print("[DataFetchingService] Fetching indices data")
        dow_jones = self.repository.fetch_data('DowJones')  # Dow Jones Index
        nasdaq = self.repository.fetch_data('NASDAQ')       # Nasdaq Index
        sp500 = self.repository.fetch_data('S&P')         # S&P 500 Index

        # Extract Date and Close columns for each dataset
        dow_jones_data = dow_jones.data[['Date', 'Close']].rename(columns={'Close': 'DowJones'})
        nasdaq_data = nasdaq.data[['Date', 'Close']].rename(columns={'Close': 'Nasdaq'})
        sp500_data = sp500.data[['Date', 'Close']].rename(columns={'Close': 'S&P'})

        # Merge the dataframes on the 'Date' column
        indices_data = pd.merge(dow_jones_data, nasdaq_data, on='Date', how='outer')
        indices_data = pd.merge(indices_data, sp500_data, on='Date', how='outer')
        
        return indices_data

    def fetch_commodities_data(self) -> pd.DataFrame:
        """Fetch commodities data."""
        print("[DataFetchingService] Fetching commodities data")
        gold = self.repository.fetch_data('PriceOfGold')  # Gold price
        oil = self.repository.fetch_data('PriceOfCrudeOil')    # Oil price
        
        # Extract Date and Close columns for each dataset
        gold_data = gold.data[['Date', 'Close']].rename(columns={'Close': 'Gold'})
        oil_data = oil.data[['Date', 'Close']].rename(columns={'Close': 'Oil'})

        # Merge the dataframes on the 'Date' column
        commodities_data = pd.merge(gold_data, oil_data, on='Date', how='outer')

        return commodities_data
