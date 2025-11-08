# repair_web_table.py
import sqlite3

def repair_web_table():
    db_path = "campus_gadgets.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 REPAIRING WEB_REGISTRATIONS TABLE")
    print("=" * 50)
    
    # Check current structure
    cursor.execute("PRAGMA table_info(web_registrations)")
    current_columns = cursor.fetchall()
    
    print("📋 Current table structure:")
    for col in current_columns:
        print(f"   {col[1]:20} {col[2]:15} {'PK' if col[5] else ''}")
    
    # Define the complete table structure we need
    required_columns = [
        ('id', 'INTEGER PRIMARY KEY'),
        ('student_name', 'TEXT NOT NULL'),
        ('registration_number', 'TEXT NOT NULL'),
        ('national_id', 'TEXT'),
        ('gadget_type', 'TEXT NOT NULL'),
        ('brand', 'TEXT NOT NULL'),
        ('model', 'TEXT NOT NULL'),
        ('serial_number', 'TEXT UNIQUE NOT NULL'),
        ('color', 'TEXT'),
        ('additional_details', 'TEXT'),
        ('gadget_photo', 'TEXT'),
        ('passport_photo', 'TEXT'),
        ('student_card_photo', 'TEXT'),
        ('record_number', 'TEXT'),
        ('created_at', 'TIMESTAMP'),
        ('status', 'TEXT')
    ]
    
    # Create new table with correct structure
    print("\n🔄 Creating new table structure...")
    
    # Backup existing data
    cursor.execute("DROP TABLE IF EXISTS web_registrations_backup")
    cursor.execute("CREATE TABLE web_registrations_backup AS SELECT * FROM web_registrations")
    
    # Drop and recreate the table
    cursor.execute("DROP TABLE IF EXISTS web_registrations")
    
    # Build CREATE TABLE statement
    column_defs = [f"{name} {type_}" for name, type_ in required_columns]
    create_sql = f"CREATE TABLE web_registrations ({', '.join(column_defs)})"
    cursor.execute(create_sql)
    
    print("✅ New table created with correct structure")
    
    # Show final structure
    cursor.execute("PRAGMA table_info(web_registrations)")
    final_columns = cursor.fetchall()
    
    print("\n📋 Final table structure:")
    for col in final_columns:
        print(f"   {col[1]:20} {col[2]:15} {'PK' if col[5] else ''}")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Table repair completed!")
    print("💡 Restart your application and try loading web registrations again")

if __name__ == "__main__":
    repair_web_table()