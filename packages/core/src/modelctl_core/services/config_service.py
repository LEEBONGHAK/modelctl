class ConfigService:
    def __init__(self):

        self.manager = ConfigManager()

    def get(self):

        return self.manager.load()

    def save(self, cfg):

        self.manager.save(cfg)

    def set_provider(
        self,
        provider,
    ):

        cfg = self.get()

        cfg.default_provider = provider

        self.save(cfg)

    def set_launcher(
        self,
        launcher,
    ):

        cfg = self.get()

        cfg.default_launcher = launcher

        self.save(cfg)
