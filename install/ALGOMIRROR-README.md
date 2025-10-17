# AlgoMirror Installation Guide

## Overview

**AlgoMirror** is a proprietary enterprise-grade multi-account management platform that provides a unified interface to manage multiple OpenAlgo trading accounts from different brokers.

### Key Features
- ✅ Manage 20+ OpenAlgo accounts from single dashboard
- ✅ Support for 22+ brokers (all OpenAlgo-supported brokers)
- ✅ Real-time connection monitoring with ping API
- ✅ Unified funds, positions, orders, holdings view
- ✅ Military-grade encryption for API keys (Fernet AES-128)
- ✅ Single-user security model (first user = admin)
- ✅ Rate limiting and CSRF protection
- ✅ SSL/TLS with Let's Encrypt
- ✅ Production-ready with Gunicorn + Nginx

---

## Architecture

```
AlgoMirror (Port 8000)
├── Manages Multiple OpenAlgo Accounts
│   ├── OpenAlgo Instance 1 (Zerodha) → Port 5000
│   ├── OpenAlgo Instance 2 (Fyers) → Port 5001
│   ├── OpenAlgo Instance 3 (Angel) → Port 5002
│   └── OpenAlgo Instance N...
│
└── Features
    ├── Unified Dashboard
    ├── Connection Monitoring
    ├── Consolidated Views
    └── Encrypted API Keys
```

---

## Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ or Debian 11+
- **RAM**: 2GB minimum (4GB+ recommended)
- **Storage**: 10GB+ available
- **CPU**: 1+ core

### Domain Setup
1. **DNS Configuration**
   ```
   algomirror.example.com → Your Server IP
   ```

2. **Wait for DNS Propagation** (5-60 minutes)

### OpenAlgo Instances
- AlgoMirror **connects to** OpenAlgo instances
- You need at least one OpenAlgo instance running
- See `openalgo1/install/` for OpenAlgo installation scripts

---

## Installation

### Step 1: Download Installation Script

```bash
# Create installation directory
mkdir -p ~/algomirror-install
cd ~/algomirror-install

# Download installation script
# (Update URL when repository is public)
wget https://raw.githubusercontent.com/marketcalls/algomirror/main/install/install-algomirror.sh

# Make executable
chmod +x install-algomirror.sh
```

### Step 2: Run Installation

```bash
sudo ./install-algomirror.sh
```

