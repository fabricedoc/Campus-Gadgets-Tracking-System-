import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib
matplotlib.use('Agg')  # For server-side plotting

class AdvancedReports:
    def __init__(self, db_path="campus_gadgets.db"):
        self.db_path = db_path
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Set style for better looking charts
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def generate_daily_activity_report(self, start_date, end_date):
        """Generate daily activity report with charts"""
        conn = self.get_connection()
        
        # Daily activity data
        daily_query = """
        SELECT 
            DATE(check_in_time) as activity_date,
            COUNT(CASE WHEN status = 'checked_in' THEN 1 END) as check_ins,
            COUNT(CASE WHEN status = 'checked_out' THEN 1 END) as check_outs,
            COUNT(*) as total_activities
        FROM check_records 
        WHERE DATE(check_in_time) BETWEEN ? AND ?
        GROUP BY DATE(check_in_time)
        ORDER BY activity_date
        """
        
        daily_df = pd.read_sql_query(daily_query, conn, params=(start_date, end_date))
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Daily activity line chart
        if not daily_df.empty:
            ax1.plot(daily_df['activity_date'], daily_df['check_ins'], marker='o', label='Check-ins', linewidth=2)
            ax1.plot(daily_df['activity_date'], daily_df['check_outs'], marker='s', label='Check-outs', linewidth=2)
            ax1.set_title('Daily Check-in/Check-out Activity', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Number of Activities')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Gadget type distribution
        gadget_query = """
        SELECT gadget_type, COUNT(*) as count
        FROM gadgets 
        WHERE created_at BETWEEN ? AND ?
        GROUP BY gadget_type
        ORDER BY count DESC
        """
        
        gadget_df = pd.read_sql_query(gadget_query, conn, params=(start_date, end_date))
        
        if not gadget_df.empty:
            ax2.pie(gadget_df['count'], labels=gadget_df['gadget_type'], autopct='%1.1f%%', startangle=90)
            ax2.set_title('Gadget Type Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Save chart
        chart_path = os.path.join(self.reports_dir, f"daily_activity_{start_date}_to_{end_date}.png")
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        conn.close()
        
        return {
            'daily_data': daily_df,
            'gadget_data': gadget_df,
            'chart_path': chart_path
        }
    
    def generate_trend_analysis_report(self, period_days=30):
        """Generate trend analysis with multiple charts"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=period_days)).strftime('%Y-%m-%d')
        
        conn = self.get_connection()
        
        # Registration trends
        trend_query = """
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as daily_registrations,
            SUM(COUNT(*)) OVER (ORDER BY DATE(created_at)) as cumulative_registrations
        FROM gadgets 
        WHERE DATE(created_at) BETWEEN ? AND ?
        GROUP BY DATE(created_at)
        ORDER BY date
        """
        
        trend_df = pd.read_sql_query(trend_query, conn, params=(start_date, end_date))
        
        # Status distribution
        status_query = """
        SELECT 
            registration_status,
            COUNT(*) as count
        FROM gadgets 
        WHERE created_at BETWEEN ? AND ?
        GROUP BY registration_status
        """
        
        status_df = pd.read_sql_query(status_query, conn, params=(start_date, end_date))
        
        # Create comprehensive visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Registration trend
        if not trend_df.empty:
            ax1.plot(trend_df['date'], trend_df['daily_registrations'], marker='o', color='blue', linewidth=2)
            ax1.set_title('Daily Registration Trend', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Registrations')
            ax1.grid(True, alpha=0.3)
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            # Cumulative trend
            ax2.plot(trend_df['date'], trend_df['cumulative_registrations'], marker='s', color='green', linewidth=2)
            ax2.set_title('Cumulative Registrations', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Total Registrations')
            ax2.grid(True, alpha=0.3)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        # Status distribution
        if not status_df.empty:
            ax3.bar(status_df['registration_status'], status_df['count'], color=['#28a745', '#ffc107', '#dc3545'])
            ax3.set_title('Registration Status Distribution', fontsize=12, fontweight='bold')
            ax3.set_xlabel('Status')
            ax3.set_ylabel('Count')
            ax3.tick_params(axis='x', rotation=45)
        
        # Hourly activity pattern
        hourly_query = """
        SELECT 
            strftime('%H', check_in_time) as hour,
            COUNT(*) as activity_count
        FROM check_records 
        WHERE DATE(check_in_time) BETWEEN ? AND ?
        GROUP BY strftime('%H', check_in_time)
        ORDER BY hour
        """
        
        hourly_df = pd.read_sql_query(hourly_query, conn, params=(start_date, end_date))
        
        if not hourly_df.empty:
            ax4.bar(hourly_df['hour'], hourly_df['activity_count'], color='orange', alpha=0.7)
            ax4.set_title('Hourly Activity Pattern', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Hour of Day')
            ax4.set_ylabel('Activity Count')
        
        plt.tight_layout()
        
        # Save chart
        chart_path = os.path.join(self.reports_dir, f"trend_analysis_{start_date}_to_{end_date}.png")
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        conn.close()
        
        return {
            'trend_data': trend_df,
            'status_data': status_df,
            'hourly_data': hourly_df,
            'chart_path': chart_path
        }
    
    def generate_comprehensive_dashboard(self):
        """Generate a comprehensive dashboard with multiple metrics"""
        conn = self.get_connection()
        
        # Overall statistics
        stats_query = """
        SELECT 
            (SELECT COUNT(*) FROM students) as total_students,
            (SELECT COUNT(*) FROM gadgets) as total_gadgets,
            (SELECT COUNT(*) FROM gadgets WHERE status = 'checked_in') as gadgets_in_campus,
            (SELECT COUNT(*) FROM gadgets WHERE registration_status = 'approved') as approved_gadgets,
            (SELECT COUNT(*) FROM gadgets WHERE registration_status = 'pending') as pending_gadgets,
            (SELECT COUNT(*) FROM check_records WHERE DATE(check_in_time) = DATE('now')) as today_activities
        """
        
        stats = pd.read_sql_query(stats_query, conn).iloc[0]
        
        # Top students with most gadgets
        top_students_query = """
        SELECT 
            s.full_name,
            s.registration_number,
            COUNT(g.id) as gadget_count
        FROM students s
        LEFT JOIN gadgets g ON s.id = g.student_id
        GROUP BY s.id
        HAVING gadget_count > 0
        ORDER BY gadget_count DESC
        LIMIT 10
        """
        
        top_students = pd.read_sql_query(top_students_query, conn)
        
        # Gadget brand popularity
        brand_query = """
        SELECT 
            brand,
            COUNT(*) as count
        FROM gadgets 
        WHERE brand IS NOT NULL AND brand != ''
        GROUP BY brand
        ORDER BY count DESC
        LIMIT 10
        """
        
        brand_popularity = pd.read_sql_query(brand_query, conn)
        
        # Create dashboard visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Statistics summary
        stats_labels = ['Total Students', 'Total Gadgets', 'In Campus', 'Approved', 'Pending', "Today's Activity"]
        stats_values = [stats['total_students'], stats['total_gadgets'], stats['gadgets_in_campus'], 
                       stats['approved_gadgets'], stats['pending_gadgets'], stats['today_activities']]
        
        bars = ax1.bar(stats_labels, stats_values, color=sns.color_palette("Set2"))
        ax1.set_title('System Overview Statistics', fontsize=14, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, stats_values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    int(value), ha='center', va='bottom', fontweight='bold')
        
        # Top students
        if not top_students.empty:
            ax2.barh(top_students['full_name'], top_students['gadget_count'], color='lightblue')
            ax2.set_title('Top Students by Gadget Count', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Number of Gadgets')
        
        # Brand popularity
        if not brand_popularity.empty:
            ax3.bar(brand_popularity['brand'], brand_popularity['count'], color='lightgreen')
            ax3.set_title('Top Gadget Brands', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Brand')
            ax3.set_ylabel('Count')
            ax3.tick_params(axis='x', rotation=45)
        
        # Registration status pie chart
        status_counts = [stats['approved_gadgets'], stats['pending_gadgets']]
        status_labels = ['Approved', 'Pending']
        ax4.pie(status_counts, labels=status_labels, autopct='%1.1f%%', startangle=90)
        ax4.set_title('Registration Status Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Save dashboard
        dashboard_path = os.path.join(self.reports_dir, f"comprehensive_dashboard_{datetime.now().strftime('%Y%m%d')}.png")
        plt.savefig(dashboard_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        conn.close()
        
        return {
            'statistics': stats.to_dict(),
            'top_students': top_students,
            'brand_popularity': brand_popularity,
            'dashboard_path': dashboard_path
        }
    
    def generate_student_activity_report(self, registration_number=None):
        """Generate individual student activity report"""
        conn = self.get_connection()
        
        if registration_number:
            # Specific student report
            student_query = """
            SELECT 
                s.full_name,
                s.registration_number,
                s.national_id,
                COUNT(g.id) as total_gadgets,
                COUNT(CASE WHEN g.registration_status = 'approved' THEN 1 END) as approved_gadgets,
                COUNT(CASE WHEN g.status = 'checked_in' THEN 1 END) as gadgets_in_campus
            FROM students s
            LEFT JOIN gadgets g ON s.id = g.student_id
            WHERE s.registration_number = ?
            GROUP BY s.id
            """
            
            student_data = pd.read_sql_query(student_query, conn, params=(registration_number,))
            
            if not student_data.empty:
                student_gadgets_query = """
                SELECT 
                    g.record_number,
                    g.gadget_type,
                    g.brand,
                    g.model,
                    g.serial_number,
                    g.registration_status,
                    g.status,
                    g.created_at
                FROM gadgets g
                JOIN students s ON g.student_id = s.id
                WHERE s.registration_number = ?
                ORDER BY g.created_at DESC
                """
                
                gadgets_data = pd.read_sql_query(student_gadgets_query, conn, params=(registration_number,))
                
                # Create student report visualization
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
                
                # Gadget status
                status_counts = gadgets_data['registration_status'].value_counts()
                ax1.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
                ax1.set_title('Gadget Registration Status', fontweight='bold')
                
                # Gadget types
                type_counts = gadgets_data['gadget_type'].value_counts()
                ax2.bar(type_counts.index, type_counts.values, color=sns.color_palette("Set3"))
                ax2.set_title('Gadget Types', fontweight='bold')
                ax2.tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                
                chart_path = os.path.join(self.reports_dir, f"student_report_{registration_number}.png")
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                
                return {
                    'student_info': student_data.iloc[0].to_dict(),
                    'gadgets_list': gadgets_data,
                    'chart_path': chart_path
                }
        
        conn.close()
        return None
    
    def export_report_to_pdf(self, report_data, report_type, filename=None):
        """Export report to PDF format"""
        if not filename:
            filename = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join(self.reports_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph(f"Campus Gadget System - {report_type.replace('_', ' ').title()}", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Report date
        date_text = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(date_text)
        story.append(Spacer(1, 20))
        
        # Add chart if exists
        if 'chart_path' in report_data and os.path.exists(report_data['chart_path']):
            chart_img = Image(report_data['chart_path'], width=6*inch, height=4*inch)
            story.append(chart_img)
            story.append(Spacer(1, 20))
        
        # Add data tables
        for key, data in report_data.items():
            if isinstance(data, pd.DataFrame) and not data.empty:
                # Convert DataFrame to table
                table_data = [data.columns.tolist()] + data.values.tolist()
                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(Paragraph(key.replace('_', ' ').title(), styles['Heading2']))
                story.append(table)
                story.append(Spacer(1, 12))
        
        doc.build(story)
        return filepath
    
    def get_available_reports(self):
        """Get list of available generated reports"""
        reports = []
        for file in os.listdir(self.reports_dir):
            if file.endswith('.pdf'):
                reports.append({
                    'filename': file,
                    'filepath': os.path.join(self.reports_dir, file),
                    'created_time': os.path.getctime(os.path.join(self.reports_dir, file))
                })
        
        return sorted(reports, key=lambda x: x['created_time'], reverse=True)

# Example usage and testing
if __name__ == "__main__":
    reports = AdvancedReports()
    
    # Test different reports
    print("Generating sample reports...")
    
    # Daily activity report
    daily_report = reports.generate_daily_activity_report('2024-01-01', '2024-12-31')
    reports.export_report_to_pdf(daily_report, "Daily_Activity_Report")
    
    # Trend analysis
    trend_report = reports.generate_trend_analysis_report(30)
    reports.export_report_to_pdf(trend_report, "Trend_Analysis_Report")
    
    # Comprehensive dashboard
    dashboard_report = reports.generate_comprehensive_dashboard()
    reports.export_report_to_pdf(dashboard_report, "Comprehensive_Dashboard")
    
    print("Sample reports generated successfully!")
    print("Available reports:", [r['filename'] for r in reports.get_available_reports()])