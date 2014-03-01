from PySide.QtGui import *
from PySide.QtCore import QSize
## Pop-up window to add a dialog
class addTaskDialog(QDialog):
    def __init__(self, groups):
        super(addTaskDialog, self).__init__()
        priorval = [0,1,2,3]

        self.label = QLabel('Add Task')
        self.text = QLineEdit()
        self.groups = QComboBox()
        for i in groups:
            self.groups.addItem(i.getName())
        self.priorities = QComboBox()
        for i in priorval:
            self.priorities.addItem(i)
        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton('Cancel')
        self.cancel.clicked.connect(self.reject)

        self.buttons = QHBoxLayout()
        self.buttons.addStretch(1)
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.text)
        self.mainLayout.addWidget(self.groups)
        self.mainLayout.addWidget(self.priorities)
        self.mainLayout.addLayout(self.buttons)

        self.setLayout(self.mainLayout)

    def check(self):
        if self.text.text() != '':
            self.accept()



class addGroupDialog(QDialog):
    def __init__(self):
        super(addGroupDialog, self).__init__()
        priorval = [0,1,2,3]

        self.label = QLabel('Add Group')
        self.text = QLineEdit()
        self.priorities = QComboBox()
        for i in priorval:
            self.priorities.addItem(str(i))
        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.check)
        self.cancel = QPushButton('Cancel')
        self.cancel.clicked.connect(self.reject)

        self.buttons = QHBoxLayout()
        self.buttons.addStretch(1)
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.text)
        self.mainLayout.addWidget(self.priorities)
        self.mainLayout.addLayout(self.buttons)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('Add Group')
        self.setFixedSize(QSize(300, 150))

    def check(self):
        if self.text.text() != '':
            self.accept()
