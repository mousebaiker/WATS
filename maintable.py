from PySide.QtGui import *

import language
from PySide.QtCore import Signal


class MainTable(QTableWidget):
    changed = Signal(int)

    def __init__(self, weeknum):
        super(MainTable, self).__init__()
        self.weeknum = weeknum
        self.setRowCount(48)
        self.setColumnCount(7)
        self.rowsheaders = []
        self.columnheaders = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.columnheaderslan = language.languagedict['lang_mainTableHeaders']
        for i in range(0, 1440, 30):
            hours = i//60
            minutes = i - hours*60
            hours = '0' + str(hours)
            minutes = '0' + str(minutes)
            hours = hours[-2:]
            minutes = minutes[-2:]
            self.rowsheaders.append(str(hours) + ':' + str(minutes))
        self.setVerticalHeaderLabels(self.rowsheaders)
        self.setHorizontalHeaderLabels(self.columnheaderslan)
        for i in range(len(self.rowsheaders)):
            for c in range(len(self.columnheaders)):
                newItem = QTableWidgetItem()
                self.setItem(i, c, newItem)

        self.setCurrentCell(12, 0)
        self.acceptDrops()

        #Signal binding
        self.cellChanged.connect(self.onChange)

    def getWeeknum(self):
        """Return the number of the week that table is currently represents"""

        return self.weeknum

    def getTasks(self, weekday):
        """ Returns the dictionary of (time:task) pairs for a given day of the week"""

        if weekday not in self.columnheaders:
            return
        result = {}
        column = self.columnheaders.index(weekday)
        row = 0
        for time in self.rowsheaders:
            item = self.item(row, column).text()
            if item != '':
                result[time] = item
            row += 1
        return result

    def setItemsColumn(self, items, column):
        """Sets items for a whole column. Column is presented as index"""

        for row in items:
            self.item(row, column).setText(items[row])

    def setItemRowCol(self, item, rowname, columnname):
        """Sets item for a particular row and column names.
        Rowname and columnname should be examples of strings(headers of the table)"""

        row = self.rowsheaders.index(rowname)
        column = self.columnheaderslan.index(columnname)

        self.item(row, column).setText(item)

    def setItemTime(self, item, start, end, columnname):
        """Sets items for a given amount of time. Start and end are examples of strings(headers of table)"""

        fromto = self.rowsheaders[self.rowsheaders.index(start): self.rowsheaders.index(end) + 1]
        column = self.columnheaderslan.index(columnname)

        for rowname in fromto:
            row = self.rowsheaders.index(rowname)
            self.item(row, column).setText(item)

    def clearItems(self):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                self.item(row,column).setText('')

    def onChange(self):
        self.changed.emit(self.weeknum)