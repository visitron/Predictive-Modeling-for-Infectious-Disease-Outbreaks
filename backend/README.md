# Outbreak Prediction System - Backend

Real-time outbreak prediction API using FastAPI, XGBoost, and WebSockets.

## Features

- 🔮 **XGBoost Model Integration**: Loads pre-trained model for outbreak prediction
- 🌐 **WebSocket Broadcasting**: Real-time predictions to all connected clients
- 📊 **Simulated Data Generation**: Realistic medical/weather/WASH data simulation
- 🚨 **Outbreak Detection**: Automatic flagging when thresholds exceeded

## Prerequisites

- Python 3.10+
- pip

## Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Model Setup

Place your trained XGBoost model file at:

```
backend/model/xgb_log_target.model
```

> **Note**: The system will run with simulated predictions if the model file is not present.

## Running the Server

```bash
# Development mode with auto-reload
uvicorn app:app --reload --port 8000

# Production mode
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/metadata` | GET | Feature list, model version, refresh interval |
| `/health` | GET | Health check status |

### WebSocket Endpoint

| Endpoint | Description |
|----------|-------------|
| `/ws` | Real-time prediction updates |

## Configuration

Edit `config.py` to modify:

- `REFRESH_INTERVAL`: Prediction broadcast interval (default: 10 seconds)
- `DISTRICTS`: List of districts to simulate
- `SIMULATION_RANGES`: Value ranges for simulated data
- `OUTBREAK_CASE_THRESHOLD`: Case count threshold for outbreak flag
- `OUTBREAK_PROB_THRESHOLD`: Probability threshold for alerts

## WebSocket Message Format

### Batch Prediction Message

```json
{
  "type": "batch_prediction",
  "items": [
    {
      "ts": "2025-12-05T18:00:00Z",
      "district": "ballari",
      "predicted_log": 2.557,
      "predicted_cases": 11.86,
      "predicted_cases_rounded": 12,
      "outbreak_prob": 0.82,
      "outbreak_flag": true,
      "input_features": {...},
      "model_version": "xgb_log_target"
    }
  ]
}
```

## Project Structure

```
backend/
├── app.py                    # FastAPI application
├── config.py                 # Configuration and feature order
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── model/
│   └── xgb_log_target.model  # XGBoost model (you provide)
└── services/
    ├── __init__.py
    ├── model_service.py      # Model loading and inference
    ├── simulation_service.py # Data simulation
    ├── prediction_service.py # Prediction coordination
    └── websocket_manager.py  # WebSocket client management
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## License

MIT
