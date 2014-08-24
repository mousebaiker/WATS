import paths
import shutil
import os
from PySide.QtGui import *
from PySide.QtCore import QDate

# Decorator maker. Input: mode - 'save' or 'load'
# Wraps the save or load function, making all the necessary file twerks before and after
def filemove(mode):
    def decorator(func):
        def wrapper(self):
            if mode == 'save':
                if paths.savePath == '':
                        savedialog = QFileDialog()
                        savedialog.setAcceptMode(QFileDialog.AcceptSave)
                        savedialog.setDefaultSuffix('txt')
                        savedialog.exec_()
                        paths.savePath = savedialog.selectedFiles()[0][:-4] + 'file.txt'
                else:
                    if not os.path.isfile(os.path.basename(paths.savePath)[:-8]):
                        shutil.move(paths.savePath[:-8], os.curdir)

            elif mode == 'load':
                loaddialog = QFileDialog()
                loaddialog.setFileMode(QFileDialog.ExistingFile)
                loaddialog.setFilter('*.txt')
                loaddialog.exec_()
                paths.savePath = loaddialog.selectedFiles()[0]
                if os.path.split(paths.savePath)[0].replace('/', '\\') != os.path.abspath(os.path.curdir):
                    try:
                        shutil.move(paths.savePath[:-8], os.curdir)
                    except FileNotFoundError:
                        #TODO Error message box
                        print('File not found')
                        return
            else:
                raise AttributeError

            func(self)
            # Move everything back
            if not os.path.isfile(paths.savePath[:-8]):
                shutil.move(os.path.basename(paths.savePath)[:-8], paths.savePath[:-8])
        return wrapper
    return decorator


def countPercent(given, total):
    """Returns the percent number of given against total"""
    return int((float(given)/total) * 100)


def fromDatetoQDate(date):
    """Returns the QDate object generated from datatime.date object"""
    return QDate.fromString(date.isoformat(), 'yyyy-MM-dd')

def getWeekDif(first, last):
    """Returns how many weeks are between 2 given days
    first, last - tuples (weekNum, year)"""

    if first.weekNumber()[1] < last.weekNumber()[1]:
        # 28 December is chosen as indicator of the last week
        # It is not 31 December, because sometimes it is considered as the 1 week of the new year
        firstyearsum = QDate(first.year(), 12, 28).weekNumber()[0] - first.weekNumber()[0]
        lastyearsum = last.weekNumber()[0]
        middleyearsum = sum([QDate(first.weekNumber()[1] + 1 + i, 12, 28).weekNumber()[0]
                             for i in range(last.weekNumber()[1] - first.weekNumber()[1] - 1)])
        return firstyearsum + lastyearsum + middleyearsum
    elif first.weekNumber()[1] == last.weekNumber()[1]:
        return last.weekNumber()[0] - first.weekNumber()[0]