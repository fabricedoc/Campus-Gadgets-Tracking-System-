import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from datetime import datetime, timedelta
import os
from reports_module import AdvancedReports
from PIL import Image, ImageTk

class ReportsGUI:
    def __init__(self, parent=None):
        self.parent = parent
        self.reports = AdvancedReports()
        
        if parent is None:
            self.root = ctk.CTk()
            self.root.title("Advanced Reports - Campus Gadget System")
            self.root.geometry("1200x800")
            self.setup_ui()
        else:
            self.setup_ui_in_parent(parent)
    
    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.setup_ui_in_parent(main_frame)
        
        # Run the application
        self.root.mainloop()
    
    def setup_ui_in_parent(self, parent):
        # Title
        title_label = ctk.CTkLabel(parent, text="📊 Advanced Reports & Analytics", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)
        
        # Report selection frame
        selection_frame = ctk.CTkFrame(parent)
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(selection_frame, text="Select Report Type:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=10)
        
        # Report type buttons
        report_types_frame = ctk.CTkFrame(selection_frame)
        report_types_frame.pack(fill="x", pady=10)
        
        report_types = [
            ("📈 Daily Activity Report", self.generate_daily_report),
            ("📊 Trend Analysis", self.generate_trend_report),
            ("🏆 Comprehensive Dashboard", self.generate_dashboard),
            ("👨‍🎓 Student Report", self.generate_student_report)
        ]
        
        for i, (text, command) in enumerate(report_types):
            btn = ctk.CTkButton(report_types_frame, text=text, command=command,
                               height=40, font=ctk.CTkFont(size=12))
            btn.pack(side="left", expand=True, padx=5)
        
        # Date range frame (for date-specific reports)
        self.date_frame = ctk.CTkFrame(parent)
        self.date_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.date_frame, text="Date Range:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=5)
        
        date_input_frame = ctk.CTkFrame(self.date_frame)
        date_input_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(date_input_frame, text="From:", width=60).pack(side="left", padx=5)
        self.start_date_entry = ctk.CTkEntry(date_input_frame, placeholder_text="YYYY-MM-DD")
        self.start_date_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(date_input_frame, text="To:", width=60).pack(side="left", padx=5)
        self.end_date_entry = ctk.CTkEntry(date_input_frame, placeholder_text="YYYY-MM-DD")
        self.end_date_entry.pack(side="left", padx=5)
        
        # Set default dates (last 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        self.start_date_entry.insert(0, start_date.strftime('%Y-%m-%d'))
        self.end_date_entry.insert(0, end_date.strftime('%Y-%m-%d'))
        
        # Student search frame
        self.student_frame = ctk.CTkFrame(parent)
        self.student_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.student_frame, text="Student Registration Number:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=5)
        
        student_input_frame = ctk.CTkFrame(self.student_frame)
        student_input_frame.pack(fill="x", pady=5)
        
        self.student_reg_entry = ctk.CTkEntry(student_input_frame, placeholder_text="Enter registration number")
        self.student_reg_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Results area
        self.results_frame = ctk.CTkFrame(parent)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initially hide student frame
        self.student_frame.pack_forget()
    
    def generate_daily_report(self):
        try:
            start_date = self.start_date_entry.get().strip()
            end_date = self.end_date_entry.get().strip()
            
            if not start_date or not end_date:
                messagebox.showerror("Error", "Please enter both start and end dates")
                return
            
            # Show loading
            self.show_loading("Generating Daily Activity Report...")
            
            # Generate report
            report_data = self.reports.generate_daily_activity_report(start_date, end_date)
            
            # Export to PDF
            pdf_path = self.reports.export_report_to_pdf(report_data, "Daily_Activity_Report")
            
            # Display results
            self.display_report_results(report_data, pdf_path, "Daily Activity Report")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_trend_report(self):
        try:
            # Show loading
            self.show_loading("Generating Trend Analysis Report...")
            
            # Generate report (last 30 days)
            report_data = self.reports.generate_trend_analysis_report(30)
            
            # Export to PDF
            pdf_path = self.reports.export_report_to_pdf(report_data, "Trend_Analysis_Report")
            
            # Display results
            self.display_report_results(report_data, pdf_path, "Trend Analysis Report")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_dashboard(self):
        try:
            # Show loading
            self.show_loading("Generating Comprehensive Dashboard...")
            
            # Generate dashboard
            report_data = self.reports.generate_comprehensive_dashboard()
            
            # Export to PDF
            pdf_path = self.reports.export_report_to_pdf(report_data, "Comprehensive_Dashboard")
            
            # Display results
            self.display_report_results(report_data, pdf_path, "Comprehensive Dashboard")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate dashboard: {str(e)}")
    
    def generate_student_report(self):
        try:
            registration_number = self.student_reg_entry.get().strip()
            
            if not registration_number:
                messagebox.showerror("Error", "Please enter a registration number")
                return
            
            # Show loading
            self.show_loading(f"Generating Report for {registration_number}...")
            
            # Generate student report
            report_data = self.reports.generate_student_activity_report(registration_number)
            
            if report_data:
                # Export to PDF
                pdf_path = self.reports.export_report_to_pdf(report_data, f"Student_Report_{registration_number}")
                
                # Display results
                self.display_report_results(report_data, pdf_path, f"Student Report - {registration_number}")
            else:
                messagebox.showwarning("Not Found", f"No student found with registration number: {registration_number}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate student report: {str(e)}")
    
    def show_loading(self, message):
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        loading_label = ctk.CTkLabel(self.results_frame, text=message, 
                                   font=ctk.CTkFont(size=16))
        loading_label.pack(expand=True)
        
        self.results_frame.update()
    
    def display_report_results(self, report_data, pdf_path, title):
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_label = ctk.CTkLabel(self.results_frame, text=f"📊 {title}", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=10)
        
        # PDF path info
        pdf_info = ctk.CTkLabel(self.results_frame, 
                               text=f"Report saved as: {os.path.basename(pdf_path)}",
                               font=ctk.CTkFont(size=12))
        pdf_info.pack(pady=5)
        
        # Display chart if available
        if 'chart_path' in report_data and os.path.exists(report_data['chart_path']):
            try:
                # Load and display chart image
                image = Image.open(report_data['chart_path'])
                image = image.resize((800, 500), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                image_label = ctk.CTkLabel(self.results_frame, image=photo, text="")
                image_label.image = photo  # Keep a reference
                image_label.pack(pady=10)
            except Exception as e:
                error_label = ctk.CTkLabel(self.results_frame, 
                                         text=f"Could not display chart: {str(e)}",
                                         text_color="red")
                error_label.pack(pady=10)
        
        # Summary statistics
        if 'statistics' in report_data:
            stats_frame = ctk.CTkFrame(self.results_frame)
            stats_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(stats_frame, text="Key Statistics:", 
                        font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=5)
            
            stats = report_data['statistics']
            for key, value in stats.items():
                stat_frame = ctk.CTkFrame(stats_frame)
                stat_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(stat_frame, text=key.replace('_', ' ').title() + ":", 
                           width=150, anchor="w").pack(side="left", padx=5)
                ctk.CTkLabel(stat_frame, text=str(value)).pack(side="left", padx=5)
        
        # Action buttons
        action_frame = ctk.CTkFrame(self.results_frame)
        action_frame.pack(pady=20)
        
        ctk.CTkButton(action_frame, text="📁 Open Report Folder", 
                     command=self.open_reports_folder).pack(side="left", padx=5)
        
        ctk.CTkButton(action_frame, text="🔄 Generate Another Report", 
                     command=self.clear_results).pack(side="left", padx=5)
    
    def open_reports_folder(self):
        try:
            reports_dir = os.path.abspath("reports")
            if os.path.exists(reports_dir):
                os.startfile(reports_dir)  # Windows
            else:
                messagebox.showinfo("Info", "Reports directory not found")
        except:
            messagebox.showerror("Error", "Could not open reports folder")
    
    def clear_results(self):
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Show welcome message
        welcome_label = ctk.CTkLabel(self.results_frame, 
                                   text="Select a report type from above to generate analytics",
                                   font=ctk.CTkFont(size=14))
        welcome_label.pack(expand=True)

# Integration with main application
def add_reports_to_main_app(main_app):
    """Add reports functionality to the main campus gadget application"""
    def show_advanced_reports():
        main_app.clear_content()
        
        ctk.CTkLabel(main_app.content_frame, text="📊 Advanced Reports & Analytics", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Create reports GUI within main app
        reports_gui = ReportsGUI()
        reports_gui.setup_ui_in_parent(main_app.content_frame)
    
    return show_advanced_reports

# Standalone testing
if __name__ == "__main__":
    app = ReportsGUI()