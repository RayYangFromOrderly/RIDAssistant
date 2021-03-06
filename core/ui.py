
from core.utils import AnimatedProperty
from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from core.utils import get_screen_size


class RCollectionDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QGridLayout())

        self.items = []

    def add_item(self, item):
        self.layout().addWidget(item)

class RGridDisplay(RCollectionDisplay):
    def __init__(self):
        super().__init__()
        self.setLayout(QGridLayout())


class RPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus_rate = AnimatedProperty(0)
        self.focus_rate.bind_to(self._update)
        self.target_size = QSize(200, 50)
        self.start_size = QSize(100, 50)

    def focusInEvent(self, event):
        self.focus_rate.slide_to(1)

    def focusOutEvent(self, event):
        self.focus_rate.slide_to(0)

    def _update(self, val):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        center = self.height()
        rad = 10
        gradient = QLinearGradient(0, center-rad*2, 0, center)
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(0.5, QColor(0, 212, 183, 255 * self.focus_rate.value))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(gradient))
        half_width = self.height() / 2

        points = [
            QPoint(half_width, 0), QPoint(0, half_width), QPoint(half_width, self.height()),
            QPoint(self.width() - half_width, self.height()), QPoint(self.width(), self.height() - half_width),
            QPoint(self.width() - half_width, 0)
        ]

        painter.drawPolygon(points)
        self.setText('100')
        self.setFont(QFont('electrolize'))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())
        self.resize(self.start_size + (self.target_size - self.start_size) * self.focus_rate.value)


class RLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus_rate = AnimatedProperty(0)
        self.focus_rate.bind_to(self._update)
        self.setMaxLength(30)
        self.setStyleSheet('padding-left: 10px;border: 0px solid red; background-color: rgba(0, 0, 0, 0);font: 20px "electrolize"')

    def focusInEvent(self, event):
        self.focus_rate.slide_to(1)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.focus_rate.slide_to(0)
        super().focusOutEvent(event)

    def _update(self, val):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        center = self.height()
        rad = 10
        gradient = QLinearGradient(0, center-rad, 0, center+rad)
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(0.5, QColor(0, 0, 0, 255))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(gradient))
        half_height = self.height() / 2
        first_rate = min(self.focus_rate.value / 10, 0.1)
        second_rate = (self.focus_rate.value - first_rate) / 10 * 9

        points = [QPoint(0, half_height), QPoint(half_height, self.height())]
        painter.setPen(QPen(QColor(0, 212, 183), 2))
        painter.drawPolyline(points)

        points = [QPoint(half_height, self.height()), QPoint(self.width() * second_rate, self.height())]
        painter.setPen(QPen(QColor(0, 212, 183), 2))
        painter.drawPolyline(points)
        painter.setPen(QPen(QColor(255, 255, 255)))
        super().paintEvent(event)


class SearchBox(RLineEdit):
    def __init__(self, *args):
        super().__init__(*args)
        self.model = QStringListModel()
        self.model.setStringList(['some', 'words', 'in', 'my', 'dictionary'])

        self.completer = QCompleter()
        self.completer.setModel(self.model)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(self.completer)

    def set_selections(self, selections):
        self.model.setStringList(selections)


class RWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_size = get_screen_size()
        self.expand_rate = AnimatedProperty(0)
        self.target_position = QPoint(0, 0)

        self.start_position = QPoint(0, 0)

    def show(self, *args, **kwargs):
        super().show(*args, **kwargs)
        self.expand_rate.bind_to(self.expand)
        self.expand_rate.slide_to(1)

    def expand(self, rate):
        value = self.target_size * rate
        self.resize(value)
        self.move(self.start_position + (self.target_position - self.start_position) * rate)


class UnitButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(100, 100)
        half_width = self.width() / 2
        self.points = [QPoint(half_width, 0), QPoint(0, half_width), QPoint(half_width, self.width()), QPoint(self.width(), half_width),  QPoint(half_width, 0)]
        self.setMask(QRegion(QPolygon(self.points)))
        self.focus_rate = AnimatedProperty(0)
        self.focus_rate.bind_to(self._update)

    def _update(self, value):
        self.update()

    def enterEvent(self, event) -> None:
        self.focus_rate.slide_to(1, 200)
        return super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.focus_rate.slide_to(0, 200)
        return super().leaveEvent(event)

    def paintEvent(self, _=None):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 212, 183), 3))
        painter.drawPolyline(QPolygon(self.points))

        gradient = QLinearGradient(50, 100, 50, 0)
        gradient.setColorAt(0.0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))


        gradient.setColorAt(0.0, QColor(0, 212, 183, 0))
        gradient.setColorAt(1.0, QColor(0, 212, 183, 100))

        gradient.setColorAt(0.0, QColor(0, 0, 0, 100 * self.focus_rate.value))
        painter.setBrush(gradient)
        painter.drawPolygon(QPolygon(self.points))

        painter.setPen(QPen(gradient, 10))
        painter.drawPolyline(QPolygon(self.points))
        super().paintEvent(_)


class UnitPanel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(100, 100)
        half_width = self.width() / 2
        self.points = [QPoint(half_width, 0), QPoint(0, half_width), QPoint(half_width, self.width()), QPoint(self.width(), half_width),  QPoint(half_width, 0)]
        self.setMask(QRegion(QPolygon(self.points)))
        self.focus_rate = AnimatedProperty(0)
        self.focus_rate.bind_to(self._update)

    def _update(self, value):
        self.update()

    def enterEvent(self, event) -> None:
        self.focus_rate.slide_to(1, 200)
        return super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.focus_rate.slide_to(0, 200)
        return super().leaveEvent(event)

    def paintEvent(self, _=None):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 212, 183), 3))
        painter.drawPolyline(QPolygon(self.points))

        gradient = QLinearGradient(50, 100, 50, 0)
        gradient.setColorAt(0.0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))


        gradient.setColorAt(0.0, QColor(0, 212, 183, 0))
        gradient.setColorAt(1.0, QColor(0, 212, 183, 100))

        gradient.setColorAt(0.0, QColor(0, 0, 0, 100 * self.focus_rate.value))
        painter.setBrush(gradient)
        painter.drawPolygon(QPolygon(self.points))

        painter.setPen(QPen(gradient, 10))
        painter.drawPolyline(QPolygon(self.points))
        super().paintEvent(_)


class NeoLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.units = []

    def paintEvent(self, pe):
        
        painter = QtGui.QPainter(self)
        painter.setFont(QFont('Consolas', 10))
        if self.units:
            from core.utils import get_point
            for i, unit in enumerate(self.units):
                direction = unit.direction
                begin = unit.begin
                style = unit.style

                size_rate = i / len(self.units)
                size = QPoint(500, 500)
                left_top = size * (size_rate) / 2
                r = 250 * (1-size_rate)
                import math
                rate = min(1, unit.current / unit.max)
                end = begin + rate * direction
                angle = end * math.pi * 2

                y = -math.sin(angle) * r
                x = math.cos(angle) * r

                x += 250
                y += 250
                size = size * (1-size_rate/2)
                if style == 'arc':
                    painter.setPen(QPen(QColor(128, 238, 242, 50), 3))
                    painter.setBrush(QBrush(QColor(100, 100, 100)))

                elif style == 'bar_fill':
                    pen = QPen(QColor(128, 238, 242, 90), 20, Qt.DotLine)
                    painter.setPen(pen)

                elif style == 'pane':
                    painter.setPen(QPen(QColor(128, 238, 242, 30), 60))

                elif style == 'dash':
                    pen = QPen(QColor(128, 238, 242, 90), 10, Qt.DashLine)
                    painter.setPen(pen)

                painter.drawArc(QRect(left_top, size), begin * 16 * 360, rate * 16 * 360 * direction)
                painter.drawText(QPoint(x, y), unit.text())
                if rate >= 1:
                    unit.glow += 0.1 * unit.glow_direction
                    pen = painter.pen()
                    pen.setColor(QColor(255, 255, 255, unit.glow * 255))
                    painter.setPen(pen)
                    painter.drawArc(QRect(left_top, size), begin * 16 * 360, rate * 16 * 360 * direction)
                    if unit.glow_direction > 0 and unit.glow >= 1 or (unit.glow_direction < 0 and unit.glow <= 0):
                        unit.glow_direction *= -1
                        unit.glow_count += 1
                        if unit.glow_count == 4:
                            self.units.remove(unit)

    def load(self, unit):
        self.units.append(unit)
