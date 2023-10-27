from quart import Blueprint

asset_blue = Blueprint('asset', __name__, url_prefix='/asset')
from . import api
