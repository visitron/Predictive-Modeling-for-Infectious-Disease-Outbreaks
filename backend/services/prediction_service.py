"""
Prediction Service for coordinating model inference and output formatting.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, List
import math

import numpy as np

from config import (
    FEATURE_ORDER,
    OUTBREAK_CASE_THRESHOLD,
    OUTBREAK_PROB_THRESHOLD,
    MODEL_VERSION,
)
from .model_service import ModelService
from .simulation_service import SimulationService

logger = logging.getLogger(__name__)


class PredictionService:
    """Service for running predictions and formatting output."""
    
    def __init__(self, model_service: ModelService, simulation_service: SimulationService):
        self.model_service = model_service
        self.simulation_service = simulation_service
    
    def features_to_vector(self, features: Dict[str, Any]) -> np.ndarray:
        """
        Convert feature dictionary to ordered numpy array.
        
        Args:
            features: Dictionary of feature values.
        
        Returns:
            np.ndarray: Feature vector in correct order.
        """
        vector = []
        for feature_name in FEATURE_ORDER:
            if feature_name not in features:
                logger.warning(f"Missing feature: {feature_name}, using 0.0")
                vector.append(0.0)
            else:
                vector.append(float(features[feature_name]))
        
        return np.array(vector, dtype=np.float32).reshape(1, -1)
    
    def calculate_outbreak_probability(self, predicted_cases: float) -> float:
        """
        Calculate outbreak probability based on predicted cases.
        Uses a sigmoid-like function for smooth probability scaling.
        
        Args:
            predicted_cases: The predicted number of cases.
        
        Returns:
            float: Outbreak probability between 0 and 1.
        """
        # Sigmoid function centered at threshold
        k = 0.2  # Steepness factor
        midpoint = OUTBREAK_CASE_THRESHOLD
        
        prob = 1 / (1 + math.exp(-k * (predicted_cases - midpoint)))
        return round(prob, 3)
    
    def predict_for_district(self, district: str) -> Dict[str, Any]:
        """
        Generate prediction for a single district.
        
        Args:
            district: Name of the district.
        
        Returns:
            Dict containing complete prediction output.
        """
        # Generate simulated features
        features = self.simulation_service.generate_features(district)
        
        # Convert to feature vector
        feature_vector = self.features_to_vector(features)
        
        # Run prediction
        if self.model_service.is_loaded:
            predicted_log = float(self.model_service.predict(feature_vector)[0])
        else:
            # Fallback: simulate prediction when model not available
            predicted_log = self._simulate_prediction(features)
        
        # Convert log prediction to case count
        predicted_cases = math.exp(predicted_log) - 1
        predicted_cases = max(0, predicted_cases)  # Ensure non-negative
        
        # Calculate outbreak metrics
        outbreak_prob = self.calculate_outbreak_probability(predicted_cases)
        outbreak_flag = (
            outbreak_prob > OUTBREAK_PROB_THRESHOLD or 
            predicted_cases > OUTBREAK_CASE_THRESHOLD
        )
        
        # Update lag state for next iteration
        self.simulation_service.update_lag_state(district, predicted_cases)
        
        # Format output
        return {
            "ts": datetime.now(timezone.utc).isoformat(),
            "district": district,
            "predicted_log": round(predicted_log, 3),
            "predicted_cases": round(predicted_cases, 2),
            "predicted_cases_rounded": round(predicted_cases),
            "outbreak_prob": outbreak_prob,
            "outbreak_flag": outbreak_flag,
            "input_features": features,
            "model_version": MODEL_VERSION,
        }
    
    def predict_batch(self) -> Dict[str, Any]:
        """
        Generate predictions for all districts.
        
        Returns:
            Dict containing batch prediction message.
        """
        districts = self.simulation_service.get_districts()
        predictions = []
        
        for district in districts:
            try:
                prediction = self.predict_for_district(district)
                predictions.append(prediction)
            except Exception as e:
                logger.error(f"Error predicting for {district}: {e}")
                continue
        
        return {
            "type": "batch_prediction",
            "items": predictions,
        }
    
    def _simulate_prediction(self, features: Dict[str, Any]) -> float:
        """
        Simulate a prediction when model is not available.
        Uses a simple heuristic based on input features.
        
        Args:
            features: Dictionary of feature values.
        
        Returns:
            float: Simulated log prediction.
        """
        # Base prediction from lag features
        lag1 = features.get("No. of Cases_lag_1", 10)
        lag2 = features.get("No. of Cases_lag_2", 10)
        
        # Weather impact
        humidity = features.get("prev_avg_humidity", 60)
        temp = features.get("prev_avg_temp", 30)
        
        # Sanitation impact (lower sanitation = higher cases)
        sanitation = features.get(
            "Population living in households that use an improved sanitation facility (%)", 
            70
        )
        
        # E.coli impact
        ecoli = features.get("E_coli", 100)
        
        # Simple heuristic formula
        base_cases = (lag1 + lag2) / 2
        weather_factor = 1 + (humidity - 50) / 100 + (temp - 25) / 50
        sanitation_factor = 1 + (100 - sanitation) / 100
        ecoli_factor = 1 + ecoli / 1000
        
        predicted_cases = base_cases * weather_factor * sanitation_factor * ecoli_factor
        predicted_cases = max(1, predicted_cases)  # Ensure positive
        
        # Convert to log
        predicted_log = math.log(predicted_cases + 1)
        
        # Add some noise
        import random
        predicted_log += random.uniform(-0.3, 0.3)
        
        return predicted_log
