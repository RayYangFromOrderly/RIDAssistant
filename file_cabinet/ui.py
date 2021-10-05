
from core.utils import apply_glow_effect
from core.ui import RWidget
from tools.ui import ToolPanel
from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class AddItem(RWidget):
    def __init__(self, folder, parent):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.folder = folder
        self.setWindowOpacity(0.5)
        self.setGeometry(0, 0, 400, 250)
        self.move(self.parent().rect().center() - self.rect().center())
        layout = QVBoxLayout()
        self.setLayout(layout)
        tab = QTabWidget()


        folder_tab = QWidget()
        container = QHBoxLayout()
        folder_tab.setLayout(container)
        container.addWidget(QLineEdit())

        tab.addTab(folder_tab, QPixmap('assets//image//icon-cabinet.png'), 'Folder')

        variable_tab = QWidget()
        container = QHBoxLayout()
        variable_tab.setLayout(container)
        self. input = QLineEdit()
        container.addWidget(self.input)

        tab.addTab(variable_tab, QPixmap('assets//image//icon-cabinet.png'), 'Variable')

        layout.addWidget(tab)
        tab.setFixedHeight(70)
        confirm_button = QPushButton('Create')
        cancel_button = QPushButton('Cancel')
        confirm_button.setFixedWidth(200)
        cancel_button.setFixedWidth(200)
        confirm_button.clicked.connect(self.confirm)

        self.tab_container = tab

        button_layout = QHBoxLayout()
        button_group = QWidget()
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        button_group.setLayout(button_layout)
        layout.addWidget(button_group)
        self.setFocusPolicy(Qt.ClickFocus)
        self.target_size = QSize(600, 200)
        self.setStyleSheet('QWidget{background-color: rgba(255, 255, 255, 50);border:2px solid rgb(0, 212, 183);}')
        apply_glow_effect(self)

    def confirm(self):
        from file_cabinet.objects import Folder, Variable
        type = self.tab_container.currentWidget().objectName()
        if type == 'Folder':
            folder = Folder()
            folder.name = self.input.text()
            self.folder.folders.append(folder)
        else:
            variable = Variable()
            variable.name = self.input.text()
            self.folder.variables.append(variable)


    def cancel(self):
        print('cancel')


class CabinetPanel(ToolPanel):
    def __init__(self, cabinet):
        super().__init__(QPixmap('assets//image//icon-cabinet.png'))
        self.path = [] # test > main > Phone
        self.current_folder = cabinet.root_folder
        self.refresh()

    def refresh(self):
        for folder in self.current_folder.folders:
            self.container.addWidget(FolderItem(folder))
        for variable in self.current_folder.variables:
            self.addWidget(VariableItem(variable))

        new_item = QPushButton()
        new_item.setText('+')
        new_item.clicked.connect(self.add_item)

        self.container.addWidget(new_item)

    def get_name(self):
        return 'Cabinet'

    def add_item(self):
        popup = AddItem(self.current_folder, self)
        popup.show()

class FolderItem(QWidget):
    def __init__(self, folder):
        self.label = QLabel(folder.name, self)
        super().__init__()

class VariableItem(QWidget):
    def __init__(self, variable):
        self.label = QLabel(variable.name, self)
        super().__init__()