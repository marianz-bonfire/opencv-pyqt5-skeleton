from PyQt5.QtWidgets import *


class SourceView(QTreeView, QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainWindow = parent
        self.bottom_widget = QWidget()
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.addWidget(QLabel('Control Options:'))

        # Add a text field (QLineEdit)
        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText('Enter control input...')
        self.bottom_layout.addWidget(self.text_field)

        self.bottom_widget.setLayout(self.bottom_layout)

    def select_source(self):
        pass

