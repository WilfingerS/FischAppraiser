class AppConfig:
    def __init__(self):
        self.name = "Mutation Appraiser"
        self.version = "1.0"
        self.lang = "EN"

    def get_title(self):
        return f"{self.name} v{self.version} ({self.lang})"