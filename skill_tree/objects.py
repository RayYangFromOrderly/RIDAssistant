from skill_tree.ui import SkillTreePanel
from PySide6.QtCore import QObject, QRect
from PySide6.QtWidgets import QRadioButton
import os
import json
from abc import ABC


from tools.objects import Tool


class SkillTree(Tool):
    def setup(self):
        panel = SkillTreePanel(self)
        self.assistant.add_tab(panel)

class Skill:
    def __init__(self):
        self.name = ''
        self.id = 0