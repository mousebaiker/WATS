from PySide.QtGui import *
from PySide.QtCore import QTime
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


class addBlockDialog(QDialog):
    def __init__(self, groups, weekdays):
        super(addBlockDialog, self).__init__()
        self.groups = groups

        ##Layouts
        self.topLayout = QVBoxLayout()
        self.mainLayout = QGridLayout()
        self.timeLayout = QHBoxLayout()
        self.buttons = QHBoxLayout()


        ##Main Elements
        self.statusLabel = QLabel(u'Статус')
        self.status = QComboBox()
        for status in groups:
            self.status.addItem(status.getName())
        self.status.activated.connect(self.updatetasks)

        self.tasksLabel = QLabel(u'Задание')
        self.tasks = QComboBox()

        self.weekdayLabel = QLabel(u'День недели')
        self.weekday = QComboBox()
        for weekday in weekdays:
            self.weekday.addItem(weekday)

        self.timeLabel = QLabel(u'Время')
        self.start = QTimeEdit(QTime(6, 0))
        self.start.setDisplayFormat('hh:mm')
        self.end = QTimeEdit(QTime(7, 0))
        self.end.setDisplayFormat('hh:mm')

        ##Buttons
        self.ok = QPushButton(languagedict['lang_OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['lang_CancelButton'])
        self.cancel.clicked.connect(self.reject)

        ##Laying out
            #Time
        self.timeLayout.addWidget(self.start)
        self.timeLayout.addWidget(self.end)

            #Central
        self.mainLayout.addWidget(self.statusLabel, 0, 0)
        self.mainLayout.addWidget(self.status, 1, 0)
        self.mainLayout.addWidget(self.tasksLabel, 0, 1)
        self.mainLayout.addWidget(self.tasks, 1, 1)
        self.mainLayout.addWidget(self.weekdayLabel, 2, 0)
        self.mainLayout.addWidget(self.weekday, 3, 0)
        self.mainLayout.addWidget(self.timeLabel, 2, 1)
        self.mainLayout.addLayout(self.timeLayout, 3,1)

            #Buttons
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)

            #Top level
        self.topLayout.addLayout(self.mainLayout)
        self.topLayout.addLayout(self.buttons)

        # Main settings
        self.setLayout(self.topLayout)
        self.setWindowTitle(u'Добавить блок заданий')

    def check(self):
        self.accept()

    def updatetasks(self):
        status = (i for i in self.groups if self.status.currentText() == i.getName())
        status = next(status)

        self.tasks.clear()
        for task in status:
            self.tasks.addItem(task.getTask())