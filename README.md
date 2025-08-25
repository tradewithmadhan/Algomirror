# 🏢 AlgoMirror - Enterprise Multi-Account OpenAlgo Management Platform

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/openflare/algomirror)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![OpenAlgo](https://img.shields.io/badge/openalgo-compatible-orange.svg)](https://openalgo.in)

> **Enterprise-grade multi-account management platform for OpenAlgo trading applications**

AlgoMirror is a proprietary, secure, and scalable multi-account management platform developed by **OpenFlare Technologies**. It provides traders and institutions with a unified interface to manage multiple OpenAlgo trading accounts across different brokers, featuring advanced security, real-time monitoring, and comprehensive analytics.

## 🎯 **Why AlgoMirror?**

- **🔒 Zero-Trust Security** - No default accounts, first user becomes admin
- **⚡ Enterprise Performance** - Multi-tier rate limiting and optimized queries  
- **🏢 Multi-Account Management** - Unlimited accounts across different brokers
- **🔐 Bank-Level Encryption** - Fernet encryption for all sensitive data
- **📊 Real-Time Analytics** - Aggregated P&L, positions, and performance metrics
- **🎨 Native OpenAlgo UI** - Exact design language matching OpenAlgo

---

## 🌟 **Key Features**

### 🛡️ **Advanced Security Architecture**
- **Zero Default Accounts** - First registered user automatically becomes admin
- **Fernet Encryption** - Military-grade AES 128 encryption for API keys
- **Multi-Tier Rate Limiting** - Prevents abuse with intelligent throttling
- **CSRF Protection** - Complete protection against cross-site request forgery
- **Content Security Policy** - XSS prevention with strict CSP headers
- **Audit Logging** - JSON-structured activity logs for compliance
- **Session Security** - HTTPOnly, Secure, SameSite cookie protection

### 📈 **Trading & Account Management**
- **Multi-Broker Support** - 22+ supported brokers via OpenAlgo
- **Real-Time Synchronization** - Live data updates with WebSocket support
- **Unified Dashboard** - Aggregated metrics across all accounts
- **Position Tracking** - Real-time P&L calculations and portfolio monitoring
- **Order Management** - Order book and trade book across multiple accounts
- **Holdings Analysis** - Investment portfolio performance and analytics
- **Connection Testing** - Built-in ping API for connection validation

### 🎨 **User Experience**
- **OpenAlgo Theme Matching** - Pixel-perfect UI consistency
- **Dark/Light Mode** - Automatic theme detection and switching
- **Mobile Responsive** - Fully optimized for all device types
- **Progressive Web App** - Fast loading with modern web standards
- **Intuitive Navigation** - Clean, organized interface design

### 🏗️ **Enterprise Architecture**
- **Blueprint Organization** - Modular Flask application structure
- **Database Migrations** - Flask-Migrate for schema versioning
- **Background Tasks** - Async operations for heavy computations
- **Caching Layer** - Redis integration for performance optimization
- **Production Ready** - Gunicorn, nginx, SSL/TLS support

---

## 📋 **Prerequisites**

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.8+ | Core runtime |
| **Node.js** | 14+ | CSS build system (Tailwind) |
| **OpenAlgo** | Latest | Trading platform integration |
| **SQLite** | Built-in | Development database |
| **PostgreSQL** | 12+ | Production database (recommended) |
| **Redis** | 6+ | Session storage & rate limiting (optional) |

---

## 🚀 **Quick Start Guide**

### 1️⃣ **Environment Setup**
```bash
# Clone the repository
git clone https://github.com/openflare/algomirror.git
cd Algomirror

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Create virtual environment (macOS/Linux)  
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ **Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt

# Install Node.js dependencies and build CSS
npm install
npm run build-css
```

### 3️⃣ **Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit configuration (required)
nano .env
```

**Essential `.env` Configuration:**
```env
SECRET_KEY=your-super-secret-key-here-change-this
DATABASE_URL=sqlite:///instance/algomirror.db
FLASK_ENV=development
LOG_LEVEL=INFO
ENCRYPTION_KEY=auto-generated-or-provide-your-own
```

### 4️⃣ **Initialize Database**
```bash
# Create database schema
python init_db.py

# Optional: Create test data (development only)
python init_db.py testdata
```

### 5️⃣ **Launch Application**
```bash
# Start the development server
python app.py

# Application available at: http://localhost:8000
```

### 6️⃣ **First Login**
1. Navigate to `http://localhost:8000`
2. Click **"Get Started"** to register
3. **First user automatically becomes admin** 🔐
4. Login and start adding your OpenAlgo accounts

---

## 👤 **User Management & Security**

### 🔐 **Zero-Trust Authentication**
- **No Default Accounts** - Enhanced security by design
- **First User = Admin** - Automatic admin privileges for first registration
- **Strong Password Policy** - Enforced complexity requirements
- **Session Management** - 24-hour session lifetime with secure cookies

### 🛡️ **Password Requirements**
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter (A-Z)
- ✅ At least one lowercase letter (a-z)  
- ✅ At least one number (0-9)
- ✅ At least one special character (`!@#$%^&*()_+-=[]{}|;:,.<>?`)
- ❌ Cannot be common passwords (password, 123456, etc.)

### ⚡ **Rate Limiting Protection**

| Endpoint Category | Rate Limit | Purpose |
|------------------|------------|---------|
| **Global** | 1000/minute | Overall IP protection |
| **Authentication** | 10/minute | Login/register/password |
| **API Data** | 100/minute | Trading data retrieval |
| **Heavy Operations** | 20/minute | Connection tests/data refresh |

---

## 🔧 **OpenAlgo Account Integration**

### 📊 **Supported Brokers (22+)**
- 5paisa & 5paisa (XTS)
- Aliceblue
- AngelOne  
- Compositedge (XTS)
- Dhan & Dhan(Sandbox)
- Firstock
- Flattrade
- Fyers
- Groww
- IIFL (XTS)
- IndiaBulls
- IndMoney
- Kotak Securities
- Paytm
- Pocketful
- Shoonya
- Upstox
- Wisdom Capital (XTS)
- Zebu
- Zerodha

### ➕ **Adding New Accounts**

1. **Prerequisites Checklist:**
   - ✅ OpenAlgo application is running on target host
   - ✅ Valid API key obtained from OpenAlgo dashboard
   - ✅ Correct host URL (e.g., `http://127.0.0.1:5000`)
   - ✅ WebSocket URL configured (e.g., `ws://127.0.0.1:8765`)

2. **Add Account Process:**
   - Navigate to **Accounts** → **Add Account**
   - Choose broker from dropdown (auto-detected via ping API)
   - Enter connection details and API key
   - **Test Connection** button validates before saving
   - Account automatically connects and syncs data

### 🔍 **Connection Validation**
AlgoMirror uses the OpenAlgo **ping API** for connection testing:
```bash
# Manual ping test
curl -X POST http://127.0.0.1:5000/api/v1/ping \
  -H "Content-Type: application/json" \
  -d '{"apikey":"your_api_key_here"}'

# Expected response
{
  "status": "success",
  "data": {
    "broker": "upstox",
    "message": "pong"
  }
}
```

---

## 📁 **Project Architecture**

### 🏗️ **Directory Structure**
```
AlgoMirror/
├── 📁 app/                          # Main application package
│   ├── 🐍 __init__.py              # Flask app factory + security config
│   ├── 🗄️ models.py                # SQLAlchemy database models
│   ├── 📁 auth/                    # Authentication blueprint
│   │   ├── 🐍 routes.py            # Login, register, password management
│   │   └── 📝 forms.py             # WTForms validation
│   ├── 📁 main/                    # Dashboard and landing pages
│   │   └── 🐍 routes.py            # Home and dashboard routes
│   ├── 📁 accounts/                # Account management
│   │   ├── 🐍 routes.py            # CRUD operations, connection testing
│   │   └── 📝 forms.py             # Account forms with broker validation
│   ├── 📁 trading/                 # Trading features
│   │   └── 🐍 routes.py            # Funds, positions, orders, holdings
│   ├── 📁 api/                     # REST API endpoints
│   │   └── 🐍 routes.py            # API data endpoints
│   ├── 📁 utils/                   # Utility functions
│   │   ├── 🔧 rate_limiter.py      # Multi-tier rate limiting
│   │   └── 🔌 openalgo_client.py   # Extended OpenAlgo API client
│   ├── 📁 templates/               # Jinja2 HTML templates
│   │   ├── 🎨 base.html            # Core HTML structure & theme
│   │   ├── 🖼️ layout.html          # Auth/non-auth layouts
│   │   ├── 📁 auth/               # Authentication templates
│   │   ├── 📁 main/               # Dashboard templates
│   │   ├── 📁 accounts/           # Account management templates
│   │   └── 📁 trading/            # Trading feature templates
│   └── 📁 static/                  # Static assets
│       ├── 🎨 css/                # Compiled Tailwind CSS
│       ├── 🖼️ favicon/            # App icons and favicons
│       └── 📱 js/                 # Client-side JavaScript
├── 🗄️ migrations/                  # Database migrations (Flask-Migrate)
├── 📊 logs/                        # Application logs (auto-created)
├── ⚙️ config.py                   # Application configuration
├── 🚀 app.py                      # Application entry point
├── 🛠️ init_db.py                  # Database initialization utility
└── 📦 requirements.txt            # Python dependencies
```

### 🎨 **Frontend Technology Stack**
- **Tailwind CSS** - Utility-first CSS framework
- **DaisyUI** - Component library with OpenAlgo theming
- **Heroicons** - Consistent icon system
- **Socket.IO** - Real-time WebSocket communication
- **Vanilla JavaScript** - Lightweight client-side interactions

### 🛢️ **Database Schema**

#### **Core Models:**
- **`User`** - User accounts with admin/regular roles
- **`TradingAccount`** - OpenAlgo account connections (encrypted API keys)
- **`ActivityLog`** - Audit trail for all user actions
- **`Order`** - Order history and tracking
- **`Position`** - Current positions with P&L
- **`Holding`** - Long-term holdings and performance

#### **Security Features:**
- **Fernet Encryption** - API keys encrypted at rest
- **Unique Constraints** - Prevent duplicate accounts
- **Foreign Key Relationships** - Data integrity enforcement
- **JSON Columns** - Flexible metadata storage

---

## 🛠️ **Development Workflow**

### 🔄 **CSS Development**
```bash
# Watch for changes during development
npm run watch-css

# Build for production
npm run build-css
```

### 🗄️ **Database Management**
```bash
# Initialize fresh database
python init_db.py

# Reset database (⚠️ deletes all data)
python init_db.py reset

# Create test data (development only)
python init_db.py testdata

# Create migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

### 🔍 **Debugging & Monitoring**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python app.py

# Check application health
curl http://localhost:8000/api/health

# Monitor rate limits
curl -I http://localhost:8000/api/some-endpoint
# Look for X-RateLimit-* headers
```

### 🧪 **Testing Connection Issues**
```bash
# Test OpenAlgo server availability
curl http://127.0.0.1:5000

# Test ping API endpoint
curl -X POST http://127.0.0.1:5000/api/v1/ping \
  -H "Content-Type: application/json" \
  -d '{"apikey":"your_api_key"}'

# Expected successful response:
# {"status":"success","data":{"broker":"upstox","message":"pong"}}

# Common error responses:
# 404 - API endpoint not available (OpenAlgo not running properly)
# 403 - Invalid API key
# Connection timeout - Server not accessible
```

---

## 🚀 **Production Deployment**

### 🏢 **Production Requirements**
- **PostgreSQL** - Scalable relational database
- **Redis** - Session storage and rate limiting
- **Nginx/Apache** - Reverse proxy and load balancing
- **SSL Certificate** - HTTPS encryption (Let's Encrypt recommended)
- **Systemd/Docker** - Process management

### ⚙️ **Production Configuration**
```env
# Production .env
SECRET_KEY=randomly-generated-256-bit-key
DATABASE_URL=postgresql://user:password@localhost/algomirror_prod
REDIS_URL=redis://localhost:6379/0
FLASK_ENV=production
SESSION_TYPE=redis
LOG_LEVEL=WARNING
```

### 🐳 **Docker Deployment**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### 🌐 **Nginx Configuration**
```nginx
server {
    listen 443 ssl http2;
    server_name algomirror.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/algomirror.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/algomirror.yourdomain.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 📊 **API Integration & Usage**

### 🔌 **OpenAlgo SDK Integration**
AlgoMirror uses the official OpenAlgo Python SDK with custom extensions:

```python
from app.utils.openalgo_client import ExtendedOpenAlgoAPI

# Initialize client with ping support
client = ExtendedOpenAlgoAPI(
    api_key='your_api_key',
    host='http://127.0.0.1:5000'
)

# Test connection (AlgoMirror extension)
ping_response = client.ping()

# Standard OpenAlgo operations
funds = client.funds()
positions = client.positionbook() 
orders = client.orderbook()
holdings = client.holdings()
```

### 🔍 **Extended API Methods**
AlgoMirror adds the following methods to the standard OpenAlgo client:

#### **`ping()` Method**
```python
response = client.ping()
# Returns: {
#   "status": "success",
#   "data": {
#     "broker": "upstox", 
#     "message": "pong"
#   }
# }
```

### 📋 **API Endpoints**
AlgoMirror provides its own REST API for integration:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/accounts` | GET | List user's trading accounts |
| `/api/accounts/{id}/test` | POST | Test account connection |
| `/api/accounts/{id}/refresh` | POST | Refresh account data |
| `/api/dashboard/summary` | GET | Aggregated dashboard data |
| `/api/health` | GET | Application health check |

---

## 🔧 **Configuration Reference**

### 🌍 **Environment Variables**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ | `dev-key` | Flask session encryption key |
| `DATABASE_URL` | ❌ | `sqlite:///algomirror.db` | Database connection string |
| `FLASK_ENV` | ❌ | `development` | Application environment |
| `LOG_LEVEL` | ❌ | `INFO` | Logging verbosity level |
| `REDIS_URL` | ❌ | `memory://` | Redis connection for caching |
| `ENCRYPTION_KEY` | ❌ | Auto-generated | Fernet encryption key |
| `CORS_ORIGINS` | ❌ | `http://localhost:8000` | Allowed CORS origins |

### ⚡ **Rate Limiting Configuration**
```python
# config.py
RATELIMIT_STORAGE_URL = "redis://localhost:6379/1"
RATELIMIT_DEFAULT = "1000 per minute"

# Custom rate limits per blueprint
AUTH_RATE_LIMIT = "10 per minute"    # Login, register
API_RATE_LIMIT = "100 per minute"     # Data endpoints  
HEAVY_RATE_LIMIT = "20 per minute"   # Connection tests
```

### 🛡️ **Security Configuration**
```python
# Content Security Policy
CSP = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "'unsafe-inline'", 'cdn.socket.io'],
    'style-src': ["'self'", "'unsafe-inline'"],
    'img-src': ["'self'", 'data:', 'https:'],
    'connect-src': ["'self'", 'ws:', 'wss:'],
}

# Session Configuration
SESSION_COOKIE_SECURE = True        # HTTPS only
SESSION_COOKIE_HTTPONLY = True     # No JS access
SESSION_COOKIE_SAMESITE = 'Lax'    # CSRF protection
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
```

---

## 🐛 **Troubleshooting Guide**

### ❌ **Common Issues & Solutions**

#### **Connection Issues**
```bash
# Problem: "Cannot connect to OpenAlgo server"
# Solution: Verify OpenAlgo is running and accessible
curl http://127.0.0.1:5000
curl -X POST http://127.0.0.1:5000/api/v1/ping -d '{"apikey":"test"}'
```

#### **API Key Issues**  
```bash
# Problem: "Invalid OpenAlgo API key"
# Solution: Check API key in OpenAlgo dashboard
# Ensure key has proper permissions and is active
```

#### **Database Issues**
```bash
# Problem: Database connection errors
python init_db.py reset  # ⚠️ Deletes all data
python init_db.py        # Reinitialize

# Problem: Migration errors
flask db stamp head      # Mark current state
flask db migrate         # Create new migration
flask db upgrade         # Apply changes
```

#### **CSS/Styling Issues**
```bash
# Problem: Styles not loading
npm run build-css       # Rebuild CSS
# Check app/static/css/compiled.css exists

# Problem: Theme not switching
# Clear browser cache and localStorage
```

#### **Rate Limiting Issues**
```bash
# Problem: Rate limit exceeded
# Wait for limit reset (check X-RateLimit-Reset-After header)
# Or increase limits in config.py for development
```

### 📋 **Debug Checklist**

1. **Environment Setup**
   - [ ] Virtual environment activated
   - [ ] All dependencies installed (`pip install -r requirements.txt`)
   - [ ] CSS compiled (`npm run build-css`)
   - [ ] Database initialized (`python init_db.py`)

2. **OpenAlgo Integration**  
   - [ ] OpenAlgo server running on specified host
   - [ ] Ping API responding (`/api/v1/ping` endpoint)
   - [ ] Valid API key with proper permissions
   - [ ] Correct host URL format (`http://127.0.0.1:5000`)

3. **Application Health**
   - [ ] No error logs in `logs/algomirror.log`
   - [ ] Database file exists (`instance/algomirror.db`)
   - [ ] All required environment variables set
   - [ ] Port 8000 not in use by other applications

---

## 📈 **Performance Optimization**

### 🚀 **Performance Features**
- **Database Indexing** - Optimized queries with strategic indexes
- **Connection Pooling** - Efficient database connection management
- **Redis Caching** - Fast access to frequently requested data
- **Lazy Loading** - Relationships loaded only when needed
- **JSON Caching** - Account data cached to reduce API calls
- **Rate Limiting** - Prevents server overload and API abuse

### 📊 **Monitoring & Analytics**
```python
# Built-in performance monitoring
@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request  
def after_request(response):
    duration = time.time() - g.start_time
    logger.info(f"Request completed in {duration:.3f}s")
    return response
```

### 🔧 **Production Optimization**
```python
# config.py - Production settings
class ProductionConfig(Config):
    # Database connection pooling
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    # Redis caching
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')
    
    # Session optimization
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
```

---

## 📚 **Additional Resources**

### 🔗 **Documentation Links**
- **OpenAlgo Documentation**: [https://docs.openalgo.in](https://docs.openalgo.in)
- **Flask Framework**: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Tailwind CSS**: [https://tailwindcss.com](https://tailwindcss.com)
- **DaisyUI Components**: [https://daisyui.com](https://daisyui.com)

### 🆘 **Support Channels**
- **GitHub Issues**: [Create Issue](https://github.com/openflare/algomirror/issues)
- **Email Support**: support@openflare.tech
- **Documentation**: [Internal Wiki](./docs/)

### 🧪 **Development Resources**
- **API Testing**: Use Postman collection in `./docs/postman/`
- **Database Schema**: Visual diagram in `./docs/database-schema.png`
- **Security Audit**: Review `./docs/security-checklist.md`

---

## 👥 **Contributing & Licensing**

### 📄 **Proprietary License**
This software is **proprietary and confidential** property of OpenFlare Technologies.

**Copyright © 2024 OpenFlare Technologies. All Rights Reserved.**

- ❌ **No unauthorized copying, modification, or distribution**
- ❌ **No reverse engineering or decompilation** 
- ❌ **No resale or redistribution**
- ✅ **Licensed for use per agreement terms only**

### 🏢 **OpenFlare Technologies**
- **Website**: [https://openflare.tech](https://openflare.tech)
- **Email**: contact@openflare.tech
- **GitHub**: [@openflare](https://github.com/openflare)

### 🙏 **Acknowledgments**
- **OpenAlgo Platform**: Foundation for algorithmic trading
- **Flask Ecosystem**: Robust web framework and extensions
- **Tailwind CSS & DaisyUI**: Modern UI framework and components
- **SQLAlchemy**: Powerful ORM and database toolkit

---

## 📊 **Version History**

### 🚀 **v1.0.0** (Current)
- ✅ Multi-account OpenAlgo integration with 22+ brokers
- ✅ Zero-trust security architecture with no default accounts  
- ✅ Fernet encryption for API keys and sensitive data
- ✅ Multi-tier rate limiting with intelligent throttling
- ✅ Real-time dashboard with aggregated analytics
- ✅ Extended OpenAlgo client with ping API support
- ✅ Mobile-responsive UI with OpenAlgo theme matching
- ✅ Comprehensive audit logging and activity tracking
- ✅ Production-ready deployment with Docker support
- ✅ Built-in connection testing and validation
- ✅ SQLAlchemy ORM with database migrations
- ✅ Flask blueprint architecture for modularity

### 🔮 **Planned Features** (Future Releases)
- 📊 **Advanced Analytics** - Portfolio performance analysis
- 🔔 **Alert System** - Real-time notifications and alerts  
- 📱 **Mobile App** - Native iOS/Android applications
- 🤖 **API Automation** - Webhook integrations and automation
- 🔄 **Data Export** - CSV/Excel export functionality
- 📈 **Backtesting** - Strategy backtesting capabilities

---

<div align="center">

## 🏆 **AlgoMirror - Enterprise Trading Made Simple**

**Secure • Scalable • Professional**

[![OpenFlare](https://img.shields.io/badge/Built%20by-OpenFlare%20Technologies-blue?style=for-the-badge)](https://openflare.tech)
[![OpenAlgo](https://img.shields.io/badge/Powered%20by-OpenAlgo-orange?style=for-the-badge)](https://openalgo.in)

---

*Copyright © 2024 OpenFlare Technologies. All Rights Reserved.*

</div>