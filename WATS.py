from PySide.QtCore import *
import sys
from database import *
from maintable import *
from tasks_widget import *


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
        self.rightclickpos = event.pos()
        if self.taskwidget.isItemAtPoint(self.rightclickpos):
            self.dragging = True
            self.dragtext = self.taskwidget.getText(self.rightclickpos)



    def mouseReleaseEvent(self, event):
        if event.button() != Qt.RightButton:
            return
        if self.dragging:
            position = event.pos() - QPoint(self.taskwidget.geometry().width() + 30, 25)
            self.frame1.setText(str(position))
            if self.table.itemAt(position) is not None:
                self.table.itemAt(position).setText(self.dragtext)
        self.dragging = False




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connected = False
        # actions fro working with database
        self.dbConAct = QAction('Connect', self)
        self.saveAct = QAction('Save',self)
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
            self.mainLayout.initTasks()
        else:
            label = 'Oh, NO'
        self.statusBar().showMessage(label)

    def initializeMenu(self):
        self.dbConAct.triggered.connect(self.connectTrigger)
        self.saveAct.triggered.connect(self.save)
        self.statusBar()
        self.menu = self.menuBar()
        self.filemenu = self.menu.addMenu('&File')
        self.filemenu.addAction(self.dbConAct)
        self.filemenu.addAction(self.saveAct)

  #
  #
  ## <End> Functions handling  menu buttons signals

    def save(self):
    ## Saving tasks widget block
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
            print(str(id_))

            for task in group:
                query = QSqlQuery()
                query.prepare("INSERT INTO tasks (name, status) VALUES (:name, :id)")
                query.bindValue(":name", task.getTask())
                query.bindValue(":id", id_)
                query.exec_()
    ################

    ##Saving maintable block
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
                        fields += '"'+time +'"'+ ','
                        values += str(tasks[time]) + ','
                    fields = 'weekday,' + fields[:-1]
                    values = '"'+weekday + '_' + str(weeknum)+ '"' + ', ' + values[:-1]
                    request = 'INSERT INTO main (' + fields + ') VALUES (' + values + ')'
                    print request
                    query = QSqlQuery()
                    query.exec_(request)
                    print(query.lastError())


    ################


def main():
    app = QApplication(sys.argv)

    mainGui = MainWindow()
    mainGui.initializeMenu()
    mainGui.draw()
    sys.exit(app.exec_()) 

if __name__ == '__main__':
    main()
