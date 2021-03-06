import shutil
import os

from PySide.QtGui import *
from PySide.QtCore import QDate

import paths


SALT = str(QDate.currentDate().toString('ddMMyyyy'))

# Decorator maker. Input: mode - 'save' or 'load'
# Wraps the save or load function, making all the necessary file twerks before and after
def filemove(mode):
    def decorator(func):
        def wrapper(layout):
            dateadded = False
            if mode == 'save':
                if paths.savePath == '':
                        savedialog = QFileDialog()
                        savedialog.setAcceptMode(QFileDialog.AcceptSave)
                        savedialog.setDefaultSuffix('txt')
                        savedialog.exec_()
                        if savedialog.result() != QDialog.Accepted:
                            return
                        paths.savePath = savedialog.selectedFiles()[0][:-4] + 'file.txt'
                else:
                    if not os.path.isfile(os.path.basename(paths.savePath)[:-8]):
                        shutil.move(paths.savePath[:-8], os.curdir)

            elif mode == 'load':
                loaddialog = QFileDialog()
                loaddialog.setFileMode(QFileDialog.ExistingFile)
                loaddialog.setFilter('*.txt')
                loaddialog.exec_()
                if loaddialog.result() != QDialog.Accepted:
                    return
                paths.savePath = loaddialog.selectedFiles()[0]
                if os.path.split(paths.savePath)[0].replace('/', '\\') != os.path.abspath(os.path.curdir):
                    try:
                        shutil.move(paths.savePath[:-8], os.curdir)
                    except FileNotFoundError:
                        #TODO Error message box
                        print('File not found')
                        return
                    except shutil.Error:
                        try:
                            shutil.move(paths.savePath[:-8], paths.savePath[:-8] + SALT)
                            shutil.move(paths.savePath[:-8] + SALT, os.curdir)
                            dateadded = True
                        except shutil.Error:
                            print('Unable to move file')
                            return


            else:
                raise AttributeError

            func(layout)
            # Move everything back
            if not os.path.isfile(paths.savePath[:-8]):
                if dateadded:
                    shutil.move(os.path.basename(paths.savePath)[:-8] + SALT, paths.savePath[:-8])
                else:
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


def isItemAtPoint(position, layout):
    """Returns True if there is a task label on given position, otherwise False"""
    for item in range(layout.count()):
        if layout.itemAt(item).geometry().contains(position):
            return True
    return False


def itemAtPoint(position, layout):
    """Returns item at given position"""
    for item in range(layout.count()):
        if layout.itemAt(item).geometry().contains(position):
            return layout.itemAt(item)
    return 0


def countGroupTasksInList(group, array):
    count = 0
    for val in array:
        if val in group:
            count += 1
    return count


def transpose(x):
    return list(map(list, zip(*x)))