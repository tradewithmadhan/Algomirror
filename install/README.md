# AlgoMirror Installation Scripts

## What is AlgoMirror?

**AlgoMirror** is a proprietary enterprise-grade multi-account management platform that provides a unified interface to manage multiple OpenAlgo trading accounts.

### Key Capabilities
- 🎯 Manage 20+ OpenAlgo accounts from single dashboard
- 🔌 Support for 22+ brokers (all OpenAlgo-supported brokers)
- 📊 Unified view of funds, positions, orders, holdings
- 🔐 Military-grade encryption for API keys
- ⚡ Real-time connection monitoring
- 🛡️ Single-user security model
- 📱 Mobile-responsive interface

---

## Available Files

| File | Description | Use Case |
|------|-------------|----------|
| `install-algomirror.sh` | Installation script | First-time setup |
| `manage-algomirror.sh` | Management tool | Daily operations |
| `ALGOMIRROR-README.md` | Complete documentation | Full reference |
| `QUICK-REFERENCE.md` | Command cheat sheet | Quick lookups |

---

## Quick Start

### Prerequisites

1. **Server**: Ubuntu 20.04+ or Debian 11+
2. **Domain**: DNS configured (e.g., algomirror.example.com)
3. **OpenAlgo**: At least one OpenAlgo instance running

### Installation

```bash
# Download installation script
chmod +x install-algomirror.sh

# Run installation
sudo ./install-algomirror.sh

# Answer prompts:
# - Domain name: algomirror.example.com
# - Default OpenAlgo host: http://127.0.0.1:5000 (optional)
# - Default OpenAlgo WebSocket: ws://127.0.0.1:8765 (optional)
```

### First Access

🚨 **CRITICAL**: Register immediately after installation!

1. Visit https://algomirror.example.com
2. Register your account
3. **First user becomes admin**
4. **All future registrations are blocked**

---

## What Gets Installed

### System Packages
- Python 3 (with virtual environment)
- Nginx (reverse proxy)
- Node.js & npm (for CSS compilation)
- Certbot (SSL certificates)
- UFW (firewall)
- uv (fast package manager)

### Python Application
- Flask web framework
- SQLAlchemy database ORM
- Fernet encryption for API keys
- Flask-Login for authentication
- Flask-Limiter for rate limiting
- OpenAlgo client library

### Configuration
- SQLite database (production can use PostgreSQL)
- SSL certificate via Let's Encrypt
- Systemd service for auto-start
- Nginx reverse proxy with Unix socket
- Firewall rules (ports 22, 80, 443)

---

## File Structure After Installation

```
/var/python/algomirror/
├── app/                           # Application code
│   ├── accounts/                 # Account management
│   ├── auth/                     # Authentication
│   ├── main/                     # Dashboard
│   ├── trading/                  # Trading views
│   ├── strategy/                 # Strategy builder
│   ├── templates/                # HTML templates
│   ├── static/                   # CSS, JS, images
│   ├── models.py                 # Database models
│   ├── .env                      # ⚠️ Configuration (sensitive!)
│   └── app.py                    # Application entry point
├── venv/                          # Python virtual environment
├── instance/                      # SQLite database
│   └── algomirror.db             # Main database
├── logs/                          # Application logs
│   ├── algomirror.log
│   ├── access.log
│   └── error.log
└── algomirror.sock               # Unix socket for Nginx
```

---

## Management

### Using Management Script

```bash
# Interactive mode
./manage-algomirror.sh

# Command line mode
./manage-algomirror.sh status      # Show status
./manage-algomirror.sh restart     # Restart service
./manage-algomirror.sh logs 100    # View logs
./manage-algomirror.sh backup      # Backup database
./manage-algomirror.sh update      # Update AlgoMirror
```

### Manual Commands

```bash
# Service control
sudo systemctl start algomirror
sudo systemctl stop algomirror
sudo systemctl restart algomirror
sudo systemctl status algomirror

# View logs
sudo journalctl -u algomirror -f

# Edit configuration
sudo nano /var/python/algomirror/app/.env
sudo systemctl restart algomirror
```

---

## Architecture

### How It Works

```
User's Browser
      ↓
   HTTPS (443)
      ↓
Nginx Reverse Proxy
      ↓
Unix Socket (algomirror.sock)
      ↓
Gunicorn (WSGI Server)
      ↓
Flask Application (Port 8000 internally)
      ↓
      ├→ SQLite Database (user data, settings)
      ├→ Encrypted API Keys (Fernet encryption)
      └→ OpenAlgo API Calls
           ↓
           ├→ OpenAlgo Instance 1 (Zerodha)
           ├→ OpenAlgo Instance 2 (Fyers)
           ├→ OpenAlgo Instance 3 (Angel)
           └→ OpenAlgo Instance N...
```

### Port Usage

- **External**: 443 (HTTPS)
- **Internal**: 8000 (Flask app)
- **Nginx → App**: Unix socket (no network port)

### Security Features

1. **Encryption**:
   - All API keys encrypted with Fernet (AES-128)
   - Encryption key stored in .env
   - Decryption only in-memory during API calls

2. **Authentication**:
   - Single-user model (first user = admin)
   - Strong password policy
   - Session management with secure cookies

3. **Network**:
   - SSL/TLS with Let's Encrypt
   - Firewall (only ports 22, 80, 443 open)
   - CSRF protection on all forms

4. **Rate Limiting**:
   - 10 requests/minute on auth endpoints
   - 100 requests/minute on API endpoints
   - Protection against brute force attacks

---

## Comparison: OpenAlgo vs AlgoMirror

