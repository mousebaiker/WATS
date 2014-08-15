# -*- coding: utf-8 -*-
import sys

from PySide.QtCore import *

from database import *
from maintable import *
from tasks_widget import *
from evaluator import *
from dialogs import *
import language
import paths
import datetime
import os
import helpers
import globals


class Layout(QWidget):
    def __init__(self):
        super(Layout, self).__init__()
        self.taskwidget = TasksWidget([])
        self.scrollarea = QScrollArea()
        self.tab = QTabWidget()

        ##Calendar init
        self.calendar = QCalendarWidget()
        self.calendar.setMaximumHeight(200)
        self.calendar.selectionChanged.connect(self.tabCheck)

        self.table = MainTable(1)
        ##Layouts        self.hb = QHBoxLayout()
        self.vb = QVBoxLayout()
        ## Splitters
        self.vsplitter = QSplitter()
        self.bottomsplitter = QSplitter(Qt.Vertical)

        self.dragging = False
        self.dragtext = ''

    def initTasks(self):
        """Initializes and fills the task widget"""

        statuses = getStatuses()
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

        self.tab.addTab(self.table, 'Week 1')

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
            position = event.pos() - QPoint(self.taskwidget.geometry().width() + 55, 30)
            if self.table.itemAt(position) is not None:
                self.table.itemAt(position).setText(self.dragtext)
        self.dragging = False

    def tabCheck(self):
        date = self.calendar.selectedDate()


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

    @helpers.filemove('save')
    def save(self):
        """"Saves the state of the program and moves the save file to specified place"""

        # Create a file if there is no previous save
        # else move db to current folder to save
        if not os.path.isfile(paths.savePath):
            # Create txt and write down the first day of usage
            savefile = open(paths.savePath, mode = 'w')
            savefile.write(str(globals.DAYFIRST.toordinal()))
            savefile.close()

        filename = os.path.basename(paths.savePath)[:-8]
    ## Saving tasks widget block
    #
        self.connectTrigger(filename)
        truncate()
        groups = self.mainLayout.taskwidget.getGroups()

        for group in groups:
            query = QSqlQuery()
            query.prepare("INSERT INTO status (name) VALUES (:name)")
            query.bindValue(":name", group.getName())
            query.exec_()

            query = QSqlQuery("SELECT rowid FROM status WHERE name = '"+group.getName() + "' ")
            query.next()
            id_ = query.value(0)

            for task in group:
                query = QSqlQuery()
                query.prepare("INSERT INTO tasks (name, status) VALUES (:name, :id)")
                query.bindValue(":name", task.getTask())
                query.bindValue(":id", id_)
                query.exec_()
    #
    #
    ################

    ##Saving maintable block
    #
        weeknum = self.mainLayout.table.getWeeknum()
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for weekday in weekdays:
            tasks = self.mainLayout.table.getTasks(weekday)
            if tasks:
                fields = ''
                values = ''
                for time in tasks:
                    query = QSqlQuery("SELECT rowid FROM tasks WHERE name ='" + tasks[time] + "'")
                    query.next()
                    tasks[time] = query.value(0)
                    fields += '"' + time + '"' + ','
                    values += str(tasks[time]) + ','
                fields = 'weekday,' + fields[:-1]
                values = '"'+weekday + '_' + str(weeknum) + '"' + ', ' + values[:-1]
                request = 'INSERT INTO main (' + fields + ') VALUES (' + values + ')'
                query = QSqlQuery()
                query.exec_(request)
        print('Saved')
    #
    #
    #
    ################

        # Restoring the original state
        dropConnection()

    @helpers.filemove('load')
    def load(self):
        """"Loads the file and restores the saved state"""

        # Restore the first day of usage
        globals.DAYFIRST = datetime.date.fromordinal(int(open(paths.savePath).read().splitlines()[0]))

        filename = os.path.basename(paths.savePath)[:-8]
        self.connectTrigger(filename)
        self.mainLayout.initTasks()
        self.mainLayout.table.clearItems()
        #### Loading main table
        #
        #
        weeknum = self.mainLayout.table.getWeeknum()
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for weekday in weekdays:
            day = weekday + '_' + str(weeknum)

            q = 'SELECT * FROM main WHERE weekday = "' + day + '"'
            query = QSqlQuery(q)
            query.next()
            record = query.record()
            indexes = []
            if not record.isEmpty():
                for i in range(0, 44):
                    if not record.isNull(i + 1):
                        indexes.append(i)
            values = {}
            for index in indexes:
                q = QSqlQuery("SELECT name FROM tasks WHERE rowid ='"+str(query.value(index + 1))+"'")
                q.next()
                values[index] = q.value(0)

            if values:
                self.mainLayout.table.setItemsColumn(values, weekdays.index(weekday))
        #
        #
        ################
        dropConnection()

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