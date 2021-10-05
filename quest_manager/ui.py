
from core.utils import apply_glow_effect
from core.ui import RWidget, UnitButton, UnitPanel, SearchBox
from tools.ui import ToolPanel
from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from .objects import QuestSeries

class QuestManagerPanel(ToolPanel):
    def __init__(self, cabinet):
        super().__init__(QPixmap('assets//image//icon-tree.png'))
        self.container = QVBoxLayout(self)
        self.setLayout(self.container)
        self.search_box = SearchBox(self)
        self.search_box.setFixedWidth(700)
        self.container.addWidget(self.search_box)
        self.quest_grid = QuestGrid(self)
        self.container.addWidget(self.quest_grid)


        data = [QuestSeries(), QuestSeries(), QuestSeries(), QuestSeries()]
        self.quest_grid.setup(data)

    def refresh(self):
        pass

    def get_name(self):
        return 'skill tree'

class QuestGrid(QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.setStyleSheet('background-color: rgb(100, 100, 100)')

    def setup(self, data):
        for quest_series in data:
            item = QuestSeriesItem(self)
            item.setup(quest_series)
            self.layout.addWidget(item)

class QuestSeriesItem(UnitPanel):
    def setup(self, quest_series):
        self.quest_series = quest_series


class QuestSeriesPanel(UnitPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_panel = NodePanel(self.parent())
        self.node_panel.hide()
        self.setIcon(QPixmap('assets//image//icon-language.png'))
        self.setIconSize(self.size() / 2)

    def enterEvent(self, event) -> None:
        self.node_panel.show()
        self.node_panel.target_position = QPoint(self.width(), self.height())
        self.node_panel.target_size = QSize(600, 400)
        return super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.node_panel.hide()
        return super().leaveEvent(event)


class QuestOverlay(RWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def paintEvent(self, event) -> None:
        return super().paintEvent(event)
