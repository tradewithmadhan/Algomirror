"""
Professional WebSocket Manager with Account Failover
Handles real-time data streaming with enterprise-grade reliability
"""

import json
import threading
import time
import logging
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, List, Optional, Any
import websocket
import pytz

logger = logging.getLogger(__name__)


class ExponentialBackoff:
    """Exponential backoff strategy for reconnection"""
    
    def __init__(self, base=2, max_delay=60):
        self.base = base
        self.max_delay = max_delay
        self.attempt = 0
    
    def get_next_delay(self):
        delay = min(self.base ** self.attempt, self.max_delay)
        self.attempt += 1
        return delay
    
    def reset(self):
        self.attempt = 0


class WebSocketDataProcessor:
    """Process incoming WebSocket data based on subscription mode"""
    
    def __init__(self):
        self.quote_handlers = []
        self.depth_handlers = []
        self.ltp_handlers = []
    
    def register_quote_handler(self, handler):
        self.quote_handlers.append(handler)
    
    def register_depth_handler(self, handler):
        self.depth_handlers.append(handler)
    
    def register_ltp_handler(self, handler):
        self.ltp_handlers.append(handler)
    
    def on_data_received(self, data):
        """
        Process incoming WebSocket data based on subscription mode
        """
        try:
            mode = data.get('mode', 'ltp')
            
            if mode == 'quote':
                self.handle_quote_update(data)
            elif mode == 'depth':
                self.handle_depth_update(data)
            else:  # ltp
                self.handle_ltp_update(data)
        except Exception as e:
            logger.error(f"Error processing WebSocket data: {e}")
    
    def handle_quote_update(self, data):
        """Process quote mode data"""
        for handler in self.quote_handlers:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Error in quote handler: {e}")
    
    def handle_depth_update(self, data):
        """Process depth mode data (option strikes)"""
        for handler in self.depth_handlers:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Error in depth handler: {e}")
    
    def handle_ltp_update(self, data):
        """Process LTP mode data"""
        for handler in self.ltp_handlers:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Error in LTP handler: {e}")


