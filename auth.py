import hashlib
from database import Database

class AuthSystem:
    def __init__(self):
        self.db = Database()
        self.current_user = None
    
    def login(self, username, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT id, name, username, role FROM users 
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.current_user = {
                'id': user[0],
                'name': user[1],
                'username': user[2],
                'role': user[3]
            }
            return True
        return False
    
    def logout(self):
        self.current_user = None
    
    def is_authenticated(self):
        return self.current_user is not None
    
    def is_admin(self):
        return self.current_user and self.current_user['role'] == 'admin'