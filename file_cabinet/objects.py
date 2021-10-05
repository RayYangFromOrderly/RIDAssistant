from PySide6.QtCore import QObject, QRect
from PySide6.QtWidgets import QRadioButton
from file_cabinet.ui import CabinetPanel
import os
import json
from abc import ABC

from tools.objects import Tool


class Cabinet(Tool):
    def setup(self):
        if not os.path.isfile('file_tree.json'):
            with open('file_tree.json', 'w') as file:
                file.write('{"name": "Root"}')

        self.file_tree = json.load(open('file_tree.json'))
        self.root_folder = Folder(self.file_tree)
        panel = CabinetPanel(self)
        self.assistant.add_tab(panel)
        panel.setGeometry(QRect(0, 0, 500, 500))
        panel.container.addWidget(QRadioButton())


class Folder:
    def __init__(self, data):
        if data:
            self.name = data['name']
            self.folders = []
            self.variables = []
            if 'nodes' in data:
                for node in data['nodes']:
                    if node['type'] == 'folder':
                        folder = Folder(node)
                        self.folders.append(folder)
                    else:
                        variable = Variable(node)
                        self.variables.append(variable)


class Variable:
    def __init__(self, node=None):
        if node:
            self.name = node['name']
            source_type = node['source_type']
            for Source in VariableSource.__subclasses__():
                if Source.__name__ == source_type:
                    source_type = Source
                    break

            self.source = source_type(node['source'])
            self.id = node['id']

    def get_value(self):
        return self.source.get_value()

class VariableSource(ABC):
    def __init__(self, data):
        self.id = data['id']

    def get_value():
        return NotImplemented


class Value(VariableSource):
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value
