# -*- coding: utf-8 -*-
import sys
import datetime

from PySide.QtCore import *

from database import *
from tasks_widget import *
from evaluator import *
from dialogs import *
from tabs import Tabs
import language
import helpers
import globals
import save


class Layout(QWidget):
    def __init__(self):
        super(Layout, self).__init__()
        self.taskwidget = TasksWidget([])
        self.scrollarea = QScrollArea()

        # Tabs
        self.tab = Tabs()

        ##Calendar init
        self.calendar = QCalendarWidget()
        self.calendar.setMaximumHeight(200)
        self.calendar.selectionChanged.connect(self.tabCheck)


        ##Layouts
        self.vb = QVBoxLayout()
        ## Splitters
        self.vsplitter = QSplitter()
        self.bottomsplitter = QSplitter(Qt.Vertical)

        self.dragging = False
        self.dragtext = ''

        #Keeping track of changed and not currently saved tables
        self.notsaved = []

    def initTasks(self, statuses):
        """Initializes and fills the task widget"""

        stats = []
        for status in statuses:
            group = TaskGroup(status)
            tasks = getTasks(status)
            for task in tasks:
                group.addTask(Task(task))
            stats.append(group)
        self.taskwidget.setGroups(stats)
        self.taskwidget.updateme()

    def create(self):
        """Binds together every layout and widget"""

        self.scrollarea.setWidget(self.taskwidget)
        self.scrollarea.setWidgetResizable(True)

        self.tab.openTab(1)

        self.vsplitter.addWidget(self.scrollarea)
        self.vsplitter.addWidget(self.tab)

        self.bottomsplitter.addWidget(self.vsplitter)
        self.bottomsplitter.addWidget(self.calendar)

        self.vb.addWidget(self.bottomsplitter)
        self.setLayout(self.vb)

    def mousePressEvent(self, event):
        """The 'mouse-press' part of tasks drag&drop feature"""

        if event.buttons() != Qt.RightButton:
            return
        rightclick = event.pos()
        scroll = self.scrollarea.verticalScrollBar().value()
        self.rightclickpos = rightclick + QPoint(0, scroll)
        if self.taskwidget.isItemAtPoint(self.rightclickpos):
            self.dragging = True
            self.dragtext = self.taskwidget.getText(self.rightclickpos)

    def mouseReleaseEvent(self, event):
        """The 'mouse-release' part of tasks drag&drop feature"""

        if event.button() != Qt.RightButton:
            return
        if self.dragging:
            position = event.pos() - QPoint(self.taskwidget.geometry().width() + 55, 55)
            table = self.tab.currentWidget()
            if table.itemAt(position) is not None:
                table.itemAt(position).setText(self.dragtext)
        self.dragging = False

    def tabCheck(self):
        selectdate = self.calendar.selectedDate()
        startdate = helpers.fromDatetoQDate(globals.DAYFIRST)
        weeknum = helpers.getWeekDif(startdate, selectdate) + 1
        self.tab.openTab(weeknum)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connected = False
        self.mainLayout = Layout()

        #Generate the first day of usage
        today = datetime.date.today()
        dayT = today - datetime.timedelta(today.weekday())
        globals.DAYFIRST = dayT

    def draw(self):
        """Main output function"""

        ## Models should be created after database connection
        self.mainLayout.create()
        self.setCentralWidget(self.mainLayout)
        self.showMaximized()
        self.setWindowTitle('WATS?')
        self.show()

    def connectTrigger(self, name):
        if setConnection(name):
            label = 'Yeahaaaaa'
        else:
            label = 'Oh, NO'
        self.statusBar().showMessage(label)

    def initializeMenu(self):
        """Initializes the main menu and hooks up all the necessary signals"""

        # Actions
            #File
        self.loadlanguageAct = QAction(language.languagedict['lang_languageMenuItem'], self)
        self.saveAct = QAction(language.languagedict['lang_saveMenuItem'], self)
        self.loadAct = QAction(language.languagedict['lang_loadMenuItem'], self)
        self.evaluateAct = QAction(language.languagedict['lang_evaluateMenuItem'], self)

            #Edit
        self.addblockAct = QAction(language.languagedict['lang_addblockMenuItem'], self)

        self.loadlanguageAct.triggered.connect(self.loadlanguage)
        self.saveAct.triggered.connect(self.save)
        self.loadAct.triggered.connect(self.load)
        self.evaluateAct.triggered.connect(self.evaluate)
        self.addblockAct.triggered.connect(self.addblock)

        self.statusBar()
        self.menu = self.menuBar()

        #File
        self.filemenu = self.menu.addMenu(language.languagedict['lang_fileMenu'])
        self.filemenu.addAction(self.saveAct)
        self.filemenu.addAction(self.loadAct)
        self.filemenu.addAction(self.evaluateAct)
        self.filemenu.addAction(self.loadlanguageAct)

        #Edit
        self.editmenu = self.menu.addMenu(language.languagedict['lang_editMenu'])
        self.editmenu.addAction(self.addblockAct)
  #
  #
  ## <End> Functions handling  menu buttons signals

    def save(self):
        save.save(self.mainLayout)

    def load(self):
        save.load(self.mainLayout)

    def evaluate(self):
        """Sets up and shows the evaluation of schedule"""

        self.evWindow = EvaluatorWindow(self.mainLayout.table)

        days = language.languagedict['lang_mainTableHeaders']
        self.evWindow.generate(self.mainLayout.taskwidget.groups, days)

        self.evWindow.draw()

    def loadlanguage(self):
        """Loads and updates the language of program elements - the language file is chosen via dialog"""

        language.chooseLanguageFile(self)
        language.loadLanguage()
        self.updatelanguage()

    def updatelanguage(self):
        """Updates the language of already loaded elements"""

        self.mainLayout.table.setHorizontalHeaderLabels(language.languagedict['lang_mainTableHeaders'])
        self.loadlanguageAct.setText(language.languagedict['lang_languageMenuItem'])
        self.saveAct.setText(language.languagedict['lang_saveMenuItem'])
        self.loadAct.setText(language.languagedict['lang_loadMenuItem'])
        self.evaluateAct.setText(language.languagedict['lang_evaluateMenuItem'])
        self.filemenu.setTitle(language.languagedict['lang_fileMenu'])
        self.addblockAct.setText(language.languagedict['lang_addblockMenuItem'])
        self.editmenu.setTitle(language.languagedict['lang_editMenu'])

    def addblock(self):
        """Adds the tasks onto main table - the properties of the block are received through dialog"""

        dialog = addBlockDialog(self.mainLayout.taskwidget.groups)
        dialog.exec_()
        if dialog.result() == QDialog.Accepted:

            # # Reading information
            task = dialog.tasks.currentText()
            weekday = dialog.weekday.currentText()
            start = dialog.start.time()
            end = dialog.end.time()

            # # Rounding minutes
            if start.minute() > 30:
                start = QTime(start.hour(), 30)
            else:
                start = QTime(start.hour(), 0)

            if end.minute() > 30:
                end = QTime(end.hour(), 30)
            else:
                end = QTime(end.hour(), 0)

            start = start.toString('hh:mm')
            end = end.toString('hh:mm')
            self.mainLayout.table.setItemTime(task, start, end, weekday)


def main():
    app = QApplication(sys.argv)
    language.loadLanguage()

    mainGui = MainWindow()
    mainGui.initializeMenu()
    mainGui.draw()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()