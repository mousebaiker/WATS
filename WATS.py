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
        self.table = MainTable(15021997)
        ##Layouts        self.hb = QHBoxLayout()
        self.vb = QVBoxLayout()
        ## Splitters
        self.vsplitter = QSplitter()
        self.bottomsplitter = QSplitter(Qt.Vertical)

        self.dragging = False
        self.dragtext = ''

    def initTasks(self):
        statuses = getStatuses()
        self.taskwidget.setGroups(statuses)
        self.taskwidget.update()


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
        self.dbAdd = QAction('Add a record', self)
        self.dbDel = QAction('Delete a record', self)

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
            label = 'Oh Shit'
        self.statusBar().showMessage(label)

    def initializeMenu(self):
        self.dbConAct.triggered.connect(self.connectTrigger)
        self.statusBar()
        self.menu = self.menuBar()
        self.filemenu = self.menu.addMenu('&File')
        self.filemenu.addAction(self.dbConAct)

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
