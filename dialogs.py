from PySide.QtGui import *
from PySide.QtCore import QTime, Qt, Slot, Signal

from maintable import MainTable
from language import languagedict
import global_vars
import helpers


class addTaskDialog(QDialog):
    """Dialog for adding tasks"""
    def __init__(self):
        super(addTaskDialog, self).__init__()
        self.label = QLabel(languagedict['addTaskText'])
        self.text = QLineEdit()

        self.ok = QPushButton(languagedict['OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['CancelButton'])
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
        self.setWindowTitle(languagedict['addTaskTitle'])

    def check(self):
        if self.text.text() != '':
            self.accept()


class delTaskDialog(QDialog):
    """Dialog for deleting tasks"""
    def __init__(self, tasks):
        super(delTaskDialog, self).__init__()
        self.label = QLabel(languagedict['delTaskText'])
        self.params = QComboBox()
        for task in tasks:
            self.params.addItem(task.text())

        self.ok = QPushButton(languagedict['OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['CancelButton'])
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
        self.setWindowTitle(languagedict['delTaskTitle'])

    def check(self):
        if self.params.currentText() != '':
            self.accept()


class addGroupDialog(QDialog):
    """Dialog for adding groups"""
    def __init__(self):
        super(addGroupDialog, self).__init__()

        self.label = QLabel(languagedict['addStatusText'])
        self.text = QLineEdit()
        self.ok = QPushButton(languagedict['OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['CancelButton'])
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
        self.setWindowTitle(languagedict['addStatusTitle'])

    def check(self):
        if self.text.text() != '':
            self.accept()


class delGroupDialog(QDialog):
    """Dialog for deleting groups"""
    def __init__(self, groups):
        super(delGroupDialog, self).__init__()

        self.label = QLabel(languagedict['delStatusText'])

        self.params = QComboBox()
        for group in groups:
            self.params.addItem(group.getName())
        self.ok = QPushButton(languagedict['OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['CancelButton'])
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
        self.setWindowTitle(languagedict['delStatusTitle'])

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

        # Layouts
        self.topLayout = QVBoxLayout()
        self.mainLayout = QGridLayout()
        self.timeLayout = QHBoxLayout()
        self.buttons = QHBoxLayout()

        # Main Elements
        self.statusLabel = QLabel(languagedict['addBlockStatus'])
        self.status = QComboBox()
        for status in groups:
            self.status.addItem(status.getName())
        self.status.activated.connect(self.updatetasks)

        self.tasksLabel = QLabel(languagedict['addBlockTask'])
        self.tasks = QComboBox()

        self.weekdayLabel = QLabel(languagedict['addBlockWeekday'])
        self.weekday = QComboBox()
        for weekday in languagedict['mainTableHeaders']:
            self.weekday.addItem(weekday)

        self.timeLabel = QLabel(languagedict['addBlockTime'])
        self.start = QTimeEdit(QTime(6, 0))
        self.start.setDisplayFormat('hh:mm')
        self.end = QTimeEdit(QTime(7, 0))
        self.end.setDisplayFormat('hh:mm')

        # Buttons
        self.ok = QPushButton(languagedict['OKButton'])
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton(languagedict['CancelButton'])
        self.cancel.clicked.connect(self.reject)

        # Laying out
        # Time
        self.timeLayout.addWidget(self.start)
        self.timeLayout.addWidget(self.end)

        # Central
        self.mainLayout.addWidget(self.statusLabel, 0, 0)
        self.mainLayout.addWidget(self.status, 1, 0)
        self.mainLayout.addWidget(self.tasksLabel, 0, 1)
        self.mainLayout.addWidget(self.tasks, 1, 1)
        self.mainLayout.addWidget(self.weekdayLabel, 2, 0)
        self.mainLayout.addWidget(self.weekday, 3, 0)
        self.mainLayout.addWidget(self.timeLabel, 2, 1)
        self.mainLayout.addLayout(self.timeLayout, 3, 1)

        # Buttons
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)

        # Top level
        self.topLayout.addWidget(self.errorstatus)
        self.topLayout.addLayout(self.mainLayout)
        self.topLayout.addLayout(self.buttons)

        # Main settings
        self.setLayout(self.topLayout)
        self.setWindowTitle(languagedict['addBlockTitle'])

    def check(self):
        if self.start.time() <= self.end.time():
            self.accept()
        else:
            self.errorstatus.setText(languagedict['addBlockTimeError'])


    def updatetasks(self):
        status = (i for i in self.groups if self.status.currentText() == i.getName())
        status = next(status)

        self.tasks.clear()
        for task in status:
            self.tasks.addItem(task.getTask())


class Scroller(QWidget):
    changed = Signal(str)

    def __init__(self, scrollvalues):
        super(Scroller, self).__init__()

        # Scroller values
        self.scrollervalues = scrollvalues
        self.curscrollindex = 0
        self.curscrolltext = self.scrollervalues[self.curscrollindex]

        # Mid label
        self.curscrolllabel = QLabel('<h2>' + str(self.curscrolltext) + '</h2>')

        # Arrows
        leftarrowImage = QPixmap.fromImage(QImage('icons/left_arrow.png'))
        self.leftarrow = QLabel()
        self.leftarrow.setPixmap(leftarrowImage)

        rightarrowImage = QPixmap.fromImage(QImage('icons/right_arrow.png'))
        self.rightarrow = QLabel()
        self.rightarrow.setPixmap(rightarrowImage)

        self.arrows = QHBoxLayout()
        self.arrows.addWidget(self.leftarrow)
        self.arrows.addStretch(1)
        self.arrows.addWidget(self.curscrolllabel)
        self.arrows.addStretch(1)
        self.arrows.addWidget(self.rightarrow)

        self.mainlayout = QVBoxLayout()
        self.mainlayout.addLayout(self.arrows)
        self.setLayout(self.mainlayout)

    def shift(self, value):
        if (self.curscrollindex + value >= len(self.scrollervalues)) or (self.curscrollindex + value < 0):
            return
        self.curscrollindex += value
        self.curscrolltext = self.scrollervalues[self.curscrollindex]
        self.curscrolllabel.setText('<h2>' + str(self.curscrolltext) + '</h2>')
        self.changed.emit(str(self.curscrolltext))

    def shifttoleft(self):
        self.shift(-1)

    def shifttoright(self):
        self.shift(1)

    def gettext(self):
        return self.curscrolltext


    def mousePressEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        position = event.pos()
        if helpers.isItemAtPoint(position, self.mainlayout):
            item = helpers.itemAtPoint(position, self.mainlayout)

            # Repeat until we get an actual item
            prevlayout = QHBoxLayout()
            while isinstance(item, QLayout):
                prevlayout = item
                item = helpers.itemAtPoint(position, item)
            if isinstance(item, QWidgetItem) and isinstance(item.widget(), QLabel):
                index = prevlayout.indexOf(item.widget())
                if index == 0:
                    self.shifttoleft()
                if index == 4:
                    self.shifttoright()


class EvaluationDialog(QDialog):
    def __init__(self, weeknum, upperconstraints):
        super(EvaluationDialog, self).__init__()
        self.weeknum = weeknum
        self.upperconstraints = upperconstraints

        self.slidervalues = global_vars.EVAL_VALUES.get(self.weeknum, [0 for i in range(7)])

        # Layouts
        self.arrows = QHBoxLayout()
        self.buttons = QHBoxLayout()
        self.vbox = QVBoxLayout()

        # Upper label
        self.label = QLabel()
        self.label.setText('<div align = "center"><h3>'
                           + languagedict['WeekHeader'] + ' '
                           + str(self.weeknum) + '</h3></div>')

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.upperconstraints[0])
        self.slider.setTickInterval(1)
        self.slider.setValue(self.slidervalues[0])
        self.slider.valueChanged.connect(self.sliderChanged)

        self.sliderlabel = QLabel(
            '<div align = "center"><font size = "14">' + str(self.slider.value()) + '</font></div>')

        # Buttons
        self.ok = QPushButton(languagedict['OKButton'])
        self.ok.clicked.connect(self.okPush)
        self.cancel = QPushButton(languagedict['CancelButton'])
        self.cancel.clicked.connect(self.reject)

        # Layouts set-up
        # Buttons
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)

        # Scroller
        self.scroller = Scroller(languagedict['mainTableHeaders'])
        self.scroller.changed.connect(self.scrollerChanged)

        # Main elements
        self.vbox.addWidget(self.label)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.scroller)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.sliderlabel)
        self.vbox.addWidget(self.slider)
        self.vbox.addLayout(self.buttons)

        self.setLayout(self.vbox)
        self.setWindowTitle(languagedict['evaluateMenuItem'])

    def okPush(self):
        global_vars.EVAL_VALUES[self.weeknum] = self.slidervalues
        self.accept()

    @Slot(str)
    def scrollerChanged(self, weekday):
        num = global_vars.WEEKDAYSLANGUAGE.index(weekday)
        self.slider.setMaximum(self.upperconstraints[num])
        self.slider.setValue(self.slidervalues[num])

    @Slot(int)
    def sliderChanged(self, value):
        self.sliderlabel.setText('<div align = "center"><font size = "14">' + str(value) + '</font></div>')
        self.slidervalues[global_vars.WEEKDAYSLANGUAGE.index(self.scroller.gettext())] = value


class GenerateDayDialog(QDialog):
    def __init__(self):
        super(GenerateDayDialog, self).__init__()
        # Return variables
        self.isweek = False

        # Header
        self.title = languagedict['generateLabel']
        self.titlelabel = QLabel('<div align = "center"><h3> ' + self.title + '</h3></div>')
        # Options
        self.options = QComboBox()
        for day in languagedict['mainTableHeaders']:
            self.options.addItem(day)

        # Buttons
        self.ok = QPushButton(languagedict['OKButton'])
        self.cancel = QPushButton(languagedict['CancelButton'])
        self.generateweek = QPushButton(languagedict['generateWholeWeek'])
        self.generateweek.setMaximumWidth(100)
        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)
        self.generateweek.clicked.connect(self.weekPush)

        # Layouts
        self.buttons = QHBoxLayout()
        self.vbox = QVBoxLayout()

        # Layout set up
        # Buttons
        self.buttons.addWidget(self.generateweek)
        self.buttons.addStretch(1)
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)


        # Main
        self.vbox.addWidget(self.titlelabel)
        self.vbox.addWidget(self.options)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.buttons)

        self.setLayout(self.vbox)
        self.setWindowTitle(languagedict['generateTitle'])

    def isWeek(self):
        return self.isweek

    def getDay(self):
        return self.options.currentText()

    @Slot()
    def weekPush(self):
        self.isweek = True
        self.accept()


