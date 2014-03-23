import paths
languagedict = {}
def loadLanguage():
    lanfile = open(paths.languagePath)
    lanstrings = lanfile.read().splitlines()
    for lanstring in lanstrings:
        lanstring = lanstring.split(' ')
        if len(lanstring) > 2 and lanstring[0] != '#' and lanstring[1] == '=':
            global languagedict
            languagedict[lanstring[0]] = eval(' '.join(lanstring[2:]))
