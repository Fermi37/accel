
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class QuitButton:

    def __init__(self, main_window, button_name):
        self.btn = QtGui.QPushButton(self.button_name)
        self.button_name = button_name
        self.main_window = main_window

    def action_handle(self):
        self.main_window.close()

    def make(self):
        return self.btn.clicked.connect(self.action_handle())


class SaveButton(QuitButton):
    def action_handle(self):
        pass


class PauseButton(QuitButton):
    def action_handle(self):
        pass

