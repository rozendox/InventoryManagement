from flask import Blueprint

bp = Blueprint('inventory', __name__)

from app.inventory import routes