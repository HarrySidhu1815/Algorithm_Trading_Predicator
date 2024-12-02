from services.data_services.IDataRepository import IDataRepository
from pymongo import MongoClient
import pandas as pd
from services.data_services.market_data import MarketData


class MarketDatabaseHandler(IDataRepository):
    def __init__(self, db_uri: str):
        self.client = MongoClient(db_uri)
        self.db = self.client['Stocks']

    def fetch_data(self, symbol: str) -> MarketData:
        # Fetch data from the MongoDB collection and return a Stock instance.
        collection = self.db[symbol]
        
        cursor = collection.find()
        data = pd.DataFrame(list(cursor))

        if "_id" in data.columns:
            data.drop(columns=["_id"], inplace=True)

        stock = MarketData(symbol, data)
        return stock