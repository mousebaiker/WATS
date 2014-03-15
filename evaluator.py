#encoding:utf-8
from PySide.QtGui import *


class Evaluator(object):
    def __init__(self, table):
        self.table = table
        self.columnsnum = self.table.columnCount()
        self.rowsnum = self.table.rowCount()

    def total(self):
        return self.columnsnum * self.rowsnum

    def countEmpty(self):
        empty = 0
        for row in range(self.rowsnum):
            for column in range(self.columnsnum):
                text = self.table.item(row, column).text()
                if not text:
                    empty += 1
        return empty

    def countEmptyPercent(self):
        empty = self.countEmpty()
        total = self.total()
        return int((empty/total) * 100)


class EvaluatorWindow(QWidget):
    def __init__(self, table):
        super(EvaluatorWindow, self).__init__()
        self.evaluator = Evaluator(table)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.setWindowTitle(u'Пожалуйста')
        self.resize(200, 450)

    def generate(self):
        self.emptyPercent = self.evaluator.countEmptyPercent()

    def draw(self):
        emtprcLabel = QLabel(u'Вы не заполнили ' + str(self.emptyPercent) + u'% вашего распорядка.')
        self.mainLayout.addWidget(emtprcLabel)
        self.show()