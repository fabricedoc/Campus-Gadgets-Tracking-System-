import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk

class WebRegistrationDebugger:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Web Registrations Debug Tool")
        self.root.geometry("1000x700")
        
        # Database path - adjust if needed
        self.db_path = "campus_gadgets.db"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(main_frame, text="🔧 Web Registrations Debug Tool", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Database info section
        db_frame = ctk.CTkFrame(main_frame)
        db_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(db_frame, text="Database Information", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=10)
        
        # Database path
        path_frame = ctk.CTkFrame(db_frame)
        path_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(path_frame, text="Database Path:", width=120).pack(side="left", padx=5)
        self.db_path_entry = ctk.CTkEntry(path_frame)
        self.db_path_entry.insert(0, self.db_path)
        self.db_path_entry.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(path_frame, text="Update Path", command=self.update_db_path).pack(side="left", padx=5)
        
        # Check database button
        ctk.CTkButton(db_frame, text="🔍 Check Database Structure", 
                      command=self.check_database_structure).pack(pady=10)
        
        # Web registrations section
        web_reg_frame = ctk.CTkFrame(main_frame)
        web_reg_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(web_reg_frame, text="Web Registrations Data", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=10)
        
        # Create treeview for web registrations
        columns = ("ID", "Student Name", "Reg Number", "Gadget Type", "Serial No", "Status", "Created At")
        self.tree = ttk.Treeview(web_reg_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(web_reg_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Action buttons
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(action_frame, text="🔄 Load Web Registrations", 
                      command=self.load_web_registrations).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="📊 Show Database Stats", 
                      command=self.show_database_stats).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="🐛 Debug Selected Record", 
                      command=self.debug_selected_record).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="🗑️ Clear All Data", 
                      command=self.clear_all_data).pack(side="left", padx=5)
        
        # Results area
        self.results_text = ctk.CTkTextbox(main_frame, height=200)
        self.results_text.pack(fill="x", padx=10, pady=10)
        
        # Load initial data
        self.load_web_registrations()
    
    def update_db_path(self):
        self.db_path = self.db_path_entry.get().strip()
        self.log_message(f"Database path updated to: {self.db_path}")
        self.load_web_registrations()
    
    def get_connection(self):
        """Get database connection"""
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            self.log_message(f"❌ Database connection failed: {str(e)}")
            return None
    
    def log_message(self, message):
        """Add message to results area"""
        self.results_text.configure(state="normal")
        self.results_text.insert("end", f"{message}\n")
        self.results_text.see("end")
        self.results_text.configure(state="disabled")
    
    def check_database_structure(self):
        """Check if web_registrations table exists and show its structure"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            self.log_message("\n" + "="*50)
            self.log_message("🔍 CHECKING DATABASE STRUCTURE")
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
                    self.log_message(f"   {name:20} {type_:15} {'PK' if pk else ''} {'NOT NULL' if notnull else ''}")
                
                # Count records by status
                cursor.execute("SELECT status, COUNT(*) FROM web_registrations GROUP BY status")
                status_counts = cursor.fetchall()
                
                self.log_message("\n📊 RECORD COUNTS BY STATUS:")
                for status, count in status_counts:
                    self.log_message(f"   {status:15}: {count} records")
                    
            else:
                self.log_message("❌ web_registrations table DOES NOT EXIST")
                
                # Show all tables in database
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                self.log_message("\n📁 ALL TABLES IN DATABASE:")
                for table in tables:
                    self.log_message(f"   {table[0]}")
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Error checking database: {str(e)}")
            conn.close()
    
    def load_web_registrations(self):
        """Load all web registrations into the treeview"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            cursor = conn.cursor()
            
            # Check if table exists first
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='web_registrations'")
            if not cursor.fetchone():
                self.log_message("❌ web_registrations table not found")
                conn.close()
                return
            
            # Load all web registrations
            cursor.execute('''
                SELECT id, student_name, registration_number, gadget_type, 
                       serial_number, status, created_at
                FROM web_registrations 
                ORDER BY created_at DESC
            ''')
            
            records = cursor.fetchall()
            
            if not records:
                self.log_message("ℹ️ No web registrations found in database")
            else:
                self.log_message(f"✅ Loaded {len(records)} web registration records")
                
                for record in records:
                    self.tree.insert("", "end", values=record)
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Error loading web registrations: {str(e)}")
            conn.close()
    
    def show_database_stats(self):
        """Show comprehensive database statistics"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            self.log_message("\n" + "="*50)
            self.log_message("📊 DATABASE STATISTICS")
            self.log_message("="*50)
            
            # Count records in all relevant tables
            tables = ['students', 'gadgets', 'check_records', 'web_registrations', 'users']
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                self.log_message(f"   {table:15}: {count:4} records")
            
            # Show web registration status breakdown
            cursor.execute('''
                SELECT status, COUNT(*) as count 
                FROM web_registrations 
                GROUP BY status
            ''')
            status_breakdown = cursor.fetchall()
            
            self.log_message("\n🌐 WEB REGISTRATIONS STATUS BREAKDOWN:")
            for status, count in status_breakdown:
                self.log_message(f"   {status:15}: {count:4} records")
            
            # Show recent activity
            cursor.execute('''
                SELECT gadget_type, COUNT(*) as count
                FROM gadgets 
                GROUP BY gadget_type
                ORDER BY count DESC
            ''')
            gadget_types = cursor.fetchall()
            
            self.log_message("\n💻 GADGET TYPE DISTRIBUTION:")
            for gadget_type, count in gadget_types:
                self.log_message(f"   {gadget_type:15}: {count:4} gadgets")
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Error showing statistics: {str(e)}")
            conn.close()
    
    def debug_selected_record(self):
        """Debug the selected web registration record"""
        selected = self.tree.selection()
        if not selected:
            self.log_message("❌ Please select a record to debug")
            return
        
        item_values = self.tree.item(selected[0])['values']
        if not item_values:
            self.log_message("❌ No data in selected record")
            return
        
        record_id = item_values[0]
        
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            self.log_message("\n" + "="*50)
            self.log_message(f"🐛 DEBUGGING RECORD ID: {record_id}")
            self.log_message("="*50)
            
            # Get full record details
            cursor.execute('''
                SELECT * FROM web_registrations WHERE id = ?
            ''', (record_id,))
            
            record = cursor.fetchone()
            
            if not record:
                self.log_message("❌ Record not found in database!")
                conn.close()
                return
            
            # Get column names
            cursor.execute("PRAGMA table_info(web_registrations)")
            columns = [col[1] for col in cursor.fetchall()]
            
            self.log_message("\n📋 FULL RECORD DETAILS:")
            for col_name, value in zip(columns, record):
                self.log_message(f"   {col_name:25}: {value}")
            
            # Check if this would pass the approval criteria
            cursor.execute('''
                SELECT student_name, registration_number, status
                FROM web_registrations 
                WHERE id = ? AND status = 'pending'
            ''', (record_id,))
            
            approval_check = cursor.fetchone()
            
            self.log_message("\n✅ APPROVAL CHECK:")
            if approval_check:
                self.log_message("   Status: PASS - Record is pending and can be approved")
            else:
                # Check why it failed
                cursor.execute('''
                    SELECT status FROM web_registrations WHERE id = ?
                ''', (record_id,))
                actual_status = cursor.fetchone()[0]
                self.log_message(f"   Status: FAIL - Current status is '{actual_status}' (expected 'pending')")
            
            # Check for potential issues
            self.log_message("\n🔍 POTENTIAL ISSUES:")
            
            # Check if serial number already exists in gadgets table
            cursor.execute('''
                SELECT COUNT(*) FROM gadgets WHERE serial_number = ?
            ''', (record[7],))  # serial_number is typically at index 7
            
            serial_exists = cursor.fetchone()[0]
            if serial_exists > 0:
                self.log_message(f"   ❌ Serial number '{record[7]}' already exists in gadgets table")
            else:
                self.log_message(f"   ✅ Serial number '{record[7]}' is unique")
            
            # Check if student already exists
            cursor.execute('''
                SELECT COUNT(*) FROM students WHERE registration_number = ?
            ''', (record[3],))  # registration_number is typically at index 3
            
            student_exists = cursor.fetchone()[0]
            if student_exists > 0:
                self.log_message(f"   ⚠️  Student with reg number '{record[3]}' already exists")
            else:
                self.log_message(f"   ✅ Student with reg number '{record[3]}' will be created")
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Error debugging record: {str(e)}")
            conn.close()
    
    def clear_all_data(self):
        """Clear the results area"""
        if messagebox.askyesno("Confirm Clear", "Clear all debug messages?"):
            self.results_text.configure(state="normal")
            self.results_text.delete("1.0", "end")
            self.results_text.configure(state="disabled")
    
    def run(self):
        """Start the debug tool"""
        self.root.mainloop()

if __name__ == "__main__":
    debugger = WebRegistrationDebugger()
    debugger.run()