from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
import numpy as np

class IModelTrainer(ABC):
    @abstractmethod
    def train_model(self, training_data: Tuple[np.ndarray, np.ndarray], params: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def evaluate_model(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        pass