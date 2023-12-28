from flask import Blueprint
from .controllers.auth_controller import resources

api = Blueprint('api', __name__)

api.register_blueprint(resources, url_prefix="/v1")