from PySide.QtGui import *


class MainTable(QTableWidget):
    def __init__(self, date):
        super(MainTable, self).__init__()
        self.date = date
        self.setRowCount(48)
        self.setColumnCount(7)
        rowsheaders = []
        columnheaders = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i in range(0, 1440, 30):
            hours = i//60
            minutes = i - hours*60
            hours = '0' + str(hours)
            minutes = '0' + str(minutes)
            hours = hours[-2:]
            minutes = minutes[-2:]
            rowsheaders.append(str(hours) + ':' + str(minutes))
        self.setVerticalHeaderLabels(rowsheaders)
        self.setHorizontalHeaderLabels(columnheaders)
        for i in range(len(rowsheaders)):
            for c in range(len(columnheaders)):
                newItem = QTableWidgetItem()
                self.setItem(i,c,newItem)

        self.acceptDrops()