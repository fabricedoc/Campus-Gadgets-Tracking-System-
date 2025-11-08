import sqlite3
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime

class ApprovalProcessDebugger:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Approval Process Debugger")
        self.root.geometry("1000x700")
        
        self.db_path = "campus_gadgets.db"
        self.current_selected_id = None
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="🔍 Approval Process Debugger", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Web registrations display
        reg_frame = ctk.CTkFrame(main_frame)
        reg_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(reg_frame, text="Web Registrations", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=10)
        
        # Treeview for web registrations
        columns = ("ID", "Student", "Reg Number", "Gadget", "Serial", "Status")
        self.tree = ttk.Treeview(reg_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        scrollbar = ttk.Scrollbar(reg_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Debug controls
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        # Selected ID display
        id_frame = ctk.CTkFrame(controls_frame)
        id_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(id_frame, text="Selected ID:", width=100).pack(side="left", padx=5)
        self.selected_id_label = ctk.CTkLabel(id_frame, text="None", text_color="yellow")
        self.selected_id_label.pack(side="left", padx=5)
        
        # Debug buttons
        debug_buttons_frame = ctk.CTkFrame(controls_frame)
        debug_buttons_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(debug_buttons_frame, text="🔍 Debug Selected Record", 
                      command=self.debug_selected_record, width=200).pack(side="left", padx=5)
        ctk.CTkButton(debug_buttons_frame, text="✅ Test Approval", 
                      command=self.test_approval, width=200, fg_color="green").pack(side="left", padx=5)
        ctk.CTkButton(debug_buttons_frame, text="🔄 Refresh Data", 
                      command=self.load_web_registrations, width=200).pack(side="left", padx=5)
        ctk.CTkButton(debug_buttons_frame, text="📝 Create Test Record", 
                      command=self.create_test_record, width=200).pack(side="left", padx=5)
        
        # Results area
        self.results_text = ctk.CTkTextbox(main_frame, height=300)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load initial data
        self.load_web_registrations()
    
    def log_message(self, message):
        """Add message to results area"""
        self.results_text.configure(state="normal")
        self.results_text.insert("end", f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.results_text.see("end")
        self.results_text.configure(state="disabled")
    
    def get_connection(self):
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            self.log_message(f"❌ Database connection failed: {str(e)}")
            return None
    
    def load_web_registrations(self):
        """Load web registrations into treeview"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            # Clear treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='web_registrations'")
            if not cursor.fetchone():
                self.log_message("❌ web_registrations table does not exist!")
                conn.close()
                return
            
            # Load data
            cursor.execute('''
                SELECT id, student_name, registration_number, gadget_type, serial_number, status
                FROM web_registrations 
                ORDER BY id DESC
            ''')
            
            records = cursor.fetchall()
            
            if records:
                for record in records:
                    self.tree.insert("", "end", values=record)
                self.log_message(f"✅ Loaded {len(records)} web registrations")
            else:
                self.log_message("ℹ️ No web registrations found")
                # Add a placeholder
                self.tree.insert("", "end", values=("No data", "", "", "", "", ""))
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Error loading data: {str(e)}")
            conn.close()
    
    def on_tree_select(self, event):
        """Handle treeview selection"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            if values and values[0] != "No data":
                self.current_selected_id = values[0]
                self.selected_id_label.configure(text=str(self.current_selected_id))
                self.log_message(f"📌 Selected record ID: {self.current_selected_id}")
    
    def debug_selected_record(self):
        """Debug the currently selected record"""
        if not self.current_selected_id:
            self.log_message("❌ Please select a record first")
            return
        
        self.log_message(f"\n🔍 DEBUGGING RECORD ID: {self.current_selected_id}")
        
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # STEP 1: Check if record exists at all
            self.log_message("STEP 1: Checking if record exists...")
            cursor.execute("SELECT id, student_name, status FROM web_registrations WHERE id = ?", (self.current_selected_id,))
            record = cursor.fetchone()
            
            if not record:
                self.log_message("❌ RECORD NOT FOUND IN DATABASE!")
                self.log_message("💡 The ID in the treeview doesn't match the database")
                conn.close()
                return
            
            record_id, student_name, status = record
            self.log_message(f"✅ Record found: ID={record_id}, Student={student_name}, Status={status}")
            
            # STEP 2: Check if record has pending status
            self.log_message("\nSTEP 2: Checking status for approval...")
            if status == 'pending':
                self.log_message("✅ Status is 'pending' - ready for approval")
            else:
                self.log_message(f"❌ Status is '{status}' - cannot approve (must be 'pending')")
                conn.close()
                return
            
            # STEP 3: Try the exact query used in approval process
            self.log_message("\nSTEP 3: Testing approval query...")
            cursor.execute('''
                SELECT student_name, registration_number, national_id, gadget_type, brand, model, serial_number 
                FROM web_registrations 
                WHERE id = ? AND status = 'pending'
            ''', (self.current_selected_id,))
            
            approval_data = cursor.fetchone()
            
            if approval_data:
                self.log_message("✅ Approval query SUCCESSFUL!")
                self.log_message(f"   Data retrieved: {approval_data}")
            else:
                self.log_message("❌ Approval query FAILED!")
                self.log_message("💡 This is why you get 'not found or already processed'")
                self.log_message("   The record exists but the query conditions fail")
            
            # STEP 4: Check for potential issues
            self.log_message("\nSTEP 4: Checking for potential issues...")
            
            # Check if serial number already exists in gadgets
            if approval_data:
                serial_number = approval_data[6]  # serial_number is at index 6
                cursor.execute("SELECT COUNT(*) FROM gadgets WHERE serial_number = ?", (serial_number,))
                serial_count = cursor.fetchone()[0]
                
                if serial_count > 0:
                    self.log_message(f"❌ Serial number '{serial_number}' already exists in gadgets table")
                else:
                    self.log_message(f"✅ Serial number '{serial_number}' is available")
            
            conn.close()
            
        except Exception as e:
            self.log_message(f"❌ Debug error: {str(e)}")
            conn.close()
    
    def test_approval(self):
        """Test the actual approval process"""
        if not self.current_selected_id:
            self.log_message("❌ Please select a record first")
            return
        
        self.log_message(f"\n🧪 TESTING APPROVAL FOR ID: {self.current_selected_id}")
        
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # STEP 1: Get the data using the same query as your main app
            cursor.execute('''
                SELECT student_name, registration_number, national_id, gadget_type, brand, model, serial_number 
                FROM web_registrations 
                WHERE id = ? AND status = 'pending'
            ''', (self.current_selected_id,))
            
            web_data = cursor.fetchone()
            
            if not web_data:
                self.log_message("❌ APPROVAL FAILED AT STEP 1")
                self.log_message("💡 This is the exact error you're seeing!")
                self.log_message("   The query returned no data because:")
                self.log_message("   - Record doesn't exist, OR")
                self.log_message("   - Status is not 'pending', OR") 
                self.log_message("   - There's a database connection issue")
                
                # Let's find out exactly why
                cursor.execute("SELECT id, student_name, status FROM web_registrations WHERE id = ?", (self.current_selected_id,))
                actual_record = cursor.fetchone()
                
                if actual_record:
                    self.log_message(f"   Actual record: ID={actual_record[0]}, Status='{actual_record[2]}'")
                    if actual_record[2] != 'pending':
                        self.log_message(f"   💡 Status should be 'pending' but is '{actual_record[2]}'")
                else:
                    self.log_message("   💡 Record doesn't exist in database at all!")
                
                conn.close()
                return
            
            self.log_message("✅ Step 1: Data retrieval successful")
            
            # STEP 2: Process the approval
            student_name, reg_number, national_id, gadget_type, brand, model, serial_number = web_data
            
            self.log_message(f"   Processing: {student_name} - {gadget_type}")
            
            # Check if student exists
            cursor.execute("SELECT id FROM students WHERE registration_number = ?", (reg_number,))
            student = cursor.fetchone()
            
            if student:
                student_id = student[0]
                self.log_message(f"✅ Student exists: ID {student_id}")
                # Update student info
                cursor.execute('''
                    UPDATE students SET full_name = ?, national_id = ? 
                    WHERE id = ?
                ''', (student_name, national_id, student_id))
            else:
                # Create new student
                cursor.execute('''
                    INSERT INTO students (full_name, registration_number, national_id)
                    VALUES (?, ?, ?)
                ''', (student_name, reg_number, national_id))
                student_id = cursor.lastrowid
                self.log_message(f"✅ Created new student: ID {student_id}")
            
            # Generate record number
            record_number = f"WEB{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.log_message(f"✅ Generated record number: {record_number}")
            
            # Register gadget
            cursor.execute('''
                INSERT INTO gadgets (student_id, record_number, gadget_type, brand, model, serial_number, status)
                VALUES (?, ?, ?, ?, ?, ?, 'checked_in')
            ''', (student_id, record_number, gadget_type, brand, model, serial_number))
            
            gadget_id = cursor.lastrowid
            self.log_message(f"✅ Gadget registered: ID {gadget_id}")
            
            # Create check-in record
            cursor.execute('''
                INSERT INTO check_records (gadget_id, check_in_time, status)
                VALUES (?, ?, ?)
            ''', (gadget_id, datetime.now(), 'checked_in'))
            self.log_message("✅ Check-in record created")
            
            # Mark web registration as approved
            cursor.execute('''
                UPDATE web_registrations SET status = 'approved' 
                WHERE id = ?
            ''', (self.current_selected_id,))
            self.log_message("✅ Web registration marked as approved")
            
            conn.commit()
            conn.close()
            
            self.log_message("🎉 APPROVAL TEST COMPLETED SUCCESSFULLY!")
            self.log_message("💡 If this worked but your main app doesn't, check:")
            self.log_message("   1. Button command binding in main app")
            self.log_message("   2. Treeview selection handling")
            self.log_message("   3. Database connection in main app")
            
            # Refresh data to show changes
            self.load_web_registrations()
            
        except Exception as e:
            self.log_message(f"❌ Approval test failed: {str(e)}")
            conn.close()
    
    def create_test_record(self):
        """Create a test web registration"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            current_time = datetime.now().strftime("%H%M%S")
            test_data = (
                f"Debug Student {current_time}",
                f"DEBUG{current_time}",
                'DEBUG123',
                'Laptop',
                'Debug Brand',
                'Debug Model',
                f'DEBUG_SN_{current_time}'
            )
            
            cursor.execute('''
                INSERT INTO web_registrations 
                (student_name, registration_number, national_id, gadget_type, brand, model, serial_number, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
            ''', test_data)
            
            conn.commit()
            test_id = cursor.lastrowid
            
            self.log_message(f"✅ Created test registration with ID: {test_id}")
            self.log_message("   This record has status 'pending' and should be approvable")
            
            conn.close()
            
            # Refresh to show new record
            self.load_web_registrations()
            
        except Exception as e:
            self.log_message(f"❌ Test creation failed: {str(e)}")
            conn.close()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    debugger = ApprovalProcessDebugger()
    debugger.run()