| Feature | OpenAlgo | AlgoMirror |
|---------|----------|------------|
| **Purpose** | Broker API interface | Multi-account manager |
| **Broker Connection** | Direct to one broker | Manages multiple OpenAlgo instances |
| **Port** | 5000 (Flask), 8765 (WebSocket) | 8000 (Flask only) |
| **Users** | Single user per instance | Single user (manages all accounts) |
| **API Keys** | One set per instance | Multiple (one per OpenAlgo account) |
| **Use Case** | Trading with one broker | Managing multiple broker accounts |
| **Installation** | One per broker | One AlgoMirror for all OpenAlgo instances |

### Typical Setup

```
Server Setup:
├── OpenAlgo Instance 1 (trade1.example.com) - Zerodha
├── OpenAlgo Instance 2 (trade2.example.com) - Fyers
├── OpenAlgo Instance 3 (trade3.example.com) - Angel
└── AlgoMirror (algomirror.example.com) - Manages all 3
```

---

## Common Use Cases

### 1. Multi-Broker Trading
Manage accounts with Zerodha, Fyers, Angel One from single interface.

### 2. Family Accounts
Manage trading accounts for family members (different OpenAlgo instances).

### 3. Multiple Strategies
Run different strategies on different brokers, monitor from one place.

### 4. Backup Brokers
Primary and backup broker accounts, switch easily if one has issues.

---

## Troubleshooting

### Installation Issues

**Problem**: SSL certificate fails
```bash
# Ensure DNS is propagated
nslookup algomirror.example.com

# Wait 5-60 minutes if just configured
# Try manual certificate
sudo certbot --nginx -d algomirror.example.com
```

**Problem**: Service won't start
```bash
# Check logs
sudo journalctl -u algomirror -n 100

# Common issues:
# - Port 8000 in use
# - Database permissions
# - Missing dependencies
```

### Runtime Issues

**Problem**: Can't connect to OpenAlgo
- Verify OpenAlgo is running
- Check OpenAlgo API key is correct
- Test ping endpoint manually
- Verify network connectivity

**Problem**: 502 Bad Gateway
- Check if AlgoMirror service is running
- Restart both services
- Check Nginx logs

**Problem**: Lost admin password
- Use management script: `./manage-algomirror.sh reset-password`
- Or manually via Flask shell (see QUICK-REFERENCE.md)

---

## Upgrading

### From Development to Production

1. **Switch to PostgreSQL**:
   ```bash
   # Install PostgreSQL
   sudo apt install postgresql

   # Update .env
   DATABASE_URL=postgresql://user:pass@localhost/algomirror_prod

   # Run migrations
   flask db upgrade
   ```

2. **Enable Redis**:
   ```bash
   # Install Redis
   sudo apt install redis-server

   # Update .env
   REDIS_URL=redis://localhost:6379/0
   SESSION_TYPE=redis
   ```

3. **Configure monitoring and backups**

### Updating AlgoMirror

```bash
# Use management script
./manage-algomirror.sh update

# Or manually (see ALGOMIRROR-README.md)
```

---

## Security Best Practices

### 1. Encryption Key Backup

Your `.env` file contains the encryption key:

```bash
# Backup immediately after installation
sudo cp /var/python/algomirror/app/.env \
       ~/algomirror_env_backup.env

# Store securely (not on same server!)
```

⚠️ **Without this key, you cannot decrypt API keys!**

### 2. Regular Backups

```bash
# Backup database
sudo cp /var/python/algomirror/instance/algomirror.db \
       ~/algomirror_backup_$(date +%Y%m%d).db

# Schedule daily backups (see QUICK-REFERENCE.md)
```

### 3. Firewall

```bash
# Check firewall status
sudo ufw status

# Only allow necessary ports
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

### 4. Updates

```bash
# Regular system updates
sudo apt update && sudo apt upgrade -y

# Regular AlgoMirror updates
./manage-algomirror.sh update
```

---

## Support & Documentation

### Documentation Files
- **ALGOMIRROR-README.md**: Complete installation and usage guide
- **QUICK-REFERENCE.md**: Command cheat sheet
- **README.md**: This file (overview)

### Management Tools
- **manage-algomirror.sh**: Interactive management script

### Getting Help
1. Check logs: `sudo journalctl -u algomirror -f`
2. Review documentation files
3. Check OpenAlgo documentation for API issues

---

## FAQ

**Q: Can I install multiple AlgoMirror instances?**
A: Technically yes (different domains), but typically one AlgoMirror manages all OpenAlgo accounts.

**Q: Do I need OpenAlgo running?**
A: Yes! AlgoMirror is a **management interface** for OpenAlgo instances.

**Q: Can I use custom domain?**
A: Yes, use `algomirror.com` instead of `algomirror.example.com`.

**Q: How many accounts can I manage?**
A: Unlimited. Tested with 50+ OpenAlgo accounts.

**Q: Is data encrypted?**
A: Yes. All API keys are encrypted using Fernet (AES-128).

**Q: Can I migrate to another server?**
A: Yes. Backup entire `/var/python/algomirror` directory and `.env` file.

**Q: What if I forget admin password?**
A: Reset using `./manage-algomirror.sh reset-password`

---

## License

**Proprietary Software**
Copyright © 2024 OpenFlare Technologies. All Rights Reserved.

Unauthorized copying, modification, or distribution is prohibited.

---

## Quick Links

- **Installation**: `install-algomirror.sh`
- **Management**: `manage-algomirror.sh`
- **Full Docs**: `ALGOMIRROR-README.md`
- **Quick Reference**: `QUICK-REFERENCE.md`
- **OpenAlgo Multi-Instance**: `../openalgo1/install/`

---

**Version**: 1.0
**Last Updated**: January 2025
**Compatibility**: Python 3.8+, Ubuntu 20.04+, Debian 11+
