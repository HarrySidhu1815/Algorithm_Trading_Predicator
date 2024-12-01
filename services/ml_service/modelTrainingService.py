from typing import Any, Dict, Tuple
import pandas as pd
import numpy as np
import xgboost as xgb
from services.data_services.market_data import MarketData
from core.observer import EventObserver, EventPublisher
from services.ml_service.MLModel import MLModel
from services.data_services.IDataRepository import IDataRepository
from services.ml_service.IModelTrainer import IModelTrainer

class ModelTrainingService(EventObserver, IModelTrainer):
    def __init__(self, repository: IDataRepository, publisher: EventPublisher, model: MLModel):
        self.repository = repository
        self.publisher = publisher
        self.model = model

    def on_event(self, event: Any) -> None:
        if self.is_interested_in(event):
            symbol = event['symbol']
            print(f"[ModelTrainingService] Received cleaned data for {symbol}.")
            
            # Get cleaned stock data
            preprocessed_data: dict = event['preprocessed_data']

            # Convert features back to DataFrame
            X = pd.DataFrame(preprocessed_data['features'])
            y_1D = np.array(preprocessed_data['target_1D'])
            y_5D = np.array(preprocessed_data['target_5D'])

            # Prepare training and test data for 1D target
            training_data_1D, test_data_1D = self.model.prepare_data(X, y_1D)
            self.train_model(training_data_1D, {"max_depth": 5, "eta": 0.1, "objective": "reg:squarederror"})
            predictions_1D = self.evaluate_model(test_data_1D)

            # Prepare training and test data for 5D target
            training_data_5D, test_data_5D = self.model.prepare_data(X, y_5D)
            self.train_model(training_data_5D, {"max_depth": 5, "eta": 0.1, "objective": "reg:squarederror"})
            predictions_5D = self.evaluate_model(test_data_5D)

            # Publish ML_UPDATED event with both 1D and 5D predictions
            self.publisher.publish({
                'type': 'ML_UPDATED',
                'symbol': symbol,
                'target_1D_predictions': predictions_1D.tolist(),
                'target_5D_predictions': predictions_5D.tolist(),
                'original_data': X.to_dict(orient='records'),
                'target_1D_original_data' : test_data_1D[1],
                'target_5D_original_data' : test_data_5D[1],
            })

    def is_interested_in(self, event: Any) -> bool:
        return event.get('type') == 'DATA_PREPROCESSED'
    
    def train_model(self, training_data: Tuple[np.ndarray, np.ndarray], params: Dict[str, Any]) -> None:
        # Train the model using the provided training data and parameters.
        dtrain = xgb.DMatrix(training_data[0], label=training_data[1])
        self.model.train(dtrain, params)
    
    def evaluate_model(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        # Evaluate the model using the provided test data and return predictions.
        dtest = xgb.DMatrix(test_data[0])
        return self.model.predict(dtest)
