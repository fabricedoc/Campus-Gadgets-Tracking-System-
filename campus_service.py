import time
import threading
from production_server import serve_app
from config import create_backup, Config
import schedule

def run_scheduler():
    """Run scheduled tasks"""
    schedule.every(24).hours.do(create_backup)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    print("🏫 Campus Gadget System Service Starting...")
    
    # Setup directories
    from config import setup_directories
    setup_directories()
    
    # Create initial backup
    create_backup()
    
    # Start scheduler in background
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Start web server
    print("🌐 Starting web server...")
    serve_app()

if __name__ == "__main__":
    main()