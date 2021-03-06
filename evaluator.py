# -*- coding: utf-8 -*-
from PySide.QtGui import *

import language
import helpers


class Evaluator(object):
    """Implementation of logical and mathematical part of evaluator"""
    def __init__(self, table):
        self.table = table
        self.columnsnum = self.table.columnCount()
        self.rowsnum = self.table.rowCount()

    def total(self):
        """Returns the total number of fields in table"""

        return self.columnsnum * self.rowsnum

    def countEmpty(self):
        """Returns the number of empty cells in table"""
        return sum(self.countEmptyforColumns())

    def countEmptyPercent(self):
        return helpers.countPercent(self.countEmpty(), self.total())

    def countEmptyforColumns(self):
        """Returns the number of empty cells in table for each row
           result = [empty_row1, empty_row2, ...]
        """
        result = []
        for column in range(self.columnsnum):
            empty = 0
            for row in range(self.rowsnum):
                text = self.table.item(row, column).text()
                if not text:
                    empty += 1
            result.append(empty)
        return result

    def countEmptyPercentforColumns(self):
        return [helpers.countPercent(i, self.rowsnum) for i in self.countEmptyforColumns()]

    def countGroupTasks(self, group, columnindex):
        """Returns the number of tasks of given group in given column"""

        items = 0
        for row in range(self.rowsnum):
            text = self.table.item(row, columnindex).text()
            if text in group:
                items += 1
        return items

    def countGroupTasksPercent(self, group, columnindex):
        return self.countGroupTasks(group, columnindex) / self.rowsnum

    def countTask(self, task, rowindex):

        items = 0
        for column in range(self.columnsnum):
            text = self.table.item(rowindex, column).text()
            if text == task:
                items += 1
        return items

    def countTaskPercent(self, task, rowindex):
        return self.countTask(task, rowindex) / self.columnsnum

class EvaluatorWindow(QWidget):
    """Implementation of graphical part and output of evaluator"""
    def __init__(self, table):
        super(EvaluatorWindow, self).__init__()
        self.evaluationvalues = {}
        self.evaluator = Evaluator(table)
        self.mainLayout = QVBoxLayout()
        self.scrollLayout = QVBoxLayout()
        self.layoutWidget = QWidget()
        self.scroll = QScrollArea()
        self.setLayout(self.scrollLayout)
        self.setWindowTitle(language.languagedict['evalTitle'])
        self.resize(550, 300)

    def generate(self, groups, days):
        """
        Generates the dictionary of pairs (day: group_dict).
        Exception '__EMPTY__' field - contains the percent of empty blanks.
        group_dict - dictionary of pairs (group: percent)

         """

        self.days = days
        self.evaluationvalues['__EMPTY__'] = helpers.countPercent(self.evaluator.countEmpty(), self.evaluator.total())
        for index, day in enumerate(days):
            evaluationvalues = {}
            for group in groups:
                evaluationvalues[group.getName()] = helpers.countPercent(self.evaluator.countGroupTasks(group, index), self.evaluator.rowsnum)
            self.evaluationvalues[day] = evaluationvalues

    def draw(self):
        """Creates window and outputs the information"""

        emtprcLabel = QLabel()
        emtprcLabel.setText('<div align = "center" size = "4"><font size = "4">' +
                            language.languagedict['evalEmptyStart'] + str(self.evaluationvalues['__EMPTY__']) +
                            language.languagedict['evalEmptyEnd'] + '</font></div>')
        emtprcLabel.setFrameStyle(QFrame.StyledPanel)
        emtprcLabel.setMaximumHeight(25)
        self.mainLayout.addWidget(emtprcLabel)
        for day in self.days:
            daylabel = QLabel()
            daylabel.setText('<font size = 4>' + day + ':' + '</font>')
            self.mainLayout.addWidget(daylabel)
            for group in self.evaluationvalues[day]:
                if group != '__EMPTY__':
                    label = QLabel(language.languagedict['evalGroupsStart'] + group
                                   + language.languagedict['evalGroupsMiddle'] + str(
                        self.evaluationvalues[day][group])
                                   + language.languagedict['evalGroupsEnd'])
                    self.mainLayout.addWidget(label)
            self.mainLayout.addWidget(QLabel())
        self.layoutWidget.setLayout(self.mainLayout)
        self.scroll.setWidget(self.layoutWidget)
        self.scrollLayout.addWidget(self.scroll)
        self.show()