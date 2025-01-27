from .cart import cart
from .errors import Errors
from .donate import donate_bp

from flask import Blueprint

routes_bp = Blueprint('routes_bp', __name__)

routes_bp.register_blueprint(donate_bp)
routes_bp.register_blueprint(cart)