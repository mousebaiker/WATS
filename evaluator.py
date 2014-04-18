# -*- coding: utf-8 -*-
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

    def countPercent(self, given, total):
        return int((float(given)/total) * 100)

    def countGroupTasks(self, group, columnindex):
        items = 0
        for row in range(self.rowsnum):
            text = self.table.item(row, columnindex).text()
            if text in group:
                items += 1
        return items

class EvaluatorWindow(QWidget):
    def __init__(self, table):
        super(EvaluatorWindow, self).__init__()
        self.evaluationvalues = {}
        self.evaluator = Evaluator(table)
        self.mainLayout = QVBoxLayout()
        self.scrollLayout = QVBoxLayout()
        self.layoutWidget = QWidget()
        self.scroll = QScrollArea()
        self.setLayout(self.scrollLayout)
        self.setWindowTitle(u'Оценка')
        self.resize(550, 300)

    def generate(self, groups, days):
        self.days = days
        self.evaluationvalues['__EMPTY__'] = self.evaluator.countPercent(self.evaluator.countEmpty(), self.evaluator.total())
        for day, index in days:
            evaluationvalues = {}
            for group in groups:
                evaluationvalues[group.getName()] = self.evaluator.countPercent(self.evaluator.countGroupTasks(group, index), self.evaluator.rowsnum)
            self.evaluationvalues[day] = evaluationvalues

    def draw(self):
        emtprcLabel = QLabel()
        emtprcLabel.setText('<div align = "center" size = "4"><font size = "4">'u'Вы не заполнили ' + str(self.evaluationvalues['__EMPTY__']) + u'% вашего распорядка.' + '</font></div>')
        emtprcLabel.setFrameStyle(QFrame.StyledPanel)
        emtprcLabel.setMaximumHeight(25)
        self.mainLayout.addWidget(emtprcLabel)
        for day in (i[0] for i in self.days):
            daylabel = QLabel()
            daylabel.setText('<font size = 4>' + day + ':' +'</font>')
            self.mainLayout.addWidget(daylabel)
            for group in self.evaluationvalues[day]:
                if group != '__EMPTY__':
                    label = QLabel(u'Задания группы "' + group + u'" занимает ' + str(self.evaluationvalues[day][group]) + u'% от вашего общего распорядка')
                    self.mainLayout.addWidget(label)
            self.mainLayout.addWidget(QLabel())
        self.layoutWidget.setLayout(self.mainLayout)
        self.scroll.setWidget(self.layoutWidget)
        self.scrollLayout.addWidget(self.scroll)
        self.show()
