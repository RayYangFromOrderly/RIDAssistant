from abc import ABC

from PySide6.QtCore import QObject, QThread, Signal, Slot

class LoadingStep(QObject):
    update = Signal()
    def __init__(self, assistant):
        super().__init__()

        self.assistant = assistant
        self.progress = 0
        self.task_index = 0
        self.task_length = 1

    def execute(self):
        return NotImplemented


class LoadTool(LoadingStep):
    def execute(self):
        assistant = self.assistant
        self.task_length = len(self.assistant.tools)
        for i, tool in enumerate(assistant.tools):
            self.task_index = i
            self.update.emit()
            tool.setup()


    def predict_rate(self):
        pass

class LoadTaskSet(QObject):
    update = Signal(bool)
    def __init__(self, assistant):
        super().__init__()
        assistant.load_tasks = self
        self.steps = [
            LoadTool(assistant)
        ]

    def run(self):
        for step in self.steps:
            self.step = step
            step.update.connect(self._task_update)
            step.execute()
        self.update.emit(True)

    @Slot()
    def _task_update(self):
        self.update.emit(False)
