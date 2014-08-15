import paths
import shutil
import os
from PySide.QtGui import *


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