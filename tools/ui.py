from core.ui import RWidget
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class ToolPanel(RWidget):
    def __init__(self, pixmap):
        super().__init__()
        self.container = QVBoxLayout()
        self.setLayout(self.container)
        self.tab_pixmap = pixmap