import sqlite3
import os
import sys

def create_web_registrations_table():
    """
    Standalone script to permanently create the web_registrations table
    in the campus_gadgets database
    """
    
    # Database path - using the same as your main application
    db_path = "campus_gadgets.db"
    
    print("=" * 60)
    print("🏗️  WEB REGISTRATIONS TABLE CREATION TOOL")
    print("=" * 60)
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("💡 Make sure you're running this from the same directory as your main application")
        return False
    
    print(f"📁 Database found: {db_path}")
    print(f"📊 Database size: {os.path.getsize(db_path)} bytes")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n🔍 Checking current database state...")
        
        # Check if web_registrations table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='web_registrations'")
        existing_table = cursor.fetchone()
        
        if existing_table:
            print("❌ web_registrations table already exists!")
            print("💡 The table might have different structure or permissions")
            
            # Show current table structure
            cursor.execute("PRAGMA table_info(web_registrations)")
            current_columns = cursor.fetchall()
            
            print("\n📋 Current table structure:")
            for col in current_columns:
                col_id, name, type_, notnull, default, pk = col
                print(f"   {name:25} {type_:15} {'PK' if pk else ''} {'NOT NULL' if notnull else ''}")
            
            # Ask if user wants to recreate the table
            response = input("\n⚠️  Do you want to DROP and RECREATE the table? (yes/no): ")
            if response.lower() != 'yes':
                print("Operation cancelled.")
                conn.close()
                return False
            
            # Drop existing table
            print("🗑️  Dropping existing web_registrations table...")
            cursor.execute("DROP TABLE web_registrations")
            conn.commit()
            print("✅ Table dropped successfully")
        
        print("\n🏗️  Creating web_registrations table...")
        
        # Create the web_registrations table with proper structure
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
                color TEXT,
                additional_details TEXT,
                passport_photo TEXT,
                student_card_photo TEXT,
                gadget_photo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                
                -- Add constraints for data integrity
                CHECK (status IN ('pending', 'approved', 'rejected', 'processed'))
            )
        ''')
        
        print("✅ Table structure created successfully!")
        
        # Create indexes for better performance
        print("📈 Creating indexes...")
        cursor.execute('CREATE INDEX idx_web_reg_status ON web_registrations(status)')
        cursor.execute('CREATE INDEX idx_web_reg_created ON web_registrations(created_at)')
        cursor.execute('CREATE INDEX idx_web_reg_serial ON web_registrations(serial_number)')
        cursor.execute('CREATE INDEX idx_web_reg_student ON web_registrations(registration_number)')
        
        print("✅ Indexes created successfully!")
        
        # Add sample data for testing
        print("\n📝 Adding sample test data...")
        
        sample_data = [
            ('John Doe', '2024/001', 'ID123456', 'Laptop', 'Dell', 'XPS 13', 'DLXPS13001', 'Silver', 'Personal laptop for studies', None, None, None),
            ('Jane Smith', '2024/002', 'ID789012', 'Tablet', 'iPad', 'Pro 12.9', 'IPADPRO001', 'Space Gray', 'Digital art tablet', None, None, None),
            ('Mike Johnson', '2024/003', 'ID345678', 'Guitar', 'Fender', 'Stratocaster', 'FENDSTR001', 'Sunburst', 'Electric guitar for music club', None, None, None)
        ]
        
        for data in sample_data:
            try:
                cursor.execute('''
                    INSERT INTO web_registrations 
                    (student_name, registration_number, national_id, gadget_type, brand, model, serial_number, color, additional_details, passport_photo, student_card_photo, gadget_photo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)
            except sqlite3.IntegrityError:
                print(f"   ⚠️  Skipped duplicate serial number: {data[6]}")
        
        conn.commit()
        print("✅ Sample data added successfully!")
        
        # Verify the table was created correctly
        print("\n🔍 Verifying table creation...")
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM web_registrations")
        record_count = cursor.fetchone()[0]
        print(f"📊 Records in table: {record_count}")
        
        # Show records by status
        cursor.execute("SELECT status, COUNT(*) FROM web_registrations GROUP BY status")
        status_counts = cursor.fetchall()
        
        print("📈 Records by status:")
        for status, count in status_counts:
            print(f"   {status:10}: {count} records")
        
        # Show all tables in database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print(f"\n📁 All tables in database ({len(tables)} total):")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   {table_name:20} - {count:4} records")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("🎉 WEB REGISTRATIONS TABLE CREATION COMPLETED!")
        print("=" * 60)
        print("\n📋 What was created:")
        print("   ✅ web_registrations table with proper structure")
        print("   ✅ Indexes for fast searching")
        print("   ✅ Sample test data (3 records)")
        print("   ✅ All necessary constraints")
        
        print("\n🚀 Next steps:")
        print("   1. Restart your main application")
        print("   2. Go to 'Web Registrations' in the admin panel")
        print("   3. You should see the sample data")
        print("   4. Test the approval functionality")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def verify_table_creation():
    """Verify that the table was created correctly"""
    db_path = "campus_gadgets.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found for verification")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n" + "=" * 60)
        print("🔍 VERIFICATION CHECK")
        print("=" * 60)
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='web_registrations'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ VERIFICATION FAILED: web_registrations table not found")
            conn.close()
            return False
        
        print("✅ Table exists")
        
        # Check table structure
        cursor.execute("PRAGMA table_info(web_registrations)")
        columns = cursor.fetchall()
        
        expected_columns = ['id', 'student_name', 'registration_number', 'national_id', 
                          'gadget_type', 'brand', 'model', 'serial_number', 'color',
                          'additional_details', 'passport_photo', 'student_card_photo',
                          'gadget_photo', 'created_at', 'status']
        
        actual_columns = [col[1] for col in columns]
        
        print("📋 Column verification:")
        for expected in expected_columns:
            if expected in actual_columns:
                print(f"   ✅ {expected}")
            else:
                print(f"   ❌ {expected} - MISSING")
        
        # Check data
        cursor.execute("SELECT COUNT(*) FROM web_registrations")
        count = cursor.fetchone()[0]
        print(f"📊 Data verification: {count} records found")
        
        conn.close()
        
        if count > 0:
            print("\n🎉 VERIFICATION SUCCESSFUL!")
            print("The web_registrations table is ready to use.")
            return True
        else:
            print("\n⚠️  Table created but no data found")
            return True
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

if __name__ == "__main__":
    print("Starting web registrations table creation...")
    
    # Create the table
    success = create_web_registrations_table()
    
    if success:
        # Verify the creation
        verify_table_creation()
        
        print("\n" + "=" * 60)
        print("✅ SCRIPT EXECUTION COMPLETED")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Run your main application")
        print("2. Test web registration approvals")
        print("3. The table will persist permanently in your database")
    else:
        print("\n" + "=" * 60)
        print("❌ SCRIPT EXECUTION FAILED")
        print("=" * 60)
        print("\nPlease check:")
        print("1. Database file exists in the same directory")
        print("2. You have write permissions")
        print("3. The database is not locked by another application")
    
    input("\nPress Enter to exit...")