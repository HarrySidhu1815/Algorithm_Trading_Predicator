from typing import Any, Dict, Tuple
import pandas as pd
import numpy as np
import xgboost as xgb
from services.data_services.market_data import MarketData
from core.observer import EventObserver, EventPublisher
from services.ml_service.MLModel import MLModel
from services.data_services.IDataRepository import IDataRepository

class ModelTrainingService(EventObserver):
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

            # Prepare training and test data (using 1D target for training as an example)
            training_data, test_data = self.model.prepare_data(X, y_1D)

            # Train the model using MLModel
            dtrain = xgb.DMatrix(training_data[0], label=training_data[1])
            self.model.train(dtrain, {"max_depth": 5, "eta": 0.1, "objective": "reg:squarederror"})

            # Predict the 1D and 5D targets
            dtest = xgb.DMatrix(test_data[0])
            predictions_1D = self.model.predict(dtest)

            # Repeat the training and prediction for 5D target
            training_data_5D, test_data_5D = self.model.prepare_data(X, y_5D)
            dtrain_5D = xgb.DMatrix(training_data_5D[0], label=training_data_5D[1])
            self.model.train(dtrain_5D, {"max_depth": 5, "eta": 0.1, "objective": "reg:squarederror"})
            dtest_5D = xgb.DMatrix(test_data_5D[0])
            predictions_5D = self.model.predict(dtest_5D)

            # Combine original data with predictions
            # combined_data_1D = self.combine_data_with_predictions(X, y_1D, predictions_1D, target_type="1D")
            # combined_data_5D = self.combine_data_with_predictions(X, y_5D, predictions_5D, target_type="5D")

            # Publish ML_UPDATED event with both 1D and 5D predictions
            self.publisher.publish({
                'type': 'ML_UPDATED',
                'symbol': symbol,
                'target_1D_predictions': predictions_1D.tolist(),
                'target_5D_predictions': predictions_5D.tolist(),
                'original_data': X.to_dict(orient='records'),
                'target_1D_orginial_data' : test_data[1],
                'target_5D_orginial_data' : test_data_5D[1],
            })

    def is_interested_in(self, event: Any) -> bool:
        return event.get('type') == 'DATA_PREPROCESSED'

    # def combine_data_with_predictions(self, data: pd.DataFrame, target: np.ndarray, predictions: np.ndarray, target_type: str) -> pd.DataFrame:
    #     # Append the predicted rows to the existing DataFrame
    #     prediction_rows = pd.DataFrame(predictions, columns=['Predicted_' + target_type])
    #     updated_data = pd.concat([data, prediction_rows], axis=1)
    #     print(f"[ModelTrainingService] Combined {target_type} predictions with existing data.")
    #     return updated_data
