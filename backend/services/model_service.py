"""
Model Service for loading and running inference with XGBoost model.
"""

import logging
from pathlib import Path
from typing import Optional

import numpy as np
import xgboost as xgb

from config import MODEL_PATH, MODEL_VERSION

logger = logging.getLogger(__name__)


class ModelService:
    """Service for managing the XGBoost outbreak prediction model."""
    
    def __init__(self):
        self.model: Optional[xgb.Booster] = None
        self.model_version: str = MODEL_VERSION
        self.is_loaded: bool = False
    
    def load_model(self) -> bool:
        """
        Load the XGBoost booster model from disk.
        
        Returns:
            bool: True if model loaded successfully, False otherwise.
        """
        try:
            model_path = Path(MODEL_PATH)
            
            if not model_path.exists():
                logger.warning(
                    f"Model file not found at {model_path}. "
                    "Please place your trained model at this location."
                )
                return False
            
            self.model = xgb.Booster()
            self.model.load_model(str(model_path))
            self.is_loaded = True
            
            logger.info(f"Model loaded successfully from {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.is_loaded = False
            return False
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """
        Run prediction on input features.
        
        Args:
            features: Input feature array of shape (n_samples, n_features)
        
        Returns:
            np.ndarray: Raw log predictions from the model.
        
        Raises:
            RuntimeError: If model is not loaded.
        """
        if not self.is_loaded or self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Create DMatrix for XGBoost
        dmatrix = xgb.DMatrix(features)
        
        # Assign feature names to match model expectation
        from config import FEATURE_ORDER
        dmatrix.feature_names = FEATURE_ORDER
        
        # Get predictions (log-transformed)
        predictions = self.model.predict(dmatrix)
        
        return predictions
    
    def get_model_info(self) -> dict:
        """Get model metadata."""
        return {
            "version": self.model_version,
            "is_loaded": self.is_loaded,
            "model_path": str(MODEL_PATH),
        }
