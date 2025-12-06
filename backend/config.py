"""
Configuration module for the Outbreak Prediction System.
Contains feature ordering, district definitions, and simulation parameters.
"""

import os
from pathlib import Path

# Model Configuration
MODEL_PATH = Path(__file__).parent / "model" / "xgb_log_target.model"
MODEL_VERSION = "xgb_log_target"
REFRESH_INTERVAL = 10  # seconds

# Districts for simulation
DISTRICTS = [
    "ballari",
    "bengaluru_urban",
    "bengaluru_rural",
    "mysuru",
    "mangaluru",
    "hubli_dharwad",
    "belagavi",
    "kalaburagi",
    "davangere",
    "shivamogga"
]

# Feature order - MUST match the exact order used during model training
FEATURE_ORDER = [
    "weekly_avg_temp",
    "weekly_avg_humidity",
    "weekly_avg_precipitation",
    "prev_avg_temp",
    "prev_avg_humidity",
    "prev_avg_precipitation",
    "No. of Cases_lag_1",
    "No. of Cases_lag_2",
    "cases_roll2",
    "Number of households",
    "Population",
    "Area",
    "Population density",
    "Population of children b/w (0-4) age",
    "Population of children b/w (5-9) age",
    "literacy rate",
    "E_coli",
    "Total_Coliform",
    "Population living in households with an improved drinking-water source (%)",
    "Population living in households that use an improved sanitation facility (%)",
    "Households using clean fuel for cooking (%)",
    "Households with access to electricity (%)",
    "Households using iodized salt (%)",
    "Prevalence of diarrhoea in the last 2 weeks (children under 5) (%)",
    "Children with diarrhoea who received ORS (%)",
    "Children with diarrhoea who received zinc (%)",
    "Children with diarrhoea taken to a health facility (%)",
    "Disease_Acute Diarrheal Disease",
    "Disease_Acute Diarrheal Diseases",
    "Disease_Acute Gastroenteritis",
    "Disease_Chickenpox",
    "Disease_Chikungunya",
    "Disease_Cholera",
    "Disease_Dengue",
    "Disease_Fever",
    "Disease_Food Poisoning",
    "Disease_Hand Foot Mouth Disease (HFMD)",
    "Disease_Hepatitis A",
    "Disease_Human Rabies",
    "Disease_Japanese Encephalitis",
    "Disease_Kyasanur Forest Disease",
    "Disease_Leptospirosis",
    "Disease_Malaria",
    "Disease_Measles",
    "Disease_Mumps",
    "Disease_Typhoid",
    "Disease_Zika Virus",
    "Disease_nan"
]

# Simulation ranges for realistic data generation
SIMULATION_RANGES = {
    # Weather ranges
    "prev_avg_temp": (15.0, 40.0),
    "prev_avg_precipitation": (0.0, 50.0),
    "prev_avg_humidity": (30.0, 95.0),
    "weekly_avg_temp": (15.0, 40.0),
    "weekly_avg_humidity": (30.0, 95.0),
    "weekly_avg_precipitation": (0.0, 50.0),
    
    # Lag features - initial ranges (will be updated based on predictions)
    "No. of Cases_lag_1": (0, 100),
    "No. of Cases_lag_2": (0, 100),
    "cases_roll2": (0, 100),
    
    # Demographic features
    "Number of households": (50000, 500000),
    "Population": (200000, 2000000),
    "Area": (500, 5000),  # sq km
    "Population density": (100, 2000),  # per sq km
    "Population of children b/w (0-4) age": (10000, 100000),
    "Population of children b/w (5-9) age": (10000, 100000),
    "literacy rate": (60.0, 95.0),
    
    # Water quality indicators
    "E_coli": (0, 1000),  # CFU/100ml
    "Total_Coliform": (0, 5000),  # CFU/100ml
    
    # WASH indicators (percentages)
    "Population living in households with an improved drinking-water source (%)": (50.0, 99.0),
    "Population living in households that use an improved sanitation facility (%)": (40.0, 95.0),
    "Households using clean fuel for cooking (%)": (20.0, 80.0),
    "Households with access to electricity (%)": (70.0, 99.0),
    "Households using iodized salt (%)": (60.0, 95.0),
    
    # Health indicators (percentages)
    "Prevalence of diarrhoea in the last 2 weeks (children under 5) (%)": (2.0, 15.0),
    "Children with diarrhoea who received ORS (%)": (40.0, 90.0),
    "Children with diarrhoea who received zinc (%)": (10.0, 50.0),
    "Children with diarrhoea taken to a health facility (%)": (50.0, 90.0),
}

# Disease frequency distribution (for realistic one-hot selection)
DISEASE_FREQUENCIES = {
    "Disease_nan": 0.05,
    "Disease_Cholera": 0.05,
    "Disease_Acute Diarrheal Disease": 0.20,
    "Disease_Food Poisoning": 0.10,
    "Disease_Human Rabies": 0.01,
    "Disease_Dengue": 0.10,
    "Disease_Zika Virus": 0.02,
    "Disease_Kyasanur Forest Disease": 0.02,
    "Disease_Acute Diarrheal Diseases": 0.05,
    "Disease_Acute Gastroenteritis": 0.05,
    "Disease_Chickenpox": 0.05,
    "Disease_Chikungunya": 0.05,
    "Disease_Fever": 0.05,
    "Disease_Hand Foot Mouth Disease (HFMD)": 0.02,
    "Disease_Hepatitis A": 0.02,
    "Disease_Japanese Encephalitis": 0.02,
    "Disease_Leptospirosis": 0.02,
    "Disease_Malaria": 0.05,
    "Disease_Measles": 0.02,
    "Disease_Mumps": 0.02,
    "Disease_Typhoid": 0.05,
}

# Outbreak thresholds
OUTBREAK_CASE_THRESHOLD = 10  # Cases above this trigger outbreak flag
OUTBREAK_PROB_THRESHOLD = 0.6  # Probability threshold for alerts
