from PySide.QtSql import *


def setConnection(username=None, password=None):
        dab = QSqlDatabase.addDatabase("QSQLITE")
        dab.setDatabaseName('test_new')
        if username != None:
            dab.setUsername(username)
        if password != None:
            dab.setPassword(password)
        if not dab.open():
            return False
        time = []
        for i in range(0, 1440, 30):
            hours = i//60
            minutes = i - hours*60
            hours = '0' + str(hours)
            minutes = '0' + str(minutes)
            hours = hours[-2:]
            minutes = minutes[-2:]
            time.append(str(hours) + ':' + str(minutes))
        print(time)
        q_main = 'CREATE TABLE main(weekday varchar, task int, time int)'
        query = QSqlQuery()
        query.exec_(q_main)

        q_task = 'CREATE TABLE tasks(name varchar, status varchar)'
        query.exec_(q_task)

        q_status = 'CREATE TABLE status(name varchar, comments text)'
        query.exec_(q_status)

        q_time = 'CREATE TABLE time(hour varchar)'
        query.exec_(q_time)

        query = QSqlQuery('SELECT * FROM time')
        if not query.next():
            for hour in time:
                query.prepare('INSERT INTO time(hour) VALUES (:hour)')
                query.bindValue(":hour", hour)
                query.exec_()
        return True


def getStatuses():
    q = 'SELECT name FROM status'
    query = QSqlQuery(q)
    result = []
    while query.next():
        result.append(query.value(0))
    return result


def getTasks(status):
    id ='SELECT rowid FROM status WHERE name ="' + status + '"'
    query = QSqlQuery(id)
    query.next()
    id =str(query.value(0))
    q = 'SELECT name FROM tasks WHERE status ="' + id + '"'
    query = QSqlQuery(q)
    result = []
    while query.next():
        result.append(query.value(0))
    return result


def truncate():
    query = QSqlQuery('DELETE FROM main')
    query.exec_()
    query = QSqlQuery('DELETE FROM tasks')
    query.exec_()
    query = QSqlQuery('DELETE FROM status')
    query.exec_()
