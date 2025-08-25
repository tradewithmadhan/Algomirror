from flask import render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app.trading import trading_bp
from app.models import TradingAccount
from app.utils.openalgo_client import ExtendedOpenAlgoAPI
from datetime import datetime

def get_selected_accounts():
    """Get accounts to display based on user selection"""
    selected_account_id = request.args.get('account')
    
    if selected_account_id:
        try:
            # Convert to integer for database query
            account_id = int(selected_account_id)
            # Single account view
            account = TradingAccount.query.filter_by(
                id=account_id, 
                user_id=current_user.id,
                is_active=True
            ).first()
            return [account] if account else []
        except (ValueError, TypeError):
            # Invalid account ID, return all accounts
            return current_user.get_active_accounts()
    else:
        # Multi-account view
        return current_user.get_active_accounts()

@trading_bp.route('/funds')
@login_required
def funds():
    accounts = get_selected_accounts()
    funds_data = []
    
    for account in accounts:
        try:
            # Create API client for this account
            client = ExtendedOpenAlgoAPI(
                api_key=account.get_api_key(),
                host=account.host_url
            )
            
            # Fetch real-time funds data
            response = client.funds()
            
            if response.get('status') == 'success':
                account_funds = response.get('data', {})
                account_funds['account_name'] = account.account_name
                account_funds['account_id'] = account.id
                account_funds['broker'] = account.broker_name
                
                # Update cached data
                account.last_funds_data = account_funds
                account.last_data_update = datetime.utcnow()
                from app import db
                db.session.commit()
                
                funds_data.append(account_funds)
            elif account.last_funds_data:
                # Use cached data if API fails
                account_funds = account.last_funds_data.copy()
                account_funds['account_name'] = account.account_name
                account_funds['account_id'] = account.id
                account_funds['broker'] = account.broker_name
                funds_data.append(account_funds)
                
        except Exception as e:
            current_app.logger.error(f'Error fetching funds for account {account.id}: {str(e)}')
            # Use cached data if available
            if account.last_funds_data:
                account_funds = account.last_funds_data.copy()
                account_funds['account_name'] = account.account_name
                account_funds['account_id'] = account.id
                account_funds['broker'] = account.broker_name
                funds_data.append(account_funds)
    
    return render_template('trading/funds.html', 
                         funds_data=funds_data,
                         single_account=len(accounts) == 1,
                         accounts=current_user.get_active_accounts())

@trading_bp.route('/orderbook')
@login_required
def orderbook():
    accounts = get_selected_accounts()
    orderbook_data = []
    
    for account in accounts:
        try:
            # Create API client for this account
            client = ExtendedOpenAlgoAPI(
                api_key=account.get_api_key(),
                host=account.host_url
            )
            
            # Fetch orderbook data
            response = client.orderbook()
            
            if response.get('status') == 'success':
                data = response.get('data', {})
                orders = data.get('orders', [])
                
                # Add account info to each order
                for order in orders:
                    order['account_name'] = account.account_name
                    order['account_id'] = account.id
                    order['broker'] = account.broker_name
                
                orderbook_data.extend(orders)
                
        except Exception as e:
            current_app.logger.error(f'Error fetching orderbook for account {account.id}: {str(e)}')
    
    # Calculate statistics
    statistics = {
        'total_buy_orders': sum(1 for order in orderbook_data if order.get('action') == 'BUY'),
        'total_sell_orders': sum(1 for order in orderbook_data if order.get('action') == 'SELL'),
        'total_completed_orders': sum(1 for order in orderbook_data if order.get('order_status') == 'complete'),
        'total_open_orders': sum(1 for order in orderbook_data if order.get('order_status') in ['open', 'pending']),
        'total_rejected_orders': sum(1 for order in orderbook_data if order.get('order_status') == 'rejected'),
        'total_cancelled_orders': sum(1 for order in orderbook_data if order.get('order_status') == 'cancelled')
    }
    
    return render_template('trading/orderbook.html',
                         orderbook_data=orderbook_data,
                         statistics=statistics,
                         single_account=len(accounts) == 1,
                         accounts=current_user.get_active_accounts())

@trading_bp.route('/tradebook')
@login_required
def tradebook():
    accounts = get_selected_accounts()
    tradebook_data = []
    
    for account in accounts:
        try:
            # Create API client for this account
            client = ExtendedOpenAlgoAPI(
                api_key=account.get_api_key(),
                host=account.host_url
            )
            
            # Fetch tradebook data
            response = client.tradebook()
            
            if response.get('status') == 'success':
                trades = response.get('data', [])
                
                # Add account info to each trade
                for trade in trades:
                    trade['account_name'] = account.account_name
                    trade['account_id'] = account.id
                    trade['broker'] = account.broker_name
                
                tradebook_data.extend(trades)
                
        except Exception as e:
            current_app.logger.error(f'Error fetching tradebook for account {account.id}: {str(e)}')
    
    # Calculate total P&L
    total_pnl = 0
    for trade in tradebook_data:
        try:
            # Calculate P&L based on action
            quantity = float(trade.get('quantity', 0))
            avg_price = float(trade.get('average_price', 0))
            trade_value = float(trade.get('trade_value', 0))
            
            if trade.get('action') == 'SELL':
                total_pnl += trade_value
            else:
                total_pnl -= trade_value
        except (ValueError, TypeError):
            pass
    
    return render_template('trading/tradebook.html',
                         tradebook_data=tradebook_data,
                         total_pnl=total_pnl,
                         single_account=len(accounts) == 1,
                         accounts=current_user.get_active_accounts())

