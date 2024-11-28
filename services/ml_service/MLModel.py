from typing import Any, Dict, Tuple
import pandas as pd
import xgboost as xgb
import numpy as np

# MLModel class for managing the XGBoost model
class MLModel:
    def __init__(self):
        self.model = xgb.Booster()  # Initialize an empty XGBoost model

    def train(self, dtrain: xgb.DMatrix, params: Dict[str, Any]) -> None:
        self.model = xgb.train(params, dtrain)

    def predict(self, dtest: xgb.DMatrix) -> np.ndarray:
        return self.model.predict(dtest)

    def save_model(self, filepath: str) -> None:
        self.model.save_model(filepath)

    def load_model(self, filepath: str) -> None:
        self.model = xgb.Booster()
        self.model.load_model(filepath)
    
    def prepare_data(self, features: pd.DataFrame, target: np.ndarray) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
        # Example split: 80% training, 20% testing
        split_idx = int(len(features) * 0.8)
        X_train, y_train = features[:split_idx], target[:split_idx]
        X_test, y_test = features[split_idx:], target[split_idx:]
        print("[MLModel] Data prepared for training and testing.")
        return (X_train, y_train), (X_test, y_test)
