from PySide.QtGui import *
from PySide.QtCore import QTime, Qt, Slot

from language import languagedict
import global_vars
import helpers


class addTaskDialog(QDialog):
    """Dialog for adding tasks"""
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
    """Dialog for deleting tasks"""
    def __init__(self, tasks):
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
    """Dialog for adding groups"""
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
    """Dialog for deleting groups"""
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
    """Dialog for adding the block of tasks"""
    def __init__(self, groups):
        super(addBlockDialog, self).__init__()
        self.groups = groups

        # Status
        self.errorstatus = QLabel()

        ##Layouts
        self.topLayout = QVBoxLayout()
        self.mainLayout = QGridLayout()
        self.timeLayout = QHBoxLayout()
        self.buttons = QHBoxLayout()


        ##Main Elements
        self.statusLabel = QLabel(languagedict['lang_addBlockStatus'])
        self.status = QComboBox()
        for status in groups:
            self.status.addItem(status.getName())
        self.status.activated.connect(self.updatetasks)

        self.tasksLabel = QLabel(languagedict['lang_addBlockTask'])
        self.tasks = QComboBox()

        self.weekdayLabel = QLabel(languagedict['lang_addBlockWeekday'])
        self.weekday = QComboBox()
        for weekday in languagedict['lang_mainTableHeaders']:
            self.weekday.addItem(weekday)

        self.timeLabel = QLabel(languagedict['lang_addBlockTime'])
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
        self.mainLayout.addLayout(self.timeLayout, 3, 1)

            #Buttons
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)

            #Top level
        self.topLayout.addWidget(self.errorstatus)
        self.topLayout.addLayout(self.mainLayout)
        self.topLayout.addLayout(self.buttons)

        # Main settings
        self.setLayout(self.topLayout)
        self.setWindowTitle(languagedict['lang_addBlockTitle'])

    def check(self):
        if self.start.time() <= self.end.time():
            self.accept()
        else:
            self.errorstatus.setText(languagedict['lang_addBlockTimeError'])


    def updatetasks(self):
        status = (i for i in self.groups if self.status.currentText() == i.getName())
        status = next(status)

        self.tasks.clear()
        for task in status:
            self.tasks.addItem(task.getTask())


class evaluationDialog(QDialog):
    def __init__(self, weeknum):
        super(evaluationDialog, self).__init__()
        self.weeknum = weeknum

        self.slidervalues = global_vars.EVAL_VALUES.get(self.weeknum, [0 for i in range(7)])

        # Layouts
        self.arrows = QHBoxLayout()
        self.buttons = QHBoxLayout()
        self.vbox = QVBoxLayout()

        # Upper label
        self.label = QLabel()
        self.label.setText('<div align = "center"><h3> Неделя №' + str(self.weeknum) + '</h3></div>')

        # Weekdays list
        self.weekday = QLabel()
        self.weekday.setText('<h4>' + global_vars.WEEKDAYS[0] + '</h4>')
        self.weekdaynum = 0

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10)
        self.slider.setTickInterval(1)
        self.slider.setValue(self.slidervalues[0])
        self.slider.valueChanged.connect(self.sliderChanged)

        self.sliderlabel = QLabel(
            '<div align = "center"><font size = "14">' + str(self.slider.value()) + '</font></div>')

        # Buttons
        self.ok = QPushButton(languagedict['lang_OKButton'])
        self.ok.clicked.connect(self.okPush)
        self.cancel = QPushButton(languagedict['lang_CancelButton'])
        self.cancel.clicked.connect(self.reject)

        # Arrows
        leftarrowImage = QPixmap.fromImage(QImage('icons/left_arrow.png'))
        self.leftarrow = QLabel()
        self.leftarrow.setPixmap(leftarrowImage)

        rightarrowImage = QPixmap.fromImage(QImage('icons/right_arrow.png'))
        self.rightarrow = QLabel()
        self.rightarrow.setPixmap(rightarrowImage)

        # Layouts set-up
        # Buttons
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)

        # Arrows
        self.arrows.addWidget(self.leftarrow)
        self.arrows.addStretch(1)
        self.arrows.addWidget(self.weekday)
        self.arrows.addStretch(1)
        self.arrows.addWidget(self.rightarrow)

        # Main elements
        self.vbox.addWidget(self.label)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.arrows)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.sliderlabel)
        self.vbox.addWidget(self.slider)
        self.vbox.addLayout(self.buttons)

        self.setLayout(self.vbox)
        self.setWindowTitle("Оценить")

    def okPush(self):
        global_vars.EVAL_VALUES[self.weeknum] = self.slidervalues
        self.accept()

    def mousePressEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        position = event.pos()
        if helpers.isItemAtPoint(position, self.vbox):
            item = helpers.itemAtPoint(position, self.vbox)

            # Repeat until we get an actual item
            while (isinstance(item, QLayout)):
                prevlayout = item
                item = helpers.itemAtPoint(position, item)
            if isinstance(item, QWidgetItem) and isinstance(item.widget(), QLabel):
                index = prevlayout.indexOf(item.widget())
                if index == 0:
                    self.shifttoleft()
                if index == 4:
                    self.shifttoright()

    def shift(self, value):
        try:
            global_vars.WEEKDAYS[self.weekdaynum + value]
        except IndexError:
            return

        self.weekdaynum += value
        self.weekday.setText('<h4>' + global_vars.WEEKDAYS[self.weekdaynum] + '</h4>')
        self.slider.setValue(self.slidervalues[self.weekdaynum])

    def shifttoleft(self):
        self.shift(-1)


    def shifttoright(self):
        self.shift(1)

    @Slot(int)
    def sliderChanged(self, value):
        self.sliderlabel.setText('<div align = "center"><font size = "14">' + str(value) + '</font></div>')
        self.slidervalues[self.weekdaynum] = value

