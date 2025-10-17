# AlgoMirror Quick Reference

## Installation

```bash
# Download and run installer
chmod +x install-algomirror.sh
sudo ./install-algomirror.sh

# Follow prompts for domain and OpenAlgo defaults
```

## Service Management

```bash
# Start
sudo systemctl start algomirror

# Stop
sudo systemctl stop algomirror

# Restart
sudo systemctl restart algomirror

# Status
sudo systemctl status algomirror

# Enable auto-start
sudo systemctl enable algomirror
```

## View Logs

```bash
# Last 50 lines
sudo journalctl -u algomirror -n 50

# Real-time
sudo journalctl -u algomirror -f

# Application logs
tail -f /var/python/algomirror/logs/algomirror.log

# Error logs
tail -f /var/python/algomirror/logs/error.log

# Nginx logs
tail -f /var/log/nginx/algomirror_access.log
tail -f /var/log/nginx/algomirror_error.log
```

## File Locations

| Component | Path |
|-----------|------|
| Installation | `/var/python/algomirror/` |
| Application | `/var/python/algomirror/app/` |
| Configuration | `/var/python/algomirror/app/.env` |
| Database | `/var/python/algomirror/instance/algomirror.db` |
| Logs | `/var/python/algomirror/logs/` |
| Virtual Env | `/var/python/algomirror/venv/` |
| Nginx Config | `/etc/nginx/sites-available/<domain>` |
| Service File | `/etc/systemd/system/algomirror.service` |
| SSL Certs | `/etc/letsencrypt/live/<domain>/` |

## Configuration

```bash
# View config
cat /var/python/algomirror/app/.env

# Edit config
sudo nano /var/python/algomirror/app/.env

# Restart after changes
sudo systemctl restart algomirror
```

## Database Operations

```bash
# Backup database
sudo cp /var/python/algomirror/instance/algomirror.db \
       ~/algomirror_backup_$(date +%Y%m%d).db

# View database
sqlite3 /var/python/algomirror/instance/algomirror.db

# Inside SQLite:
.tables                  # List all tables
.schema User             # View table schema
SELECT * FROM user;      # Query users
.quit                    # Exit
```

## Reset Admin Password

```bash
cd /var/python/algomirror/app
source ../venv/bin/activate
flask shell

>>> from app.models import User
>>> user = User.query.first()
>>> user.set_password('new_password_here')
>>> db.session.commit()
>>> exit()
```

## SSL Certificate Management

```bash
# Check expiry
sudo certbot certificates

# Renew
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

## Nginx Operations

```bash
# Test config
sudo nginx -t

# Reload
sudo systemctl reload nginx

# Restart
sudo systemctl restart nginx

# View config
cat /etc/nginx/sites-available/<domain>
```

## Update AlgoMirror

```bash
# Stop service
sudo systemctl stop algomirror

# Backup
sudo cp -r /var/python/algomirror \
       /var/python/algomirror_backup_$(date +%Y%m%d)

# Pull latest
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

# Run migrations
flask db upgrade

# Restart
sudo systemctl start algomirror
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u algomirror -n 100

# Remove stale socket
sudo rm /var/python/algomirror/algomirror.sock
sudo systemctl restart algomirror
```

### 502 Bad Gateway

```bash
# Restart services
sudo systemctl restart algomirror
sudo systemctl restart nginx

# Check Nginx logs
tail -f /var/log/nginx/algomirror_error.log
```

### Database Locked

```bash
# Stop service
sudo systemctl stop algomirror

# Check for locks
sudo lsof /var/python/algomirror/instance/algomirror.db

# Restart
sudo systemctl start algomirror
```

### Connection to OpenAlgo Failed

```bash
# Test OpenAlgo ping
curl -k https://trade1.example.com/api/v1/ping \
  -H "Content-Type: application/json" \
  -d '{"apikey":"your_api_key"}'

# Check network
ping trade1.example.com

# Verify API key in OpenAlgo
```

## Management Script

```bash
# Interactive mode
./manage-algomirror.sh

# Command line mode
./manage-algomirror.sh status
./manage-algomirror.sh restart
./manage-algomirror.sh logs 100
./manage-algomirror.sh backup
./manage-algomirror.sh update
```

## Key Environment Variables

```bash
# Flask
FLASK_ENV=production
SECRET_KEY='your-secret-key'

# Database
DATABASE_URL=sqlite:////var/python/algomirror/instance/algomirror.db

# Encryption
ENCRYPTION_KEY='your-fernet-key'

# CORS
CORS_ORIGINS=https://algomirror.example.com

# OpenAlgo Defaults
DEFAULT_OPENALGO_HOST=http://127.0.0.1:5000
DEFAULT_OPENALGO_WS=ws://127.0.0.1:8765

# Monitoring
PING_MONITORING_ENABLED=true
PING_MONITORING_INTERVAL=30
```

## Backup Strategy

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

# Keep last 7 days
find $BACKUP_DIR -mtime +7 -delete
EOF

chmod +x ~/backup_algomirror.sh

# Schedule daily at 2 AM
(crontab -l; echo "0 2 * * * ~/backup_algomirror.sh") | crontab -
```

## Security Checklist

- [ ] First user registered as admin
- [ ] Strong password set
- [ ] Encryption key backed up
- [ ] Firewall configured (UFW)
- [ ] SSL certificate active
- [ ] Regular database backups
- [ ] .env file permissions correct
- [ ] OpenAlgo API keys encrypted

## Performance Monitoring

```bash
# Check resources
htop

# Disk usage
df -h
du -sh /var/python/algomirror/*

# Process info
ps aux | grep algomirror

# Memory usage
free -h
```

## Common Tasks

**Add OpenAlgo Account:**
1. Login to AlgoMirror
2. Go to Accounts → Add Account
3. Enter details and test connection
4. Save

**View All Accounts:**
- Dashboard shows all connected accounts
- Green = Connected
- Red = Disconnected

**Unified Views:**
- Funds: Consolidated across all accounts
- Positions: All open positions
- Orders: Complete order book
- Holdings: Long-term holdings

**Strategy Builder:**
- Create multi-leg strategies
- Risk profiles: Fixed, Balanced, Conservative, Aggressive
- Execute across multiple accounts

## Emergency Recovery

**Database Corrupted:**
```bash
sudo systemctl stop algomirror
# Restore from backup
sudo cp ~/algomirror_backup_YYYYMMDD.db \
       /var/python/algomirror/instance/algomirror.db
sudo systemctl start algomirror
```

**Lost Encryption Key:**
- Cannot decrypt existing API keys
- Must re-add all accounts
- Keep .env backed up!

**Service Keeps Crashing:**
```bash
# Check logs
sudo journalctl -u algomirror -n 200

# Common issues:
# - Database permissions
# - Port conflicts
# - Missing dependencies
# - Corrupted database
```

## Useful One-Liners

```bash
# Quick status
systemctl is-active algomirror && echo "Running" || echo "Stopped"

# Tail all logs
tail -f /var/python/algomirror/logs/*.log

# Count accounts
sqlite3 /var/python/algomirror/instance/algomirror.db \
  "SELECT COUNT(*) FROM trading_account;"

# Find large log files
find /var/python/algomirror/logs -type f -size +10M

# Check certificate expiry days
sudo certbot certificates | grep "VALID:"
```

## Support Resources

- **Full Docs**: `ALGOMIRROR-README.md`
- **Management Script**: `./manage-algomirror.sh`
- **Logs**: Start here for troubleshooting
- **OpenAlgo Docs**: For OpenAlgo-specific issues

---

**Quick Help**: Run `./manage-algomirror.sh` for interactive management menu
