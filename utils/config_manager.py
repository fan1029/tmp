

class ContextManager:
    def __init__(self, config):
        self.config = config

    def __enter__(self):
        return self.config

    def __exit__(self, exc_type, exc_value, traceback):
        self.config.save()