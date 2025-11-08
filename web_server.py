from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
from datetime import datetime
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'web_uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect('campus_gadgets.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_web_database():
    """Ensure database has web-specific fields"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Add web-specific fields if they don't exist
    try:
        cursor.execute("PRAGMA table_info(gadgets)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'web_registered' not in columns:
            cursor.execute("ALTER TABLE gadgets ADD COLUMN web_registered BOOLEAN DEFAULT 0")
        
        if 'registration_status' not in columns:
            cursor.execute("ALTER TABLE gadgets ADD COLUMN registration_status TEXT DEFAULT 'pending'")
            
    except Exception as e:
        print(f"Database initialization warning: {e}")
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get form data
            student_data = {
                'full_name': request.form.get('full_name', '').strip(),
                'registration_number': request.form.get('registration_number', '').strip().upper(),
                'national_id': request.form.get('national_id', '').strip()
            }
            
            gadget_data = {
                'gadget_type': request.form.get('gadget_type', '').strip(),
                'brand': request.form.get('brand', '').strip(),
                'model': request.form.get('model', '').strip(),
                'serial_number': request.form.get('serial_number', '').strip(),
                'color': request.form.get('color', '').strip(),
                'additional_details': request.form.get('additional_details', '').strip()
            }
            
            # Validate required fields
            required_student = ['full_name', 'registration_number', 'national_id']
            required_gadget = ['gadget_type', 'brand', 'model', 'serial_number']
            
            for field in required_student:
                if not student_data[field]:
                    return jsonify({'success': False, 'message': f'Please fill in {field.replace("_", " ").title()}'})
            
            for field in required_gadget:
                if not gadget_data[field]:
                    return jsonify({'success': False, 'message': f'Please fill in gadget {field.replace("_", " ").title()}'})
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if serial number already exists
            cursor.execute("SELECT id FROM gadgets WHERE serial_number = ?", (gadget_data['serial_number'],))
            if cursor.fetchone():
                conn.close()
                return jsonify({'success': False, 'message': 'This serial number is already registered'})
            
            # Check if student exists
            cursor.execute("SELECT id FROM students WHERE registration_number = ?", (student_data['registration_number'],))
            student = cursor.fetchone()
            
            if student:
                student_id = student[0]
                # Update student info
                cursor.execute('''
                    UPDATE students SET full_name = ?, national_id = ? 
                    WHERE id = ?
                ''', (student_data['full_name'], student_data['national_id'], student_id))
            else:
                # Create new student
                cursor.execute('''
                    INSERT INTO students (full_name, registration_number, national_id)
                    VALUES (?, ?, ?)
                ''', (student_data['full_name'], student_data['registration_number'], student_data['national_id']))
                student_id = cursor.lastrowid
            
            # Handle file uploads
            photos_dir = "student_photos"
            os.makedirs(photos_dir, exist_ok=True)
            web_uploads_dir = app.config['UPLOAD_FOLDER']
            os.makedirs(web_uploads_dir, exist_ok=True)
            
            passport_filename = None
            card_filename = None
            gadget_filename = None
            
            # Process passport photo
            if 'passport_photo' in request.files:
                file = request.files['passport_photo']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"{student_data['registration_number']}_passport_{datetime.now().strftime('%Y%m%d%H%M%S')}{os.path.splitext(file.filename)[1]}")
                    file_path = os.path.join(web_uploads_dir, filename)
                    file.save(file_path)
                    passport_filename = os.path.join(photos_dir, filename)
                    shutil.copy2(file_path, passport_filename)
            
            # Process student card photo
            if 'student_card_photo' in request.files:
                file = request.files['student_card_photo']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"{student_data['registration_number']}_card_{datetime.now().strftime('%Y%m%d%H%M%S')}{os.path.splitext(file.filename)[1]}")
                    file_path = os.path.join(web_uploads_dir, filename)
                    file.save(file_path)
                    card_filename = os.path.join(photos_dir, filename)
                    shutil.copy2(file_path, card_filename)
            
            # Process gadget photo
            if 'gadget_photo' in request.files:
                file = request.files['gadget_photo']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"{student_data['registration_number']}_{gadget_data['serial_number']}_gadget_{datetime.now().strftime('%Y%m%d%H%M%S')}{os.path.splitext(file.filename)[1]}")
                    file_path = os.path.join(web_uploads_dir, filename)
                    file.save(file_path)
                    gadget_filename = os.path.join(photos_dir, filename)
                    shutil.copy2(file_path, gadget_filename)
            
            # Generate record number
            record_number = f"WEB{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Register gadget (pending approval)
            cursor.execute('''
                INSERT INTO gadgets (student_id, record_number, gadget_type, brand, model, 
                                  serial_number, color, additional_details, passport_photo, 
                                  student_card_photo, gadget_photo, web_registered, registration_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, record_number, gadget_data['gadget_type'], gadget_data['brand'], 
                  gadget_data['model'], gadget_data['serial_number'], gadget_data['color'],
                  gadget_data['additional_details'], passport_filename, card_filename, 
                  gadget_filename, 1, 'pending'))
            
            gadget_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True, 
                'message': 'Gadget registration submitted successfully! Your registration is pending approval from campus security.',
                'record_number': record_number
            })
            
        except sqlite3.IntegrityError as e:
            return jsonify({'success': False, 'message': 'Registration number or serial number already exists'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'})
    
    return render_template('register.html')

@app.route('/check-status', methods=['GET', 'POST'])
def check_status():
    if request.method == 'POST':
        registration_number = request.form.get('registration_number', '').strip().upper()
        serial_number = request.form.get('serial_number', '').strip()
        
        if not registration_number or not serial_number:
            return render_template('status.html', error='Please provide both registration number and serial number')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT g.record_number, s.full_name, g.gadget_type, g.brand, g.model, 
                   g.registration_status, g.created_at
            FROM gadgets g
            JOIN students s ON g.student_id = s.id
            WHERE s.registration_number = ? AND g.serial_number = ?
        ''', (registration_number, serial_number))
        
        gadget = cursor.fetchone()
        conn.close()
        
        if gadget:
            return render_template('status.html', gadget=dict(gadget))
        else:
            return render_template('status.html', error='No registration found with the provided details')
    
    return render_template('status.html')

@app.route('/api/pending-registrations')
def get_pending_registrations():
    """API endpoint for desktop app to get pending registrations"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT g.id, g.record_number, s.full_name, s.registration_number, 
               g.gadget_type, g.brand, g.model, g.serial_number, g.color,
               g.additional_details, g.passport_photo, g.student_card_photo, 
               g.gadget_photo, g.created_at
        FROM gadgets g
        JOIN students s ON g.student_id = s.id
        WHERE g.registration_status = 'pending' AND g.web_registered = 1
        ORDER BY g.created_at DESC
    ''')
    
    pending = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(pending)

@app.route('/api/approve-registration/<int:gadget_id>', methods=['POST'])
def approve_registration(gadget_id):
    """API endpoint for desktop app to approve a registration"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Update registration status
        cursor.execute('''
            UPDATE gadgets SET registration_status = 'approved' 
            WHERE id = ?
        ''', (gadget_id,))
        
        # Create initial check-in record
        cursor.execute('''
            INSERT INTO check_records (gadget_id, check_in_time, status)
            SELECT id, created_at, 'checked_in' FROM gadgets WHERE id = ?
        ''', (gadget_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Registration approved successfully'})
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'success': False, 'message': str(e)})
# Add these routes to your existing web_server.py



@app.route('/api/register', methods=['POST'])
def register_gadget():
    """API endpoint for web form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['student_name', 'registration_number', 'national_id', 
                          'gadget_type', 'brand', 'model', 'serial_number']
        
        for field in required_fields:
            if not data.get(field) or not str(data[field]).strip():
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check for duplicates
        cursor.execute('SELECT id FROM web_registrations WHERE serial_number = ?', (data['serial_number'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Serial number already registered'}), 400
        
        # Insert registration
        cursor.execute('''
            INSERT INTO web_registrations 
            (student_name, registration_number, national_id, gadget_type, brand, model, serial_number, color, additional_details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['student_name'].strip(),
            data['registration_number'].strip(),
            data['national_id'].strip(),
            data['gadget_type'].strip(),
            data['brand'].strip(),
            data['model'].strip(),
            data['serial_number'].strip(),
            data.get('color', '').strip(),
            data.get('additional_details', '').strip()
        ))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Registration submitted successfully!',
            'id': record_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500
@app.route('/api/reject-registration/<int:gadget_id>', methods=['POST'])
def reject_registration(gadget_id):
    """API endpoint for desktop app to reject a registration"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE gadgets SET registration_status = 'rejected' 
            WHERE id = ?
        ''', (gadget_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Registration rejected'})
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'success': False, 'message': str(e)})

# web_server.py - PRODUCTION VERSION
from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from datetime import datetime
from flask_cors import CORS  # Add this import

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

# Use environment variable for database or default
DB_PATH = os.environ.get('DATABASE_URL', 'campus_gadgets_online.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')  # You'll create this

@app.route('/api/register', methods=['POST'])
def register_gadget():
    # Your existing registration logic
    pass

@app.route('/api/pending-registrations', methods=['GET'])
def get_pending_registrations():
    # Your existing pending registrations logic
    pass

# Add security middleware
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    init_web_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
