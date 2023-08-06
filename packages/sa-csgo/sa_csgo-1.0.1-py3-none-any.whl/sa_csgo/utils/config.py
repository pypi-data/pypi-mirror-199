import json
import os
import pkg_resources

config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.json")

class ConfigManager:
    data = '';

    @staticmethod
    def get(name):
        with open(config_file_path, "r") as file:
            data = json.load(file)
            return data['config'][name]

    @staticmethod
    def getEntire(name):
        with open(config_file_path, "r") as file:
            return json.load(file)

    @staticmethod
    def setProperty(name, value):
        data = ConfigManager.getEntire()
        data['config'][name] = value
        
        with open(config_file_path, "w") as file:
            json.dump(data,file)
            return value