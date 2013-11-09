from PySide.QtSql import *
def setConnection(username = 0, password = 0):
        dab = QSqlDatabase.addDatabase("QSQLITE")
        dab.setDatabaseName('test')
        if username != 0:
            dab.setUsername(username)
        if password != 0 :
            dab.setPassword(password)
        if not dab.open():
            return False
        query = QSqlQuery()
        query.exec_('create table test(lol varchar(20))')
        return True
def addRecord(record):
    query = QSqlQuery()
    request = 'INSERT INTO test VALUES("' + record + '")'
    return query.exec_(request)
def delRecord(row):
    query = QSqlQuery()
    request = 'DELETE FROM test WHERE rowid =' + row
    return query.exec_(request)