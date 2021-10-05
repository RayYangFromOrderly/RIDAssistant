import os
import json

from PySide6.QtGui import QColor

class Settings:
    def save(self, path):
        with open(path, 'w') as file:
            file.write(self.__dict__)

    def load(self, path):
        with open(path) as file:
            data = json.load(file)
            for k in data:
                self.__setattr__(k, data[k])

class ProjectSettings:
    def __init__(self):
        self.root_settings_file = 'settings.json'


class AssistantSettings(Settings):
    def __init__(self):
        self.root_path = os.environ.get("ProgramFiles")

class StylePreferences(Settings):
    def __init__(self):
        self.main_color = QColor(0, 212, 183)