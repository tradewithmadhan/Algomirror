# Gunicorn configuration for AlgoMirror
# Uses sync workers with threading for background tasks
# (eventlet is deprecated and incompatible with Python 3.13+)

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    pass

def on_starting(server):
    """Called just before the master process is initialized."""
    pass

# Worker configuration - use sync workers (gthread for better threading support)
worker_class = 'gthread'
workers = 1
threads = 4  # Number of threads per worker
timeout = 120  # Request timeout in seconds

# Binding
bind = 'unix:/var/python/algomirror/algomirror.sock'

# Logging
loglevel = 'info'
accesslog = '/var/python/algomirror/logs/access.log'
errorlog = '/var/python/algomirror/logs/error.log'

# Keep-alive
keepalive = 5
