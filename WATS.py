from PySide.QtCore import *
from PySide.QtGui import *
import sys
from database import *
from maintable import *
from tasks_widget import *

#class sqlModel(QSqlTableModel):
#    def __init__(self):
#        super(sqlModel, self).__init__()
#
#    def initializeModel(self, name):
#        self.setTable(name)
#        self.setEditStrategy(QSqlTableModel.OnRowChange)
#        self.select()
#        self.setHeaderData(0, Qt.Horizontal, "id")
#        self.setHeaderData(1, Qt.Horizontal, "lol")
#
#
#class sqlView(QTableView):
#    def __init__(self):
#        super(sqlView,self).__init__()
#
#    def createView(self, model):
#        self.setModel(model)


class Layout(QWidget):
    def __init__(self):
        super(Layout, self).__init__()
        self.taskwidget = TasksWidget()
        self.scrollarea = QScrollArea()
        self.frame1 = QLabel(self)
        self.table = MainTable(15021997)
        ##Layouts
        self.hb = QHBoxLayout()
        self.vb = QVBoxLayout()
        ## Splitters
        self.vsplitter = QSplitter()
        self.bottomsplitter = QSplitter(Qt.Vertical)
    def create(self):

        self.scrollarea.setWidget(self.taskwidget)
        self.scrollarea.setWidgetResizable(True)

        self.vsplitter.addWidget(self.scrollarea)
        self.vsplitter.addWidget(self.table)

        self.bottomsplitter.addWidget(self.vsplitter)
        self.bottomsplitter.addWidget(self.frame1)

        self.vb.addWidget(self.bottomsplitter)
        self.setLayout(self.vb)

    def update(self):
        self.sqlmodel = sqlModel()
        self.sqlmodel.initializeModel('test')
        self.sqlview.createView(self.sqlmodel)

    def addRecord(self):
        addRecord(str(random.random()))
        self.update()

    def delRecord(self, row):
        result = self.sqlmodel.removeRow(int(row - 1))
        self.update()
        return result

    def mousePressEvent(self, event):
        if event.buttons() != Qt.RightButton:
            return
        self.rightclickpos = event.pos()
        if self.taskwidget.isItemAtPoint(self.rightclickpos):
            self.dragging = True
            self.dragtext = self.taskwidget.getText(self.rightclickpos)
            self.taskwidget.pushLabel(self.taskwidget.itemAtPoint(self.rightclickpos))


    def mouseReleaseEvent(self, event):
        if event.button() != Qt.RightButton:
            self.frame1.setText(self.dragtext)
            return
        self.taskwidget.unpushLabel(self.taskwidget.itemAtPoint(self.rightclickpos))
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
        self.dbAdd = QAction('Add a record', self)
        self.dbDel = QAction('Delete a record', self)

        self.mainLayout = Layout()
    ##Main output function
    def draw(self):
        ## Models should be created after database connection
        self.mainLayout.create()
        #self.setCentralWidget(self.sqlview)
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
            self.mainLayout.update()
        else:
            label = 'Oh Shit'
        self.statusBar().showMessage(label)

    # "Add record" button
    def addRecord(self):
        if self.connected:
            self. aRDText, self.aRDSuccess = QInputDialog.getText(self,'Add a record', 'Enter the name:')
            if self.aRDSuccess:
                self.statusBar().showMessage(str(addRecord(self.aRDText)))
        self.mainLayout.update()

    # 'Delete record' button
    def delRecord(self):
        if self.connected:
            self. dRDText, self.dRDSuccess = QInputDialog.getText(self, 'Delete a record', 'Enter the row:')
            if self.dRDSuccess:
                self.statusBar().showMessage(str(self.mainLayout.delRecord(int(self.dRDText))))
        self.mainLayout.update()

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



def main():
    app = QApplication(sys.argv)

    mainGui = MainWindow()
    mainGui.initializeMenu()
    mainGui.draw()
    sys.exit(app.exec_()) 

if __name__ == '__main__':
    main()
