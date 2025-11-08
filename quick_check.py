import sqlite3

def quick_check():
    db_path = "campus_gadgets.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 QUICK WEB REGISTRATIONS CHECK")
        print("=" * 50)
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='web_registrations'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ web_registrations table does not exist!")
            return
        
        print("✅ web_registrations table exists")
        
        # Check records and status
        cursor.execute("SELECT id, student_name, status FROM web_registrations")
        records = cursor.fetchall()
        
        print(f"📊 Found {len(records)} records:")
        for record in records:
            print(f"   ID: {record[0]}, Student: {record[1]}, Status: {record[2]}")
        
        # Check pending records
        cursor.execute("SELECT COUNT(*) FROM web_registrations WHERE status = 'pending'")
        pending_count = cursor.fetchone()[0]
        print(f"\n⏳ Pending records available for approval: {pending_count}")
        
        if pending_count == 0:
            print("💡 No pending records found. Records might already be processed.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    quick_check()