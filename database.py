from PySide.QtSql import *

import global_vars


def setConnection(name, username=0, password=0):
    """Creates db using specified name and creates suitable empty tables"""

    dab = QSqlDatabase.addDatabase("QSQLITE")
    dab.setDatabaseName(name)
    if username != 0:
        dab.setUsername(username)
    if password != 0:
        dab.setPassword(password)
    if not dab.open():
        return False
    time = ''
    for i in range(0, 1440, 30):
        hours = i // 60
        minutes = i - hours * 60
        hours = '0' + str(hours)
        minutes = '0' + str(minutes)
        hours = hours[-2:]
        minutes = minutes[-2:]
        time = time + ' "' + str(hours) + ':' + str(minutes) + '" int,'
    time = time[:-1]
    q_main = 'CREATE TABLE main(weekday varchar,' + time + ')'
    query = QSqlQuery()
    query.exec_(q_main)

    q_task = 'CREATE TABLE tasks(name varchar, status varchar)'
    query.exec_(q_task)

    q_status = 'CREATE TABLE status(name varchar, comments text)'
    query.exec_(q_status)

    days = ''
    for day in global_vars.WEEKDAYS:
        days += day + ' integer, '

    q_eval = 'CREATE TABLE evaluation(week integer, ' + days[:-2] + ')'
    query.exec_(q_eval)
    return True


def truncate():
    """Clears the tables"""

    query = QSqlQuery('DELETE FROM main')
    query.exec_()
    query = QSqlQuery('DELETE FROM tasks')
    query.exec_()
    query = QSqlQuery('DELETE FROM status')
    query.exec_()


def dropConnection():
    """Kills connection - allowing to move db file"""

    QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())


def getStatuses():
    """Returns all the statuses"""

    q = 'SELECT name FROM status'
    query = QSqlQuery(q)
    result = []
    while query.next():
        result.append(query.value(0))
    return result


def getTasks(status):
    """Returns all the tasks for the specified status"""

    id = 'SELECT rowid FROM status WHERE name ="' + status + '"'
    query = QSqlQuery(id)
    query.next()
    id = str(query.value(0))
    q = 'SELECT name FROM tasks WHERE status ="' + id + '"'
    query = QSqlQuery(q)
    result = []
    while query.next():
        result.append(query.value(0))
    return result