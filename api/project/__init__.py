from quart import Blueprint
project_blue  = Blueprint('project',__name__,url_prefix='/project')
from . import api