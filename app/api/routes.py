from flask import jsonify, request
from flask_login import login_required, current_user
from app.api import api_bp
from app.models import TradingAccount
from app.utils.rate_limiter import api_rate_limit

@api_bp.route('/accounts')
@login_required
@api_rate_limit()
def get_accounts():
    """Get user's trading accounts"""
    accounts = current_user.get_active_accounts()
    
    accounts_data = []
    for account in accounts:
        accounts_data.append({
            'id': account.id,
            'name': account.account_name,
            'broker': account.broker_name,
            'status': account.connection_status,
            'is_primary': account.is_primary,
            'last_connected': account.last_connected.isoformat() if account.last_connected else None
        })
    
    return jsonify({
        'status': 'success',
        'data': accounts_data
    })