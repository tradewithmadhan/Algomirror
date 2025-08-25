"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-12-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # Create indexes for users
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    
    # Create trading_accounts table
    op.create_table('trading_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('account_name', sa.String(length=100), nullable=False),
        sa.Column('broker_name', sa.String(length=100), nullable=False),
        sa.Column('host_url', sa.String(length=500), nullable=False),
        sa.Column('websocket_url', sa.String(length=500), nullable=False),
        sa.Column('api_key_encrypted', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_primary', sa.Boolean(), nullable=True, default=False),
        sa.Column('last_connected', sa.DateTime(), nullable=True),
        sa.Column('connection_status', sa.String(length=50), nullable=True, default='disconnected'),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('last_funds_data', sa.JSON(), nullable=True),
        sa.Column('last_positions_data', sa.JSON(), nullable=True),
        sa.Column('last_holdings_data', sa.JSON(), nullable=True),
        sa.Column('last_data_update', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create unique constraint for user_id and account_name
    op.create_index('_user_account_uc', 'trading_accounts', ['user_id', 'account_name'], unique=True)
    
    # Create activity_logs table
    op.create_table('activity_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True, default='success'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['account_id'], ['trading_accounts.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index for created_at for better performance
    op.create_index(op.f('ix_activity_logs_created_at'), 'activity_logs', ['created_at'], unique=False)
    
    # Create orders table
    op.create_table('orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.String(length=100), nullable=False),
        sa.Column('symbol', sa.String(length=50), nullable=False),
        sa.Column('exchange', sa.String(length=20), nullable=False),
        sa.Column('action', sa.String(length=10), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('order_type', sa.String(length=20), nullable=True),
        sa.Column('product', sa.String(length=20), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('placed_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['account_id'], ['trading_accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create unique constraint for account_id and order_id
    op.create_index('_account_order_uc', 'orders', ['account_id', 'order_id'], unique=True)
    
    # Create positions table
    op.create_table('positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=50), nullable=False),
        sa.Column('exchange', sa.String(length=20), nullable=False),
        sa.Column('product', sa.String(length=20), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('average_price', sa.Float(), nullable=True),
        sa.Column('ltp', sa.Float(), nullable=True),
        sa.Column('pnl', sa.Float(), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['account_id'], ['trading_accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create unique constraint for account_id, symbol, exchange, and product
    op.create_index('_account_position_uc', 'positions', ['account_id', 'symbol', 'exchange', 'product'], unique=True)
    
    # Create holdings table
    op.create_table('holdings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=50), nullable=False),
        sa.Column('exchange', sa.String(length=20), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('average_price', sa.Float(), nullable=True),
        sa.Column('ltp', sa.Float(), nullable=True),
        sa.Column('pnl', sa.Float(), nullable=True),
        sa.Column('pnl_percent', sa.Float(), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['account_id'], ['trading_accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create unique constraint for account_id, symbol, and exchange
    op.create_index('_account_holding_uc', 'holdings', ['account_id', 'symbol', 'exchange'], unique=True)

def downgrade():
    # Drop tables in reverse order
    op.drop_table('holdings')
    op.drop_table('positions')
    op.drop_table('orders')
    op.drop_table('activity_logs')
    op.drop_table('trading_accounts')
    op.drop_table('users')