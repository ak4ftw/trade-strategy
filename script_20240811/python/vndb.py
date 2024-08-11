import mysql.connector
import tools



class Db:
    host = "localhost"
    port = '3306'
    user = "root"
    passwd = "root"
    database = "vnpy"
    charset = "utf8mb4"
    connect = ''
    lastrowid = 0
    rowcount = 0
    def ConnectDb(self):
        DBconnect = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database,
            charset=self.charset,
        )
        self.connect = DBconnect
    def CloseDb(self):
        self.connect.close()
    def Execute(self, sql = 'SHOW databases', val = () ):
        mc = self.connect.cursor()
        mc.execute(sql, val)
        fetchall = mc.fetchall()
        self.lastrowid = mc.lastrowid
        self.rowcount = mc.rowcount
        return fetchall
    def ExecuteInsert(self, sql = 'SHOW databases', val = () ):
        mc = self.connect.cursor()
        mc.execute(sql, val)
        self.connect.commit()
        self.lastrowid = mc.lastrowid
        self.rowcount = mc.rowcount
        return mc.lastrowid
    def ExecuteUpdate(self, sql = 'SHOW databases'):
        mc = self.connect.cursor()
        mc.execute(sql)
        self.connect.commit()
        self.lastrowid = mc.lastrowid
        self.rowcount = mc.rowcount
        return mc.lastrowid
    def ExecuteTruncate(self, tableName):
        mc = self.connect.cursor()
        sql = "TRUNCATE `" + tableName + "`"
        mc.execute(sql)
    def UpdateForm(self, dataDict = {}):
        strData = ' '
        for i in dataDict:
            strData = strData + "`{key}` = '{value}' ,".format(key = i, value = dataDict.get(i))
        strData = strData[0:-1] + ' '
        return strData


