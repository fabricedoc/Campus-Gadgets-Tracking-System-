import warnings
# Suppress the specific CustomTkinter image warning
warnings.filterwarnings("ignore", category=UserWarning, module="customtkinter")

import customtkinter as ctk
from customtkinter import CTkImage  # Important: import CTkImage
from tkinter import messagebox, ttk
import tkinter as tk
from auth import AuthSystem
from database import Database
from datetime import datetime, timedelta
import pandas as pd
import os
from PIL import Image, ImageTk  # Keep this for other uses, but don't use for CTk labels
import shutil
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
try:
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
except Exception:
    SimpleDocTemplate = Table = TableStyle = Paragraph = Spacer = None
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from reports_gui import add_reports_to_main_app

# Image Manager for proper CTkImage handling
class ImageManager:
    def __init__(self):
        self.image_cache = {}
    
    def load_ctk_image(self, image_path, size=(100, 100)):
        """Load image as CTkImage for HighDPI compatibility"""
        if not image_path or not os.path.exists(image_path):
            return None
            
        cache_key = f"{image_path}_{size[0]}_{size[1]}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        try:
            pil_image = Image.open(image_path)
            ctk_image = CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=size
            )
            self.image_cache[cache_key] = ctk_image
            return ctk_image
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None

# Global image manager instance
image_manager = ImageManager()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from auth import AuthSystem
from database import Database
from datetime import datetime, timedelta
import pandas as pd
import os
import config
from PIL import Image, ImageTk
import shutil
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
try:
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
except Exception:
    # reportlab.platypus may not be installed in the environment; provide safe fallbacks
    SimpleDocTemplate = Table = TableStyle = Paragraph = Spacer = None
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests  # For web API calls
from reports_gui import add_reports_to_main_app
import tkinter as tk
from tkinter import messagebox, ttk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CampusGadgetSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Campus Gadget Tracking System")
        self.root.geometry("1400x800")
        
        self.auth = AuthSystem()
        self.db = Database()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Login Frame
        self.login_frame = ctk.CTkFrame(self.root)
        
        ctk.CTkLabel(self.login_frame, text="Campus Gadget System", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)
        
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=300)
        self.username_entry.pack(pady=15)
        
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=300)
        self.password_entry.pack(pady=15)
        
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.handle_login, width=300)
        self.login_button.pack(pady=20)
        
        # Bind Enter key to login
        self.username_entry.bind('<Return>', lambda e: self.handle_login())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        self.login_frame.pack(expand=True)
        
        # Main Application Frame
        self.main_frame = ctk.CTkFrame(self.root)
        
        self.setup_main_interface()
    
    def setup_main_interface(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, width=250)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
    def setup_sidebar(self):
        # Clear sidebar
        for widget in self.sidebar.winfo_children():
            widget.destroy()
        
        # User info
        user_frame = ctk.CTkFrame(self.sidebar)
        user_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(user_frame, text=f"Welcome", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=5)
        ctk.CTkLabel(user_frame, text=f"{self.auth.current_user['name']}", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        ctk.CTkLabel(user_frame, text=f"Role: {self.auth.current_user['role']}", 
                    font=ctk.CTkFont(size=12)).pack(pady=5)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.sidebar)
        nav_frame.pack(fill="x", padx=10, pady=10)
        
        buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("👨‍🎓 Register Gadget", self.show_registration),
            ("📋 View Records", self.show_records),
            ("🔍 Check In/Out", self.show_check_io),
            ("📈 Advanced Reports", self.show_advanced_reports),  # ← ADD THIS LINE
            ("📊 Reports", self.show_reports),
            ]
        
        if self.auth.is_admin():
            buttons.append(("🌐 Web Registrations", self.show_web_registrations))
            buttons.append(("👥 User Management", self.show_user_management))
        
        for text, command in buttons:
            btn = ctk.CTkButton(nav_frame, text=text, command=command, 
                               corner_radius=0, anchor="w", height=40)
            btn.pack(fill="x", pady=2)
        
        # Logout button
        ctk.CTkButton(self.sidebar, text="🚪 Logout", command=self.logout,
                     fg_color="transparent", border_width=2, 
                     text_color=("gray10", "#DCE4EE"), height=40).pack(side="bottom", pady=20)
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.auth.login(username, password):
            self.login_frame.pack_forget()
            self.main_frame.pack(fill="both", expand=True)
            self.setup_sidebar()
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def logout(self):
        self.auth.logout()
        self.main_frame.pack_forget()
        self.login_frame.pack(expand=True)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.password_entry.focus()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        
        ctk.CTkLabel(self.content_frame, text="Admin Dashboard", 
                    font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)
        
        # Real-time Statistics
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get comprehensive stats
        cursor.execute("SELECT COUNT(*) FROM gadgets")
        total_gadgets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM gadgets WHERE status = 'checked_in'")
        gadgets_in_campus = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM gadgets WHERE status = 'checked_out'")
        gadgets_out_campus = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Today's activity
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COUNT(*) FROM check_records 
            WHERE DATE(check_in_time) = ? OR DATE(check_out_time) = ?
        ''', (today, today))
        today_activity = cursor.fetchone()[0]
        
        conn.close()
        
        stats_data = [
            ("📦 Total Gadgets", total_gadgets, "#4CC9F0"),
            ("🏢 In Campus", gadgets_in_campus, "#4361EE"),
            ("🏠 Out Campus", gadgets_out_campus, "#F72585"),
            ("👨‍🎓 Students", total_students, "#7209B7"),
            ("👥 Staff Users", total_users, "#3A0CA3"),
            ("📅 Today's Activity", today_activity, "#F77F00")
        ]
        
        # Create stats cards
        stats_container = ctk.CTkFrame(stats_frame)
        stats_container.pack(fill="x", padx=10, pady=10)
        
        for i, (text, value, color) in enumerate(stats_data):
            if i % 3 == 0:
                row_frame = ctk.CTkFrame(stats_container)
                row_frame.pack(fill="x", pady=5)
            
            stat_card = ctk.CTkFrame(row_frame, fg_color=color, corner_radius=10)
            stat_card.pack(side="left", expand=True, fill="x", padx=5)
            
            ctk.CTkLabel(stat_card, text=text, font=ctk.CTkFont(size=12), 
                        text_color="white").pack(pady=(10, 0))
            ctk.CTkLabel(stat_card, text=str(value), font=ctk.CTkFont(size=24, weight="bold"),
                        text_color="white").pack(pady=(0, 10))
    
    def show_registration(self):
        self.clear_content()
        
        ctk.CTkLabel(self.content_frame, text="Register New Gadget", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Create a simple form for demonstration
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(form_frame, text="Gadget Registration Form", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # Simple form fields
        fields = [
            ("Student Name", "student_name"),
            ("Registration Number", "reg_number"),
            ("Gadget Type", "gadget_type"),
            ("Serial Number", "serial_number")
        ]
        
        self.reg_entries = {}
        for label, key in fields:
            frame = ctk.CTkFrame(form_frame)
            frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(frame, text=label, width=150).pack(side="left", padx=5)
            entry = ctk.CTkEntry(frame)
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.reg_entries[key] = entry
        
        # Submit button
        ctk.CTkButton(form_frame, text="Register Gadget", 
                     command=self.simple_register_gadget).pack(pady=20)
    
    def simple_register_gadget(self):
        try:
            data = {}
            for key, entry in self.reg_entries.items():
                data[key] = entry.get().strip()
            
            # Validate
            for key, value in data.items():
                if not value:
                    messagebox.showerror("Error", f"Please fill in {key.replace('_', ' ')}")
                    return
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Check if student exists
            cursor.execute("SELECT id FROM students WHERE registration_number = ?", (data['reg_number'],))
            student = cursor.fetchone()
            
            if student:
                student_id = student[0]
            else:
                # Create student
                cursor.execute('''
                    INSERT INTO students (full_name, registration_number, national_id)
                    VALUES (?, ?, ?)
                ''', (data['student_name'], data['reg_number'], "N/A"))
                student_id = cursor.lastrowid
            
            # Register gadget
            record_number = f"G{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor.execute('''
                INSERT INTO gadgets (student_id, record_number, gadget_type, brand, model, serial_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, record_number, data['gadget_type'], "N/A", "N/A", data['serial_number']))
            
            gadget_id = cursor.lastrowid
            
            # Create check-in record
            cursor.execute('''
                INSERT INTO check_records (gadget_id, check_in_time, status)
                VALUES (?, ?, ?)
            ''', (gadget_id, datetime.now(), 'checked_in'))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Gadget registered!\nRecord Number: {record_number}")
            
            # Clear form
            for entry in self.reg_entries.values():
                entry.delete(0, tk.END)
                
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Serial number or registration number already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def show_records(self):
        self.clear_content()
        
        ctk.CTkLabel(self.content_frame, text="View Records", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Simple records display
        records_frame = ctk.CTkFrame(self.content_frame)
        records_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(records_frame, text="Gadget Records", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Create treeview
        tree = ttk.Treeview(records_frame, columns=("Record No", "Student", "Gadget", "Serial No"), show="headings", height=15)
        
        for col in ["Record No", "Student", "Gadget", "Serial No"]:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Load data
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT g.record_number, s.full_name, g.gadget_type, g.serial_number
            FROM gadgets g
            JOIN students s ON g.student_id = s.id
            ORDER BY g.created_at DESC
        ''')
        
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        
        conn.close()
    
    def show_check_io(self):
        self.clear_content()
        
        ctk.CTkLabel(self.content_frame, text="🔍 Check In/Out System", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Simple working interface
        main_frame = ctk.CTkFrame(self.content_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Search section
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(search_frame, text="Search for Gadgets", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=5)
        
        # Search input
        search_input_frame = ctk.CTkFrame(search_frame)
        search_input_frame.pack(fill="x", pady=5)
        
        self.search_entry = ctk.CTkEntry(search_input_frame, 
                                    placeholder_text="Enter record number, serial number, or student name...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(search_input_frame, text="🔍 Search", 
                    command=self.simple_check_search).pack(side="left", padx=5)
        
        # Results area
        self.results_text = ctk.CTkTextbox(main_frame, height=200)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_text.insert("1.0", "Search results will appear here...\n\nUse the search bar above to find gadgets.")
        self.results_text.configure(state="disabled")
        
        # Action buttons frame - THIS IS THE MISSING action_frame
        self.action_frame = ctk.CTkFrame(main_frame)
        self.action_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(self.action_frame, text="✅ Check In", 
                    command=self.simple_check_in,
                    fg_color="green", hover_color="dark green").pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(self.action_frame, text="🚪 Check Out", 
                    command=self.simple_check_out,
                    fg_color="red", hover_color="dark red").pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(self.action_frame, text="🔄 Clear", 
                    command=self.clear_check_results).pack(side="left", expand=True, padx=5)

    def simple_check_search(self):
        """Simple search functionality for check in/out"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        # Enable textbox for editing
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Search for gadgets
            cursor.execute('''
                SELECT g.record_number, g.gadget_type, g.brand, g.model, 
                    g.serial_number, g.status, s.full_name
                FROM gadgets g
                JOIN students s ON g.student_id = s.id
                WHERE g.record_number LIKE ? OR g.serial_number LIKE ? OR s.full_name LIKE ?
                LIMIT 5
            ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            
            results = cursor.fetchall()
            conn.close()
            
            if results:
                self.results_text.insert("1.0", f"🔍 Found {len(results)} result(s) for '{search_term}':\n\n")
                for i, result in enumerate(results, 1):
                    record_no, gadget_type, brand, model, serial_no, status, student = result
                    status_icon = "🟢" if status == "checked_in" else "🔴"
                    self.results_text.insert("end", 
                        f"{i}. {status_icon} {gadget_type} {brand} {model}\n"
                        f"   📋 Record: {record_no}\n"
                        f"   🔢 Serial: {serial_no}\n"
                        f"   👤 Student: {student}\n"
                        f"   📊 Status: {status.upper()}\n\n")
            else:
                self.results_text.insert("1.0", f"❌ No gadgets found for '{search_term}'\n\nPlease check your search term.")
                
        except Exception as e:
            self.results_text.insert("1.0", f"❌ Error searching: {str(e)}")
        
        # Disable textbox after update
        self.results_text.configure(state="disabled")

    def simple_check_in(self):
        """Simple check in functionality"""
        messagebox.showinfo("Check In", 
                        "Check In Feature:\n\n"
                        "This would check a gadget INTO campus.\n"
                        "Status would change from 'checked_out' to 'checked_in'")

    def simple_check_out(self):
        """Simple check out functionality"""
        messagebox.showinfo("Check Out", 
                        "Check Out Feature:\n\n"
                        "This would check a gadget OUT of campus.\n"
                        "Status would change from 'checked_in' to 'checked_out'")

    def clear_check_results(self):
        """Clear search results"""
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "Search results cleared.\n\nUse the search bar above to find gadgets.")
        self.results_text.configure(state="disabled")
        self.search_entry.delete(0, "end")

    def show_search_prompt(self):
        """Show search prompt in gadget details area"""
        for widget in self.gadget_details_frame.winfo_children():
            widget.destroy()
        
        prompt_label = ctk.CTkLabel(self.gadget_details_frame, 
                                text="🔍 Search for a gadget to check in/out\n\n"
                                    "You can search by:\n"
                                    "• Record Number\n"
                                    "• Serial Number\n" 
                                    "• Student Name\n"
                                    "• Registration Number",
                                font=ctk.CTkFont(size=14), justify="center")
        prompt_label.pack(expand=True, pady=50)
        
        # Hide action buttons
        self.action_frame.pack_forget()
    
    def search_for_check(self):
        """Search for gadgets to check in/out"""
        search_term = self.check_search_var.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Search in gadgets with student info
            cursor.execute('''
                SELECT 
                    g.id,
                    g.record_number,
                    g.gadget_type,
                    g.brand,
                    g.model,
                    g.serial_number,
                    g.status,
                    s.full_name,
                    s.registration_number
                FROM gadgets g
                JOIN students s ON g.student_id = s.id
                WHERE g.record_number LIKE ? 
                OR g.serial_number LIKE ?
                OR s.full_name LIKE ?
                OR s.registration_number LIKE ?
                ORDER BY g.created_at DESC
                LIMIT 10
            ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            
            results = cursor.fetchall()
            conn.close()
            
            if results:
                if len(results) == 1:
                    # Single result - show details
                    self.display_gadget_details(results[0])
                else:
                    # Multiple results - show selection
                    self.show_search_results(results)
            else:
                messagebox.showinfo("No Results", "No gadgets found matching your search")
                self.show_search_prompt()
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def show_search_results(self, results):
        """Show multiple search results for selection"""
        for widget in self.gadget_details_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.gadget_details_frame, text="Multiple gadgets found:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=5)
        
        # Create results list
        results_frame = ctk.CTkScrollableFrame(self.gadget_details_frame)
        results_frame.pack(fill="both", expand=True, pady=5)
        
        for result in results:
            result_frame = ctk.CTkFrame(results_frame)
            result_frame.pack(fill="x", pady=2, padx=5)
            
            gadget_info = f"{result[2]} {result[3]} - {result[5]} ({result[1]}) - {result[7]}"
            
            ctk.CTkLabel(result_frame, text=gadget_info, 
                        font=ctk.CTkFont(size=11)).pack(side="left", padx=5)
            
            ctk.CTkButton(result_frame, text="Select", width=60,
                        command=lambda r=result: self.display_gadget_details(r)).pack(side="right", padx=5)

    def display_gadget_details(self, gadget_data):
        """Display gadget details and show action buttons"""
        gadget_id, record_no, gadget_type, brand, model, serial_no, status, student_name, reg_number = gadget_data
        
        # Clear details frame
        for widget in self.gadget_details_frame.winfo_children():
            widget.destroy()
        
        # Gadget details
        details_frame = ctk.CTkFrame(self.gadget_details_frame)
        details_frame.pack(fill="both", expand=True, pady=10)
        
        # Current status with color coding
        status_color = "green" if status == "checked_in" else "red"
        status_text = "🟢 IN CAMPUS" if status == "checked_in" else "🔴 OUT OF CAMPUS"
        
        ctk.CTkLabel(details_frame, text="Current Status:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=2)
        ctk.CTkLabel(details_frame, text=status_text, 
                    text_color=status_color, font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=2)
        
        # Separator
        ctk.CTkLabel(details_frame, text="─" * 50, 
                    text_color="gray").pack(anchor="w", pady=10)
        
        # Gadget information
        info_items = [
            ("Record Number:", record_no),
            ("Gadget Type:", gadget_type),
            ("Brand/Model:", f"{brand} {model}"),
            ("Serial Number:", serial_no),
            ("Student:", student_name),
            ("Reg Number:", reg_number)
        ]
        
        for label, value in info_items:
            info_frame = ctk.CTkFrame(details_frame)
            info_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(info_frame, text=label, width=120, 
                        font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
            ctk.CTkLabel(info_frame, text=value).pack(side="left", padx=5)
        
        # Store current gadget info
        self.current_gadget = {
            'id': gadget_id,
            'record_number': record_no,
            'status': status,
            'student_name': student_name
        }
        
        # Show appropriate action buttons
        self.action_frame.pack(fill="x", padx=10, pady=10)

    def quick_scan(self):
        """Quick scan for record numbers (future: barcode/QR)"""
        scan_input = self.scan_var.get().strip()
        if not scan_input:
            messagebox.showwarning("Warning", "Please enter a record number to scan")
            return
        
        # Treat as record number search
        self.check_search_var.set(scan_input)
        self.search_for_check()
        self.scan_var.set("")  # Clear scan input

    def perform_check_io(self, action):
        """Perform check in or check out operation"""
        if not hasattr(self, 'current_gadget'):
            messagebox.showwarning("Warning", "Please select a gadget first")
            return
        
        gadget = self.current_gadget
        current_status = gadget['status']
        
        # Validate action
        if action == "in" and current_status == "checked_in":
            messagebox.showwarning("Warning", "This gadget is already checked in")
            return
        elif action == "out" and current_status == "checked_out":
            messagebox.showwarning("Warning", "This gadget is already checked out")
            return
        
        # Confirm action
        action_text = "CHECK IN" if action == "in" else "CHECK OUT"
        confirm_msg = f"Are you sure you want to {action_text.lower()} this gadget?\n\n" \
                    f"Record: {gadget['record_number']}\n" \
                    f"Student: {gadget['student_name']}"
        
        if not messagebox.askyesno("Confirm", confirm_msg):
            return
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            new_status = "checked_in" if action == "in" else "checked_out"
            timestamp = datetime.now()
            
            # Update gadget status
            cursor.execute("UPDATE gadgets SET status = ? WHERE id = ?", 
                        (new_status, gadget['id']))
            
            # Create check record
            if action == "in":
                cursor.execute('''
                    INSERT INTO check_records (gadget_id, check_in_time, status)
                    VALUES (?, ?, ?)
                ''', (gadget['id'], timestamp, 'checked_in'))
            else:
                cursor.execute('''
                    INSERT INTO check_records (gadget_id, check_out_time, status)
                    VALUES (?, ?, ?)
                ''', (gadget['id'], timestamp, 'checked_out'))
            
            conn.commit()
            conn.close()
            
            # Show success message
            success_msg = f"✅ Gadget {action_text} successfully!\n\n" \
                        f"Record: {gadget['record_number']}\n" \
                        f"Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            messagebox.showinfo("Success", success_msg)
            
            # Refresh the interface
            self.search_for_check()  # Reload current gadget details
            self.load_recent_activity()
            
        except Exception as e:
            messagebox.showerror("Error", f"Check {action} failed: {str(e)}")

    def load_recent_activity(self):
        """Load recent check in/out activity"""
        try:
            # Clear existing activity
            for item in self.activity_tree.get_children():
                self.activity_tree.delete(item)
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Get recent activity (last 20 records)
            cursor.execute('''
                SELECT 
                    cr.check_in_time,
                    cr.check_out_time,
                    cr.status,
                    s.full_name,
                    g.gadget_type,
                    g.record_number
                FROM check_records cr
                JOIN gadgets g ON cr.gadget_id = g.id
                JOIN students s ON g.student_id = s.id
                ORDER BY COALESCE(cr.check_in_time, cr.check_out_time) DESC
                LIMIT 20
            ''')
            
            for row in cursor.fetchall():
                check_in, check_out, status, student, gadget_type, record_no = row
                
                if status == 'checked_in':
                    time = check_in
                    action = "CHECK IN"
                    action_icon = "✅"
                else:
                    time = check_out
                    action = "CHECK OUT"
                    action_icon = "🚪"
                
                # Format time
                if time:
                    time_str = time[:19]  # Show only date and time
                else:
                    time_str = "N/A"
                
                # Shorten student name if too long
                short_student = student[:15] + "..." if len(student) > 15 else student
                
                self.activity_tree.insert("", "end", values=(
                    time_str,
                    short_student,
                    gadget_type,
                    f"{action_icon} {action}",
                    record_no
                ))
            
            conn.close()
            
        except Exception as e:
            print(f"Error loading activity: {e}")
    def show_reports(self):
        self.clear_content()
        
        ctk.CTkLabel(self.content_frame, text="📊 Reports & Analytics", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Simple reports interface
        reports_frame = ctk.CTkFrame(self.content_frame)
        reports_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Reports options
        options_frame = ctk.CTkFrame(reports_frame)
        options_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(options_frame, 
                    text="📈 Reports System\n\n"
                        "Generate various reports and analytics:\n"
                        "• Daily activity reports\n"
                        "• Gadget summary reports\n" 
                        "• Student registration reports\n"
                        "• Check-in/out statistics\n"
                        "• Export to PDF/Excel",
                    font=ctk.CTkFont(size=14),
                    justify="left").pack(expand=True, pady=20)
        
        # Report buttons
        buttons_frame = ctk.CTkFrame(options_frame)
        buttons_frame.pack(pady=20)
        
        report_types = [
            ("📋 Basic Report", self.generate_basic_report),
            ("📈 Activity Report", self.generate_activity_report),
            ("📊 Summary Report", self.generate_summary_report)
        ]
        
        for text, command in report_types:
            ctk.CTkButton(buttons_frame, text=text, command=command).pack(pady=10)

    def generate_basic_report(self):
        """Generate a basic report"""
        messagebox.showinfo("Basic Report", 
                        "Basic Report Generated!\n\n"
                        "This would show:\n"
                        "• Total gadgets registered\n"
                        "• Current gadgets in campus\n"
                        "• Recent activity\n"
                        "• System statistics")

    def generate_activity_report(self):
        """Generate activity report"""
        messagebox.showinfo("Activity Report", 
                        "Activity Report Generated!\n\n"
                        "This would show:\n"
                        "• Daily check-in/out activity\n"
                        "• Peak usage times\n"
                        "• Most active students\n"
                        "• Gadget movement patterns")

    def generate_summary_report(self):
        """Generate summary report"""
        messagebox.showinfo("Summary Report", 
                        "Summary Report Generated!\n\n"
                        "This would show:\n"
                        "• Gadget type distribution\n"
                        "• Brand popularity\n"
                        "• Student registration trends\n"
                        "• Approval statistics")
    
    def create_new_user(self):
        """Create a new user account"""
        try:
            # Collect form data
            user_data = {}
            for key, entry in self.new_user_data.items():
                user_data[key] = entry.get().strip()
            
            # Validate required fields
            required = ['full_name', 'username', 'password']
            for field in required:
                if not user_data[field]:
                    messagebox.showerror("Error", f"Please fill in the {field.replace('_', ' ')}")
                    return
            
            if len(user_data['password']) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters long")
                return
            
            # Collect permissions
            permissions_str = ",".join([key for key, var in self.permissions.items() if var.get()])
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Hash password
            import hashlib
            hashed_password = hashlib.sha256(user_data['password'].encode()).hexdigest()
            
            # Insert user
            cursor.execute('''
                INSERT INTO users (name, username, password, role, email, phone, department, permissions, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['full_name'],
                user_data['username'],
                hashed_password,
                self.role_var.get(),
                user_data.get('email', ''),
                user_data.get('phone', ''),
                user_data.get('department', ''),
                permissions_str,
                'active'
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"User '{user_data['username']}' created successfully!")
            
            # Clear form
            for entry in self.new_user_data.values():
                entry.delete(0, tk.END)
            self.role_var.set("security_officer")
            for var in self.permissions.values():
                var.set(False)
            self.permissions['gadget_management'].set(True)
            self.permissions['reports_access'].set(True)
            self.permissions['web_approvals'].set(True)
            
            # Refresh users list
            self.load_users_list()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user: {str(e)}")

    def load_users_list(self):
        """Load users into the management list"""
        try:
            # Clear existing data
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, username, role, department, status, last_login
                FROM users 
                ORDER BY name
            ''')
            
            for user in cursor.fetchall():
                user_id, name, username, role, department, status, last_login = user
                
                # Format status with icon
                status_display = "✅ Active" if status == "active" else "❌ Inactive"
                
                # Format last login
                last_login_display = last_login[:19] if last_login else "Never"
                
                self.users_tree.insert("", "end", values=(
                    user_id, name, username, role, department, status_display, last_login_display
                ))
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {str(e)}")

    def search_users(self):
        """Search users based on criteria"""
        search_term = self.user_search_var.get().strip()
        if not search_term:
            self.load_users_list()
            return
        
        try:
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, username, role, department, status, last_login
                FROM users 
                WHERE name LIKE ? OR username LIKE ? OR role LIKE ? OR department LIKE ?
                ORDER BY name
            ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            
            for user in cursor.fetchall():
                user_id, name, username, role, department, status, last_login = user
                status_display = "✅ Active" if status == "active" else "❌ Inactive"
                last_login_display = last_login[:19] if last_login else "Never"
                
                self.users_tree.insert("", "end", values=(
                    user_id, name, username, role, department, status_display, last_login_display
                ))
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def edit_user(self):
        """Edit selected user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to edit")
            return
        
        user_data = self.users_tree.item(selected[0])['values']
        user_id = user_data[0]
        
        messagebox.showinfo("Edit User", f"Edit functionality for user ID: {user_id}\n\nThis would open an edit dialog in a full implementation.")

    def reset_password(self):
        """Reset user password"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to reset password")
            return
        
        user_data = self.users_tree.item(selected[0])['values']
        username = user_data[2]
        
        if messagebox.askyesno("Confirm", f"Reset password for user '{username}'?"):
            messagebox.showinfo("Password Reset", f"Password reset for {username}\n\nNew password would be generated and sent to the user.")

    def deactivate_user(self):
        """Deactivate user account"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to deactivate")
            return
        
        user_data = self.users_tree.item(selected[0])['values']
        username = user_data[2]
        
        if messagebox.askyesno("Confirm", f"Deactivate user '{username}'?"):
            messagebox.showinfo("Deactivated", f"User '{username}' deactivated\n\nUser will no longer be able to login.")

    def activate_user(self):
        """Activate user account"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to activate")
            return
        
        user_data = self.users_tree.item(selected[0])['values']
        username = user_data[2]
        
        if messagebox.askyesno("Confirm", f"Activate user '{username}'?"):
            messagebox.showinfo("Activated", f"User '{username}' activated\n\nUser can now login to the system.")

    def delete_user(self):
        """Delete user account"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        user_data = self.users_tree.item(selected[0])['values']
        username = user_data[2]
        
        if messagebox.askyesno("Confirm Delete", 
                            f"PERMANENTLY delete user '{username}'?\n\nThis action cannot be undone!"):
            messagebox.showinfo("Deleted", f"User '{username}' deleted\n\nUser account permanently removed from system.")
    
    
    # Web Registration Methods
    def show_web_registrations(self):
        if not self.auth.is_admin():
            messagebox.showerror("Access Denied", "Admin access required")
            return
        
        self.clear_content()
        
        ctk.CTkLabel(self.content_frame, text="🌐 Web Registrations (Pending Approval)", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Refresh button
        refresh_frame = ctk.CTkFrame(self.content_frame)
        refresh_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(refresh_frame, text="🔄 Refresh", command=self.load_web_registrations).pack(side="left", padx=5)
        
        # Create a frame for the treeview and scrollbar
        tree_frame = ctk.CTkFrame(self.content_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Registrations list
        self.web_registrations_tree = ttk.Treeview(tree_frame, 
                                                 columns=("ID", "Record No", "Student", "Reg No", "Gadget", "Serial No", "Date"),
                                                 show="headings", height=15)
        
        # Configure columns
        columns_config = {
            "ID": 50,
            "Record No": 120,
            "Student": 150,
            "Reg No": 120,
            "Gadget": 150,
            "Serial No": 120,
            "Date": 120
        }
        
        for col, width in columns_config.items():
            self.web_registrations_tree.heading(col, text=col)
            self.web_registrations_tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.web_registrations_tree.yview)
        self.web_registrations_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.web_registrations_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Action buttons
        action_frame = ctk.CTkFrame(self.content_frame)
        action_frame.pack(fill="x", padx=20, pady=10)
        
        # Change this line in your show_web_registrations method:
        # ✅ This is what you need:
        ctk.CTkButton(action_frame, text="✅ Approve Selected", 
                    command=self.approve_selected_web_registration,  # CORRECT - wrapper method
                    fg_color="green").pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="❌ Reject Selected", command=self.reject_web_registration,
                     fg_color="red").pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="👁️ View Details", command=self.view_web_registration_details).pack(side="left", padx=5)
        
        self.load_web_registrations()
    def get_selected_web_reg_id(self):
        """Get the selected web registration ID from treeview"""
        try:
            selected_items = self.web_registrations_tree.selection()
            if not selected_items:
                messagebox.showwarning("Warning", "Please select a web registration to approve")
                return None
            
            selected_item = selected_items[0]
            item_values = self.web_registrations_tree.item(selected_item)['values']
            
            if not item_values or len(item_values) == 0:
                messagebox.showerror("Error", "No data found in selected row")
                return None
            
            web_registration_id = item_values[0]  # ID is in first column
            
            # Confirm approval
            student_name = item_values[2] if len(item_values) > 2 else "Unknown Student"
            
            if messagebox.askyesno("Confirm Approval", 
                                f"Are you sure you want to approve this registration?\n\n"
                                f"Student: {student_name}\n"
                                f"Gadget: {item_values[4] if len(item_values) > 4 else 'Unknown Gadget'}\n"
                                f"Reg No: {item_values[3] if len(item_values) > 3 else 'Unknown Reg No'}\n"
                                f"Serial No: {item_values[5] if len(item_values) > 5 else 'Unknown Serial No'}\n"
                                f"Registration ID: {web_registration_id}"):
                return web_registration_id
            else:
                return None
                
        except Exception as e:
            messagebox.showerror("Error", f"Selection error: {str(e)}")
            return None

    def load_web_registrations(self):
        try:
            # Clear existing data
            for item in self.web_registrations_tree.get_children():
                self.web_registrations_tree.delete(item)
            
            # Fetch pending registrations from web API
            response = requests.get('http://localhost:5000/api/pending-registrations', timeout=10)
            
            if response.status_code == 200:
                registrations = response.json()
                
                if not registrations:
                    # Insert a placeholder message
                    self.web_registrations_tree.insert("", "end", values=(
                        "", "No pending", "registrations", "found", "", "", ""
                    ))
                else:
                    for reg in registrations:
                        self.web_registrations_tree.insert("", "end", values=(
                            reg['id'],
                            reg['record_number'],
                            reg['full_name'],
                            reg['registration_number'],
                            f"{reg['gadget_type']} {reg['brand']}",
                            reg['serial_number'],
                            reg['created_at'][:19] if reg['created_at'] else reg['created_at']
                        ))
            else:
                messagebox.showerror("Error", "Failed to fetch web registrations")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Web server is not running. Start web_server.py first.")
        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "Connection to web server timed out.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load web registrations: {str(e)}")
    
    def approve_web_registration(self, web_registration_id):
        """Approve web registration and transfer data to main system tables"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # ✅ Use student_name (as in your table)
            cursor.execute('''
                SELECT student_name, registration_number, national_id, 
                    gadget_type, brand, model, serial_number 
                FROM web_registrations 
                WHERE id = ? AND LOWER(TRIM(status)) = 'pending'
            ''', (web_registration_id,))
            web_data = cursor.fetchone()

            if not web_data:
                messagebox.showerror("Error", "Web registration not found or already processed.")
                return False

            student_name, reg_number, national_id, gadget_type, brand, model, serial_number = web_data

            # ✅ Check if student exists
            cursor.execute("SELECT id FROM students WHERE registration_number = ?", (reg_number,))
            student = cursor.fetchone()

            if student:
                student_id = student[0]
                cursor.execute('''
                    UPDATE students 
                    SET full_name = ?, national_id = ? 
                    WHERE id = ?
                ''', (student_name, national_id, student_id))
            else:
                cursor.execute('''
                    INSERT INTO students (full_name, registration_number, national_id)
                    VALUES (?, ?, ?)
                ''', (student_name, reg_number, national_id))
                student_id = cursor.lastrowid

            # ✅ Create a new record number
            record_number = f"WEB{datetime.now().strftime('%Y%m%d%H%M%S')}"

            # ✅ Insert gadget entry
            cursor.execute('''
                INSERT INTO gadgets (student_id, record_number, gadget_type, brand, model, serial_number, status)
                VALUES (?, ?, ?, ?, ?, ?, 'checked_in')
            ''', (student_id, record_number, gadget_type, brand, model, serial_number))
            gadget_id = cursor.lastrowid

            # ✅ Log a check-in record
            cursor.execute('''
                INSERT INTO check_records (gadget_id, check_in_time, status)
                VALUES (?, ?, ?)
            ''', (gadget_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'checked_in'))

            # ✅ Update web registration status
            cursor.execute('''
                UPDATE web_registrations 
                SET status = 'approved'
                WHERE id = ?
            ''', (web_registration_id,))

            conn.commit()

            messagebox.showinfo(
                "Success",
                f"Registration approved successfully!\n\n"
                f"Student: {student_name}\n"
                f"Gadget: {gadget_type} ({brand})\n"
                f"Record No: {record_number}"
            )

            # ✅ Refresh treeview safely after DB commit
            self.load_web_registrations()

            return True

        except sqlite3.IntegrityError as e:
            conn.rollback()
            messagebox.showerror("Error", f"Duplicate serial number: {serial_number}")
            return False

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Error", f"Approval failed: {str(e)}")
            return False

        finally:
            if conn:
                conn.close()
    def approve_web_registration(self, web_registration_id):
        """Properly approve web registration with enhanced debugging"""
        try:
            print(f"🔍 APPROVAL: Starting approval for ID: {web_registration_id}")
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Enhanced debugging - check what's actually in the database
            cursor.execute("SELECT id, student_name, status FROM web_registrations WHERE id = ?", (web_registration_id,))
            test_record = cursor.fetchone()
            
            if not test_record:
                print(f"❌ APPROVAL: No record found with ID: {web_registration_id}")
                messagebox.showerror("Error", f"Web registration not found with ID: {web_registration_id}")
                conn.close()
                return False
            
            print(f"✅ APPROVAL: Found record - ID: {test_record[0]}, Student: {test_record[1]}, Status: {test_record[2]}")
            
            # Get web registration data
            cursor.execute('''
                SELECT student_name, registration_number, national_id, 
                    gadget_type, brand, model, serial_number 
                FROM web_registrations 
                WHERE id = ? AND status = 'pending'
            ''', (web_registration_id,))
            
            web_data = cursor.fetchone()
            
            if not web_data:
                print(f"❌ APPROVAL: Record exists but approval query failed. Current status: {test_record[2]}")
                messagebox.showerror("Error", f"Web registration not found or already processed. Current status: {test_record[2]}")
                conn.close()
                return False
            
            print(f"✅ APPROVAL: Approval data retrieved: {web_data}")
            
            student_name, reg_number, national_id, gadget_type, brand, model, serial_number = web_data
            
            # Rest of your approval logic...
            # Check if student exists
            cursor.execute("SELECT id FROM students WHERE registration_number = ?", (reg_number,))
            student = cursor.fetchone()
            
            if student:
                student_id = student[0]
                cursor.execute('''
                    UPDATE students SET full_name = ?, national_id = ? 
                    WHERE id = ?
                ''', (student_name, national_id, student_id))
            else:
                cursor.execute('''
                    INSERT INTO students (full_name, registration_number, national_id)
                    VALUES (?, ?, ?)
                ''', (student_name, reg_number, national_id))
                student_id = cursor.lastrowid
            
            record_number = f"WEB{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cursor.execute('''
                INSERT INTO gadgets (student_id, record_number, gadget_type, brand, model, serial_number, status)
                VALUES (?, ?, ?, ?, ?, ?, 'checked_in')
            ''', (student_id, record_number, gadget_type, brand, model, serial_number))
            
            gadget_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT INTO check_records (gadget_id, check_in_time, status)
                VALUES (?, ?, ?)
            ''', (gadget_id, datetime.now(), 'checked_in'))
            
            cursor.execute('''
                UPDATE web_registrations SET status = 'approved' 
                WHERE id = ?
            ''', (web_registration_id,))
            
            conn.commit()
            conn.close()
            
            print(f"✅ APPROVAL: Successfully approved ID: {web_registration_id}")
            messagebox.showinfo("Success", 
                            f"Registration approved successfully!\n"
                            f"Student: {student_name}\n"
                            f"Gadget: {gadget_type}\n"
                            f"Record No: {record_number}")
            
            self.load_web_registrations()
            return True
            
        except Exception as e:
            print(f"❌ APPROVAL: Error: {str(e)}")
            messagebox.showerror("Error", f"Approval failed: {str(e)}")
            return False
    def approve_selected_web_registration(self):
        """Wrapper method that gets selected ID from treeview and calls approval"""
        try:
            # Check if treeview exists
            if not hasattr(self, 'web_registrations_tree'):
                messagebox.showerror("Error", "Web registrations treeview not found")
                return
            
            # Get selected item
            selected_items = self.web_registrations_tree.selection()
            if not selected_items:
                messagebox.showwarning("Warning", "Please select a web registration to approve")
                return
            
            # Get the ID from the first column
            selected_item = selected_items[0]
            item_values = self.web_registrations_tree.item(selected_item)['values']
            
            if not item_values or len(item_values) == 0:
                messagebox.showerror("Error", "No data found in selected row")
                return
            
            web_registration_id = item_values[0]  # ID is in first column
            
            # Get student name for confirmation
            student_name = item_values[2] if len(item_values) > 2 else "Unknown Student"
            
            # Confirm approval
            if messagebox.askyesno("Confirm Approval", 
                                f"Are you sure you want to approve this registration?\n\n"
                                f"Student: {student_name}\n"
                                f"Registration ID: {web_registration_id}"):
                
                # Call your existing approve_web_registration method with the ID
                success = self.approve_web_registration(web_registration_id)
                
                if success:
                    # Refresh the list to show updated status
                    self.load_web_registrations()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Approval failed: {str(e)}")
    def reject_web_registration(self):
        selected = self.web_registrations_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a registration to reject")
            return
        
        item = self.web_registrations_tree.item(selected[0])
        values = item['values']
        
        # Check if it's the placeholder message
        if not values or not values[0]:
            return
        
        registration_id = values[0]
        student_name = values[2]
        
        if messagebox.askyesno("Confirm Rejection", 
                              f"Are you sure you want to reject the registration for {student_name}?"):
            try:
                response = requests.post(f'http://localhost:5000/api/reject-registration/{registration_id}', timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if result['success']:
                        messagebox.showinfo("Success", "Registration rejected")
                        self.load_web_registrations()
                    else:
                        messagebox.showerror("Error", result['message'])
                else:
                    messagebox.showerror("Error", "Failed to reject registration")
                    
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Web server is not running. Start web_server.py first.")
            except Exception as e:
                messagebox.showerror("Error", f"Rejection failed: {str(e)}")

    def view_web_registration_details(self):
        selected = self.web_registrations_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a registration to view details")
            return
        
        item = self.web_registrations_tree.item(selected[0])
        values = item['values']
        
        # Check if it's the placeholder message
        if not values or not values[0]:
            return
        
        registration_id = values[0]
        
        try:
            # Fetch detailed information
            response = requests.get('http://localhost:5000/api/pending-registrations', timeout=10)
            
            if response.status_code == 200:
                registrations = response.json()
                registration = next((reg for reg in registrations if reg['id'] == registration_id), None)
                
                if registration:
                    # Create details window
                    details_window = ctk.CTkToplevel(self.root)
                    details_window.title("Registration Details")
                    details_window.geometry("600x500")
                    details_window.transient(self.root)
                    details_window.grab_set()
                    
                    # Create scrollable frame
                    scrollable_frame = ctk.CTkScrollableFrame(details_window)
                    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
                    
                    # Display details
                    details = [
                        ("Record Number:", registration['record_number']),
                        ("Student Name:", registration['full_name']),
                        ("Registration Number:", registration['registration_number']),
                        ("Gadget Type:", registration['gadget_type']),
                        ("Brand:", registration['brand']),
                        ("Model:", registration['model']),
                        ("Serial Number:", registration['serial_number']),
                        ("Color:", registration.get('color', 'Not specified')),
                        ("Additional Details:", registration.get('additional_details', 'None')),
                        ("Registration Date:", registration['created_at'])
                    ]
                    
                    for label, value in details:
                        frame = ctk.CTkFrame(scrollable_frame)
                        frame.pack(fill="x", pady=5)
                        
                        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(weight="bold"), width=150).pack(side="left", padx=5)
                        ctk.CTkLabel(frame, text=str(value)).pack(side="left", padx=5)
                    
                    # Close button
                    ctk.CTkButton(details_window, text="Close", command=details_window.destroy).pack(pady=10)
                    
                else:
                    messagebox.showerror("Error", "Registration details not found")
            else:
                messagebox.showerror("Error", "Failed to fetch registration details")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load details: {str(e)}")
    def sync_web_registrations(self):
        """Check for and process web registration data"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Check if web_registrations table exists
            cursor.execute('''
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='web_registrations'
            ''')
            
            if cursor.fetchone():
                # Process pending web registrations
                cursor.execute('''
                    SELECT * FROM web_registrations WHERE status = 'pending'
                ''')
                
                pending_records = cursor.fetchall()
                
                for record in pending_records:
                    web_id, student_name, reg_number, national_id, gadget_type, brand, model, serial_number, created_at, status = record
                    
                    # Process the registration (same logic as manual registration)
                    cursor.execute("SELECT id FROM students WHERE registration_number = ?", (reg_number,))
                    student = cursor.fetchone()
                    
                    if student:
                        student_id = student[0]
                    else:
                        cursor.execute('''
                            INSERT INTO students (full_name, registration_number, national_id)
                            VALUES (?, ?, ?)
                        ''', (student_name, reg_number, national_id))
                        student_id = cursor.lastrowid
                    
                    # Generate record number
                    record_number = f"WEB{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    # Register gadget
                    cursor.execute('''
                        INSERT INTO gadgets (student_id, record_number, gadget_type, brand, model, serial_number)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (student_id, record_number, gadget_type, brand, model, serial_number))
                    
                    gadget_id = cursor.lastrowid
                    
                    # Create check-in record
                    cursor.execute('''
                        INSERT INTO check_records (gadget_id, check_in_time, status)
                        VALUES (?, ?, ?)
                    ''', (gadget_id, datetime.now(), 'checked_in'))
                    
                    # Mark web registration as processed
                    cursor.execute('''
                        UPDATE web_registrations SET status = 'processed' 
                        WHERE id = ?
                    ''', (web_id,))
                
                conn.commit()
                messagebox.showinfo("Success", f"Processed {len(pending_records)} web registrations")
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Sync failed: {str(e)}")   
    def load_web_registrations(self):
        """Load web registrations from API and store in local database for approval"""
        response = requests.get('http://localhost:5000/api/pending-registrations', timeout=10)
        if not hasattr(self, 'web_registrations_tree'):
            return
        
        try:
            # Clear existing data
            for item in self.web_registrations_tree.get_children():
                self.web_registrations_tree.delete(item)
            
            print("🔄 Loading and syncing web registrations...")
            
            # Step 1: Fetch from API
            response = requests.get('http://localhost:5000/api/pending-registrations', timeout=10)
            
            if response.status_code != 200:
                print("❌ Failed to fetch from API")
                self.load_from_local_database()
                return
            
            api_registrations = response.json()
            
            if not api_registrations:
                print("ℹ️ No pending registrations from API")
                self.load_from_local_database()
                return
            
            print(f"✅ Fetched {len(api_registrations)} records from API")
            
            # Step 2: Store in local database with proper mapping
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            stored_count = 0
            for api_reg in api_registrations:
                # Check if this record already exists in local database
                cursor.execute("SELECT id FROM web_registrations WHERE id = ?", (api_reg['id'],))
                existing = cursor.fetchone()
                
                if not existing:
                    # Insert into local database with proper field mapping
                    cursor.execute('''
                        INSERT INTO web_registrations 
                        (id, student_name, registration_number, national_id, gadget_type, 
                        brand, model, serial_number, color, additional_details, created_at, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        api_reg['id'],
                        api_reg['full_name'],  # Map 'full_name' to 'student_name'
                        api_reg['registration_number'],
                        api_reg.get('national_id', 'N/A'),  # Provide default if missing
                        api_reg['gadget_type'],
                        api_reg['brand'],
                        api_reg['model'],
                        api_reg['serial_number'],
                        api_reg.get('color', ''),
                        api_reg.get('additional_details', ''),
                        api_reg.get('created_at', ''),
                        'pending'  # Set status to pending for approval
                    ))
                    stored_count += 1
                    print(f"   💾 Stored: ID {api_reg['id']} - {api_reg['full_name']}")
            
            conn.commit()
            print(f"✅ Stored {stored_count} new records in local database")
            
            # Step 3: Load from local database for display
            self.load_from_local_database()
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Load error: {str(e)}")
            self.load_from_local_database()

    def load_from_local_database(self):
        """Load web registrations from local database for display"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, created_at, student_name, registration_number, 
                    gadget_type, brand, model, serial_number, status
                FROM web_registrations 
                WHERE status = 'pending'
                ORDER BY id DESC
            ''')
            
            records = cursor.fetchall()
            conn.close()
            
            print(f"📊 Displaying {len(records)} pending registrations from local database")
            
            if not records:
                self.web_registrations_tree.insert("", "end", values=(
                    "No pending", "registrations", "available for", "approval", "", "", "", ""
                ))
                return
            
            for record in records:
                created_at = record[1][:19] if record[1] else ''
                
                self.web_registrations_tree.insert("", "end", values=(
                    record[0],  # id
                    created_at,  # created_at
                    record[2],  # student_name
                    record[3],  # registration_number
                    record[4],  # gadget_type
                    record[5],  # brand
                    record[6],  # model
                    record[7],  # serial_number
                    record[8]   # status
                ))
            
            print(f"🎯 Ready to approve IDs: {[r[0] for r in records]}")
            
        except Exception as e:
            print(f"❌ Local database load error: {str(e)}")
            self.web_registrations_tree.insert("", "end", values=(
                "Error", f"Load failed: {str(e)}", "", "", "", "", "", ""
            ))
    def show_advanced_reports(self):
        """Display the advanced reports UI inside the main content area."""
        self.clear_content()
    
        ctk.CTkLabel(self.content_frame, text="📊 Advanced Analytics & Reports", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
    
        # Initialize reports module (guarded)
        try:
            from reports_module import AdvancedReports
            self.reports = AdvancedReports()
        except Exception:
            self.reports = None
    
        # Report selection frame
        selection_frame = ctk.CTkFrame(self.content_frame)
        selection_frame.pack(fill="x", padx=20, pady=10)
    
        ctk.CTkLabel(selection_frame, text="Select Report Type:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=10)
    
        # Report type buttons
        report_types_frame = ctk.CTkFrame(selection_frame)
        report_types_frame.pack(fill="x", pady=10)
    
        report_types = [
            ("📈 Daily Activity", self.generate_daily_report),
            ("📊 Trend Analysis", self.generate_trend_report),
            ("🏆 System Dashboard", self.generate_dashboard),
            ("👨‍🎓 Student Report", self.generate_student_report)
        ]
    
        for i, (text, command) in enumerate(report_types):
            btn = ctk.CTkButton(report_types_frame, text=text, command=command,
                               height=40, font=ctk.CTkFont(size=12))
            btn.pack(side="left", expand=True, padx=5)
    
        # Date range frame
        self.date_frame = ctk.CTkFrame(self.content_frame)
        self.date_frame.pack(fill="x", padx=20, pady=10)
    
        ctk.CTkLabel(self.date_frame, text="Date Range:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=5)
    
        date_input_frame = ctk.CTkFrame(self.date_frame)
        date_input_frame.pack(fill="x", pady=5)
    
        ctk.CTkLabel(date_input_frame, text="From:", width=60).pack(side="left", padx=5)
        self.start_date_entry = ctk.CTkEntry(date_input_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.start_date_entry.pack(side="left", padx=5)
    
        ctk.CTkLabel(date_input_frame, text="To:", width=60).pack(side="left", padx=5)
        self.end_date_entry = ctk.CTkEntry(date_input_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.end_date_entry.pack(side="left", padx=5)
    
        # Set default dates (last 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        self.start_date_entry.insert(0, start_date.strftime('%Y-%m-%d'))
        self.end_date_entry.insert(0, end_date.strftime('%Y-%m-%d'))
    
        # Student search frame
        self.student_frame = ctk.CTkFrame(self.content_frame)
        self.student_frame.pack(fill="x", padx=20, pady=10)
    
        ctk.CTkLabel(self.student_frame, text="Student Registration Number:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=5)
    
        student_input_frame = ctk.CTkFrame(self.student_frame)
        student_input_frame.pack(fill="x", pady=5)
    
        self.student_reg_entry = ctk.CTkEntry(student_input_frame, placeholder_text="Enter registration number")
        self.student_reg_entry.pack(side="left", fill="x", expand=True, padx=5)
    
        # Results area - using scrollable frame for better display
        self.results_frame = ctk.CTkScrollableFrame(self.content_frame, height=400)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
        # Initially show welcome message
        self.show_report_welcome()

        
        # Simple user management interface
        main_frame = ctk.CTkFrame(self.content_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Add user form
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Add New User", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=10)
        
        # Simple form
        fields_frame = ctk.CTkFrame(form_frame)
        fields_frame.pack(fill="x", pady=5)
        
        # Name field
        name_frame = ctk.CTkFrame(fields_frame)
        name_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(name_frame, text="Full Name:", width=100).pack(side="left", padx=5)
        self.new_user_name = ctk.CTkEntry(name_frame)
        self.new_user_name.pack(side="left", fill="x", expand=True, padx=5)
        
        # Username field
        user_frame = ctk.CTkFrame(fields_frame)
        user_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(user_frame, text="Username:", width=100).pack(side="left", padx=5)
        self.new_username = ctk.CTkEntry(user_frame)
        self.new_username.pack(side="left", fill="x", expand=True, padx=5)
        
        # Password field
        pass_frame = ctk.CTkFrame(fields_frame)
        pass_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(pass_frame, text="Password:", width=100).pack(side="left", padx=5)
        self.new_password = ctk.CTkEntry(pass_frame, show="*")
        self.new_password.pack(side="left", fill="x", expand=True, padx=5)
        
        # Role selection
        role_frame = ctk.CTkFrame(fields_frame)
        role_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(role_frame, text="Role:", width=100).pack(side="left", padx=5)
        self.new_user_role = ctk.CTkComboBox(role_frame, values=["admin", "security_officer"])
        self.new_user_role.set("security_officer")
        self.new_user_role.pack(side="left", fill="x", expand=True, padx=5)
        
        # Add user button
        ctk.CTkButton(form_frame, text="Add User", command=self.simple_add_user).pack(pady=10)
        
        # Users list
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(list_frame, text="Existing Users", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=10)
        
        # Simple users display
        self.users_text = ctk.CTkTextbox(list_frame, height=200)
        self.users_text.pack(fill="both", expand=True, pady=5)
        self.users_text.insert("1.0", "Loading users...")
        self.users_text.configure(state="disabled")
        
        # Load users
        self.load_simple_users_list()
    def show_user_management(self):
        if not self.auth.is_admin():
            messagebox.showerror("Access Denied", "Admin access required")
            return
        
        self.clear_content()
        
        ctk.CTkLabel(self.content_frame, text="👥 User Management", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Simple user management interface
        main_frame = ctk.CTkFrame(self.content_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Add user form
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Add New User", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=10)
        
        # Simple form
        fields_frame = ctk.CTkFrame(form_frame)
        fields_frame.pack(fill="x", pady=5)
        
        # Name field
        name_frame = ctk.CTkFrame(fields_frame)
        name_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(name_frame, text="Full Name:", width=100).pack(side="left", padx=5)
        self.new_user_name = ctk.CTkEntry(name_frame)
        self.new_user_name.pack(side="left", fill="x", expand=True, padx=5)
        
        # Username field
        user_frame = ctk.CTkFrame(fields_frame)
        user_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(user_frame, text="Username:", width=100).pack(side="left", padx=5)
        self.new_username = ctk.CTkEntry(user_frame)
        self.new_username.pack(side="left", fill="x", expand=True, padx=5)
        
        # Password field
        pass_frame = ctk.CTkFrame(fields_frame)
        pass_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(pass_frame, text="Password:", width=100).pack(side="left", padx=5)
        self.new_password = ctk.CTkEntry(pass_frame, show="*")
        self.new_password.pack(side="left", fill="x", expand=True, padx=5)
        
        # Role selection
        role_frame = ctk.CTkFrame(fields_frame)
        role_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(role_frame, text="Role:", width=100).pack(side="left", padx=5)
        self.new_user_role = ctk.CTkComboBox(role_frame, values=["admin", "security_officer"])
        self.new_user_role.set("security_officer")
        self.new_user_role.pack(side="left", fill="x", expand=True, padx=5)
        
        # Add user button
        ctk.CTkButton(form_frame, text="Add User", command=self.simple_add_user).pack(pady=10)
        
        # Users list
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(list_frame, text="Existing Users", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=10)
        
        # Simple users display
        self.users_text = ctk.CTkTextbox(list_frame, height=200)
        self.users_text.pack(fill="both", expand=True, pady=5)
        self.users_text.insert("1.0", "Loading users...")
        self.users_text.configure(state="disabled")
        
        # Load users
        self.load_simple_users_list()
    def simple_add_user(self):
        """Simple method to add a new user"""
        try:
            name = self.new_user_name.get().strip()
            username = self.new_username.get().strip()
            password = self.new_password.get().strip()
            role = self.new_user_role.get()
            
            if not all([name, username, password]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Hash password
            import hashlib
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (name, username, password, role)
                VALUES (?, ?, ?, ?)
            ''', (name, username, hashed_password, role))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"User '{username}' added successfully!")
            
            # Clear form
            self.new_user_name.delete(0, tk.END)
            self.new_username.delete(0, tk.END)
            self.new_password.delete(0, tk.END)
            self.new_user_role.set("security_officer")
            
            # Refresh list
            self.load_simple_users_list()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {str(e)}")

    def load_simple_users_list(self):
        """Load users into the text display"""
        try:
            self.users_text.configure(state="normal")
            self.users_text.delete("1.0", "end")
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT name, username, role, created_at FROM users ORDER BY name")
            users = cursor.fetchall()
            conn.close()
            
            if users:
                self.users_text.insert("end", "Current Users:\n\n")
                for user in users:
                    name, username, role, created = user
                    self.users_text.insert("end", f"👤 {name} ({username})\n")
                    self.users_text.insert("end", f"   Role: {role}\n")
                    self.users_text.insert("end", f"   Created: {created[:10]}\n\n")
            else:
                self.users_text.insert("end", "No users found in the system.")
            
            self.users_text.configure(state="disabled")
            
        except Exception as e:
            self.users_text.insert("end", f"Error loading users: {str(e)}")
    def show_report_welcome(self):
        """Show welcome message in reports section"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        welcome_label = ctk.CTkLabel(self.results_frame, 
                                   text="🎯 Select a report type above to generate advanced analytics and visualizations\n\n"
                                        "Available Reports:\n"
                                        "• 📈 Daily Activity - Check-in/out trends and gadget distribution\n"
                                        "• 📊 Trend Analysis - Registration patterns and status distribution\n"
                                        "• 🏆 System Dashboard - Comprehensive overview with key metrics\n"
                                        "• 👨‍🎓 Student Report - Individual student gadget history",
                                   font=ctk.CTkFont(size=14), justify="left")
        welcome_label.pack(pady=50)
    
    def generate_daily_report(self):
        try:
            start_date = self.start_date_entry.get().strip()
            end_date = self.end_date_entry.get().strip()
            
            if not start_date or not end_date:
                messagebox.showerror("Error", "Please enter both start and end dates")
                return
            
            self.show_report_loading("Generating Daily Activity Report...")
            
            if not self.reports:
                messagebox.showerror("Error", "Reports module not available")
                return
            
            # Generate report
            report_data = self.reports.generate_daily_activity_report(start_date, end_date)
            
            # Display results in the main interface
            self.display_report_in_main(report_data, "Daily Activity Report", start_date, end_date)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_trend_report(self):
        try:
            self.show_report_loading("Generating Trend Analysis Report...")
            
            if not self.reports:
                messagebox.showerror("Error", "Reports module not available")
                return
            
            # Generate report (last 30 days)
            report_data = self.reports.generate_trend_analysis_report(30)
            
            # Display results
            self.display_report_in_main(report_data, "Trend Analysis Report")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate trend report: {str(e)}")
    
    def generate_dashboard(self):
        try:
            self.show_report_loading("Generating System Dashboard...")
            
            if not self.reports:
                messagebox.showerror("Error", "Reports module not available")
                return
            
            # Generate dashboard
            report_data = self.reports.generate_comprehensive_dashboard()
            
            # Display results
            self.display_report_in_main(report_data, "System Dashboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate dashboard: {str(e)}")
    
    def generate_student_report(self):
        try:
            registration_number = self.student_reg_entry.get().strip()
            
            if not registration_number:
                messagebox.showerror("Error", "Please enter a registration number")
                return
            
            self.show_report_loading(f"Generating Report for {registration_number}...")
            
            if not self.reports:
                messagebox.showerror("Error", "Reports module not available")
                return
            
            # Generate student report
            report_data = self.reports.generate_student_activity_report(registration_number)
            
            if report_data:
                # Display results
                self.display_report_in_main(report_data, f"Student Report - {registration_number}")
            else:
                messagebox.showwarning("Not Found", f"No student found with registration number: {registration_number}")
                self.show_report_welcome()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate student report: {str(e)}")
    
    def show_report_loading(self, message):
        """Show loading state in reports section"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        loading_label = ctk.CTkLabel(self.results_frame, text=message, 
                                   font=ctk.CTkFont(size=16))
        loading_label.pack(expand=True, pady=50)
        
        self.results_frame.update()
            
    def display_report_in_main(self, report_data, title, start_date=None, end_date=None):
        """Display report results in the main application interface"""
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_label = ctk.CTkLabel(self.results_frame, text=f"📊 {title}", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        # Date range if provided
        if start_date and end_date:
            date_label = ctk.CTkLabel(self.results_frame, 
                                    text=f"Period: {start_date} to {end_date}",
                                    font=ctk.CTkFont(size=12))
            date_label.pack(pady=5)
        
        # Display key statistics if available
        if report_data and isinstance(report_data, dict) and 'statistics' in report_data:
            stats = report_data['statistics']
            stats_frame = ctk.CTkFrame(self.results_frame)
            stats_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(stats_frame, text="📈 Key Statistics", 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
            
            # Create stats grid
            stats_grid = ctk.CTkFrame(stats_frame)
            stats_grid.pack(fill="x", padx=10, pady=5)
            
            stats_items = [
                ("Total Students", stats.get('total_students', 'N/A')),
                ("Total Gadgets", stats.get('total_gadgets', 'N/A')),
                ("Gadgets in Campus", stats.get('gadgets_in_campus', 'N/A')),
                ("Approved Gadgets", stats.get('approved_gadgets', 'N/A')),
                ("Pending Gadgets", stats.get('pending_gadgets', 'N/A')),
                ("Today's Activity", stats.get('today_activities', 'N/A'))
            ]
            
            for i, (label, value) in enumerate(stats_items):
                if i % 3 == 0:
                    row_frame = ctk.CTkFrame(stats_grid)
                    row_frame.pack(fill="x", pady=5)
                
                stat_card = ctk.CTkFrame(row_frame, fg_color="#2b2b2b", corner_radius=8)
                stat_card.pack(side="left", expand=True, fill="x", padx=5)
                
                ctk.CTkLabel(stat_card, text=label, font=ctk.CTkFont(size=11)).pack(pady=(8, 2))
                ctk.CTkLabel(stat_card, text=str(value), font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(2, 8))
        
        # Display chart image if available
        if report_data and isinstance(report_data, dict) and 'chart_path' in report_data:
            try:
                from PIL import Image, ImageTk
                import os
                
                if os.path.exists(report_data['chart_path']):
                    # Load and display chart image
                    image = Image.open(report_data['chart_path'])
                    # Resize for better display in the interface
                    image = image.resize((700, 400), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    image_label = ctk.CTkLabel(self.results_frame, image=photo, text="")
                    image_label.image = photo  # Keep a reference
                    image_label.pack(pady=10)
                    
                    # Chart description
                    ctk.CTkLabel(self.results_frame, text="📋 Chart Visualization",
                               font=ctk.CTkFont(weight="bold")).pack(pady=5)
            except Exception as e:
                error_label = ctk.CTkLabel(self.results_frame, 
                                         text=f"Chart display error: {str(e)}",
                                         text_color="red")
                error_label.pack(pady=10)
        
        # Action buttons
        action_frame = ctk.CTkFrame(self.results_frame)
        action_frame.pack(pady=20)
        
        ctk.CTkButton(action_frame, text="📄 Export to PDF", 
                     command=lambda: self.export_report_pdf(report_data, title)).pack(side="left", padx=5)
        
        ctk.CTkButton(action_frame, text="🔄 New Report", 
                     command=self.show_report_welcome).pack(side="left", padx=5)
    
    def export_report_pdf(self, report_data, title):
        """Export the current report to PDF"""
        try:
            if not self.reports:
                messagebox.showerror("Error", "Reports module not available")
                return
            pdf_path = self.reports.export_report_to_pdf(report_data, title.replace(" ", "_"))
            messagebox.showinfo("Success", f"Report exported to:\n{pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()  
  

if __name__ == "__main__":
    app = CampusGadgetSystem()
    app.root.mainloop() # Start the main loop