from configparser import ConfigParser


class Config:
    def __init__(self, path):
        self.path = path
        self.configparser = ConfigParser()
        self.configparser.read(path)

    # TODO:
    def get(self, section, key):
        return self.configparser.get(section, key)