class AccountModel():
    TableName = 'account'
    Count = 0

    def Select(self, where='1', limitStart=0, limitEnd=10, orderBy="create_date DESC"):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} ORDER BY {orderBy} LIMIT {limitStart},{limitEnd} ".format(
            where=where, orderBy=orderBy, limitStart=limitStart, limitEnd=limitEnd)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def SelectAll(self, where='1', orderBy="create_date DESC"):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} ORDER BY {orderBy} ".format(where=where, orderBy=orderBy)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def Insert(self, account, initialMargin, margin, slice_num, slice_margin, isDisable):
        mydb = Db()
        mydb.ConnectDb()
        nowDate = tools.get_now_date_format()
        sql = "INSERT INTO `" + self.TableName + "` (account, initial_margin, margin, slice_num, slice_margin, is_disable) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (account, initialMargin, margin, slice_num, slice_margin, isDisable)
        insert = mydb.ExecuteInsert(sql, val)
        mydb.CloseDb()
        return insert

    def Update(self, where, data):
        mydb = Db()
        mydb.ConnectDb()
        strData = mydb.UpdateForm(data)
        sql = "UPDATE `item` SET {dataForm} WHERE {where} ".format(dataForm=strData, where=where)
        update = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return 1

    def GetField(self):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SHOW FULL COLUMNS FROM `item`"
        select = mydb.Execute(sql)
        mydb.CloseDb()
        return select

    def Count(self, where='1'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SELECT count(*) AS count FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.Execute(sql)
        mydb.CloseDb()
        self.Count = select[0][0]
        return self.Count
        


class SliceModel():
    TableName = 'slice'
    Count = 0

    def Select(self, where='1', limitStart=0, limitEnd=10, orderBy="create_date DESC"):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} ORDER BY {orderBy} LIMIT {limitStart},{limitEnd} ".format(
            where=where, orderBy=orderBy, limitStart=limitStart, limitEnd=limitEnd)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def SelectAll(self, where='1', orderBy="create_date DESC"):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} ORDER BY {orderBy} ".format(where=where,
                                                                                                orderBy=orderBy)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def Insert(self, account, openType, name, code, num, price):
        mydb = Db()
        mydb.ConnectDb()
        nowDate = tools.get_now_date_format()
        sql = "INSERT INTO `" + self.TableName + "` (account, open_type, name, code, num, price, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (account, openType, name, code, num, price, nowDate)
        insert = mydb.ExecuteInsert(sql, val)
        mydb.CloseDb()
        return insert

    def Update(self, where, data):
        mydb = Db()
        mydb.ConnectDb()
        strData = mydb.UpdateForm(data)
        sql = "UPDATE `" + self.TableName + "` SET {dataForm} WHERE {where}".format(dataForm=strData, where=where)
        update = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return 1

    def GetField(self):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        select = mydb.Execute(sql)
        mydb.CloseDb()
        return select

    def Count(self, where='1'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SELECT count(*) AS count FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.Execute(sql)
        mydb.CloseDb()
        self.Count = select[0][0]
        return self.Count

    def Delete(self, where='pk_id = 0'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "DELETE FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return select     
        

class SliceLogModel():
    TableName = 'slice_log'
    Count = 0

    def Select(self, where='1', limitStart=0, limitEnd=10, orderBy="create_date DESC"):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} ORDER BY {orderBy} LIMIT {limitStart},{limitEnd} ".format(
            where=where, orderBy=orderBy, limitStart=limitStart, limitEnd=limitEnd)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def SelectAll(self, where='1', orderBy="create_date DESC"):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} ORDER BY {orderBy} ".format(where=where, orderBy=orderBy)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def Insert(self, account, open_or_close, buy_or_sell, name, code, num, price, charge, slice_id, average_hold_price):
        mydb = Db()
        mydb.ConnectDb()
        nowDate = tools.get_now_date_format()
        sql = "INSERT INTO `" + self.TableName + "` (account, open_or_close, buy_or_sell, name, code, num, price, charge, slice_id, average_hold_price, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (account, open_or_close, buy_or_sell, name, code, num, price, charge, slice_id, average_hold_price, nowDate)
        insert = mydb.ExecuteInsert(sql, val)
        mydb.CloseDb()
        return insert

    def Update(self, where, data):
        mydb = Db()
        mydb.ConnectDb()
        strData = mydb.UpdateForm(data)
        sql = "UPDATE `item` SET {dataForm} WHERE {where}".format(dataForm=strData, where=where)
        update = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return 1

    def GetField(self):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        select = mydb.Execute(sql)
        mydb.CloseDb()
        return select

    def Count(self, where='1'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SELECT count(*) AS count FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.Execute(sql)
        mydb.CloseDb()
        self.Count = select[0][0]
        return self.Count       

    def Delete(self, where='pk_id = 0'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "DELETE FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return select
        
            
class KvModel():
    TableName = 'kv'
    Count = 0

    def FindByKey(self, key):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT value FROM `" + self.TableName + "` WHERE `key` = '{key}' LIMIT 1".format(key=key)
        select = mydb.Execute(sql)
        if len(select) == 0:
            return ''
            
        return select[0][0]
        
    def Select(self, where='1'):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} LIMIT 1".format(where=where)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def SelectAll(self, where='1', orderBy="pk_id ASC"):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} ORDER BY {orderBy} ".format(where=where, orderBy=orderBy)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def Insert(self, name, description, key, value):
        mydb = Db()
        mydb.ConnectDb()
        nowDate = tools.get_now_date_format()
        sql = "INSERT INTO `" + self.TableName + "` (name, description, key, value) VALUES (%s, %s, %s, %s)"
        val = (name, description, key, value)
        insert = mydb.ExecuteInsert(sql, val)
        mydb.CloseDb()
        return insert

    def Update(self, where, data):
        mydb = Db()
        mydb.ConnectDb()
        strData = mydb.UpdateForm(data)
        sql = "UPDATE `" + self.TableName + "` SET {dataForm} WHERE {where}".format(dataForm=strData, where=where)
        update = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return 1

    def GetField(self):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        select = mydb.Execute(sql)
        mydb.CloseDb()
        return select

    def Count(self, where='1'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SELECT count(*) AS count FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.Execute(sql)
        mydb.CloseDb()
        self.Count = select[0][0]
        return self.Count       

    def Delete(self, where='pk_id = 0'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "DELETE FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return select


            
class HandleBarLogModel():
    TableName = 'handle_bar_log'
    Count = 0
    
    def Insert(self, name):
        mydb = Db()
        mydb.ConnectDb()
        nowDate = tools.get_now_date_format()
        sql = "INSERT INTO `" + self.TableName + "` (name, create_date) VALUES (%s, %s)"
        val = (name, nowDate)
        insert = mydb.ExecuteInsert(sql, val)
        mydb.CloseDb()
        return insert

            
class PriceModel():
    TableName = 'price'
    Count = 0
    
    def Insert(self, name, code, price):
        mydb = Db()
        mydb.ConnectDb()
        nowDate = tools.get_now_date_format()
        sql = "INSERT INTO `" + self.TableName + "` (name, code, price, create_date) VALUES (%s, %s, %s, %s)"
        val = (name, code, price, nowDate)
        insert = mydb.ExecuteInsert(sql, val)
        mydb.CloseDb()
        return insert
        
            
class AccountDayClientEquityModel():
    TableName = 'account_day_client_equity'
    Count = 0

    def Select(self, where='1'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} LIMIT 1".format(where=where)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)
        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()
        return data

    def Insert(self, account, client_equity, date):
        mydb = Db()
        mydb.ConnectDb()
        nowDate = tools.get_now_date_format()
        sql = "INSERT INTO `" + self.TableName + "` (account, client_equity, date, create_date) VALUES (%s, %s, %s, %s)"
        val = (account, client_equity, date, nowDate)
        insert = mydb.ExecuteInsert(sql, val)
        mydb.CloseDb()
        return insert

    def Update(self, where, data):
        mydb = Db()
        mydb.ConnectDb()
        strData = mydb.UpdateForm(data)
        sql = "UPDATE `" + self.TableName + "` SET {dataForm} WHERE {where}".format(dataForm=strData, where=where)
        update = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return 1

    def Delete(self, where='pk_id = 0'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "DELETE FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return select


class CtpOrderModel():
    TableName = 'ctp_order'
    Count = 0

    def Select(self, where='1', limitStart=0, limitEnd=10, orderBy="create_date DESC"):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} ORDER BY {orderBy} LIMIT {limitStart},{limitEnd} ".format(where=where, orderBy=orderBy, limitStart=limitStart, limitEnd=limitEnd)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def SelectAll(self, where='1', orderBy="create_date DESC"):
        mydb = Db()
        mydb.ConnectDb()

        sql = "SELECT * FROM `" + self.TableName + "` WHERE {where} ORDER BY {orderBy} ".format(where=where, orderBy=orderBy)
        select = mydb.Execute(sql)
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        columns = mydb.Execute(sql)

        data = []
        for i in select:
            fieldNum = 0
            oneData = {}
            for j in i:
                oneData[columns[fieldNum][0]] = j
                fieldNum = fieldNum + 1
            data.append(oneData)
        mydb.CloseDb()

        return data

    def Insert(self, account, order_id, code, price, volume, order_type, is_complete, complete_volume, open_or_close, buy_or_sell):
        mydb = Db()
        mydb.ConnectDb()
        nowDate = tools.get_now_date_format()
        sql = "INSERT INTO `" + self.TableName + "` (account, order_id, code, price, volume, order_type, is_complete, complete_volume, open_or_close, buy_or_sell, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (account, order_id, code, price, volume, order_type, is_complete, complete_volume, open_or_close, buy_or_sell, nowDate)
        insert = mydb.ExecuteInsert(sql, val)
        mydb.CloseDb()
        return insert

    def Update(self, where, data):
        mydb = Db()
        mydb.ConnectDb()
        strData = mydb.UpdateForm(data)
        sql = "UPDATE `" + self.TableName + "` SET {dataForm} WHERE {where}".format(dataForm=strData, where=where)
        update = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return 1

    def GetField(self):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SHOW FULL COLUMNS FROM `" + self.TableName + "`"
        select = mydb.Execute(sql)
        mydb.CloseDb()
        return select

    def Count(self, where='1'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "SELECT count(*) AS count FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.Execute(sql)
        mydb.CloseDb()
        self.Count = select[0][0]
        return self.Count

    def Delete(self, where='pk_id = 0'):
        mydb = Db()
        mydb.ConnectDb()
        sql = "DELETE FROM `" + self.TableName + "` WHERE {where}".format(where=where)
        select = mydb.ExecuteUpdate(sql)
        mydb.CloseDb()
        return select
