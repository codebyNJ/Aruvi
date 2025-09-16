"""
FastAPI WebSocket Server for Smart Kolam RAG System
Real-time conversational interface for Kolam knowledge queries
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

from smart_kolam_rag import SmartKolamRAG

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Kolam RAG WebSocket API",
    description="Real-time conversational interface for Kolam knowledge queries",
    version="1.0.0"
)

# Global RAG system instance
kolam_rag: Optional[SmartKolamRAG] = None

# Connection manager for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.user_sessions[client_id] = {
            "connected_at": datetime.now(),
            "query_count": 0,
            "last_activity": datetime.now()
        }
        logger.info(f"Client {client_id} connected")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.user_sessions:
            del self.user_sessions[client_id]
        logger.info(f"Client {client_id} disconnected")

    async def send_personal_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")
                self.disconnect(client_id)

    async def broadcast(self, message: dict):
        disconnected_clients = []
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)

    def get_stats(self) -> Dict:
        return {
            "active_connections": len(self.active_connections),
            "total_sessions": len(self.user_sessions),
            "total_queries": sum(session["query_count"] for session in self.user_sessions.values())
        }

manager = ConnectionManager()

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    include_metadata: bool = False
    client_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    query: str
    confidence: float
    processing_time: float
    retrieved_docs: int
    has_tamil_content: bool
    timestamp: str
    client_id: str
    error: Optional[str] = None

# Initialize RAG system on startup
@app.on_event("startup")
async def startup_event():
    global kolam_rag
    try:
        logger.info("🚀 Initializing Smart Kolam RAG System...")
        kolam_rag = SmartKolamRAG(
            chunk_size=400,
            chunk_overlap=100,
            top_k_retrieval=3,
            similarity_threshold=0.1
        )
        
        logger.info("📚 Loading Kolam documentation...")
        kolam_rag.load_kolam_documentation()
        
        stats = kolam_rag.get_kolam_statistics()
        logger.info(f"✅ RAG System initialized with {stats['total_documents']} documents")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG system: {e}")
        raise

# Health check endpoint
@app.get("/health")
async def health_check():
    if kolam_rag is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    stats = kolam_rag.get_kolam_statistics()
    connection_stats = manager.get_stats()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "rag_stats": stats,
        "connection_stats": connection_stats
    }

# REST API endpoint for queries (alternative to WebSocket)
@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    if kolam_rag is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        client_id = request.client_id or str(uuid.uuid4())
        
        # Process query
        result = kolam_rag.smart_query(request.query, request.include_metadata)
        
        response = QueryResponse(
            answer=result['answer'],
            query=result['query'],
            confidence=result['confidence'],
            processing_time=result['processing_time'],
            retrieved_docs=result['retrieved_docs'],
            has_tamil_content=result.get('has_tamil_content', False),
            timestamp=datetime.now().isoformat(),
            client_id=client_id,
            error=result.get('error')
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time conversation
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    
    # Send welcome message
    welcome_message = {
        "type": "system",
        "message": "🎨 Welcome to Smart Kolam RAG! Ask me anything about Kolam traditions, techniques, or cultural significance.",
        "timestamp": datetime.now().isoformat(),
        "client_id": client_id
    }
    await manager.send_personal_message(welcome_message, client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Update session activity
            if client_id in manager.user_sessions:
                manager.user_sessions[client_id]["last_activity"] = datetime.now()
                manager.user_sessions[client_id]["query_count"] += 1
            
            # Process different message types
            if message_data.get("type") == "query":
                await handle_query_message(message_data, client_id)
            elif message_data.get("type") == "ping":
                await handle_ping_message(client_id)
            elif message_data.get("type") == "stats":
                await handle_stats_request(client_id)
            else:
                # Echo unknown message types
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Unknown message type",
                    "timestamp": datetime.now().isoformat(),
                    "client_id": client_id
                }, client_id)
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        await manager.send_personal_message({
            "type": "error",
            "message": f"Server error: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id
        }, client_id)
        manager.disconnect(client_id)

async def handle_query_message(message_data: dict, client_id: str):
    """Handle query messages from WebSocket clients"""
    query = message_data.get("query", "").strip()
    include_metadata = message_data.get("include_metadata", False)
    
    if not query:
        await manager.send_personal_message({
            "type": "error",
            "message": "Please provide a valid query about Kolam",
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id
        }, client_id)
        return
    
    # Send typing indicator
    await manager.send_personal_message({
        "type": "typing",
        "message": "🤔 Thinking...",
        "timestamp": datetime.now().isoformat(),
        "client_id": client_id
    }, client_id)
    
    try:
        # Process query with RAG system
        start_time = time.time()
        result = kolam_rag.smart_query(query, include_metadata)
        
        # Prepare response
        response = {
            "type": "answer",
            "query": query,
            "answer": result['answer'],
            "confidence": result['confidence'],
            "processing_time": result['processing_time'],
            "retrieved_docs": result['retrieved_docs'],
            "has_tamil_content": result.get('has_tamil_content', False),
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id
        }
        
        # Add metadata if requested
        if include_metadata and 'context_snippets' in result:
            response["context_snippets"] = result['context_snippets'][:2]  # Limit for WebSocket
            response["similarity_scores"] = result.get('similarity_scores', [])[:2]
        
        # Add error if present
        if 'error' in result:
            response["error"] = result['error']
        
        await manager.send_personal_message(response, client_id)
        
    except Exception as e:
        logger.error(f"Error processing query for {client_id}: {e}")
        await manager.send_personal_message({
            "type": "error",
            "message": f"Sorry, I encountered an error processing your query: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id
        }, client_id)

async def handle_ping_message(client_id: str):
    """Handle ping messages for connection health check"""
    await manager.send_personal_message({
        "type": "pong",
        "message": "Connection active",
        "timestamp": datetime.now().isoformat(),
        "client_id": client_id
    }, client_id)

async def handle_stats_request(client_id: str):
    """Handle statistics request"""
    try:
        rag_stats = kolam_rag.get_kolam_statistics()
        connection_stats = manager.get_stats()
        user_session = manager.user_sessions.get(client_id, {})
        
        stats_response = {
            "type": "stats",
            "rag_stats": rag_stats,
            "connection_stats": connection_stats,
            "user_session": {
                "query_count": user_session.get("query_count", 0),
                "connected_duration": str(datetime.now() - user_session.get("connected_at", datetime.now()))
            },
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id
        }
        
        await manager.send_personal_message(stats_response, client_id)
        
    except Exception as e:
        logger.error(f"Error getting stats for {client_id}: {e}")
        await manager.send_personal_message({
            "type": "error",
            "message": f"Error retrieving statistics: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id
        }, client_id)

# Serve static files (HTML client)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint serves the HTML client
@app.get("/")
async def get_chat_interface():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Kolam RAG Chat</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
                color: white;
                padding: 20px;
                text-align: center;
            }
            .chat-container {
                height: 500px;
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
            }
            .message {
                margin: 10px 0;
                padding: 12px 16px;
                border-radius: 18px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .user-message {
                background: #007bff;
                color: white;
                margin-left: auto;
                text-align: right;
            }
            .bot-message {
                background: white;
                border: 1px solid #e9ecef;
                margin-right: auto;
            }
            .system-message {
                background: #28a745;
                color: white;
                text-align: center;
                margin: 0 auto;
                font-size: 0.9em;
            }
            .error-message {
                background: #dc3545;
                color: white;
                margin: 0 auto;
            }
            .typing-message {
                background: #6c757d;
                color: white;
                margin-right: auto;
                font-style: italic;
            }
            .input-container {
                padding: 20px;
                border-top: 1px solid #e9ecef;
                background: white;
            }
            .input-group {
                display: flex;
                gap: 10px;
            }
            input[type="text"] {
                flex: 1;
                padding: 12px;
                border: 2px solid #e9ecef;
                border-radius: 25px;
                outline: none;
                font-size: 16px;
            }
            input[type="text"]:focus {
                border-color: #007bff;
            }
            button {
                padding: 12px 24px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                transition: background 0.3s;
            }
            button:hover {
                background: #0056b3;
            }
            button:disabled {
                background: #6c757d;
                cursor: not-allowed;
            }
            .stats {
                font-size: 0.8em;
                color: #6c757d;
                margin-top: 5px;
            }
            .connection-status {
                position: absolute;
                top: 10px;
                right: 10px;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 0.8em;
                font-weight: bold;
            }
            .connected {
                background: #28a745;
                color: white;
            }
            .disconnected {
                background: #dc3545;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎨 Smart Kolam RAG Chat</h1>
                <p>Ask me anything about Kolam traditions, techniques, and cultural significance!</p>
                <div id="connectionStatus" class="connection-status disconnected">Disconnected</div>
            </div>
            <div id="chatContainer" class="chat-container"></div>
            <div class="input-container">
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Ask about Kolam..." maxlength="500">
                    <button id="sendButton" onclick="sendMessage()">Send</button>
                </div>
                <div class="stats">
                    <span id="statsText">Ready to chat!</span>
                </div>
            </div>
        </div>

        <script>
            const clientId = 'client_' + Math.random().toString(36).substr(2, 9);
            let ws = null;
            let messageCount = 0;

            function connectWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/${clientId}`;
                
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function(event) {
                    updateConnectionStatus(true);
                    addMessage('system', '🎨 Connected to Smart Kolam RAG!');
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    handleMessage(data);
                };
                
                ws.onclose = function(event) {
                    updateConnectionStatus(false);
                    addMessage('error', '❌ Connection lost. Attempting to reconnect...');
                    setTimeout(connectWebSocket, 3000);
                };
                
                ws.onerror = function(error) {
                    console.error('WebSocket error:', error);
                    addMessage('error', '❌ Connection error occurred');
                };
            }

            function updateConnectionStatus(connected) {
                const statusEl = document.getElementById('connectionStatus');
                if (connected) {
                    statusEl.textContent = 'Connected';
                    statusEl.className = 'connection-status connected';
                } else {
                    statusEl.textContent = 'Disconnected';
                    statusEl.className = 'connection-status disconnected';
                }
            }

            function handleMessage(data) {
                switch(data.type) {
                    case 'system':
                        addMessage('system', data.message);
                        break;
                    case 'answer':
                        removeTypingMessage();
                        addMessage('bot', data.answer, {
                            confidence: data.confidence,
                            processing_time: data.processing_time,
                            retrieved_docs: data.retrieved_docs
                        });
                        break;
                    case 'typing':
                        addMessage('typing', data.message);
                        break;
                    case 'error':
                        removeTypingMessage();
                        addMessage('error', data.message);
                        break;
                    case 'stats':
                        updateStats(data);
                        break;
                }
            }

            function addMessage(type, content, metadata = null) {
                const chatContainer = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}-message`;
                
                let messageContent = content;
                if (metadata) {
                    messageContent += `<div class="stats">
                        Confidence: ${(metadata.confidence * 100).toFixed(1)}% | 
                        Time: ${metadata.processing_time.toFixed(2)}s | 
                        Sources: ${metadata.retrieved_docs}
                    </div>`;
                }
                
                messageDiv.innerHTML = messageContent;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                if (type === 'typing') {
                    messageDiv.id = 'typingMessage';
                }
            }

            function removeTypingMessage() {
                const typingMsg = document.getElementById('typingMessage');
                if (typingMsg) {
                    typingMsg.remove();
                }
            }

            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message || !ws || ws.readyState !== WebSocket.OPEN) {
                    return;
                }
                
                addMessage('user', message);
                
                ws.send(JSON.stringify({
                    type: 'query',
                    query: message,
                    include_metadata: true
                }));
                
                input.value = '';
                messageCount++;
                updateStats();
            }

            function updateStats(data = null) {
                const statsEl = document.getElementById('statsText');
                if (data && data.user_session) {
                    statsEl.textContent = `Queries: ${data.user_session.query_count} | Active users: ${data.connection_stats.active_connections}`;
                } else {
                    statsEl.textContent = `Messages sent: ${messageCount}`;
                }
            }

            // Event listeners
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Initialize connection
            connectWebSocket();

            // Ping every 30 seconds to keep connection alive
            setInterval(() => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({type: 'ping'}));
                }
            }, 30000);
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    uvicorn.run(
        "websocket_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
