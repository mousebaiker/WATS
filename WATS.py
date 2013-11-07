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
        if not dab.open():
            return False
        query = QSqlQuery()
        query.exec_('create table test(lol varchar(20))')
        return True
def addRecord(record):
        query = QSqlQuery()
        request = 'INSERT INTO test VALUES("' + record + '")'
        return query.exec_(request)
def delRecord(row):
    query = QSqlQuery()
    request = 'DELETE FROM test WHERE rowid =' + row
    return query.exec_(request)


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()

        # actions fro working with database
        self.dbConAct = QAction('Connect', self)
        self.dbAdd = QAction('Add a record', self)
        self.dbDel = QAction('Delete a record', self)
    ##Main output function
    def draw(self):
        ## Assigned here because models should be created after database connection
        self.sqlmodel = QSqlTableModel()
        self.initializeModel(self.sqlmodel, 'test')
        self.sqlview = self.createView(self.sqlmodel)


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

    # "Add record" button
    def addRecord(self):
        self. aRDText, self.aRDSuccess = QInputDialog.getText(self,'Add a record', 'Enter the name:')
        if self.aRDSuccess:
            self.statusBar().showMessage(str(addRecord(self.aRDText)))

    # 'Delete record' button
    def delRecord(self):
        self. dRDText, self.dRDSuccess = QInputDialog.getText(self,'Delete a record', 'Enter the row:')
        if self.dRDSuccess:
            self.statusBar().showMessage(str(delRecord(self.dRDText)))

    def initializeMenu(self):
        self.dbConAct.triggered.connect(self.connectTrigger)
        self.dbAdd.triggered.connect(self.addRecord)
        self.dbDel.triggered.connect(self.delRecord)
        self.statusBar()
        self.menu = self.menuBar()
        self.filemenu = self.menu.addMenu('&File')
        self.filemenu.addAction(self.dbConAct)
        self.filemenu.addAction(self.dbAdd)
        self.filemenu.addAction(self.dbDel)
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
