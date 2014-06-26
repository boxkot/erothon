import sqlite3

class ORM(object):

    _db     = None
    _select = ''
    _insert = ''
    _update = ''
    _delete = ''
    _table  = ''
    _where  = ''
    _order  = ''
    _limit  = ''

    def __init__(self, path):
        self._db              = sqlite3.connect(path)
        self._db.row_factory  = sqlite3.Row
        self._db.text_factory = str

    def select(self, columns = []):
        self._select = ''
        self._table  = ''
        self._where  = ''
        self._order  = ''
        self._limit  = ''
        columnsStr   = ''
        if (len(columns) == 0):
            columnsStr = '*'
        else:
            for value in columns:
                if isinstance(value, dict):
                    k, v        = value.items()[0]
                    columnsStr += '%s as %s, ' % (k, v)
                else:
                    columnsStr += '%s, ' % value
            columnsStr = columnsStr[:-2]
        self._select = 'select %s from' % columnsStr
        return self

    def table(self, table):
        tableStr = ''
        if isinstance(table, dict):
            k,v      = table.items()[0]
            tableStr = ' %s %s' % (k, v)
        else:
            tableStr = ' %s' % table
        self._table = tableStr
        return self

    def where(self, where):
        whereStr = ''
        if self._where == '':
            whereStr = ' where '
        else:
            whereStr = ' %s AND ' % self._where

        for key, value in where.items():
            if isinstance(value, int) or isinstance(value, float):
                whereStr += '%s %s AND' % (key, value)
            else:
                whereStr += '%s "%s" AND' % (key, value)
        whereStr = whereStr[:-4]
        self._where = whereStr
        return self

    def orwhere(self, where):
        whereStr = ''
        if self._where == '':
            whereStr = ' where '
        else:
            whereStr = ' %s OR ' % self._where

        for key, value in where.items():
            if isinstance(value, int) or isinstance(value, float):
                whereStr += '%s %s OR' % (key, value)
            else:
                whereStr += '%s "%s" OR' % (key, value)
        whereStr = whereStr[:-3]
        self._where = whereStr
        return self


    def order(self, order):
        orderStr = ' order by '
        for key, value in order.items():
            orderStr += '%s %s, ' % (key, value)
        orderStr = orderStr[:-2]
        self._order = orderStr
        return self

    def limit(self, limit):
        limitStr = ' limit '
        if isinstance(limit, tuple):
            k,v       = limit
            limitStr += '%s offset %s' % (k, v)
        else:
            limitStr += '%s' % limit
        self._limit = limitStr
        return self

    def _selectCreate(self):
        sql = self._select \
            + self._table  \
            + self._where  \
            + self._order  \
            + self._limit
        return sql

    def fetchAll(self):
        sql    = self._selectCreate()
        data   = []
        result = self._db.execute(sql)
        count  = 0
        for row in result:
            data.append({})
            for key in row.keys():
                data[count][key] = row[key]
            count += 1
        return data

    def fetchOne(self):
        sql = self._selectCreate()
        return self._db.execute(sql).fetchone()

    def insert(self, table, data):
        columns = ''
        values   = ''
        for key, value in data.items():
            columns = '%s%s, ' % (columns, key)
            if isinstance(value, int):
                values  = '%s%s, ' % (values, value)
            elif isinstance(value, str):
                values  = '%s\'%s\', ' % (values, value)
        columns      = '(%s)' % columns[:-2]
        values       = '(%s)' % values[:-2]
        sql          = 'insert into %s %s values %s' % (table, columns, values)
        self._insert = sql
        try:
            self._db.execute(sql)
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            return False
        return True

    def update(self, table, data):
        self._update = ''
        self._where  = ''
        dataStr      = ''
        for key, value in data.items():
            if isinstance(value, int):
                dataStr += '%s = %i, ' % (key, value)
            else:
                dataStr += '%s = \'%s\', ' % (key, value)
        dataStr = dataStr[:-2]
        self._update = 'update %s set %s' % (table, dataStr)
        return self

    def updateExe(self):
        sql = self._update \
            + self._where
        try:
            self._db.execute(sql)
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            return False
        return True

    def delete(self, table):
        self._delete = ''
        self._where  = ''
        self._delete = 'delete from %s ' % table
        return self

    def deleteExe(self):
        sql = self._delete \
            + self._where
        try:
            self._db.execute(sql)
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            return False
        return True

    def close(self):
        self._db.close()
        return self

    def toStringSelect(self):
        return self._selectCreate()

    def toStringInsert(self):
        return self._insert

    def toStringUpdate(self):
        return self._update + self._where

    def toStringDelete(self):
        return self._delete + self._where
