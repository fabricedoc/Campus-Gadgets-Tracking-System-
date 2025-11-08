# Campus Gadget System - Deployment Checklist

## Pre-Deployment
- [ ] Test all features locally
- [ ] Backup existing data
- [ ] Update configuration files
- [ ] Install on target machine

## Installation Steps
1. Copy all files to target machine
2. Run `install.bat` (Windows) or equivalent setup script
3. Configure network settings if needed
4. Test both desktop and web interfaces

## Security Considerations
- [ ] Change default admin password
- [ ] Configure firewall if needed
- [ ] Set up regular backups
- [ ] Limit physical access to server

## Network Configuration
- Web Interface: http://localhost:8080 (local)
- For network access: Configure firewall to allow port 8080
- Desktop app runs independently

## Maintenance
- Regular backups (automated)
- Monitor log files
- Update software periodically
- Train staff on usage