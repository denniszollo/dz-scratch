import time

from pyface.qt import QtGui, QtCore

from traits.api import Instance, Int, Str
from traitsui.qt4.editor import Editor
from traitsui.api import ProgressEditor

class SimpleEditor(ProgressEditor):

    def init(self, parent=ProgressEditor()):
        pass

