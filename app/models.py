from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import os
from app import db, login_manager

# Generate or load encryption key
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key()
    os.environ['ENCRYPTION_KEY'] = ENCRYPTION_KEY.decode()
else:
    ENCRYPTION_KEY = ENCRYPTION_KEY.encode()

cipher_suite = Fernet(ENCRYPTION_KEY)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    accounts = db.relationship('TradingAccount', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    logs = db.relationship('ActivityLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_active_accounts(self):
        return self.accounts.filter_by(is_active=True).all()
    
    def __repr__(self):
        return f'<User {self.username}>'

class TradingAccount(db.Model):
    __tablename__ = 'trading_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    broker_name = db.Column(db.String(100), nullable=False)
    
    # OpenAlgo connection details (encrypted)
    host_url = db.Column(db.String(500), nullable=False)
    websocket_url = db.Column(db.String(500), nullable=False)
    api_key_encrypted = db.Column(db.Text, nullable=False)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_primary = db.Column(db.Boolean, default=False)
    last_connected = db.Column(db.DateTime)
    connection_status = db.Column(db.String(50), default='disconnected')
    
    # Account metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Cached account data
    last_funds_data = db.Column(db.JSON)
    last_positions_data = db.Column(db.JSON)
    last_holdings_data = db.Column(db.JSON)
    last_data_update = db.Column(db.DateTime)
    
    # Unique constraint for user and account name
    __table_args__ = (
        db.UniqueConstraint('user_id', 'account_name', name='_user_account_uc'),
    )
    
    def set_api_key(self, api_key):
        """Encrypt and store API key"""
        encrypted = cipher_suite.encrypt(api_key.encode())
        self.api_key_encrypted = encrypted.decode()
    
    def get_api_key(self):
        """Decrypt and return API key"""
        if self.api_key_encrypted:
            decrypted = cipher_suite.decrypt(self.api_key_encrypted.encode())
            return decrypted.decode()
        return None
    
    def __repr__(self):
        return f'<TradingAccount {self.account_name} - {self.broker_name}>'

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('trading_accounts.id'), nullable=True)
    
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    
    status = db.Column(db.String(50), default='success')
    error_message = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    account = db.relationship('TradingAccount', backref='logs')
    
    def __repr__(self):
        return f'<ActivityLog {self.action} - {self.created_at}>'

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('trading_accounts.id'), nullable=False)
    
    order_id = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    exchange = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(10), nullable=False)  # BUY/SELL
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)
    order_type = db.Column(db.String(20))  # MARKET/LIMIT
    product = db.Column(db.String(20))  # MIS/CNC/NRML
    status = db.Column(db.String(50))
    
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    account = db.relationship('TradingAccount', backref='orders')
    
    # Unique constraint for account and order_id
    __table_args__ = (
        db.UniqueConstraint('account_id', 'order_id', name='_account_order_uc'),
    )
    
    def __repr__(self):
        return f'<Order {self.order_id} - {self.symbol}>'

class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('trading_accounts.id'), nullable=False)
    
    symbol = db.Column(db.String(50), nullable=False)
    exchange = db.Column(db.String(20), nullable=False)
    product = db.Column(db.String(20))
    quantity = db.Column(db.Integer, nullable=False)
    average_price = db.Column(db.Float)
    ltp = db.Column(db.Float)
    pnl = db.Column(db.Float)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    account = db.relationship('TradingAccount', backref='positions')
    
    # Unique constraint for account, symbol, exchange, and product
    __table_args__ = (
        db.UniqueConstraint('account_id', 'symbol', 'exchange', 'product', name='_account_position_uc'),
    )
    
    def __repr__(self):
        return f'<Position {self.symbol} - Qty: {self.quantity}>'

class Holding(db.Model):
    __tablename__ = 'holdings'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('trading_accounts.id'), nullable=False)
    
    symbol = db.Column(db.String(50), nullable=False)
    exchange = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    average_price = db.Column(db.Float)
    ltp = db.Column(db.Float)
    pnl = db.Column(db.Float)
    pnl_percent = db.Column(db.Float)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    account = db.relationship('TradingAccount', backref='holdings')
    
    # Unique constraint for account, symbol, and exchange
    __table_args__ = (
        db.UniqueConstraint('account_id', 'symbol', 'exchange', name='_account_holding_uc'),
    )
    
    def __repr__(self):
        return f'<Holding {self.symbol} - Qty: {self.quantity}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))