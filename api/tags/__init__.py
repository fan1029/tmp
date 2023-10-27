from quart import Blueprint

tag_blue = Blueprint('tag', __name__, url_prefix='/tag')
from . import api
