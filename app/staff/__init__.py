from flask import Blueprint

staff = Blueprint('staff', __name__)

from . import routes
