from dialogs import *
from paths import *

class Task(object):
    def __init__(self, task):
        self.task = task

    def __repr__(self):
        return self.task

    def __eq__(self, other):
        return self.task == other

    def __ne__(self, other):
        return self.task != other

    def getTask(self):
        return self.task


class TaskGroup(object):
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def __repr__(self):
        return self.name, self.tasks

    def __iter__(self):
        return self.tasks.__iter__()

    def addTask(self, task):
        self.tasks.append(task)

    def delTask(self, task):
        if task in self.tasks:
            self.tasks.remove(task)

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getTasks(self):
        return self.tasks


class TaskGroupWidget(QWidget):
    def __init__(self, name):
        super(TaskGroupWidget, self).__init__()
        self.name = name

        self.groupCont = QGroupBox()
        self.groupCont.setTitle(self.name)
        self.groupContLayout = QVBoxLayout()
        self.groupContLayout.addWidget(QLabel())
        self.groupCont.setLayout(self.groupContLayout)
        self.clear = True

        self.addTaskButton = QToolButton()
        self.addTaskIcon = QIcon(addTaskIconPath)
        self.addTaskButton.setIcon(self.addTaskIcon)
        self.addTaskButton.clicked.connect(self.addTaskPush)
        self.delTaskButton = QToolButton()
        self.delTaskIcon = QIcon(delTaskIconPath)
        self.delTaskButton.setIcon(self.delTaskIcon)
        self.delTaskButton.clicked.connect(self.delTaskPush)


        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.addTaskButton)
        self.buttonLayout.addWidget(self.delTaskButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.groupCont)
        self.mainLayout.addLayout(self.buttonLayout)

        self.setLayout(self.mainLayout)

    def addTask(self, name):
        if self.clear:
            self.clear = False
            self.groupContLayout.takeAt(0)
        element = QLabel(name)
        self.groupContLayout.addWidget(element)

    def addTaskPush(self):
        dialog = addTaskDialog()
        dialog.exec_()
        if dialog.result() == QDialog.Accepted:
            self.parentWidget().addTask(self.name, dialog.text.text())
            self.parentWidget().updateme()

    def delTaskPush(self):
        tasks = []
        for task in range(self.groupContLayout.count()):
            tasks.append(self.groupContLayout.itemAt(task).widget())
        dialog = delTaskDialog(tasks)
        dialog.exec_()
        if dialog.result() == QDialog.Accepted:
            self.parentWidget().delTask(self.name, dialog.params.currentText())
            self.parentWidget().updateme()
    def getText(self, position):
        for item in range(self.groupContLayout.count()):
            if self.groupContLayout.itemAt(item).geometry().contains(position - QPoint(0,20)):
                return self.groupContLayout.itemAt(item).widget().text()


class TasksWidget(QWidget):
    def __init__(self, groups):
        super(TasksWidget, self).__init__()

        ##main background
        self.mainFrame = QFrame()
        self.mainFrame.setFrameShape(QFrame.StyledPanel)

        self.mainLayout = QGridLayout()

        self.toolbarLayout = QHBoxLayout()

        self.addGroupIcon = QIcon(addGroupIconPath)
        self.addGroupButton = QToolButton()
        self.addGroupButton.setIcon(self.addGroupIcon)
        self.addGroupButton.setIconSize(QSize(16, 16))
        self.addGroupButton.clicked.connect(self.addGroupPush)


        self.delGroupIcon = QIcon(delGroupIconPath)
        self.delGroupButton = QToolButton()
        self.delGroupButton.setIcon(self.delGroupIcon)
        self.delGroupButton.setIconSize(QSize(16, 16))
        self.delGroupButton.clicked.connect(self.delGroupPush)
        #TODO Implement the group deleting system

        self.toolbarLayout.addStretch(1)
        self.toolbarLayout.addWidget(self.addGroupButton)
        self.toolbarLayout.addWidget(self.delGroupButton)

        self.widgetLayout = QVBoxLayout()
        self.widgetLayout.addLayout(self.mainLayout)
        self.widgetLayout.addStretch(1)
        self.widgetLayout.addLayout(self.toolbarLayout)
        ##list of labels - tasks
        self.groups = groups

        self.updateme()
        self.setLayout(self.widgetLayout)

    def updateme(self):
        child = self.mainLayout.takeAt(0)
        while child:
            child.widget().deleteLater()
            child = self.mainLayout.takeAt(0)
        # self.mainLayout.update()
        for group in self.groups:
            groupwidget = TaskGroupWidget(group.getName())
            for task in group:
                groupwidget.addTask(task.getTask())
            self.mainLayout.addWidget(groupwidget)

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
                position -= QPoint(item.widget().x(), item.widget().y())
                return item.widget().getText(position)
        return ''
    ##End Drag and drop

    ##Label pushing
    def pushLabel(self, item):
        item.widget().setFrameStyle(QFrame.Panel | QFrame.Sunken)

    def unpushLabel(self, item):
        item.widget().setFrameStyle(QFrame.Panel | QFrame.Raised)

    ##Tasks functions
    def addGroup(self, groupname):
        for group in self.groups:
            if groupname == group.getName():
                raise NameError
        self.groups.append(TaskGroup(groupname))
        self.updateme()
    def delGroup(self, groupname):
        for group in self.groups:
            if groupname == group.getName():
                self.groups.remove(group)
                return
        raise NameError

    def addTask(self, groupname, taskname):
        for group in self.groups:
            if groupname == group.getName():
                for task in group:
                    if task == taskname:
                        raise NameError
                group.addTask(Task(taskname))


    def delTask(self,groupname,taskname):
        for group in self.groups:
            if groupname == group.getName():
                for task in group:
                    if task == taskname:
                        group.delTask(task)
                        return
        raise NameError

    def addGroupPush(self):
        dialog = addGroupDialog()
        dialog.exec_()
        if dialog.result() == QDialog.Accepted:
            try:
                self.addGroup(dialog.text.text())
            except NameError:
                return
                #TODO Raise an error window stating that group with such name already exist and return to previous state

    def delGroupPush(self):
        dialog = delGroupDialog(self.groups)
        dialog.exec_()
        if dialog.result() == QDialog.Accepted:
            self.delGroup(dialog.params.currentText())
            self.updateme()

    def setGroups(self, groups):
        self.groups = groups

    def getGroups(self):
        return self.groups