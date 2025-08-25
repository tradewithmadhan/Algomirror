from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app

# Create rate limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per minute"],  # Global rate limit
    storage_uri="memory://",  # Use in-memory storage for development
    strategy="fixed-window"  # Valid strategy for Flask-Limiter
)

def init_rate_limiter(app):
    """Initialize rate limiter with app"""
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

# Specific rate limit decorators for different endpoints
def auth_rate_limit():
    """Rate limit for authentication endpoints"""
    return limiter.limit("10 per minute")

def api_rate_limit():
    """Rate limit for API endpoints"""
    return limiter.limit("100 per minute")

def heavy_rate_limit():
    """Rate limit for resource-intensive endpoints"""
    return limiter.limit("20 per minute")