class ShowDayDialog(QDialog):
    def __init__(self, day, schedules):
        super(ShowDayDialog, self).__init__()

        self.schedules = schedules

        # Layouts
        self.buttons = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        # Widgets
        self.scroller = Scroller(range(len(self.schedules)))
        self.scroller.changed.connect(self.updateDay)

        # Table
        self.table = MainTable(-1)
        self.table.columnheaders = [global_vars.WEEKDAYSLANGUAGE[global_vars.WEEKDAYS.index(day)]]
        self.table.generate(self.table.columnheaders, self.table.rowsheaders)
        self.table.setColumnWidth(0, 230)

        # Buttons
        self.ok = QPushButton(languagedict['OKButton'])
        self.ok.clicked.connect(self.accept)
        self.cancel = QPushButton(languagedict['CancelButton'])
        self.cancel.clicked.connect(self.reject)

        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)

        self.mainLayout.addWidget(self.scroller)
        self.mainLayout.addWidget(self.table)
        self.mainLayout.addLayout(self.buttons)

        self.setLayout(self.mainLayout)
        self.setWindowTitle(languagedict['showDayTitle'])
        self.setMinimumSize(300, 500)

        self.updateDay(0)

    @Slot(str)
    def updateDay(self, option):
        option = int(option)
        self.showDay(self.schedules[option])

    def showDay(self, schedule):
        scheduledict = {}
        for i, value in enumerate(schedule):
            scheduledict[i] = value

        self.table.setItemsColumn(scheduledict, 0)

    def getDay(self):
        return int(self.scroller.gettext())

