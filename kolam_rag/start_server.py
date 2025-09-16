"""
Startup script for Smart Kolam RAG WebSocket Server
Easy way to launch the real-time conversational interface
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    # Map package names to their actual import names
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'websockets': 'websockets',
        'pydantic': 'pydantic',
        'torch': 'torch',
        'sentence_transformers': 'sentence_transformers',
        'faiss-cpu': 'faiss',  # faiss-cpu package imports as 'faiss'
        'trafilatura': 'trafilatura',
        'langchain': 'langchain'
    }
    
    missing_packages = []
    
    logger.info("🔍 Checking dependencies...")
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            logger.info(f"  ✅ {package_name} ({import_name}) - OK")
        except ImportError as e:
            logger.error(f"  ❌ {package_name} ({import_name}) - MISSING: {str(e)}")
            missing_packages.append(package_name)
        except Exception as e:
            logger.error(f"  ⚠️  {package_name} ({import_name}) - ERROR: {str(e)}")
            missing_packages.append(package_name)
    
    if missing_packages:
        logger.error(f"❌ Missing required packages: {', '.join(missing_packages)}")
        logger.info("💡 Install them with:")
        logger.info(f"   pip install {' '.join(missing_packages)}")
        logger.info("   OR")
        logger.info("   pip install -r requirements.txt")
        return False
    
    logger.info("✅ All required dependencies are installed")
    return True

def start_server(host="0.0.0.0", port=8000, reload=True):
    """Start the FastAPI WebSocket server"""
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    if not (current_dir / "smart_kolam_rag.py").exists():
        logger.error("❌ smart_kolam_rag.py not found in current directory")
        logger.info("💡 Please run this script from the kolam_rag directory")
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    logger.info("🚀 Starting Smart Kolam RAG WebSocket Server...")
    logger.info(f"🌐 Server will be available at: http://{host}:{port}")
    logger.info(f"💬 Chat interface: http://localhost:{port}")
    logger.info(f"🔧 API docs: http://localhost:{port}/docs")
    logger.info(f"❤️ Health check: http://localhost:{port}/health")
    
    try:
        # Start the server using uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "smart_kolam_rag:app",  # Fixed: changed from websocket_server to smart_kolam_rag
            "--host", host,
            "--port", str(port),
            "--log-level", "info"
        ]
        
        if reload:
            cmd.append("--reload")
        
        logger.info("🎯 Starting server with command: " + " ".join(cmd))
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        logger.info("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to start server: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main function with command line argument parsing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Start Smart Kolam RAG WebSocket Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to (default: 8000)")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    
    args = parser.parse_args()
    
    print("🎨 SMART KOLAM RAG WEBSOCKET SERVER")
    print("=" * 50)
    
    success = start_server(
        host=args.host,
        port=args.port,
        reload=not args.no_reload
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()