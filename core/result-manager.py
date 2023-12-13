from utils.redis_manager import RedisMixin
from core.pluginManager import PluginManager


class ResultManager(RedisMixin):

    def __init__(self):
        self.redis = self.redis_db_n(4)
        self.pluginManager = PluginManager()
