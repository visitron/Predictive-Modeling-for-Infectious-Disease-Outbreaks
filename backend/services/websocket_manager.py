"""
WebSocket Manager for handling real-time client connections.
"""

import logging
import json
from typing import List, Dict, Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manager for WebSocket client connections and broadcasting."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket) -> None:
        """
        Accept a new WebSocket connection.
        
        Args:
            websocket: The WebSocket connection to accept.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket) -> None:
        """
        Remove a WebSocket connection.
        
        Args:
            websocket: The WebSocket connection to remove.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: Dict[str, Any]) -> None:
        """
        Broadcast a message to all connected clients.
        
        Args:
            message: The message data to broadcast.
        """
        if not self.active_connections:
            logger.debug("No active connections to broadcast to")
            return
        
        message_json = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.warning(f"Failed to send to client: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def send_personal_message(self, websocket: WebSocket, message: Dict[str, Any]) -> None:
        """
        Send a message to a specific client.
        
        Args:
            websocket: The WebSocket connection to send to.
            message: The message data to send.
        """
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.warning(f"Failed to send personal message: {e}")
            self.disconnect(websocket)
    
    def get_connection_count(self) -> int:
        """Get the number of active connections."""
        return len(self.active_connections)
