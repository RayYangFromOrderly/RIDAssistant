
from core.utils import apply_glow_effect
from core.ui import RWidget, UnitButton
from tools.ui import ToolPanel
from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class SkillTreePanel(ToolPanel):
    def __init__(self, cabinet):
        super().__init__(QPixmap('assets//image//icon-tree.png'))
        self.container = QVBoxLayout(self)
        self.setLayout(self.container)
        self.menu_bar = QWidget()
        self.menu_layout = QHBoxLayout()
        self.menu_bar.setLayout(self.menu_layout)

        Node(self)
        

    def refresh(self):
        pass

    def get_name(self):
        return 'skill tree'

class Node(UnitButton):
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

class NodePanel(RWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.setPen(QPen(QColor(100, 100, 100), 20))
        p.drawRect(self.rect())
        return super().paintEvent(event)
