from PySide.QtGui import *
from  language import languagedict

class MainTable(QTableWidget):
    def __init__(self, weeknum):
        super(MainTable, self).__init__()
        self.weeknum = weeknum
        self.setRowCount(48)
        self.setColumnCount(7)
        self.rowsheaders = []
        self.columnheaders = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.columnheaderslan = languagedict['lang_mainTableHeaders']
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

    def getWeeknum(self):
        return self.weeknum

    def getTasks(self, weekday):
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
        for row in items:
            self.item(row, column).setText(items[row])

    def clearItems(self):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                self.item(row,column).setText('')