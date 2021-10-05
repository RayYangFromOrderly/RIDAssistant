import os
from skill_tree.objects import SkillTree
from settings.objects import ProjectSettings
from main.objects import Assistant

from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from main.ui import ToolMenu, LoadingScreenHiTech

from file_cabinet.objects import Cabinet
from quest_manager.objects import QuestManager
from main.tasks import LoadTaskSet

import settings

assistant = Assistant()
settings = ProjectSettings()

task_set = LoadTaskSet(assistant)
assistant.load_tasks = task_set
assistant.tools = [Cabinet(assistant), SkillTree(assistant), QuestManager(assistant)]

if os.path.isfile(settings.root_settings_file):
    assistant.settings.load(settings.root_settings_file)
else:
    assistant.settings.save(settings.root_settings_file)


if __name__ == "__main__":
    app = QApplication([])

    window = LoadingScreenHiTech(assistant)
    window.show()
    window.hide()
    app.exec()
