from peewee import MySQLDatabase, Model
from peewee import CharField, IntegerField, DecimalField, DateTimeField, DateField
import uuid
import time

db = MySQLDatabase(database='vnpy_slave', user='root', password='root', host='localhost', port=3306)


class User(Model):
    pk_id = IntegerField(primary_key=True)
    username = CharField()
    password = CharField()
    create_date = DateTimeField()

    class Meta:
        database = db
        table_name = 'user'


class KV(Model):
    pk_id = IntegerField(primary_key=True)
    name = CharField()
    description = CharField()
    key = CharField()
    value = CharField()

    class Meta:
        database = db
        table_name = 'kv'


class CTPOrder(Model):
    pk_id = IntegerField(primary_key=True)
    account = CharField()
    order_id = CharField()
    name = CharField()
    code = CharField()
    price = DecimalField()
    volume = IntegerField()
    order_type = CharField()
    is_complete = IntegerField()
    complete_volume = IntegerField()
    open_or_close = CharField()
    buy_or_sell = CharField()
    is_close = IntegerField()
    slice_id = CharField()
    note = CharField()
    create_date = DateTimeField()

    class Meta:
        database = db
        table_name = 'ctp_order'


class Slice(Model):
    pk_id = CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    account = CharField()
    buy_or_sell = CharField()
    name = CharField()
    code = CharField()
    volume = IntegerField()
    open_price = DecimalField()
    open_charge = DecimalField()
    open_order_id = CharField()
    close_price = DecimalField()
    close_charge = DecimalField()
    close_order_id = CharField()
    is_close = IntegerField()
    note = CharField()
    close_date = DateTimeField()
    create_date = DateTimeField()

    class Meta:
        database = db
        table_name = 'slice'


class Account(Model):
    pk_id = IntegerField(primary_key=True)
    account = CharField()
    account_name = CharField()
    initial_margin = DecimalField()
    margin = DecimalField()
    slice_num = IntegerField()
    slice_margin = DecimalField()
    is_disable = IntegerField()
    balance = DecimalField()
    frozen = DecimalField()
    create_date = DateTimeField()

    class Meta:
        database = db
        table_name = 'account'


class AccountDayClientEquity(Model):
    pk_id = IntegerField(primary_key=True)
    account = CharField()
    client_equity = DecimalField()
    date = DateTimeField()
    create_date = DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    class Meta:
        database = db
        table_name = 'account_day_client_equity'


class Price(Model):
    pk_id = IntegerField(primary_key=True)
    name = CharField()
    code = CharField()
    price = IntegerField()
    create_date = DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    class Meta:
        database = db
        table_name = 'price'


class SliceDayLog(Model):
    pk_id = IntegerField(primary_key=True)
    account = CharField()
    date = DateField()
    slice_num = IntegerField()
    slice_volume = IntegerField()
    create_date = DateTimeField()

    class Meta:
        database = db
        table_name = 'slice_day_log'