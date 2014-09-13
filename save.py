import os
import datetime

from PySide.QtSql import QSqlQuery

import helpers
import global_vars
import paths
import database


@helpers.filemove('save')
def save(layout):
    """"Saves the state of the program and moves the save file to specified place"""

    # Create a file if there is no previous save
    # else move db to current folder to save
    if not os.path.isfile(paths.savePath):
        # Create txt and write down the first day of usage
        savefile = open(paths.savePath, mode='w')
        savefile.write(str(global_vars.DAYFIRST.toordinal()))
        savefile.close()

    filename = os.path.basename(paths.savePath)[:-8]

    # Saving tasks widget block
    database.setConnection(filename)
    database.truncate()
    groups = layout.taskwidget.getGroups()

    for group in groups:
        query = QSqlQuery()
        query.prepare("INSERT INTO status (name) VALUES (:name)")
        query.bindValue(":name", group.getName())
        query.exec_()

        query = QSqlQuery("SELECT rowid FROM status WHERE name = '" + group.getName() + "' ")
        query.next()
        id_ = query.value(0)

        for task in group:
            query = QSqlQuery()
            query.prepare("INSERT INTO tasks (name, status) VALUES (:name, :id)")
            query.bindValue(":name", task.getTask())
            query.bindValue(":id", id_)
            query.exec_()

    # Saving maintable
    for weeknum in layout.tab.notsaved:
        table = layout.tab.getWidgetFromWeeknum(weeknum)
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for weekday in weekdays:
            tasks = table.getTasks(weekday)
            if tasks:
                fields = ''
                values = ''
                for time in tasks:
                    query = QSqlQuery("SELECT rowid FROM tasks WHERE name ='" + tasks[time] + "'")
                    query.next()
                    tasks[time] = query.value(0)
                    fields += '"' + time + '"' + ','
                    values += str(tasks[time]) + ','
                fields = 'weekday,' + fields[:-1]
                values = '"' + weekday + '_' + str(weeknum) + '"' + ', ' + values[:-1]
                request = 'INSERT INTO main (' + fields + ') VALUES (' + values + ')'
                query = QSqlQuery()
                query.exec_(request)
    layout.tab.notsaved = []


    # Saving evaluation values
    for week in global_vars.EVAL_VALUES.keys():
        val = str(week) + ', '
        for value in global_vars.EVAL_VALUES[week]:
            val += str(value) + ', '
        request = 'INSERT INTO evaluation VALUES(' + val[:-2] + ')'
        query = QSqlQuery()
        query.exec_(request)

    print('Saved')
    # Restoring the original state
    database.dropConnection()


@helpers.filemove('load')
def load(layout):
    """"Loads the file and restores the saved state"""

    # Restore the first day of usage
    global_vars.DAYFIRST = datetime.date.fromordinal(int(open(paths.savePath).read().splitlines()[0]))

    filename = os.path.basename(paths.savePath)[:-8]
    database.setConnection(filename)
    layout.initTasks(database.getStatuses())
    layout.tab.clearAll()
    # ### Loading main table
    #
    #
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    opened = False

    q = 'SELECT * FROM main'
    query = QSqlQuery(q)
    while query.next():
        record = query.record()
        indexes = []
        if not record.isEmpty():
            for i in range(0, 44):
                if not record.isNull(i + 1):
                    indexes.append(i)
            day = str(record.field('weekday').value()).split('_')
            weekday = day[0]
            weeknum = int(day[1])

        values = {}
        for index in indexes:
            q = QSqlQuery("SELECT name FROM tasks WHERE rowid ='" + str(query.value(index + 1)) + "'")
            q.next()
            values[index] = q.value(0)

        if values:
            opened = True
            layout.tab.setValues(values, weekdays.index(weekday), weeknum)

    if not opened:
        layout.tab.openTab(1)
    #
    #
    ################

    # Loading evaluation values
    #
    q = 'SELECT * from evaluation'
    query = QSqlQuery(q)
    while query.next():
        record = query.record()
        if not record.isEmpty():
            week = record.field('week').value()
            values = []
            for day in global_vars.WEEKDAYS:
                values.append(record.field(day).value())
        global_vars.EVAL_VALUES[week] = values


    database.dropConnection()