The installer will prompt for:
1. **Domain name** (e.g., algomirror.yourdomain.com)
2. **Default OpenAlgo host** (optional, e.g., http://127.0.0.1:5000)
3. **Default OpenAlgo WebSocket** (optional, e.g., ws://127.0.0.1:8765)

### Step 3: Installation Process

The script automatically:
- ✅ Updates system packages
- ✅ Installs Python, Nginx, Node.js, npm
- ✅ Installs uv package manager
- ✅ Configures firewall (UFW)
- ✅ Creates virtual environment
- ✅ Installs Python dependencies
- ✅ Builds Tailwind CSS
- ✅ Generates security keys
- ✅ Configures environment variables
- ✅ Initializes SQLite database
- ✅ Sets up Nginx reverse proxy
- ✅ Obtains SSL certificate (Let's Encrypt)
- ✅ Creates systemd service
- ✅ Starts AlgoMirror service

---

## Post-Installation

### Step 1: Register Admin Account

🚨 **CRITICAL**: AlgoMirror is a **SINGLE-USER** application!

1. **Visit**: https://algomirror.yourdomain.com
2. **Register**: First user becomes admin automatically
3. **After first registration**: ALL future registrations are BLOCKED

**Important**: Register immediately after installation to secure your instance!

### Step 2: Add OpenAlgo Accounts

1. Navigate to **Accounts** → **Add Account**
2. Fill in details:
   - Account name (e.g., "Zerodha Trading")
   - OpenAlgo host URL (e.g., https://trade1.example.com)
   - WebSocket URL (e.g., wss://trade1.example.com/ws)
   - API key (from OpenAlgo account)
3. Click **Test Connection** to verify
4. Save account

Repeat for all your OpenAlgo instances.

### Step 3: Verify Installation

```bash
# Check service status
sudo systemctl status algomirror

# View logs
sudo journalctl -u algomirror -n 50

# Check Nginx
sudo nginx -t
sudo systemctl status nginx

# Test web access
curl -k https://algomirror.yourdomain.com
```

---

## Configuration

### Environment Variables

Located in: `/var/python/algomirror/app/.env`

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY='your-secret-key'

# Database (SQLite by default)
DATABASE_URL=sqlite:////var/python/algomirror/instance/algomirror.db

# Encryption Key (Fernet)
ENCRYPTION_KEY='your-fernet-key'

# CORS
CORS_ORIGINS=https://algomirror.yourdomain.com

# Default OpenAlgo (used in forms)
DEFAULT_OPENALGO_HOST=http://127.0.0.1:5000
DEFAULT_OPENALGO_WS=ws://127.0.0.1:8765

# Ping Monitoring
PING_MONITORING_ENABLED=true
PING_MONITORING_INTERVAL=30
PING_MAX_FAILURES=3

# Security
WTF_CSRF_SSL_STRICT=True
SESSION_COOKIE_SECURE=True
```

### Changing Configuration

```bash
# Edit environment
sudo nano /var/python/algomirror/app/.env

# Restart service
sudo systemctl restart algomirror
```

---

## File Structure

```
/var/python/algomirror/
├── app/                    # Application code
│   ├── accounts/          # Account management
│   ├── api/               # REST API endpoints
│   ├── auth/              # Authentication
│   ├── main/              # Dashboard
│   ├── trading/           # Trading views
│   ├── strategy/          # Strategy builder
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, images
│   │   └── css/           # Compiled Tailwind CSS
│   └── models.py          # Database models
├── venv/                   # Python virtual environment
├── instance/               # SQLite database
│   └── algomirror.db      # Main database
├── logs/                   # Application logs
│   ├── access.log
│   ├── error.log
│   └── algomirror.log
├── .env                    # Environment configuration
└── algomirror.sock        # Unix socket for Nginx
```

---

## Management Commands

### Service Management

```bash
# Start AlgoMirror
sudo systemctl start algomirror

# Stop AlgoMirror
sudo systemctl stop algomirror

# Restart AlgoMirror
sudo systemctl restart algomirror

# Check status
sudo systemctl status algomirror

# Enable auto-start on boot
sudo systemctl enable algomirror
```

### Viewing Logs

```bash
# View systemd logs (last 50 lines)
sudo journalctl -u algomirror -n 50

# Follow logs in real-time
sudo journalctl -u algomirror -f

# View application logs
tail -f /var/python/algomirror/logs/algomirror.log

# View Nginx logs
tail -f /var/log/nginx/algomirror_access.log
tail -f /var/log/nginx/algomirror_error.log
```

### Database Management

```bash
# Backup database
sudo cp /var/python/algomirror/instance/algomirror.db \
       ~/algomirror_backup_$(date +%Y%m%d).db

# View database
sqlite3 /var/python/algomirror/instance/algomirror.db
# Inside SQLite:
.tables          # List tables
.schema User     # View table schema
SELECT * FROM user;  # Query data
.quit            # Exit
```

### SSL Certificate Management

```bash
# Check certificate expiry
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Test renewal (dry run)
sudo certbot renew --dry-run
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status algomirror

# View detailed logs
sudo journalctl -u algomirror -n 100

# Check for socket file
ls -la /var/python/algomirror/algomirror.sock

# Remove stale socket
sudo rm /var/python/algomirror/algomirror.sock
sudo systemctl restart algomirror
```

### 502 Bad Gateway

```bash
# Check if service is running
sudo systemctl status algomirror

# Restart service and Nginx
sudo systemctl restart algomirror
sudo systemctl restart nginx

# Check Nginx logs
tail -f /var/log/nginx/algomirror_error.log
```

### Database Errors

```bash
# Stop service
sudo systemctl stop algomirror

# Check database integrity
sqlite3 /var/python/algomirror/instance/algomirror.db "PRAGMA integrity_check;"

# Restore from backup if needed
sudo cp ~/algomirror_backup_YYYYMMDD.db \
       /var/python/algomirror/instance/algomirror.db

# Fix permissions
sudo chown www-data:www-data /var/python/algomirror/instance/algomirror.db

# Restart
sudo systemctl start algomirror
```

### Connection Issues with OpenAlgo

1. **Verify OpenAlgo is running**:
   ```bash
   curl -k https://trade1.example.com/api/v1/ping \
     -H "Content-Type: application/json" \
     -d '{"apikey":"your_api_key"}'
   ```

2. **Check network connectivity**:
   ```bash
   # From AlgoMirror server
   curl -v https://trade1.example.com
   ```

3. **Verify API key is correct**:
   - Login to OpenAlgo
   - Go to Settings → API Key
   - Copy correct API key
   - Update in AlgoMirror

4. **Test from AlgoMirror**:
   - Go to Accounts
   - Click "Test Connection" on account
   - Check error message

---

## Security Best Practices

### 1. Encryption Key Management

🔐 **Critical**: Your encryption key is stored in `.env`

```bash
# View encryption key (KEEP SAFE!)
grep ENCRYPTION_KEY /var/python/algomirror/app/.env
```

**What it encrypts:**
- All OpenAlgo API keys in database
- Sensitive account credentials

**If lost:**
- Cannot decrypt existing API keys
- Must re-add all accounts

**Backup:**
```bash
# Backup .env file
sudo cp /var/python/algomirror/app/.env \
       ~/algomirror_env_backup_$(date +%Y%m%d).env
```

### 2. Firewall Configuration

```bash
# Check firewall status
sudo ufw status

# Only allow necessary ports
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 3. Regular Backups

```bash
# Create backup script
cat > ~/backup_algomirror.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/algomirror_backups
mkdir -p $BACKUP_DIR
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
cp /var/python/algomirror/instance/algomirror.db \
   $BACKUP_DIR/algomirror_${DATE}.db

# Backup .env
cp /var/python/algomirror/app/.env \
   $BACKUP_DIR/env_${DATE}.backup

# Keep last 7 days only
find $BACKUP_DIR -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

chmod +x ~/backup_algomirror.sh

# Run daily at 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup_algomirror.sh") | crontab -
```

### 4. Update Security

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python dependencies
cd /var/python/algomirror
source venv/bin/activate
pip list --outdated
# Review and update carefully
```

---

## Updating AlgoMirror

### Standard Update

```bash
# Stop service
sudo systemctl stop algomirror

# Backup everything
sudo cp -r /var/python/algomirror /var/python/algomirror_backup_$(date +%Y%m%d)

# Pull latest code
cd /var/python/algomirror/app
sudo git pull

# Update dependencies
cd /var/python/algomirror
source venv/bin/activate
uv pip install -r app/requirements.txt

# Rebuild CSS
cd app
npm install
npm run build-css

# Run migrations if needed
flask db upgrade

# Restart service
sudo systemctl start algomirror
```

### Rollback if Issues

```bash
# Stop service
sudo systemctl stop algomirror

# Restore backup
sudo rm -rf /var/python/algomirror
sudo mv /var/python/algomirror_backup_YYYYMMDD /var/python/algomirror

# Restart
sudo systemctl start algomirror
```

---

## Production Optimization

### 1. PostgreSQL (Recommended for Production)

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE algomirror_prod;
CREATE USER algomirror WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE algomirror_prod TO algomirror;
\q

# Update .env
DATABASE_URL=postgresql://algomirror:your_secure_password@localhost:5432/algomirror_prod

# Run migrations
cd /var/python/algomirror/app
source ../venv/bin/activate
flask db upgrade

# Restart
sudo systemctl restart algomirror
```

### 2. Redis (For Production Rate Limiting)

```bash
# Install Redis
sudo apt install redis-server

# Configure Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Update .env
REDIS_URL=redis://localhost:6379/0
SESSION_TYPE=redis

# Restart AlgoMirror
sudo systemctl restart algomirror
```

### 3. Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop

# Monitor resources
htop

# Monitor disk usage
df -h
du -sh /var/python/algomirror/*
```

---

## FAQ

**Q: Can I run multiple AlgoMirror instances?**
A: Technically yes, but typically one AlgoMirror manages all your OpenAlgo accounts. Use different subdomains if needed.

**Q: How many OpenAlgo accounts can I manage?**
A: Unlimited. Tested with 50+ accounts.

**Q: Does AlgoMirror replace OpenAlgo?**
A: No. AlgoMirror is a **management interface** for multiple OpenAlgo instances. You still need OpenAlgo for broker connections.

**Q: Can I add multiple users?**
A: No. AlgoMirror is intentionally single-user for security. First user = admin, all future registrations blocked.

**Q: What if I forget admin password?**
A: Reset via database:
```bash
cd /var/python/algomirror/app
source ../venv/bin/activate
flask shell
>>> from app.models import User
>>> user = User.query.first()
>>> user.set_password('new_password')
>>> db.session.commit()
>>> exit()
```

**Q: Can I use custom domain (not subdomain)?**
A: Yes. Use `algomirror.com` instead of `algomirror.example.com` during installation.

**Q: Is my data encrypted?**
A: Yes. All API keys are encrypted using Fernet (AES-128). Encryption key is in `.env` file.

**Q: Can I migrate to different server?**
A: Yes. Backup `/var/python/algomirror` directory and `.env` file. Restore on new server and restart service.

---

## Support

For issues and support:
- **GitHub**: https://github.com/marketcalls/algomirror (when available)
- **Documentation**: This file
- **Logs**: Check systemd and application logs
- **OpenAlgo Docs**: For OpenAlgo-specific issues

---

## License

**Proprietary Software** - Copyright © 2024 OpenFlare Technologies. All Rights Reserved.

Unauthorized copying, modification, or distribution is prohibited.

---

**Version**: 1.0
**Last Updated**: January 2025
**Compatibility**: Python 3.8+, Ubuntu 20.04+, Debian 11+
