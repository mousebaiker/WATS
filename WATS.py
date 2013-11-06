from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSql import * 
import sys

class database(object):
    dab = QSqlDatabase()
    def __init__(self, name):
        self.name = name
        self.dab = QSqlDatabase.addDatabase("QSQLITE")    
        self.dab.setDatabaseName(name)
        self.query = QSqlQuery()
    def setConnection(self, username = 0, password = 0):
        if username != 0:
            self.dab.setUsername(username)
        if password != 0 :
            self.dab.setPassword(password)
        return self.dab.open()
    def addRecord(self, record):
        if self.dab.isOpen():
            return self.query.exec_('insert into test values(2,"zaaazazaz")')



class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.db = database('test')
        # actions fro working with database
        self.dbConAct = QAction('Connect', self)
        self.dbAdd = QAction('Add a record', self)

        self.sqlmodel = QSqlTableModel()
        self.initializeModel(self.sqlmodel, 'test')
        self.sqlview = self.createView(self.sqlmodel)

    ##Main output function
    def draw(self):

        self.setCentralWidget(self.sqlview)
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle('WATS?')
        self.show()

  ##Functions handling menu buttons signals
  #
  # #"Connect" button
    def connectTrigger(self):
        self.connected = self.db.setConnection()
        if self.connected:
            label = 'Yeahaaaaa'
        else:
            label = 'Oh Shit'
        self.statusBar().showMessage(label)
        query = QSqlQuery()
        query.exec_('create table test(id int primary key auto increment, lol varchar(20))')
        query.exec_('insert into test values(1, "zaaazazaz")')

    # "Add record" button
    def addRecord(self):
        self. aRDText, self.aRDSuccess = QInputDialog.getText(self,'Add a record', 'Enter the name:')

        if self.aRDSuccess:
            self.db.addRecord(self.aRDText)
            self.statusBar().showMessage(str(QSqlQuery.lastError(self.db.query)))

    def initializeMenu(self):
        self.dbConAct.triggered.connect(self.connectTrigger)
        self.dbAdd.triggered.connect(self.addRecord)

        self.statusBar()
        self.menu = self.menuBar()
        self.filemenu = self.menu.addMenu('&File')
        self.filemenu.addAction(self.dbConAct)
        self.filemenu.addAction(self.dbAdd)
  #
  #
  ## <End> Functions handling  menu buttons signals

    def initializeModel(self, model, name):
        model.setTable(name)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.select()

        model.setHeaderData(0, Qt.Horizontal, "id")
        model.setHeaderData(1, Qt.Horizontal, "lol")

    def createView(self, model):
        view = QTableView()
        view.setModel(model)
        return view


def main():
    app = QApplication(sys.argv)

    mainGui = GUI()

    mainGui.connectTrigger()
    mainGui.initializeMenu()
    mainGui.draw()
    sys.exit(app.exec_()) 

if __name__ == '__main__':
    main()
