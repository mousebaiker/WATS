# -*- coding: utf-8 -*-
import sys

from PySide.QtCore import *

from database import *
from maintable import *
from tasks_widget import *
from evaluator import *
from dialogs import *
import language


class Layout(QWidget):
    def __init__(self):
        super(Layout, self).__init__()
        self.taskwidget = TasksWidget([])
        self.scrollarea = QScrollArea()
        self.frame1 = QLabel(self)
        self.table = MainTable(1)
        ##Layouts        self.hb = QHBoxLayout()
        self.vb = QVBoxLayout()
        ## Splitters
        self.vsplitter = QSplitter()
        self.bottomsplitter = QSplitter(Qt.Vertical)

        self.dragging = False
        self.dragtext = ''

    def initTasks(self):
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
        self.scrollarea.setWidget(self.taskwidget)
        self.scrollarea.setWidgetResizable(True)

        self.vsplitter.addWidget(self.scrollarea)
        self.vsplitter.addWidget(self.table)

        self.bottomsplitter.addWidget(self.vsplitter)
        self.bottomsplitter.addWidget(self.frame1)

        self.vb.addWidget(self.bottomsplitter)
        self.setLayout(self.vb)

    def mousePressEvent(self, event):
        if event.buttons() != Qt.RightButton:
            return
        rightclick = event.pos()
        scroll = self.scrollarea.verticalScrollBar().value()
        self.rightclickpos = rightclick + QPoint(0, scroll)
        if self.taskwidget.isItemAtPoint(self.rightclickpos):
            self.dragging = True
            self.dragtext = self.taskwidget.getText(self.rightclickpos)



    def mouseReleaseEvent(self, event):
        if event.button() != Qt.RightButton:
            return
        if self.dragging:
            position = event.pos() - QPoint(self.taskwidget.geometry().width() + 55, 30)
            self.frame1.setText(str(position))
            if self.table.itemAt(position) is not None:
                self.table.itemAt(position).setText(self.dragtext)
        self.dragging = False




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connected = False
        self.mainLayout = Layout()

    ##Main output function
    def draw(self):
        ## Models should be created after database connection
        self.mainLayout.create()
        self.setCentralWidget(self.mainLayout)
        self.showMaximized()
        self.setWindowTitle('WATS?')
        self.show()

  ##Functions handling menu buttons signals
  #
  # #"Connect" button
    def connectTrigger(self):
        self.connected = setConnection()
        if self.connected:
            label = 'Yeahaaaaa'
        else:
            label = 'Oh, NO'
        self.statusBar().showMessage(label)

    def initializeMenu(self):
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
        if not self.connected:
            self.connectTrigger()
    ## Saving tasks widget block
    #
    #
        # if savePath == '':
        #     # TODO File dialog for files
        # else:
        #     self.connectTrigger()

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
    #
            weeknum = self.mainLayout.table.getWeeknum()
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for weekday in weekdays:
                tasks = self.mainLayout.table.getTasks(weekday)
                if tasks:
                    values = []
                    for time in tasks:
                        # # Getting id for the task
                        query = QSqlQuery("SELECT rowid FROM tasks WHERE name ='" + tasks[time] + "'")
                        query.next()
                        taskid = query.value(0)

                        # # Getting id for the time
                        query = QSqlQuery("SELECT rowid FROM time WHERE hour ='" + time + "'")
                        query.next()
                        timeid = query.value(0)

                        values.append((weekday + '_' + str(weeknum), str(taskid), str(timeid)))

                    for value in values:
                        request = 'INSERT INTO main (weekday, task, time) VALUES ("' \
                                  + value[0] + '", ' + value[1] + ', ' + value[2] + ')'
                        query = QSqlQuery()
                        query.exec_(request)
                        print(request)
                        print(query.lastError())

                    print('Saved')

    #
    #
    ################

    def load(self):
        if not self.connected:
            self.connectTrigger()
        self.mainLayout.initTasks()
        self.mainLayout.table.clearItems()
        #### Loading main table
        #
        #
        weeknum = self.mainLayout.table.getWeeknum()
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for weekday in weekdays:
            values = []

            day = weekday + '_' + str(weeknum)

            q = 'SELECT weekday, task, time FROM main WHERE weekday = "' + day + '"'
            query = QSqlQuery(q)
            while query.next():
                values.append([query.value(i) for i in range(3)])

            items = {}
            for _, taskid, timeid in values:
                q = QSqlQuery("SELECT name FROM tasks WHERE rowid ='" + str(taskid) + "'")
                q.next()
                items[timeid] = q.value(0)

            if items:
                self.mainLayout.table.setItemsColumn(items, weekdays.index(weekday))
        #
        #
        ################

    def evaluate(self):
        self.evWindow = EvaluatorWindow(self.mainLayout.table)

        days = language.languagedict['lang_mainTableHeaders']
        self.evWindow.generate(self.mainLayout.taskwidget.groups, days)

        self.evWindow.draw()

    def loadlanguage(self):
        language.chooseLanguageFile(self)
        language.loadLanguage()
        self.updatelanguage()

    def updatelanguage(self):
        self.mainLayout.table.setHorizontalHeaderLabels(language.languagedict['lang_mainTableHeaders'])
        self.loadlanguageAct.setText(language.languagedict['lang_languageMenuItem'])
        self.saveAct.setText(language.languagedict['lang_saveMenuItem'])
        self.loadAct.setText(language.languagedict['lang_loadMenuItem'])
        self.evaluateAct.setText(language.languagedict['lang_evaluateMenuItem'])
        self.filemenu.setTitle(language.languagedict['lang_fileMenu'])
        self.addblockAct.setText(language.languagedict['lang_addblockMenuItem'])
        self.editmenu.setTitle(language.languagedict['lang_editMenu'])

    def addblock(self):
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
