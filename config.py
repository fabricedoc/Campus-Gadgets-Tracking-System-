import os
from datetime import datetime

class Config:
    # Database
    DATABASE_PATH = "campus_gadgets.db"
    BACKUP_DIR = "backups"
    
    # Web Server
    WEB_HOST = "0.0.0.0"
    WEB_PORT = 8080
    DEBUG = False
    
    # File Uploads
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    UPLOAD_FOLDER = "web_uploads"
    
    # Security
    SESSION_TIMEOUT = 3600  # 1 hour
    PASSWORD_MIN_LENGTH = 6
    
    # Backups
    AUTO_BACKUP = True
    BACKUP_INTERVAL_HOURS = 24
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "campus_system.log"

def setup_directories():
    """Create necessary directories"""
    directories = [
        Config.BACKUP_DIR,
        Config.UPLOAD_FOLDER,
        "student_photos",
        "reports",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def create_backup():
    """Create database backup"""
    if not Config.AUTO_BACKUP:
        return
    
    try:
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{Config.BACKUP_DIR}/backup_{timestamp}.db"
        
        if os.path.exists(Config.DATABASE_PATH):
            shutil.copy2(Config.DATABASE_PATH, backup_file)
            print(f"✅ Backup created: {backup_file}")
            
            # Clean old backups (keep last 7 days)
            clean_old_backups()
            
    except Exception as e:
        print(f"❌ Backup failed: {e}")

def clean_old_backups():
    """Remove backups older than 7 days"""
    try:
        import time
        current_time = time.time()
        seven_days_ago = current_time - (7 * 24 * 60 * 60)
        
        for filename in os.listdir(Config.BACKUP_DIR):
            if filename.startswith("backup_") and filename.endswith(".db"):
                filepath = os.path.join(Config.BACKUP_DIR, filename)
                if os.path.getctime(filepath) < seven_days_ago:
                    os.remove(filepath)
                    print(f"🧹 Removed old backup: {filename}")
                    
    except Exception as e:
        print(f"❌ Backup cleanup failed: {e}")