@trading_bp.route('/positions')
@login_required
def positions():
    accounts = get_selected_accounts()
    positions_data = []
    
    for account in accounts:
        try:
            # Create API client for this account
            client = ExtendedOpenAlgoAPI(
                api_key=account.get_api_key(),
                host=account.host_url
            )
            
            # Fetch position book data
            response = client.positionbook()
            
            if response.get('status') == 'success':
                positions = response.get('data', [])
                
                # Add account info to each position
                for position in positions:
                    position['account_name'] = account.account_name
                    position['account_id'] = account.id
                    position['broker'] = account.broker_name
                    
                    # Calculate additional metrics
                    try:
                        qty = float(position.get('quantity', 0))
                        avg_price = float(position.get('average_price', 0))
                        ltp = float(position.get('ltp', 0))
                        
                        if qty != 0 and avg_price != 0:
                            position['invested_value'] = abs(qty * avg_price)
                            position['current_value'] = abs(qty * ltp)
                            position['pnl_percentage'] = ((ltp - avg_price) / avg_price * 100) if avg_price else 0
                    except (ValueError, TypeError):
                        position['invested_value'] = 0
                        position['current_value'] = 0
                        position['pnl_percentage'] = 0
                
                positions_data.extend(positions)
                
                # Update cached data
                account.last_positions_data = positions
                account.last_data_update = datetime.utcnow()
                from app import db
                db.session.commit()
                
        except Exception as e:
            current_app.logger.error(f'Error fetching positions for account {account.id}: {str(e)}')
            # Use cached data if available
            if account.last_positions_data:
                positions = account.last_positions_data
                for position in positions:
                    position['account_name'] = account.account_name
                    position['account_id'] = account.id
                    position['broker'] = account.broker_name
                positions_data.extend(positions)
    
    # Calculate totals
    total_pnl = sum(float(p.get('pnl', 0)) for p in positions_data)
    total_invested = sum(float(p.get('invested_value', 0)) for p in positions_data)
    total_current = sum(float(p.get('current_value', 0)) for p in positions_data)
    
    return render_template('trading/positions.html',
                         positions_data=positions_data,
                         total_pnl=total_pnl,
                         total_invested=total_invested,
                         total_current=total_current,
                         single_account=len(accounts) == 1,
                         accounts=current_user.get_active_accounts())

@trading_bp.route('/holdings')
@login_required
def holdings():
    accounts = get_selected_accounts()
    holdings_data = []
    
    for account in accounts:
        try:
            # Create API client for this account
            client = ExtendedOpenAlgoAPI(
                api_key=account.get_api_key(),
                host=account.host_url
            )
            
            # Fetch holdings data
            response = client.holdings()
            
            if response.get('status') == 'success':
                data = response.get('data', {})
                holdings = data.get('holdings', [])
                
                # Add account info to each holding
                for holding in holdings:
                    holding['account_name'] = account.account_name
                    holding['account_id'] = account.id
                    holding['broker'] = account.broker_name
                
                holdings_data.extend(holdings)
                
                # Update cached data
                account.last_holdings_data = data
                account.last_data_update = datetime.utcnow()
                from app import db
                db.session.commit()
                
        except Exception as e:
            current_app.logger.error(f'Error fetching holdings for account {account.id}: {str(e)}')
            # Use cached data if available
            if account.last_holdings_data:
                data = account.last_holdings_data
                holdings = data.get('holdings', []) if isinstance(data, dict) else []
                for holding in holdings:
                    holding['account_name'] = account.account_name
                    holding['account_id'] = account.id
                    holding['broker'] = account.broker_name
                holdings_data.extend(holdings)
    
    # Calculate statistics
    statistics = {
        'totalholdingvalue': sum(float(h.get('quantity', 0)) * float(h.get('ltp', 0)) for h in holdings_data if h.get('ltp')),
        'totalinvvalue': 0,  # Will be calculated from holdings
        'totalprofitandloss': sum(float(h.get('pnl', 0)) for h in holdings_data),
        'totalpnlpercentage': 0
    }
    
    # Calculate total investment value and percentage
    for holding in holdings_data:
        try:
            pnl = float(holding.get('pnl', 0))
            pnl_percent = float(holding.get('pnlpercent', 0))
            if pnl_percent != 0:
                inv_value = abs(pnl / (pnl_percent / 100))
                statistics['totalinvvalue'] += inv_value
        except (ValueError, TypeError, ZeroDivisionError):
            pass
    
    if statistics['totalinvvalue'] > 0:
        statistics['totalpnlpercentage'] = (statistics['totalprofitandloss'] / statistics['totalinvvalue']) * 100
    
    return render_template('trading/holdings.html',
                         holdings_data=holdings_data,
                         statistics=statistics,
                         single_account=len(accounts) == 1,
                         accounts=current_user.get_active_accounts())