class ProfessionalWebSocketManager:
    """
    Enterprise-Grade WebSocket Connection Management with Account Failover
    """
    
    def __init__(self):
        self.connection_pool = {}
        self.max_connections = 10
        self.heartbeat_interval = 30
        self.reconnect_attempts = 5
        self.backoff_strategy = ExponentialBackoff(base=2, max_delay=60)
        self.account_failover_enabled = True
        self.data_processor = WebSocketDataProcessor()
        self.subscriptions = set()
        self.active = False
        self.ws = None
        self.ws_thread = None
        self.reconnect_thread = None
        self._lock = threading.Lock()
    
    def create_connection_pool(self, primary_account, backup_accounts=None):
        """
        Create managed connection pool with multi-account failover capability
        """
        pool = {
            'current_account': primary_account,
            'backup_accounts': backup_accounts or [],
            'connections': {},
            'status': 'initializing',
            'failover_history': [],
            'metrics': {
                'account_switches': 0,
                'total_failures': 0,
                'current_health': 100,
                'messages_received': 0,
                'messages_dropped': 0,
                'reconnect_count': 0,
                'uptime_seconds': 0,
                'last_message_time': None
            }
        }
        
        # Initialize primary account connection
        pool['connections']['primary'] = {
            'account': primary_account,
            'ws_primary': None,
            'ws_backup': None,
            'status': 'active',
            'failure_count': 0
        }
        
        # Pre-configure backup accounts (standby mode)
        for idx, backup_account in enumerate((backup_accounts or [])[:3]):
            pool['connections'][f'backup_{idx}'] = {
                'account': backup_account,
                'ws_primary': None,
                'ws_backup': None,
                'status': 'standby',
                'failure_count': 0
            }
        
        self.connection_pool = pool
        logger.info(f"Connection pool created with {len(backup_accounts or [])} backup accounts")
        return pool
    
    def connect(self, ws_url, api_key):
        """Establish WebSocket connection"""
        try:
            self.ws_url = ws_url
            self.api_key = api_key
            
            # Create WebSocket connection
            self.ws = websocket.WebSocketApp(
                ws_url,
                header={'Authorization': f'Bearer {api_key}'},
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            
            # Start WebSocket in separate thread
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            self.active = True
            logger.info("WebSocket connection established")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect WebSocket: {e}")
            return False
    
    def on_open(self, ws):
        """WebSocket opened callback"""
        logger.info("WebSocket connection opened")
        self.backoff_strategy.reset()
        
        # Resubscribe to all symbols
        if self.subscriptions:
            self.resubscribe_all()
    
    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            # Update metrics
            if self.connection_pool:
                self.connection_pool['metrics']['messages_received'] += 1
                self.connection_pool['metrics']['last_message_time'] = datetime.now()
            
            # Process data
            self.data_processor.on_data_received(data)
            
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON message: {message}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def on_error(self, ws, error):
        """WebSocket error callback"""
        logger.error(f"WebSocket error: {error}")
        
        if self.connection_pool:
            self.connection_pool['metrics']['total_failures'] += 1
    
    def on_close(self, ws):
        """WebSocket closed callback"""
        logger.warning("WebSocket connection closed")
        
        if self.active:
            # Attempt reconnection
            self.schedule_reconnection()
    
    def schedule_reconnection(self):
        """Schedule reconnection with exponential backoff"""
        if not self.reconnect_thread or not self.reconnect_thread.is_alive():
            self.reconnect_thread = threading.Thread(target=self.reconnect_with_backoff)
            self.reconnect_thread.daemon = True
            self.reconnect_thread.start()
    
    def reconnect_with_backoff(self):
        """Reconnect with exponential backoff"""
        for attempt in range(self.reconnect_attempts):
            delay = self.backoff_strategy.get_next_delay()
            logger.info(f"Reconnection attempt {attempt + 1} in {delay} seconds")
            time.sleep(delay)
            
            if self.connect(self.ws_url, self.api_key):
                logger.info("Reconnection successful")
                return
        
        logger.error("Max reconnection attempts reached")
        self.handle_connection_failure()
    
    def handle_connection_failure(self):
        """Handle complete connection failure"""
        if self.account_failover_enabled and self.connection_pool:
            self.attempt_account_failover()
    
    def attempt_account_failover(self):
        """Attempt to switch to backup account"""
        backup_accounts = self.connection_pool.get('backup_accounts', [])
        
        if backup_accounts:
            next_account = backup_accounts[0]
            logger.info(f"Switching to backup account: {next_account.name}")
            
            # Update connection pool
            self.connection_pool['current_account'] = next_account
            self.connection_pool['backup_accounts'] = backup_accounts[1:]
            self.connection_pool['metrics']['account_switches'] += 1
            
            # Connect with new account
            if hasattr(next_account, 'ws_host') and hasattr(next_account, 'get_api_key'):
                self.connect(next_account.ws_host, next_account.get_api_key())
        else:
            logger.critical("No backup accounts available for failover")
    
    def subscribe(self, subscription):
        """Subscribe to symbol with specified mode"""
        try:
            if self.ws and self.ws.sock and self.ws.sock.connected:
                message = {
                    'action': 'subscribe',
                    'exchange': subscription.get('exchange'),
                    'symbol': subscription.get('symbol'),
                    'mode': subscription.get('mode', 'ltp')
                }
                
                self.ws.send(json.dumps(message))
                self.subscriptions.add(json.dumps(subscription))
                logger.debug(f"Subscribed to {subscription}")
                return True
            else:
                logger.warning("WebSocket not connected, queuing subscription")
                self.subscriptions.add(json.dumps(subscription))
                return False
                
        except Exception as e:
            logger.error(f"Subscription error: {e}")
            return False
    
    def unsubscribe(self, subscription):
        """Unsubscribe from symbol"""
        try:
            if self.ws and self.ws.sock and self.ws.sock.connected:
                message = {
                    'action': 'unsubscribe',
                    'exchange': subscription.get('exchange'),
                    'symbol': subscription.get('symbol')
                }
                
                self.ws.send(json.dumps(message))
                
                # Remove from subscriptions set
                sub_str = json.dumps(subscription)
                if sub_str in self.subscriptions:
                    self.subscriptions.remove(sub_str)
                
                logger.debug(f"Unsubscribed from {subscription}")
                return True
                
        except Exception as e:
            logger.error(f"Unsubscription error: {e}")
            return False
    
    def resubscribe_all(self):
        """Resubscribe to all symbols after reconnection"""
        logger.info(f"Resubscribing to {len(self.subscriptions)} symbols")
        
        for sub_str in self.subscriptions:
            try:
                subscription = json.loads(sub_str)
                message = {
                    'action': 'subscribe',
                    'exchange': subscription.get('exchange'),
                    'symbol': subscription.get('symbol'),
                    'mode': subscription.get('mode', 'ltp')
                }
                self.ws.send(json.dumps(message))
                time.sleep(0.01)  # Small delay between subscriptions
            except Exception as e:
                logger.error(f"Failed to resubscribe: {e}")
    
    def disconnect(self):
        """Disconnect WebSocket"""
        try:
            self.active = False
            if self.ws:
                self.ws.close()
            logger.info("WebSocket disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting WebSocket: {e}")
    
    def get_status(self):
        """Get WebSocket connection status"""
        if not self.connection_pool:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'active' if self.active else 'inactive',
            'current_account': getattr(self.connection_pool.get('current_account'), 'name', 'Unknown'),
            'backup_accounts': len(self.connection_pool.get('backup_accounts', [])),
            'metrics': self.connection_pool.get('metrics', {}),
            'subscriptions': len(self.subscriptions),
            'connected': self.ws.sock.connected if self.ws and self.ws.sock else False
        }
    
    def register_handler(self, mode, handler):
        """Register data handler for specific mode"""
        if mode == 'quote':
            self.data_processor.register_quote_handler(handler)
        elif mode == 'depth':
            self.data_processor.register_depth_handler(handler)
        elif mode == 'ltp':
            self.data_processor.register_ltp_handler(handler)