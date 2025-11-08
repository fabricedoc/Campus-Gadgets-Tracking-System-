import sqlite3
import os
import time

def migrate_database():
    db_path = "campus_gadgets.db"
    
    if not os.path.exists(db_path):
        print("Database file not found. No migration needed.")
        return True
    
    # Try multiple times in case of lock
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            conn = sqlite3.connect(db_path, timeout=10.0)
            conn.execute("PRAGMA busy_timeout = 5000")  # 5 second timeout
            cursor = conn.cursor()
            
            print(f"Attempt {attempt + 1}/{max_attempts} to migrate database...")
            
            # Check if new columns already exist
            cursor.execute("PRAGMA table_info(gadgets)")
            columns = [column[1] for column in cursor.fetchall()]
            
            changes_made = False
            
            # Add missing columns
            if 'color' not in columns:
                print("Adding 'color' column to gadgets table...")
                cursor.execute("ALTER TABLE gadgets ADD COLUMN color TEXT")
                changes_made = True
            
            if 'additional_details' not in columns:
                print("Adding 'additional_details' column to gadgets table...")
                cursor.execute("ALTER TABLE gadgets ADD COLUMN additional_details TEXT")
                changes_made = True
            
            if 'passport_photo' not in columns:
                print("Adding 'passport_photo' column to gadgets table...")
                cursor.execute("ALTER TABLE gadgets ADD COLUMN passport_photo TEXT")
                changes_made = True
            
            if 'student_card_photo' not in columns:
                print("Adding 'student_card_photo' column to gadgets table...")
                cursor.execute("ALTER TABLE gadgets ADD COLUMN student_card_photo TEXT")
                changes_made = True
            
            if 'gadget_photo' not in columns:
                print("Adding 'gadget_photo' column to gadgets table...")
                cursor.execute("ALTER TABLE gadgets ADD COLUMN gadget_photo TEXT")
                changes_made = True
            
            if changes_made:
                conn.commit()
                print("✅ Database migration completed successfully!")
            else:
                print("✅ Database is already up to date!")
            
            conn.close()
            return True
            
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                print(f"Database is locked. Retrying in 2 seconds... (Attempt {attempt + 1}/{max_attempts})")
                time.sleep(2)
            else:
                print(f"❌ Migration failed: {e}")
                return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    print("❌ Failed to migrate database after multiple attempts.")
    print("Please make sure the application is completely closed and try again.")
    return False

def check_database_status():
    db_path = "campus_gadgets.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file does not exist.")
        return False
    
    try:
        # Try to create a backup copy to check if file is locked
        import shutil
        temp_backup = db_path + ".backup_test"
        shutil.copy2(db_path, temp_backup)
        os.remove(temp_backup)
        print("✅ Database file is accessible and not locked.")
        return True
    except Exception as e:
        print(f"❌ Database file is locked or inaccessible: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Database Migration Tool")
    print("=" * 40)
    
    # First check if database is accessible
    if check_database_status():
        print("\nStarting migration...")
        migrate_database()
    else:
        print("\nPlease close the main application and try again.")
        
    input("\nPress Enter to exit...")