from flask import Blueprint

accounts_bp = Blueprint('accounts', __name__)

from app.accounts import routes