from PySide.QtGui import QTabWidget
from PySide.QtCore import Slot

import global_vars
import language

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
            index = self.addTab(table, language.languagedict['WeekHeader'] + ' ' + str(weeknum))
            self.setCurrentIndex(index)
            self.weeksopened.append(weeknum)
        else:
            self.setCurrentIndex(self.weeksopened.index(weeknum))


    def getNotSaved(self):
        return self.notsaved

    def getWidgetFromWeeknum(self, weeknum):
        """ Returns Maintable of a specified week """

        wasopened = True
        if weeknum not in self.weeksopened:
            self.openTab(weeknum)
            widget = self.widget(self.weeksopened.index(weeknum))
            self.closeWeek(weeknum)
        else:
            widget = self.widget(self.weeksopened.index(weeknum))
        return widget

    def getWeeksOpened(self):
        return self.weeksopened

    def setValues(self, values, weekdayindex, weeknum):
        if self.count() == 0:
            self.weeksopened = []
        if weeknum not in self.weeksopened:
            self.openTab(weeknum)
        table = self.getWidgetFromWeeknum(weeknum)
        table.setItemsColumn(values, weekdayindex)

    def closeWeek(self, weeknum):
        if weeknum in self.notsaved:
            main_window = self.parent().parent().parent().parent()
            main_window.save()
        self.tabindex = self.weeksopened.index(weeknum)
        self.removeTab(self.tabindex)
        self.weeksopened.remove(weeknum)

    def updatelanguage(self):
        for i in range(len(self.weeksopened)):
            weeknum = self.tabText(i)[-1]
            self.setTabText(i, language.languagedict['WeekHeader'] + ' ' + str(weeknum))
            self.widget(i).setHorizontalHeaderLabels(global_vars.WEEKDAYSLANGUAGE)

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
