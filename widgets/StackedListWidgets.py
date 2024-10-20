from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from constants.filters import items


class StackedListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainWindow = parent
        self.setDragEnabled(True)
        self.setWordWrap(True)

        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)


class ScreenListWidget(StackedListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setFlow(QListView.TopToBottom)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.itemClicked.connect(self.show_frame)
        self.setMinimumWidth(200)

        self.move_item = None

    def contextMenuEvent(self, e):

        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item: return
        menu = QMenu()
        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(lambda: self.delete_item(item))
        menu.addAction(delete_action)
        menu.exec(QCursor.pos())

    def delete_item(self, item):

        self.takeItem(self.row(item))
        self.mainWindow.update_image()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.mainWindow.update_image()

    def show_frame(self):
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item: return
        param = item.get_params()
        if type(item) in items:
            index = items.index(type(item))
            self.mainWindow.stackedWidget.setCurrentIndex(index)
            self.mainWindow.stackedWidget.currentWidget().update_params(param)

