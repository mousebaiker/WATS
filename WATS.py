from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSql import * 
import sys

def setConnection(username = 0, password = 0):
        dab = QSqlDatabase.addDatabase("QSQLITE")
        dab.setDatabaseName('test')
        if username != 0:
            dab.setUsername(username)
        if password != 0 :
            dab.setPassword(password)
        return dab.open()
def addRecord(record):
        query = QSqlQuery()
        return query.exec_('INSERT INTO test VALUES(2,"zaaazazaz")')




class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()

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
        self.connected = setConnection()
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

            self.statusBar().showMessage(str(addRecord(self.aRDText)))

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
