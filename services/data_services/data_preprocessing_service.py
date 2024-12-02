from core.observer import EventObserver
from core.observer import EventPublisher
from typing import Any
import pandas as pd
from sklearn.preprocessing import StandardScaler


class DataPreprocessingService(EventObserver):
    def __init__(self, repository: Any, publisher: EventPublisher):
        self.repository = repository
        self.publisher = publisher
        self.scaler = StandardScaler()  # Initialize the scaler for numerical variables

    def on_event(self, event: Any) -> None:
        if self.is_interested_in(event):
            symbol = event['symbol']
            print(f"[DataPreprocessingService] Preprocessing data for {symbol}")
            
            # Fetch raw data
            stock_data = event['stock_data']  
            treasury_data = event['treasury_data']  
            indices_data = event['indices_data']  
            commodities_data = event['commodities_data']  
            
            merged_data = pd.merge(stock_data, treasury_data, on="Date")
            merged_data = pd.merge(merged_data, indices_data, on="Date")
            merged_data = pd.merge(merged_data, commodities_data, on="Date")
            
            # Preprocess data
            preprocessed_data = self.preprocess_data(pd.DataFrame(merged_data))
            
            # Notify other services
            self.publisher.publish({
                'type': 'DATA_PREPROCESSED',
                'symbol': symbol,
                'preprocessed_data': preprocessed_data
            })

    def is_interested_in(self, event: Any) -> bool:
        return event.get('type') == 'DATA_FETCHED'
    

    def preprocess_data(self, data: pd.DataFrame) -> dict:
        # Perform preprocessing steps:
        # - Extract time variables
        # - Create target variables
        # - Scale numerical data
        # - Handle missing values
        print(f"[DataPreprocessingService] Starting data preprocessing")

        # Ensure the Date column is in datetime format
        data['Date'] = pd.to_datetime(data['Date'])

        # Feature Engineering: Extract time variables
        data['Month'] = data['Date'].dt.month
        data['Day'] = data['Date'].dt.day
        data['Weekday'] = data['Date'].dt.weekday
        data['Hour'] = data['Date'].dt.hour
        data['MinuteSegment'] = data['Date'].dt.minute // 15
        data['IsMondayMorning'] = ((data['Weekday'] == 0) & (data['Hour'] < 12)).astype(int)
        data['IsFridayAfternoon'] = ((data['Weekday'] == 4) & (data['Hour'] >= 12)).astype(int)

        # Create shifted target variables for prediction
        data['Target_1D'] = data['Stock_Value'].shift(-1)
        data['Target_5D'] = data['Stock_Value'].shift(-5)

        # Handle missing values caused by shifting
        data = data.dropna()

        # Scale numerical features
        numerical_columns = ['Stock_Value', '2Y_Bond', '5Y_Bond', '10Y_Bond', 'DowJones', 'Nasdaq', 'S&P', 'Gold', 'Oil']
        
        data[numerical_columns] = self.scaler.fit_transform(data[numerical_columns])

        # Split features and targets for both 1D and 5D predictions
        X = data.drop(columns=['Date', 'Target_1D', 'Target_5D'])
        y_1D = data['Target_1D']
        y_5D = data['Target_5D']

        print(f"[DataPreprocessingService] Data preprocessing completed")

        # Return preprocessed data as a dictionary
        return {
            'features': X.to_dict(orient='records'),
            'target_1D': y_1D.tolist(),
            'target_5D': y_5D.tolist()
        }
