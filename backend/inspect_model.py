
import xgboost as xgb
from config import MODEL_PATH
import json

try:
    model = xgb.Booster()
    model.load_model(str(MODEL_PATH))
    print("Model loaded successfully.")
    features = model.feature_names
    with open("features.json", "w", encoding="utf-8") as f:
        json.dump(features, f, indent=2)
    print("Features written to features.json")
except Exception as e:
    print(f"Error inspecting model: {e}")
