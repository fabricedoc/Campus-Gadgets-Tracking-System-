import sqlite3
import hashlib
import os
import sys
from datetime import datetime

class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            # Auto-detect installation path
            if getattr(sys, 'frozen', False):
                # Running as executable
                base_path = os.path.dirname(sys.executable)
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            db_path = os.path.join(base_path, "data", "campus_gadgets.db")
        
        self.db_path = db_path
        self.ensure_directories()
        self.init_database()
        self.update_web_registrations_table()
    
    def ensure_directories(self):
        """Create necessary directories"""
        directories = [
            os.path.dirname(self.db_path),  # data directory
            os.path.join(os.path.dirname(self.db_path), "..", "reports"),
            os.path.join(os.path.dirname(self.db_path), "..", "backups"),
            os.path.join(os.path.dirname(self.db_path), "..", "logs"),
            os.path.join(os.path.dirname(self.db_path), "..", "student_photos"),
            os.path.join(os.path.dirname(self.db_path), "..", "web_uploads"),
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def init_database(self):
        """Initialize database with all tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                department TEXT,
                permissions TEXT,
                status TEXT DEFAULT 'active',
                last_login TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                registration_number TEXT UNIQUE NOT NULL,
                national_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Gadgets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gadgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                record_number TEXT UNIQUE NOT NULL,
                gadget_type TEXT NOT NULL,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                serial_number TEXT UNIQUE NOT NULL,
                color TEXT,
                additional_details TEXT,
                passport_photo TEXT,
                student_card_photo TEXT,
                gadget_photo TEXT,
                web_registered BOOLEAN DEFAULT 0,
                registration_status TEXT DEFAULT 'pending',
                status TEXT DEFAULT 'checked_in',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        # Check records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS check_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gadget_id INTEGER,
                check_in_time TIMESTAMP,
                check_out_time TIMESTAMP,
                status TEXT NOT NULL,
                FOREIGN KEY (gadget_id) REFERENCES gadgets (id)
            )
        ''')
        # Web registrations table (for student-facing web form)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS web_registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                registration_number TEXT NOT NULL,
                national_id TEXT NOT NULL,
                gadget_type TEXT NOT NULL,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                serial_number TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
            # Create default admin user
        self.create_default_user(cursor)
            
        conn.commit()
        conn.close()
            
        print(f"✅ Database initialized: {self.db_path}")
    def update_web_registrations_table(self):
        """Update web_registrations table to match API structure"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check current table structure
            cursor.execute("PRAGMA table_info(web_registrations)")
            current_columns = [col[1] for col in cursor.fetchall()]
            print(f"📋 Current columns: {current_columns}")
            
            # Add missing columns
            missing_columns = []
            
            if 'color' not in current_columns:
                cursor.execute("ALTER TABLE web_registrations ADD COLUMN color TEXT")
                missing_columns.append('color')
            
            if 'additional_details' not in current_columns:
                cursor.execute("ALTER TABLE web_registrations ADD COLUMN additional_details TEXT")
                missing_columns.append('additional_details')
            
            if 'gadget_photo' not in current_columns:
                cursor.execute("ALTER TABLE web_registrations ADD COLUMN gadget_photo TEXT")
                missing_columns.append('gadget_photo')
            
            if 'passport_photo' not in current_columns:
                cursor.execute("ALTER TABLE web_registrations ADD COLUMN passport_photo TEXT")
                missing_columns.append('passport_photo')
            
            if 'student_card_photo' not in current_columns:
                cursor.execute("ALTER TABLE web_registrations ADD COLUMN student_card_photo TEXT")
                missing_columns.append('student_card_photo')
            
            if 'record_number' not in current_columns:
                cursor.execute("ALTER TABLE web_registrations ADD COLUMN record_number TEXT")
                missing_columns.append('record_number')
            
            if missing_columns:
                print(f"✅ Added missing columns: {missing_columns}")
            else:
                print("✅ Table structure is up to date")
            
            conn.commit()
            
        except Exception as e:
            print(f"❌ Error updating table: {str(e)}")
        finally:
            conn.close()
    def create_default_user(self, cursor):
        """Create default admin user"""
        default_password = hashlib.sha256("admin123".encode()).hexdigest()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO users (name, username, password, role, permissions)
                VALUES (?, ?, ?, ?, ?)
            ''', ("Administrator", "admin", default_password, "admin", "all"))
        except:
            pass
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def create_backup(self):
        """Create database backup"""
        try:
            import shutil
            backup_dir = os.path.join(os.path.dirname(self.db_path), "..", "backups")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")
            
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, backup_file)
                return backup_file
        except Exception as e:
            print(f"Backup failed: {e}")
        return None

# Auto-initialize when run directly
if __name__ == "__main__":
    db = Database()
    print("🎉 Campus Gadget System database ready!")