import waitress as serve
from web_server import app
import logging
import os
import sys
from datetime import datetime

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('campus_system.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('CampusSystem')

def check_directories():
    """Ensure all required directories exist"""
    required_dirs = ['reports', 'student_photos', 'web_uploads', 'backups', 'logs']
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")

def print_startup_banner():
    """Display startup information"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                 CAMPUS GADGET SYSTEM SERVER                 ║
    ║                     Production Ready                        ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🚀 Server starting...
    📍 Local Access: http://localhost:8080
    🌐 Network Access: http://[YOUR-IP]:8080
    ⚡ Server: Waitress (Production WSGI)
    📊 Concurrent connections: Multiple
    📝 Log file: campus_system.log
    🛡️  Running in production mode
    
    ⏹️  Press Ctrl+C to stop the server gracefully
    """
    print(banner)

if __name__ == "__main__":
    try:
        # Check if waitress is installed
        try:
            import waitress
            logger.info("✅ Waitress production server loaded")
        except ImportError as e:
            logger.error("❌ Waitress not installed. Run: pip install waitress")
            sys.exit(1)
        
        # Setup environment
        check_directories()
        print_startup_banner()
        
        startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"🚀 Campus Gadget System starting at {startup_time}")
        logger.info("📍 Server URL: http://0.0.0.0:8080")
        logger.info("⚡ Production mode: Waitress WSGI Server")
        
        # Start Waitress production server
        serve(
            app,
            host='0.0.0.0',      # Listen on all interfaces
            port=8080,           # Port 8080
            threads=4,           # Number of threads
            url_scheme='http'    # URL scheme
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ Server error: {str(e)}")
        print(f"❌ Critical error: {e}")
        sys.exit(1)