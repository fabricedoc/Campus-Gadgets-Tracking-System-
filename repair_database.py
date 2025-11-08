# Create a file called repair_database.py
import sqlite3

def repair_database():
    db_path = "campus_gadgets.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 REPAIRING DATABASE...")
    
    # Check for duplicate IDs
    cursor.execute('''
        SELECT id, COUNT(*) as count 
        FROM web_registrations 
        GROUP BY id 
        HAVING count > 1
    ''')
    duplicates = cursor.fetchall()
    
    if duplicates:
        print("❌ Found duplicate IDs:")
        for dup in duplicates:
            print(f"   ID {dup[0]} appears {dup[1]} times")
        
        # Fix duplicates by recreating the table
        print("🔄 Recreating web_registrations table...")
        
        # Backup current data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS web_registrations_backup AS 
            SELECT * FROM web_registrations
        ''')
        
        # Drop and recreate the table
        cursor.execute("DROP TABLE IF EXISTS web_registrations")
        cursor.execute('''
            CREATE TABLE web_registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                registration_number TEXT NOT NULL,
                national_id TEXT NOT NULL,
                gadget_type TEXT NOT NULL,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                serial_number TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Restore data (this will assign new IDs)
        cursor.execute('''
            INSERT INTO web_registrations 
            (student_name, registration_number, national_id, gadget_type, brand, model, serial_number, status)
            SELECT student_name, registration_number, national_id, gadget_type, brand, model, serial_number, status
            FROM web_registrations_backup
        ''')
        
        cursor.execute("DROP TABLE web_registrations_backup")
        print("✅ Database repaired - duplicate IDs removed")
    else:
        print("✅ No duplicate IDs found")
    
    conn.commit()
    
    # Show current state
    cursor.execute("SELECT id, student_name, status FROM web_registrations ORDER BY id")
    records = cursor.fetchall()
    
    print(f"\n📊 Current records after repair:")
    for record in records:
        print(f"   ID: {record[0]}, Student: {record[1]}, Status: {record[2]}")
    
    conn.close()
    print("🎉 Database repair completed!")

if __name__ == "__main__":
    repair_database()