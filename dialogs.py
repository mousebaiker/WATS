from PySide.QtGui import *
from language import languagedict

class addTaskDialog(QDialog):
    def __init__(self):
        super(addTaskDialog, self).__init__()
        self.label = QLabel(languagedict['lang_addTaskText'])
        self.text = QLineEdit()

        self.ok = QPushButton(languagedict['lang_OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['lang_CancelButton'])
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
        self.setWindowTitle(languagedict['lang_addTaskTitle'])

    def check(self):
        if self.text.text() != '':
            self.accept()


class delTaskDialog(QDialog):
    def __init__(self,tasks):
        super(delTaskDialog, self).__init__()
        self.label = QLabel(languagedict['lang_delTaskText'])
        self.params = QComboBox()
        for task in tasks:
            self.params.addItem(task.text())

        self.ok = QPushButton(languagedict['lang_OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['lang_CancelButton'])
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
        self.setWindowTitle(languagedict['lang_delTaskTitle'])

    def check(self):
        if self.params.currentText() != '':
            self.accept()


class addGroupDialog(QDialog):
    def __init__(self):
        super(addGroupDialog, self).__init__()

        self.label = QLabel(languagedict['lang_addStatusText'])
        self.text = QLineEdit()
        self.ok = QPushButton(languagedict['lang_OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['lang_CancelButton'])
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
        self.setWindowTitle(languagedict['lang_addStatusTitle'])

    def check(self):
        if self.text.text() != '':
            self.accept()

class delGroupDialog(QDialog):
    def __init__(self, groups):
        super(delGroupDialog, self).__init__()

        self.label = QLabel(languagedict['lang_delStatusText'])

        self.params = QComboBox()
        for group in groups:
            self.params.addItem(group.getName())
        self.ok = QPushButton(languagedict['lang_OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['lang_CancelButton'])
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
        self.setWindowTitle(languagedict['lang_delStatusTitle'])

    def check(self):
        if self.params.currentText() != '':
            self.accept()
