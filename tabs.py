from PySide.QtGui import QTabWidget
from PySide.QtCore import Slot
from maintable import MainTable


class Tabs(QTabWidget):
    def __init__(self):
        super(Tabs, self).__init__()

        self.weeksopened = []
        self.notsaved = []

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)

    def openTab(self, weeknum):
        """Opens tab of the specified number of week"""
        print('Before', self.weeksopened)
        if weeknum not in self.weeksopened:
            table = MainTable(weeknum)
            table.changed.connect(self.addToNotSaved)
            index = self.addTab(table, 'Week ' + str(weeknum))
            self.setCurrentIndex(index)
            self.weeksopened.append(weeknum)
        else:
            self.setCurrentIndex(self.weeksopened.index(weeknum))
        print('After', self.weeksopened)

    def getNotSaved(self):
        return self.notsaved

    def getWidgetFromWeeknum(self, weeknum):
        """ Returns Maintable of a specified week if it is opened, else returns 0"""
        print('Get widget stuff:', self.weeksopened)
        if weeknum not in self.weeksopened:
            return 0
        return self.widget(self.weeksopened.index(weeknum))

    def setValues(self, values, weekdayindex, weeknum):
        if weeknum not in self.weeksopened:
            self.openTab(weeknum)
        table = self.getWidgetFromWeeknum(weeknum)
        table.setItemsColumn(values, weekdayindex)

    @Slot(int)
    def closeTab(self, tabindex):
        weeknum = self.widget(tabindex).getWeeknum()
        if weeknum in self.notsaved:
            return
        self.weeksopened.remove(weeknum)
        self.removeTab(tabindex)

    @Slot()
    def addToNotSaved(self, weeknum):
        if weeknum not in self.notsaved:
            self.notsaved.append(weeknum)
