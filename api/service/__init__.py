from quart import Blueprint
service_blue  = Blueprint('service',__name__,url_prefix='/service')
from . import api

