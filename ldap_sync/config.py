import configparser


class Config:
    def __init__(self, path):
        self.path = path
        self.parser = configparser.ConfigParser()
        self.parser.read(path)

    def get(self, section, key, **kw):
        return self.parser.get(section, key, **kw)

    def __getattr__(self, section):
        if section not in self.parser.sections():
            raise configparser.NoSectionError
        return ConfigSection(self.parser, section)


class ConfigSection:
    def __init__(self, parser, section):
        self.parser = parser
        self.section = section

    def __getattr__(self, option):
        return self.parser.get(self.section, option)
