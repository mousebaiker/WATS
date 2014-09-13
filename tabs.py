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

    def clearAll(self):
        self.weeksopened = []
        self.notsaved = []
        self.clear()

    def openTab(self, weeknum):
        """Opens tab of the specified number of week"""

        if weeknum not in self.weeksopened:
            table = MainTable(weeknum)
            table.changed.connect(self.addToNotSaved)
            index = self.addTab(table, 'Week ' + str(weeknum))
            self.setCurrentIndex(index)
            self.weeksopened.append(weeknum)
        else:
            self.setCurrentIndex(self.weeksopened.index(weeknum))


    def getNotSaved(self):
        return self.notsaved

    def getWidgetFromWeeknum(self, weeknum):
        """ Returns Maintable of a specified week if it is opened, else returns 0"""

        if weeknum not in self.weeksopened:
            return 0
        return self.widget(self.weeksopened.index(weeknum))

    def setValues(self, values, weekdayindex, weeknum):
        if self.count() == 0:
            self.weeksopened = []
        if weeknum not in self.weeksopened:
            self.openTab(weeknum)
        table = self.getWidgetFromWeeknum(weeknum)
        table.setItemsColumn(values, weekdayindex)

    @Slot(int)
    def closeTab(self, tabindex):
        weeknum = self.widget(tabindex).getWeeknum()
        if weeknum in self.notsaved:
            main_window = self.parent().parent().parent().parent()  # I know it's ugly
            main_window.save()
        self.weeksopened.remove(weeknum)
        self.removeTab(tabindex)

    @Slot()
    def addToNotSaved(self, weeknum):
        if weeknum not in self.notsaved:
            self.notsaved.append(weeknum)
