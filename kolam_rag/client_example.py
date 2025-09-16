"""
Python WebSocket Client Example for Smart Kolam RAG
Demonstrates how to connect and interact with the WebSocket server programmatically
"""

import asyncio
import json
import websockets
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KolamRAGClient:
    """WebSocket client for Smart Kolam RAG system"""
    
    def __init__(self, server_url="ws://localhost:8000"):
        self.server_url = server_url
        self.client_id = f"python_client_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.websocket = None
        self.running = False
    
    async def connect(self):
        """Connect to the WebSocket server"""
        try:
            ws_url = f"{self.server_url}/ws/{self.client_id}"
            logger.info(f"🔌 Connecting to {ws_url}")
            
            self.websocket = await websockets.connect(ws_url)
            self.running = True
            logger.info("✅ Connected to Smart Kolam RAG server")
            
            # Start listening for messages
            await self.listen_for_messages()
            
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            raise
    
    async def listen_for_messages(self):
        """Listen for incoming messages from the server"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self.handle_message(data)
        except websockets.exceptions.ConnectionClosed:
            logger.info("🔌 Connection closed")
            self.running = False
        except Exception as e:
            logger.error(f"❌ Error listening for messages: {e}")
            self.running = False
    
    async def handle_message(self, data):
        """Handle incoming messages from the server"""
        message_type = data.get("type", "unknown")
        
        if message_type == "system":
            logger.info(f"🎨 System: {data['message']}")
        elif message_type == "answer":
            logger.info(f"🤖 Answer: {data['answer']}")
            logger.info(f"📊 Confidence: {data['confidence']:.3f}, Time: {data['processing_time']:.2f}s")
        elif message_type == "typing":
            logger.info(f"⏳ {data['message']}")
        elif message_type == "error":
            logger.error(f"❌ Error: {data['message']}")
        elif message_type == "stats":
            logger.info(f"📈 Stats: {data}")
        elif message_type == "pong":
            logger.debug("🏓 Pong received")
        else:
            logger.info(f"📨 Unknown message type: {message_type}")
    
    async def send_query(self, query, include_metadata=False):
        """Send a query to the server"""
        if not self.websocket or not self.running:
            logger.error("❌ Not connected to server")
            return
        
        message = {
            "type": "query",
            "query": query,
            "include_metadata": include_metadata
        }
        
        logger.info(f"📤 Sending query: {query}")
        await self.websocket.send(json.dumps(message))
    
    async def send_ping(self):
        """Send a ping to check connection"""
        if not self.websocket or not self.running:
            return
        
        message = {"type": "ping"}
        await self.websocket.send(json.dumps(message))
    
    async def request_stats(self):
        """Request server statistics"""
        if not self.websocket or not self.running:
            return
        
        message = {"type": "stats"}
        await self.websocket.send(json.dumps(message))
    
    async def close(self):
        """Close the WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
            self.running = False
            logger.info("🔌 Connection closed")

async def interactive_client():
    """Interactive client for testing"""
    client = KolamRAGClient()
    
    try:
        # Connect to server
        await client.connect()
        
    except KeyboardInterrupt:
        logger.info("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"❌ Client error: {e}")
    finally:
        await client.close()

async def automated_demo():
    """Automated demo with predefined queries"""
    client = KolamRAGClient()
    
    # Demo queries
    demo_queries = [
        "What is Kolam?",
        "What are the benefits of drawing Kolam?",
        "How to draw Pulli Kolam?",
        "What materials are used for Kolam?",
        "கோலம் என்றால் என்ன?",  # Tamil query
    ]
    
    try:
        # Connect to server
        logger.info("🚀 Starting automated demo...")
        
        # Create connection task
        connection_task = asyncio.create_task(client.connect())
        
        # Wait a bit for connection to establish
        await asyncio.sleep(2)
        
        if not client.running:
            logger.error("❌ Failed to connect")
            return
        
        # Send demo queries
        for i, query in enumerate(demo_queries, 1):
            logger.info(f"\n📝 Demo Query {i}/{len(demo_queries)}")
            await client.send_query(query, include_metadata=True)
            await asyncio.sleep(3)  # Wait for response
        
        # Request statistics
        logger.info("\n📊 Requesting server statistics...")
        await client.request_stats()
        await asyncio.sleep(2)
        
        # Keep connection alive for a bit more
        await asyncio.sleep(5)
        
    except KeyboardInterrupt:
        logger.info("\n👋 Demo interrupted")
    except Exception as e:
        logger.error(f"❌ Demo error: {e}")
    finally:
        await client.close()

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Smart Kolam RAG WebSocket Client")
    parser.add_argument("--mode", choices=["interactive", "demo"], default="demo",
                       help="Client mode (default: demo)")
    parser.add_argument("--server", default="ws://localhost:8000",
                       help="WebSocket server URL (default: ws://localhost:8000)")
    
    args = parser.parse_args()
    
    print("🎨 SMART KOLAM RAG CLIENT")
    print("=" * 50)
    
    if args.mode == "interactive":
        logger.info("🎯 Starting interactive client...")
        asyncio.run(interactive_client())
    else:
        logger.info("🎯 Starting automated demo...")
        asyncio.run(automated_demo())

if __name__ == "__main__":
    main()
