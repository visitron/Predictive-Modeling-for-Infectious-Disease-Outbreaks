"""
FastAPI Application for Real-Time Outbreak Prediction System.
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from config import FEATURE_ORDER, MODEL_VERSION, REFRESH_INTERVAL
from services import ModelService, SimulationService, PredictionService, WebSocketManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize services
model_service = ModelService()
simulation_service = SimulationService()
prediction_service = PredictionService(model_service, simulation_service)
websocket_manager = WebSocketManager()

# Background task reference
background_task = None


async def prediction_loop():
    """Background task that runs predictions every REFRESH_INTERVAL seconds."""
    logger.info(f"Starting prediction loop (interval: {REFRESH_INTERVAL}s)")
    
    while True:
        try:
            # Generate batch predictions
            batch = prediction_service.predict_batch()
            
            # Broadcast to all connected clients
            await websocket_manager.broadcast(batch)
            
            outbreak_count = sum(1 for item in batch["items"] if item["outbreak_flag"])
            logger.info(
                f"Broadcast batch: {len(batch['items'])} predictions, "
                f"{outbreak_count} outbreaks, "
                f"{websocket_manager.get_connection_count()} clients"
            )
            
        except Exception as e:
            logger.error(f"Error in prediction loop: {e}")
        
        await asyncio.sleep(REFRESH_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    global background_task
    
    # Startup
    logger.info("Starting Outbreak Prediction System...")
    
    # Load model
    if model_service.load_model():
        logger.info("Model loaded successfully")
    else:
        logger.warning(
            "Model not loaded - predictions will use simulation fallback. "
            "Place your model at: backend/model/xgb_log_target.model"
        )
    
    # Start background prediction loop
    background_task = asyncio.create_task(prediction_loop())
    
    yield
    
    # Shutdown
    logger.info("Shutting down Outbreak Prediction System...")
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass


# Create FastAPI app
app = FastAPI(
    title="Outbreak Prediction System",
    description="Real-time outbreak prediction using XGBoost model",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Outbreak Prediction System",
        "version": "1.0.0",
        "endpoints": {
            "metadata": "/metadata",
            "websocket": "/ws",
        }
    }


@app.get("/metadata")
async def get_metadata():
    """
    Get model metadata and configuration.
    
    Returns feature list, model version, and refresh interval.
    """
    return {
        "feature_list": FEATURE_ORDER,
        "model_version": MODEL_VERSION,
        "refresh_interval": REFRESH_INTERVAL,
        "model_loaded": model_service.is_loaded,
        "districts": simulation_service.get_districts(),
        "active_connections": websocket_manager.get_connection_count(),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model_service.is_loaded,
        "active_connections": websocket_manager.get_connection_count(),
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time prediction updates.
    
    Clients connect here to receive batch predictions every REFRESH_INTERVAL seconds.
    """
    await websocket_manager.connect(websocket)
    
    try:
        # Send initial welcome message
        await websocket_manager.send_personal_message(
            websocket,
            {
                "type": "connection_established",
                "message": "Connected to Outbreak Prediction System",
                "refresh_interval": REFRESH_INTERVAL,
            }
        )
        
        # Keep connection alive
        while True:
            try:
                # Wait for any client messages (ping/pong, etc.)
                data = await websocket.receive_text()
                
                # Handle client messages if needed
                if data == "ping":
                    await websocket_manager.send_personal_message(
                        websocket,
                        {"type": "pong"}
                    )
                    
            except WebSocketDisconnect:
                break
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        websocket_manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
