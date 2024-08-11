import pmodel
import tools
import threading
import time
import numpy

#now_date_format = tools.get_now_date_format()

# where = f"account = '{account}' AND is_close = 0 AND create_date > '{now_date_format} 00:00:00' AND create_date <= '{now_date_format} 23:59:59'"

# where = (
#     (pmodel.CTPOrder.account == "226288")
#     & (pmodel.CTPOrder.is_close == 0)
#     & (pmodel.CTPOrder.create_date > f"{now_date_format} 00:00:00")
#     & (pmodel.CTPOrder.create_date <= f"{now_date_format} 23:59:59")
# )
# query = pmodel.CTPOrder.select().where(where)
# for v in query:
#     print(f"pk_id: {v.pk_id} account: {v.account} order_id: {v.order_id} create_date: {v.create_date} ")


#
# create = pmodel.CTPOrder.create(
#     account="123456",
#     order_id="orderid123",
#     code="jd2409",
#     create_date=tools.get_now_date_format(),
# )
# print(type(create))
# print(create.pk_id)

#
# slice_pk_id = 33
# close_order_id = "CTP.3_863416447_2"
# close_price = 4000
# update = pmodel.Slice.update(is_close=1, close_order_id=close_order_id, close_price=close_price).where(pmodel.Slice.pk_id==slice_pk_id).execute()
# print(update)

# 获取kv
# def kv_get(key):
#     get = pmodel.KV.select(pmodel.KV.value).where(pmodel.KV.key == key).first()
#     if get == None:
#         return ''
#     return get.value


# now_date_format = tools.get_now_date_format("%Y-%m-%d")
# where = (
#         (pmodel.CTPOrder.account == "226288")
#         & (pmodel.CTPOrder.is_close == 0)
#         & (pmodel.CTPOrder.create_date >= f"{now_date_format} 00:00:00")
#         & (pmodel.CTPOrder.create_date <= f"{now_date_format} 23:59:59")
# )
# select = pmodel.CTPOrder.select().where(where)
# print(select)
# print(len(select))


# import sched
# import time
#
#
#
# # 创建调度器
#
# def my_function(arg1, arg2):
#     print(f"Function executed with arguments: {arg1}, {arg2}")
#     # 重新调度函数
#     scheduler.enter(1, 1, my_function, argument=(arg1, arg2))
#
# scheduler = sched.scheduler(time.time, time.sleep)
# scheduler.enter(1, 1, my_function, argument=("Hello", "World"))
# scheduler.run()


my1 = 123

q = numpy.where(my1 == "123", "真的", "假的")
print(q)