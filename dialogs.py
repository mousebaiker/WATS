from PySide.QtGui import *

## Pop-up window to add a dialog
class addTaskDialog(QDialog):
    def __init__(self, groups):
        super(addTaskDialog, self).__init__()

        self.label = QLabel('Add Task')
        self.text = QLineEdit()
        self.groups = QComboBox()
        for i in groups:
            self.groups.addItem(i.getName())
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
        self.mainLayout.addLayout(self.buttons)

        self.setLayout(self.mainLayout)

    def check(self):
        if self.text.text() != '':
            self.accept()



class addGroupDialog(QDialog):
    def __init__(self):
        super(addGroupDialog, self).__init__()
        self.label = QLabel('Add Group')
        self.text = QLineEdit()

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
        self.mainLayout.addLayout(self.buttons)

        self.setLayout(self.mainLayout)

    def check(self):
        if self.text.text() != '':
            self.accept()
