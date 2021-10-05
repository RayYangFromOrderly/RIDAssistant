
from PySide6.QtCore import QObject, QRect
from PySide6.QtWidgets import QRadioButton
import os
import json
from abc import ABC


from tools.objects import Tool


class QuestManager(Tool):
    def setup(self):
        from .ui import QuestManagerPanel
        panel = QuestManagerPanel(self)
        self.assistant.add_tab(panel)

class Quest:
    def __init__(self):
        self.name = ''

class QuestSeries:
    def __init__(self):
        self.name = ''