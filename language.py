import paths
from PySide.QtGui import *
languagedict = {}


def loadLanguage():
    """Loads the contents of the language file (paths.languagePath) to the language dictionary"""

    lanfile = open(paths.languagePath)
    lanstrings = lanfile.read().splitlines()
    for lanstring in lanstrings:
        lanstring = lanstring.split(' ')
        if len(lanstring) > 2 and lanstring[0] != '#' and lanstring[1] == '=':
            global languagedict
            languagedict[lanstring[0]] = eval(' '.join(lanstring[2:]))


def chooseLanguageFile(widget):
    """Opens the dialog to choose language file and writes the path to paths.languagePath"""

    filepath = QFileDialog.getOpenFileName(widget,
                                           'Open Language File', 'languages/', 'Text Files (*txt)')[0]
    if filepath:
        paths.languagePath = filepath