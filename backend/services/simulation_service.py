"""
Simulation Service for generating synthetic real-time medical/weather/WASH data.
"""

import random
from typing import Dict, List, Any
from collections import defaultdict

from config import (
    DISTRICTS,
    FEATURE_ORDER,
    SIMULATION_RANGES,
    DISEASE_FREQUENCIES,
)


class SimulationService:
    """Service for generating realistic simulated outbreak data."""
    
    def __init__(self):
        # Maintain lag state for each district
        self._district_states: Dict[str, Dict[str, float]] = defaultdict(
            lambda: {
                "No. of Cases_lag_1": random.uniform(0, 50),
                "No. of Cases_lag_2": random.uniform(0, 50),
                "cases_roll2": random.uniform(0, 50),
                "last_predicted_cases": random.uniform(0, 30),
            }
        )
        
        # Initialize states for all districts
        for district in DISTRICTS:
            _ = self._district_states[district]
    
    def generate_features(self, district: str) -> Dict[str, Any]:
        """
        Generate simulated feature values for a district.
        
        Args:
            district: Name of the district.
        
        Returns:
            Dict containing all feature values in the expected format.
        """
        features = {}
        state = self._district_states[district]
        
        # Generate weather features with some temporal correlation
        features["prev_avg_temp"] = self._random_in_range("prev_avg_temp")
        features["prev_avg_precipitation"] = self._random_in_range("prev_avg_precipitation")
        features["prev_avg_humidity"] = self._random_in_range("prev_avg_humidity")
        
        # Weekly averages correlate with previous values
        features["weekly_avg_temp"] = features["prev_avg_temp"] + random.uniform(-3, 3)
        features["weekly_avg_temp"] = max(15, min(40, features["weekly_avg_temp"]))
        
        features["weekly_avg_humidity"] = features["prev_avg_humidity"] + random.uniform(-5, 5)
        features["weekly_avg_humidity"] = max(30, min(95, features["weekly_avg_humidity"]))
        
        features["weekly_avg_precipitation"] = features["prev_avg_precipitation"] + random.uniform(-5, 5)
        features["weekly_avg_precipitation"] = max(0, min(50, features["weekly_avg_precipitation"]))
        
        # Lag features from state (evolve based on predictions)
        features["No. of Cases_lag_1"] = state["No. of Cases_lag_1"]
        features["No. of Cases_lag_2"] = state["No. of Cases_lag_2"]
        features["cases_roll2"] = state["cases_roll2"]
        
        # Demographic features (relatively stable per district)
        features["Number of households"] = self._random_in_range("Number of households")
        features["Population"] = self._random_in_range("Population")
        features["Area"] = self._random_in_range("Area")
        features["Population density"] = features["Population"] / features["Area"]
        features["Population of children b/w (0-4) age"] = self._random_in_range(
            "Population of children b/w (0-4) age"
        )
        features["Population of children b/w (5-9) age"] = self._random_in_range(
            "Population of children b/w (5-9) age"
        )
        features["literacy rate"] = self._random_in_range("literacy rate")
        
        # Water quality indicators
        features["E_coli"] = self._random_in_range("E_coli")
        features["Total_Coliform"] = self._random_in_range("Total_Coliform")
        
        # WASH indicators
        features["Population living in households with an improved drinking-water source (%)"] = (
            self._random_in_range("Population living in households with an improved drinking-water source (%)")
        )
        features["Population living in households that use an improved sanitation facility (%)"] = (
            self._random_in_range("Population living in households that use an improved sanitation facility (%)")
        )
        features["Households using clean fuel for cooking (%)"] = self._random_in_range(
            "Households using clean fuel for cooking (%)"
        )
        features["Households with access to electricity (%)"] = self._random_in_range(
            "Households with access to electricity (%)"
        )
        features["Households using iodized salt (%)"] = self._random_in_range(
            "Households using iodized salt (%)"
        )
        
        # Health indicators
        features["Prevalence of diarrhoea in the last 2 weeks (children under 5) (%)"] = (
            self._random_in_range("Prevalence of diarrhoea in the last 2 weeks (children under 5) (%)")
        )
        features["Children with diarrhoea who received ORS (%)"] = self._random_in_range(
            "Children with diarrhoea who received ORS (%)"
        )
        features["Children with diarrhoea who received zinc (%)"] = self._random_in_range(
            "Children with diarrhoea who received zinc (%)"
        )
        features["Children with diarrhoea taken to a health facility (%)"] = self._random_in_range(
            "Children with diarrhoea taken to a health facility (%)"
        )
        
        # Disease one-hot encoding
        disease_features = self._select_disease()
        features.update(disease_features)
        
        return features
    
    def update_lag_state(self, district: str, predicted_cases: float) -> None:
        """
        Update the lag state for a district after prediction.
        
        Args:
            district: Name of the district.
            predicted_cases: The predicted case count.
        """
        state = self._district_states[district]
        
        # Shift lag values
        state["No. of Cases_lag_2"] = state["No. of Cases_lag_1"]
        state["No. of Cases_lag_1"] = predicted_cases
        
        # Update rolling average
        state["cases_roll2"] = (state["No. of Cases_lag_1"] + state["No. of Cases_lag_2"]) / 2
        state["last_predicted_cases"] = predicted_cases
    
    def get_districts(self) -> List[str]:
        """Get list of all districts."""
        return DISTRICTS.copy()
    
    def _random_in_range(self, feature_name: str) -> float:
        """Generate a random value within the defined range for a feature."""
        if feature_name not in SIMULATION_RANGES:
            return random.uniform(0, 100)
        
        min_val, max_val = SIMULATION_RANGES[feature_name]
        return random.uniform(min_val, max_val)
    
    def _select_disease(self) -> Dict[str, int]:
        """
        Select a disease based on natural frequency distribution.
        Returns one-hot encoded disease features.
        """
        diseases = list(DISEASE_FREQUENCIES.keys())
        probabilities = list(DISEASE_FREQUENCIES.values())
        
        # Normalize probabilities
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        
        # Select one disease
        selected = random.choices(diseases, weights=probabilities, k=1)[0]
        
        # Create one-hot encoding
        disease_features = {disease: 0 for disease in diseases}
        disease_features[selected] = 1
        
        return disease_features
