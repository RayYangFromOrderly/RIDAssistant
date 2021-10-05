import os

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class AnimatedProperty(QObject):
    def __init__(self, val, easing=QEasingCurve.InOutCubic):
        super().__init__()
        self._value = val
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setEasingCurve(easing)
        self.bind_method = None
        self.value = val

    def slide_to(self, target_val, duration=500):
        self.animation.stop()
        self.animation.setDuration(duration)
        self.animation.setEndValue(target_val)
        self.animation.start()

    @Property(float)
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        if self.bind_method:
            self.bind_method(val)

    def bind_to(self, method):
        self.bind_method = method


def get_usr_root_path():
    return os.path.join(os.getenv("HOME"), ".ridassistant")

def apply_glow_effect(widget):
    effect = QGraphicsDropShadowEffect(widget)
    effect.setColor(QColor(119, 237, 219))
    effect.setOffset(0, 0)
    effect.setBlurRadius(10)
    widget.setGraphicsEffect(effect)

def get_screen_size():

    import tkinter as tk

    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return QSize(screen_width, screen_height)

def get_point(size):
    return QPoint(size.width(), size.height())