from PySide.QtGui import *


class addTaskDialog(QDialog):
    def __init__(self):
        super(addTaskDialog, self).__init__()
        self.label = QLabel('Add Task')
        self.text = QLineEdit()

        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton('Cancel')
        self.cancel.clicked.connect(self.reject)

        self.buttons = QHBoxLayout()
        self.buttons.addStretch(1)
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.text)
        self.mainLayout.addLayout(self.buttons)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('Add Task')

    def check(self):
        if self.text.text() != '':
            self.accept()


class delTaskDialog(QDialog):
    def __init__(self,tasks):
        super(delTaskDialog, self).__init__()
        self.label = QLabel('Delete Task')
        self.params = QComboBox()
        for task in tasks:
            self.params.addItem(task.text())

        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton('Cancel')
        self.cancel.clicked.connect(self.reject)

        self.buttons = QHBoxLayout()
        self.buttons.addStretch(1)
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.params)
        self.mainLayout.addLayout(self.buttons)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('Delete Task')

    def check(self):
        if self.params.currentText() != '':
            self.accept()


class addGroupDialog(QDialog):
    def __init__(self):
        super(addGroupDialog, self).__init__()

        self.label = QLabel('Add Status')
        self.text = QLineEdit()
        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton('Cancel')
        self.cancel.clicked.connect(self.reject)

        self.buttons = QHBoxLayout()
        self.buttons.addStretch(1)
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.text)
        self.mainLayout.addLayout(self.buttons)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('Add Status')

    def check(self):
        if self.text.text() != '':
            self.accept()

class delGroupDialog(QDialog):
    def __init__(self, groups):
        super(delGroupDialog, self).__init__()

        self.label = QLabel('Delete Status')

        self.params = QComboBox()
        for group in groups:
            self.params.addItem(group.getName())
        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton('Cancel')
        self.cancel.clicked.connect(self.reject)

        self.buttons = QHBoxLayout()
        self.buttons.addStretch(1)
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.params)
        self.mainLayout.addLayout(self.buttons)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('Delete Status')

    def check(self):
        if self.params.currentText() != '':
            self.accept()
