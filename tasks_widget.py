from PySide.QtGui import *


class TasksWidget(QWidget):
    def __init__(self):
        super(TasksWidget, self).__init__()

        ##main background
        self.mainFrame = QFrame()
        self.mainFrame.setFrameShape(QFrame.StyledPanel)

        self.mainLayout = QGridLayout()

        ##list of labels - tasks
        self.tasks = ['Hue','lol']
        for i in range(70):
            self.tasks.append(str(i))
        self.show()
    def show(self):
        count = 0
        for task in self.tasks:
            label = QLabel(task)
            label.setFrameStyle(QFrame.Panel | QFrame.Raised)
            label.setMidLineWidth(3)
            label.setMaximumHeight(35)
            self.mainLayout.addWidget(label, count % 25, count//25 )
            count += 1
        self.setLayout(self.mainLayout)

    def itemAtPoint(self, position):
        for item in range(self.mainLayout.count()):
            if self.mainLayout.itemAt(item).geometry().contains(position):
                return self.mainLayout.itemAt(item)
        return 0

    def isItemAtPoint(self, position):
        for item in range(self.mainLayout.count()):
            if self.mainLayout.itemAt(item).geometry().contains(position):
                return True
        return False

    def getText(self, position):
        if self.isItemAtPoint(position):
            item = self.itemAtPoint(position)
            if item.widget() != 0:
                return item.widget().text()
        return ''
