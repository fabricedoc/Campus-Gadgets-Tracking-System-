# Campus Gadget System - User Manual

## Quick Start
1. **For Security Staff**: Run `main.py` for desktop application
2. **For Students**: Access http://localhost:8080 in web browser
3. **Default Admin Login**: admin / admin123

## Features
### Desktop Application (Security Staff)
- Register gadgets manually
- Check in/out operations  
- Approve web registrations
- Generate reports
- User management

### Web Interface (Students)
- Self-register gadgets online
- Check registration status
- Upload required documents

## Daily Operations
1. Start web server: `python production_server.py`
2. Start desktop app: `python main.py`
3. Monitor system through desktop interface
4. Regular backups are automatic

## Troubleshooting
- **Web server not starting**: Check port 8080 is available
- **Database errors**: Restore from backup
- **Login issues**: Reset password through admin account