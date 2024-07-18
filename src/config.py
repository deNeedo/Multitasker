from configparser import ConfigParser

class Config():
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config/config.ini')
    def getPrefix(self):
        return self.config['bot']['prefix']
    def getToken(self):
        return self.config['bot']['token']
    def getAdmin(self):
        return self.config['guild']['admin']
    def getBaseRole(self):
        return self.config['guild']['base_role']