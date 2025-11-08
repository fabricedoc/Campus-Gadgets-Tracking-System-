import sqlite3
import customtkinter as ctk
from tkinter import messagebox

class WebRegistrationFixer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Web Registrations Table Fixer")
        self.root.geometry("800x600")
        
        self.db_path = "campus_gadgets.db"
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="🔧 Fix Web Registrations Table", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Database info
        db_frame = ctk.CTkFrame(main_frame)
        db_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(db_frame, text="Database Actions", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=10)
        
        # Action buttons
        actions_frame = ctk.CTkFrame(db_frame)
        actions_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(actions_frame, text="1. Check Current Database", 
                      command=self.check_database, width=200).pack(pady=5)
        ctk.CTkButton(actions_frame, text="2. Create Web Registrations Table", 
                      command=self.create_web_registrations_table, width=200).pack(pady=5)
        ctk.CTkButton(actions_frame, text="3. Check All Tables", 
                      command=self.check_all_tables, width=200).pack(pady=5)
        ctk.CTkButton(actions_frame, text="4. Migrate Existing Data", 
                      command=self.migrate_existing_data, width=200).pack(pady=5)
        
        # Results area
        self.results_text = ctk.CTkTextbox(main_frame, height=300)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Run initial check
        self.check_database()
    
    def get_connection(self):
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            self.log_message(f"❌ Database connection failed: {str(e)}")
            return None
    
    def log_message(self, message):
        self.results_text.configure(state="normal")
        self.results_text.insert("end", f"{message}\n")
        self.results_text.see("end")
        self.results_text.configure(state="disabled")
    
    def check_database(self):
        """Check if web_registrations table exists"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            self.log_message("\n" + "="*50)
            self.log_message("🔍 CHECKING DATABASE")
            self.log_message("="*50)
            
            # Check if web_registrations table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='web_registrations'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                self.log_message("✅ web_registrations table EXISTS")
                
                # Show table structure
                cursor.execute("PRAGMA table_info(web_registrations)")
                columns = cursor.fetchall()
                
                self.log_message("\n📋 TABLE STRUCTURE:")
                for col in columns:
                    col_id, name, type_, notnull, default, pk = col
                    self.log_message(f"   {name:20} {type_:15} {'PK' if pk else ''}")
                
                # Count records
                cursor.execute("SELECT COUNT(*) FROM web_registrations")
                count = cursor.fetchone()[0]
                self.log_message(f"\n📊 Total records: {count}")
                
            else:
                self.log_message("❌ web_registrations table DOES NOT EXIST")
                self.log_message("💡 Click 'Create Web Registrations Table' to fix this")
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            conn.close()
    
    def create_web_registrations_table(self):
        """Create the missing web_registrations table"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            self.log_message("\n" + "="*50)
            self.log_message("🏗️ CREATING WEB_REGISTRATIONS TABLE")
            self.log_message("="*50)
            
            # Create the web_registrations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS web_registrations (
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
            
            self.log_message("✅ web_registrations table created successfully!")
            
            # Add some sample data for testing
            cursor.execute('''
                INSERT OR IGNORE INTO web_registrations 
                (student_name, registration_number, national_id, gadget_type, brand, model, serial_number)
                VALUES 
                ('John Doe', '2023/001', '123456789', 'Laptop', 'Dell', 'XPS 13', 'SN001'),
                ('Jane Smith', '2023/002', '987654321', 'Tablet', 'iPad', 'Pro 12.9', 'SN002')
            ''')
            
            conn.commit()
            
            # Verify the table was created
            cursor.execute("SELECT COUNT(*) FROM web_registrations")
            count = cursor.fetchone()[0]
            self.log_message(f"📊 Added {count} sample records for testing")
            
            self.log_message("\n🎉 Table creation completed! You can now:")
            self.log_message("   1. Restart your main application")
            self.log_message("   2. Test web registration approvals")
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Error creating table: {str(e)}")
            conn.close()
    
    def check_all_tables(self):
        """Show all tables in the database"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            self.log_message("\n" + "="*50)
            self.log_message("📁 ALL DATABASE TABLES")
            self.log_message("="*50)
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if tables:
                self.log_message("Found the following tables:")
                for table in tables:
                    table_name = table[0]
                    self.log_message(f"\n📋 {table_name}:")
                    
                    # Show table structure
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    
                    for col in columns:
                        col_id, name, type_, notnull, default, pk = col
                        self.log_message(f"   {name:20} {type_:15} {'PK' if pk else ''}")
                    
                    # Count records
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    self.log_message(f"   Records: {count}")
            else:
                self.log_message("❌ No tables found in database")
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            conn.close()
    
    def migrate_existing_data(self):
        """If you have existing data in another format, migrate it"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            self.log_message("\n" + "="*50)
            self.log_message("🔄 CHECKING FOR EXISTING DATA TO MIGRATE")
            self.log_message("="*50)
            
            # Check if there are any pending registrations in gadgets table with WEB prefix
            cursor.execute('''
                SELECT g.record_number, s.full_name, s.registration_number, 
                       g.gadget_type, g.brand, g.model, g.serial_number
                FROM gadgets g
                JOIN students s ON g.student_id = s.id
                WHERE g.record_number LIKE 'WEB%'
            ''')
            
            web_records = cursor.fetchall()
            
            if web_records:
                self.log_message(f"📋 Found {len(web_records)} web-registered gadgets:")
                
                for record in web_records:
                    record_no, student_name, reg_number, gadget_type, brand, model, serial = record
                    self.log_message(f"   {student_name} - {gadget_type} ({record_no})")
                
                self.log_message("\n💡 These records are already in the main system")
                self.log_message("   No migration needed for these")
            else:
                self.log_message("ℹ️ No existing web registrations found in gadgets table")
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Error during migration check: {str(e)}")
            conn.close()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    fixer = WebRegistrationFixer()
    fixer.run()