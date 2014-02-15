from PySide.QtGui import *
from PySide.QtCore import QSize
from dialogs import *

class Task(object):
    def __init__(self, task, priority):
        self.task = task
        self.priority = priority

    def __repr__(self):
        return self.task, self.priority

    def __eq__(self, other):
        return self.task == other

    def __ne__(self, other):
        return self.task != other

    def getTask(self):
        return self.task

    def getPriority(self):
        return self.priority

class TaskGroup(object):
    def __init__(self, name, priority):
        self.name = name
        self.tasks = []
        self.priority = priority

    def __repr__(self):
        return self.name , self.tasks, self.priority

    def __iter__(self):
        return self.tasks.__iter__()

    def addTask(self, task):
        self.tasks.append(task)

    def delTask(self, task):
        if task in self.tasks:
            self.tasks.pop(task)

    def getName(self):
        return self.name

    def getTasks(self):
        return self.tasks

    def getPriority(self):
        return self.priority


class TasksWidget(QWidget):
    def __init__(self):
        super(TasksWidget, self).__init__()

        ##main background
        self.mainFrame = QFrame()
        self.mainFrame.setFrameShape(QFrame.StyledPanel)

        self.mainLayout = QGridLayout()

        self.toolbarLayout = QHBoxLayout()

        self.addGroupIcon = QIcon('icons/add.png')
        self.addGroupButton = QToolButton()
        self.addGroupButton.setIcon(self.addGroupIcon)
        self.addGroupButton.setIconSize(QSize(16, 16))
        self.addGroupButton.clicked.connect(self.addGroupPush)


        self.delGroupIcon = QIcon('icons/del.png')
        self.delGroupIcon.Mode(QIcon.Normal)
        self.delGroupButton = QToolButton()
        self.delGroupButton.setIcon(self.delGroupIcon)
        self.delGroupButton.setIconSize(QSize(16, 16))

        self.toolbarLayout.addStretch(1)
        self.toolbarLayout.addWidget(self.addGroupButton)
        self.toolbarLayout.addWidget(self.delGroupButton)

        self.widgetLayout = QVBoxLayout()
        self.widgetLayout.addLayout(self.mainLayout)
        self.widgetLayout.addStretch(1)
        self.widgetLayout.addLayout(self.toolbarLayout)
        ##list of labels - tasks
        self.groups = []

        self.show()
    def show(self):
        count = 0
        for task in self.groups:
            label = QLabel(task)
            label.setFrameStyle(QFrame.Panel | QFrame.Raised)
            label.setMidLineWidth(3)
            label.setMaximumHeight(35)
            self.mainLayout.addWidget(label, count % 25, count//25)
            count += 1

        self.setLayout(self.widgetLayout)

    ##Drag and drop

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
    ##End Drag and drop

    ##Label pushing
    def pushLabel(self, item):
        item.widget().setFrameStyle(QFrame.Panel | QFrame.Sunken)

    def unpushLabel(self, item):
        item.widget().setFrameStyle(QFrame.Panel | QFrame.Raised)

    ##Tasks functions
    def addGroup(self, groupname, priority = 0):
        for group in self.groups:
            if groupname == group.getName:
                raise NameError
        self.groups.append(TaskGroup(groupname,priority))

    def delGroup(self, groupname):
        for group in self.groups:
            if groupname == group.getName():
                self.tasks.pop(group)
                return
        raise NameError

    def addTask(self, groupname, taskname, priority = 0):
        for group in self.groups:
            if groupname == group.getName():
                for task in group:
                    if task == taskname:
                        raise NameError
                group.addTask(Task(taskname, priority))


    def delTask(self,groupname,taskname):
        for group in self.groups:
            if groupname == group.getName():
                for task in group:
                    if task == taskname:
                        group.delTask(task)
                        return
        raise NameError

    def addTaskPush(self):
        dialog = addTaskDialog(self.groups)
        dialog.exec_()

    def addGroupPush(self):
        dialog = addGroupDialog()
        dialog.exec_()


