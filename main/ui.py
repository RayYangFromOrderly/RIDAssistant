import sys
import random
from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from core.utils import AnimatedProperty, get_screen_size
from core.ui import RWidget, SearchBox, RLineEdit, RPushButton
from core.connections import touch_api
from core.settings import Settings


class ToolMenu(QWidget):
    def __init__(self, assistant, panel_container, panel_layout, *args, **params):
        super().__init__(*args, **params)
        self.container = QVBoxLayout()
        self.panel_layout = panel_layout
        self.panel_container = panel_container
        self.tools = assistant.tools
        self.search_box = SearchBox()
        self.setLayout(self.container)
        self.container.addWidget(self.search_box)
        tool_names = []
        for panel in assistant.tabs:
            tab = Tab(panel, self)
            self.container.addWidget(tab)
            tool_names.append(panel.get_name())

        self.search_box.set_selections(tool_names)

    def switch_panel(self, panel):
        for i in reversed(range(self.panel_layout.count())): 
            self.panel_layout.itemAt(i).widget().setParent(None)
        self.panel_layout.addWidget(panel)
        panel.setParent(self.panel_container)
        panel.show()


class Tab(QPushButton):
    def __init__(self, panel, menu, *args, **params):
        super().__init__(*args, **params)
        self.tab_menu = menu
        self.panel = panel
        self.pixmap = panel.tab_pixmap
        self.setFixedSize(50, 50)
        self.setMask(QRegion(QRect(0, 0, 500, 500), QRegion.Rectangle))
        self.setIcon(self.pixmap)
        self.setIconSize(QSize(50, 50))
        self.clicked.connect(self.on_click)
        self.focus_rate = AnimatedProperty(0)
        self.focus_rate.bind_to(self._update)

    def _update(self, value):
        self.update()


    def enterEvent(self, event) -> None:
        self.focus_rate.slide_to(1, 100)
        return super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.focus_rate.slide_to(0, 100)
        return super().leaveEvent(event)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 50, 0)
        gradient.setColorAt(0.0, QColor(0, 0, 0, 0))
        gradient.setColorAt(0.1, QColor(0, 0, 0, 0))
        
        gradient.setColorAt(self.focus_rate.value, QColor(100, 100, 100, 255))
        painter.setBrush(gradient)
        painter.drawRect(0, 0, 50, 50)
        return super().paintEvent(event)

    def on_click(self, _):
        self.focus_rate.slide_to(0)
        self.tab_menu.switch_panel(self.panel)

    def initUI(self):
        super().initUI()

class Terminal(RWidget):
    def __init__(self):
        super().__init__()
        self.buffer = QLabel()
        self.buffer.setText('asd\ns')
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        
        self.vbox.addWidget(self.buffer)

class MainWindow(RWidget):
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self.resize(QSize(320, 450))
        self.move(0, 768)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setStyleSheet(
        '''
            QWidget{
                border:2px solid rgb(0, 212, 183);
                border-style: inset;
            }
        '''
        )
        self.setWindowOpacity(0.9)
        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)
        self.hbox.addWidget(Terminal())
        # </Label Properties>
        self.target_size = QSize(1200, 800)
        from core.utils import get_screen_size, get_point
        self.start_position = get_point((get_screen_size()) / 2)
        self.target_position = get_point((get_screen_size() - self.target_size) / 2)

    def setup_ui(self):
        pass

    def paintEvent(self, pe):
        painter = QtGui.QPainter(self)
        self.setWindowOpacity(self.expand_rate.value)
        painter.drawPixmap(self.rect(), QPixmap("x.png"))

class LoginScreen(RWidget):
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)
        self.vbox = QVBoxLayout()

        self.username_edit = RLineEdit()
        self.password_edit = RLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.submit_button = RPushButton()
        self.submit_button.clicked.connect(self.submit)

        self.vbox.addWidget(self.username_edit)
        self.vbox.addWidget(self.password_edit)
        self.vbox.addWidget(self.submit_button)
        self.target_size = QSize(320, 450)
        pos = (get_screen_size() - self.target_size) / 2
        self.target_position = QPoint(pos.width(), pos.height())
        pos = (get_screen_size()) / 2
        self.start_position = QPoint(pos.width(), pos.height())
        self.setLayout(self.vbox)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.8)
        painter.drawTiledPixmap(self.rect(), QPixmap('assets/image/ui-login-screen.png'))
        super().paintEvent(event)

    def submit(self):
        data = {
            'username': self.username_edit.text(),
            'password': self.password_edit.text()
        }
        data = touch_api('account/login', data=data)
        


class LoadingScreen(QMainWindow):
    def __init__(self, assistant):
        super().__init__()
        self.resize(300, 300)

        self.setStyleSheet("QMainWindow{border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.assistant = assistant
        self.task_set = assistant.load_tasks
        self.task_set.update.connect(self._task_set_update)
        self.setup_ui()
        thread = QThread()
        self.task_set.moveToThread(thread)
        self.task_set.run()

    def setup_ui(self):
        return NotImplemented

    @Slot(bool)
    def _task_set_update(self, done):
        self.on_task_update(done)
        if done:
            a = MainWindow(self.assistant)
            a.show()
            self.close()

    def on_task_update(self, done):
        return NotImplemented


class LoadingScreenHiTech(LoadingScreen):
    def setup_ui(self):
        self.resize(300, 300)

        self.setStyleSheet("QMainWindow{border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.l = QVBoxLayout()
        self.setLayout(self.l)
        self.progress = QProgressBar(self)
        self.progress.move(60, 200)
        self.progress.setGeometry(60, 200, 200, 10)
        self.progress.setLayout(self.l)
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setStyleSheet('''
            QProgressBar
            {
            border: 1px solid rgb(160,160,160);
            border-radius: 5px;
            background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f6f6, stop: 0.5 #ededed, stop: 0.55 #e4e4e4, stop: 0.6 #dbdbdb, stop: 1.0 #d2d2d2);
            font: electrolize;
            
            }
            QProgressBar::chunk
            {
                border-radius: 2px;
                background-color: cyan;
            };
            '''
        )
        self.progress.setValue(20)
        effect = QGraphicsDropShadowEffect(self.progress)
        effect.setOffset(0, 0)
        effect.setBlurRadius(10)
        self.progress.setGraphicsEffect(effect)


    def on_task_update(self, done):
        step = self.task_set.step
        self.progress.setValue(step.progress)
