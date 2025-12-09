import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app

# Default rate limits (generous for single-user trading app)
DEFAULT_GLOBAL_LIMIT = "2000 per minute"
DEFAULT_AUTH_LIMIT = "30 per minute"
DEFAULT_API_LIMIT = "500 per minute"
DEFAULT_HEAVY_LIMIT = "100 per minute"

# Create rate limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[os.environ.get('RATE_LIMIT_GLOBAL', '2000') + " per minute"],
    storage_uri="memory://",  # Use in-memory storage for development
    strategy="fixed-window"  # Valid strategy for Flask-Limiter
)

def init_rate_limiter(app):
    """Initialize rate limiter with app"""
    # Update default limits from config/env
    global_limit = app.config.get('RATE_LIMIT_GLOBAL', os.environ.get('RATE_LIMIT_GLOBAL', '2000'))
    limiter._default_limits = [f"{global_limit} per minute"]

    limiter.init_app(app)

    # Configure rate limit error handler
    @app.errorhandler(429)
    def ratelimit_handler(e):
        current_app.logger.warning(
            f"Rate limit exceeded for {get_remote_address()}",
            extra={
                'event': 'rate_limit_exceeded',
                'ip': get_remote_address(),
                'description': str(e.description)
            }
        )
        return {
            'status': 'error',
            'message': 'Rate limit exceeded. Please try again later.',
            'retry_after': e.description
        }, 429

    return limiter

def auth_rate_limit():
    """Rate limit for authentication endpoints (login, register, password change)"""
    limit = os.environ.get('RATE_LIMIT_AUTH', '30')
    return limiter.limit(f"{limit} per minute")

def api_rate_limit():
    """Rate limit for API endpoints (data retrieval, calculations)"""
    limit = os.environ.get('RATE_LIMIT_API', '500')
    return limiter.limit(f"{limit} per minute")

def heavy_rate_limit():
    """Rate limit for resource-intensive endpoints (connection tests, data refresh)"""
    limit = os.environ.get('RATE_LIMIT_HEAVY', '100')
    return limiter.limit(f"{limit} per minute")
