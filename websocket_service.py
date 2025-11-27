#!/usr/bin/env python3
"""
Standalone WebSocket Service for AlgoMirror
Runs as a separate systemd service to handle real-time data streaming.

This service:
1. Maintains persistent WebSocket connections to OpenAlgo
2. Updates position P&L in the database
3. Triggers stop-loss/take-profit via order_status_poller integration
4. Writes latest prices to a shared file/redis for the main app

Usage:
    python websocket_service.py

Or run via systemd:
    sudo systemctl start algomirror-websocket
"""

import os
import sys
import json
import time
import signal
import logging
import threading
from datetime import datetime
from pathlib import Path

# Add the app directory to path
app_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(app_dir))

# Set up logging before importing app modules
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(app_dir, 'logs', 'websocket_service.log'))
    ]
)
logger = logging.getLogger('WebSocketService')

# Import after path setup
import websocket
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(app_dir, '.env'))

# Shared data file path
SHARED_DATA_PATH = os.path.join(app_dir, 'instance', 'websocket_data.json')


class StandaloneWebSocketService:
    """
    Standalone WebSocket service that runs independently of Flask app.
    Shares data via file-based storage for simplicity.
    """

    def __init__(self):
        self.ws = None
        self.ws_url = None
        self.api_key = None
        self.authenticated = False
        self.active = False
        self.subscriptions = set()
        self.latest_prices = {}  # symbol -> {ltp, timestamp}
        self._lock = threading.Lock()
        self._shutdown = False

        # Ensure instance directory exists
        os.makedirs(os.path.dirname(SHARED_DATA_PATH), exist_ok=True)

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self._shutdown = True
        self.stop()

    def load_config_from_db(self):
        """Load WebSocket configuration from database"""
        try:
            from app import create_app, db
            from app.models import TradingAccount, StrategyExecution

            app = create_app()
            with app.app_context():
                # Get primary account with WebSocket URL
                primary_account = TradingAccount.query.filter(
                    TradingAccount.is_primary == True
                ).first()

                if not primary_account:
                    # Fallback to first account with WebSocket URL
                    primary_account = TradingAccount.query.filter(
                        TradingAccount.websocket_url.isnot(None),
                        TradingAccount.websocket_url != ''
                    ).first()

                if primary_account:
                    self.ws_url = primary_account.websocket_url
                    self.api_key = primary_account.get_api_key()
                    logger.info(f"Loaded config from account: {primary_account.account_name}")
                    logger.info(f"WebSocket URL: {self.ws_url}")
                    return True
                else:
                    logger.error("No account with WebSocket URL found")
                    return False

        except Exception as e:
            logger.error(f"Failed to load config from DB: {e}")
            return False

    def get_open_positions(self):
        """Get symbols with open positions from database"""
        try:
            from app import create_app, db
            from app.models import StrategyExecution

            app = create_app()
            with app.app_context():
                # Get all entered (open) positions
                open_executions = StrategyExecution.query.filter(
                    StrategyExecution.status == 'entered'
                ).all()

                symbols = []
                for exec in open_executions:
                    if exec.symbol:
                        symbols.append({
                            'symbol': exec.symbol,
                            'exchange': exec.exchange or 'NFO'
                        })

                logger.info(f"Found {len(symbols)} open positions to monitor")
                return symbols

        except Exception as e:
            logger.error(f"Failed to get open positions: {e}")
            return []

    def connect(self):
        """Establish WebSocket connection"""
        if not self.ws_url or not self.api_key:
            logger.error("WebSocket URL or API key not configured")
            return False

        try:
            logger.info(f"Connecting to WebSocket: {self.ws_url}")

            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )

            # Run in background thread
            self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            self.ws_thread.start()

            # Wait for connection
            time.sleep(3)

            if self.authenticated:
                self.active = True
                logger.info("WebSocket connected and authenticated")
                return True
            else:
                logger.warning("WebSocket connected but not authenticated")
                return False

        except Exception as e:
            logger.error(f"Failed to connect WebSocket: {e}")
            return False

    def _on_open(self, ws):
        """WebSocket opened callback"""
        logger.info("WebSocket connection opened")

        # Authenticate
        auth_msg = {
            "action": "authenticate",
            "api_key": self.api_key
        }
        ws.send(json.dumps(auth_msg))

    def _on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)

            # Handle authentication response
            if data.get("type") == "auth":
                if data.get("status") == "success":
                    self.authenticated = True
                    logger.info("Authentication successful")

                    # Subscribe to open positions
                    self._subscribe_to_positions()
                else:
                    logger.error(f"Authentication failed: {data}")
                return

            # Handle subscription response
            if data.get("type") == "subscribe":
                logger.debug(f"Subscription response: {data}")
                return

            # Handle market data
            if data.get("type") == "market_data":
                market_data = data.get('data', data)
                symbol = market_data.get('symbol') or data.get('symbol')
                ltp = market_data.get('ltp')

                if symbol and ltp:
                    with self._lock:
                        self.latest_prices[symbol] = {
                            'ltp': ltp,
                            'timestamp': datetime.now().isoformat(),
                            'open': market_data.get('open'),
                            'high': market_data.get('high'),
                            'low': market_data.get('low'),
                            'volume': market_data.get('volume')
                        }

                    # Update shared data file
                    self._save_prices()

                    # Check stop-loss/take-profit triggers
                    self._check_risk_triggers(symbol, ltp)

            elif data.get("ltp") is not None:
                # Direct format
                symbol = data.get('symbol')
                ltp = data.get('ltp')

                if symbol and ltp:
                    with self._lock:
                        self.latest_prices[symbol] = {
                            'ltp': ltp,
                            'timestamp': datetime.now().isoformat()
                        }

                    self._save_prices()
                    self._check_risk_triggers(symbol, ltp)

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON: {message[:100]}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _on_error(self, ws, error):
        """WebSocket error callback"""
        logger.error(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code=None, close_msg=None):
        """WebSocket closed callback"""
        logger.warning(f"WebSocket closed - Code: {close_status_code}, Message: {close_msg}")
        self.authenticated = False

        if self.active and not self._shutdown:
            # Attempt reconnection
            logger.info("Scheduling reconnection...")
            threading.Thread(target=self._reconnect, daemon=True).start()

    def _reconnect(self):
        """Reconnect with exponential backoff"""
        delays = [2, 4, 8, 16, 30, 60]

        for i, delay in enumerate(delays):
            if self._shutdown:
                return

            logger.info(f"Reconnection attempt {i+1}/{len(delays)} in {delay} seconds")
            time.sleep(delay)

            if self.connect():
                logger.info("Reconnection successful")
                return

        logger.error("All reconnection attempts failed")

    def _subscribe_to_positions(self):
        """Subscribe to symbols with open positions"""
        symbols = self.get_open_positions()

        if not symbols:
            logger.info("No open positions to subscribe")
            return

        for inst in symbols:
            symbol = inst['symbol']
            exchange = inst['exchange']

            message = {
                'action': 'subscribe',
                'symbol': symbol,
                'exchange': exchange,
                'mode': 2,  # Quote mode for position monitoring
                'depth': 5
            }

            self.ws.send(json.dumps(message))
            self.subscriptions.add(f"{exchange}:{symbol}")
            logger.info(f"Subscribed to {exchange}:{symbol}")

            time.sleep(0.05)  # Small delay between subscriptions

    def _save_prices(self):
        """Save latest prices to shared file"""
        try:
            with self._lock:
                data = {
                    'prices': self.latest_prices,
                    'updated_at': datetime.now().isoformat(),
                    'subscriptions': list(self.subscriptions)
                }

            with open(SHARED_DATA_PATH, 'w') as f:
                json.dump(data, f)

        except Exception as e:
            logger.error(f"Failed to save prices: {e}")

    def _check_risk_triggers(self, symbol, ltp):
        """Check if stop-loss or take-profit should be triggered"""
        try:
            from app import create_app, db
            from app.models import StrategyExecution, Strategy

            app = create_app()
            with app.app_context():
                # Find open positions for this symbol
                open_positions = StrategyExecution.query.filter(
                    StrategyExecution.status == 'entered',
                    StrategyExecution.symbol == symbol
                ).all()

                for position in open_positions:
                    strategy = position.strategy
                    if not strategy:
                        continue

                    entry_price = position.entry_price or 0
                    qty = position.quantity or 0
                    side = position.side  # BUY or SELL

                    # Calculate current P&L
                    if side == 'BUY':
                        pnl = (ltp - entry_price) * qty
                    else:
                        pnl = (entry_price - ltp) * qty

                    # Update position P&L in database
                    position.current_price = ltp
                    position.unrealized_pnl = pnl
                    db.session.commit()

                    # Check stop-loss
                    stop_loss = strategy.stop_loss
                    if stop_loss and pnl <= -abs(stop_loss):
                        logger.warning(f"[STOP-LOSS] Triggered for {symbol}: P&L={pnl}, Stop={stop_loss}")
                        self._trigger_exit(position, 'stop_loss')

                    # Check take-profit
                    take_profit = strategy.take_profit
                    if take_profit and pnl >= abs(take_profit):
                        logger.info(f"[TAKE-PROFIT] Triggered for {symbol}: P&L={pnl}, Target={take_profit}")
                        self._trigger_exit(position, 'take_profit')

        except Exception as e:
            logger.error(f"Error checking risk triggers: {e}")

    def _trigger_exit(self, position, reason):
        """Trigger exit order for position"""
        try:
            from app import create_app, db
            from app.models import RiskEvent
            from app.utils.strategy_executor import StrategyExecutor

            app = create_app()
            with app.app_context():
                # Log risk event
                risk_event = RiskEvent(
                    strategy_id=position.strategy_id,
                    execution_id=position.id,
                    event_type=reason,
                    trigger_value=position.unrealized_pnl,
                    action_taken='exit_triggered',
                    created_at=datetime.utcnow()
                )
                db.session.add(risk_event)
                db.session.commit()

                # Execute exit (this will be handled by the strategy executor)
                logger.info(f"Exit triggered for position {position.id}: {reason}")

                # Mark position for exit (the main app will pick this up)
                position.exit_reason = reason
                position.exit_triggered_at = datetime.utcnow()
                db.session.commit()

        except Exception as e:
            logger.error(f"Error triggering exit: {e}")

    def run(self):
        """Main service loop"""
        logger.info("Starting WebSocket Service...")

        # Load config from database
        if not self.load_config_from_db():
            logger.error("Failed to load configuration, exiting")
            return

        # Connect to WebSocket
        if not self.connect():
            logger.error("Failed to connect, will retry...")

        # Main loop - refresh subscriptions periodically
        refresh_interval = 60  # seconds
        last_refresh = time.time()

        while not self._shutdown:
            try:
                current_time = time.time()

                # Refresh subscriptions periodically
                if current_time - last_refresh >= refresh_interval:
                    if self.authenticated:
                        logger.info("Refreshing subscriptions...")
                        self._subscribe_to_positions()
                    last_refresh = current_time

                time.sleep(1)

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(5)

        logger.info("WebSocket Service stopped")

    def stop(self):
        """Stop the service"""
        self.active = False
        self._shutdown = True

        if self.ws:
            try:
                self.ws.close()
            except:
                pass

        logger.info("WebSocket service stopped")


def main():
    """Entry point"""
    service = StandaloneWebSocketService()
    service.run()


if __name__ == '__main__':
    main()
