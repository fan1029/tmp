from quart import Blueprint

note_blue = Blueprint('note', __name__, url_prefix='/note')
from . import api
