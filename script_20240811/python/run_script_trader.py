from vnpy_scripttrader import ScriptEngine
from vnpy.trader.constant import OrderType, Status, Offset, Direction

import time
import tools
import pmodel

# 入口
def run(engine: ScriptEngine):

    all_account = engine.get_all_accounts()

    if len(all_account) == 0:
        engine.write_log("没有连接到账户")
        return

    # 遍历当前登录信息
    for v in all_account:
        engine.account = v.accountid
        if pmodel.Account.select().where(pmodel.Account.account == v.accountid).first() == None:
            pmodel.Account.create(account=v.accountid, slice_num=tools.kv_get("slice_num"), balance=v.balance, froze=v.frozen, create_date=tools.get_now_date_format())


    # 要操作的合约代码
    engine.open_code = tools.kv_get("open_code")
    vt_symbols = [engine.open_code]
    engine.write_log(f"开仓代码 {vt_symbols}")

    # 当前账户持仓的代码
    account_open_code = tools.kv_account_open_code(engine.account)
    engine.write_log(f"持仓代码 {account_open_code}")

    # 订阅行情
    engine.subscribe(vt_symbols)
    engine.subscribe(account_open_code)

    # 每次开空手数
    engine.slice_open_num = tools.kv_get("slice_open_num")

    interval = 1  # 每秒执行一次
    next_time = time.time() + interval

    # 持续运行，使用strategy_active来判断是否要退出程序
    while engine.strategy_active:

        loop_handle(engine)

        next_time += interval
        sleep_time = next_time - time.time()

        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            next_time = time.time() + interval

# 初始化账户数据
def init_account(engine):
    pass

# 循环
def loop_handle(engine):
    engine.write_log("\n\n\n")
    engine.write_log(f"------------------------- 开始运行 -------------------------")
    engine.write_log("loop_handle()")

    # 获取tick数据
    tick = engine.get_tick(engine.open_code)
    # 如果tick数据为空
    if tick == None:
        engine.write_log("tick 数据错误")
        return

    # 操作时间点
    target_time = tools.kv_get("target_time")
    # 当前时间
    now_time_form = time.strftime("%H:%M:%S", time.localtime())
    engine.write_log(f"------------------------- 触发时间 -------------------------")
    engine.write_log(f"当前时间：{now_time_form} 触发时间：{target_time}")

    # 数据展示
    print_price(engine, tick)
    print_account(engine)
    print_slice(engine)

    # 更新挂单状态
    update_order(engine)
    # 挂单超时后转为市价单
    if tools.kv_get("is_open_re_order") == "1":
        re_order(engine, tick)

    # 触发开平时间点
    if now_time_form == target_time:
        slice_close(engine, tick)
        slice_open(engine, tick)

    # 收盘后x分钟触发保存数据
    if now_time_form == tools.kv_get("after_trade_time"):
        save_contract_price(tick.name, tick.symbol, tick.last_price)
        save_account_client_equity(engine, engine.account)
        tools.upload_data()
        # 改为不会自动停止
        # engine.strategy_active = False


# 交易时段运行前运行
def before_target(engine):
    pass

# 交易时段运行后运行
def after_target(engine):
    pass

# 账户信息
def print_account(engine):
    engine.write_log(f"------------------------- 账户信息 -------------------------")
    all_account = engine.get_all_accounts()
    for v in all_account:
        engine.write_log(f"账号 {v.accountid} 接口 {v.gateway_name} 余额 {v.balance} 冻结 {v.frozen}")

# 输出价格使用
def print_price(engine, tick):
    engine.write_log(f"------------------------- 当前价格 -------------------------")
    #engine.write_log(f"tick {tick}")
    engine.write_log(f"品名 {tick.name} 代码 {tick.symbol}")
    engine.write_log(f"最新价格 {tick.last_price} 总手数 {tick.volume} 总金额 {tick.turnover}")
    engine.write_log(f"卖出价格 ask_price_3 {tick.ask_price_3} ask_volume_3 {tick.ask_volume_3}")
    engine.write_log(f"卖出价格 ask_price_2 {tick.ask_price_2} ask_volume_2 {tick.ask_volume_2}")
    engine.write_log(f"卖出价格 ask_price_1 {tick.ask_price_1} ask_volume_1 {tick.ask_volume_1}")
    engine.write_log(f"买入价格 bid_price_1 {tick.bid_price_1} bid_volume_1 {tick.bid_volume_1}")
    engine.write_log(f"买入价格 bid_price_2 {tick.bid_price_2} bid_volume_2 {tick.bid_volume_2}")
    engine.write_log(f"买入价格 bid_price_3 {tick.bid_price_3} bid_volume_3 {tick.bid_volume_3}")
    #engine.write_log(f"-------------------------当前价格-------------------------")

# 输出持仓情况
def print_slice(engine):
    engine.write_log(f"------------------------- 持仓情况 -------------------------")
    engine.write_log(f"账户 {engine.account}")
    where = (
        (pmodel.Slice.account == engine.account)
        & (pmodel.Slice.is_close == 0)
    )
    ctp_order_list = pmodel.Slice.select().where(where)
    engine.write_log(f"持仓数量 {len(ctp_order_list)} 份")
    for v in ctp_order_list:
        engine.write_log(f"id {v.pk_id} : 名称 {v.name} 代码 {v.code} 多或空 {v.buy_or_sell} 手数 {v.volume} 开仓价格 {v.open_price} 盈利价格 {v.open_price - 2} 开仓日期 {v.create_date}")
    #engine.write_log(f"-------------------------持仓情况-------------------------")

# 开仓
def slice_open(engine, tick):
    engine.write_log("slice_open()")

    # 是否开启每日开仓
    if tools.kv_get("is_open_slice") != "1":
        engine.write_log("已关闭 每日开仓")
        return

    # 如果今天开过仓了就不开仓了
    if tools.is_today_open():
        engine.write_log("今日已经开过仓")
        return

    # 如果今天挂单未全部成交就不开
    if is_today_order_uncomplete(engine):
        engine.write_log("今日有挂单未成交 或 未完全成交")
        return

    # 如果持仓超过15份了就不开仓了
    if get_account_slice_num(engine) >= int(tools.kv_get("slice_num")):
        engine.write_log(f"持仓超过设置份数" + tools.kv_get("slice_num"))
        return

    # 开仓
    vt_symbol = engine.open_code
    price = tick.last_price
    volume = engine.slice_open_num
    order_type = OrderType.LIMIT
    order_id = engine.short(vt_symbol=vt_symbol, price=price, volume=volume, order_type=order_type)

    # 如果开仓失败提示
    if order_id == "":
        engine.write_log("开仓失败 未返回 order_id")
        return

    # 开仓成功 存储 order_id 用于撤单和确认成交
    engine.write_log("挂单成功 order_id：" + order_id)
    create = pmodel.CTPOrder.create(
        account=engine.account,
        order_id=order_id,
        name=tick.name,
        code=vt_symbol,
        price=price,
        volume=volume,
        order_type="limit",
        is_complete=0,
        complete_volume=0,
        open_or_close="open",
        buy_or_sell="sell",
        create_date=tools.get_now_date_format()
    )
    engine.write_log(f"CTPOrder order_id {create}")

# 平仓
def slice_close(engine, tick):
    engine.write_log("slice_close()")

    # 是否开启每日平仓
    if tools.kv_get("is_open_slice") != "1":
        engine.write_log("已关闭 每日平仓")
        return

    where = (
        (pmodel.Slice.account == engine.account)
        & (pmodel.Slice.is_close == 0)
    )
    ctp_order_list = pmodel.Slice.select().where(where)
    #engine.write_log(ctp_order_list)
    #engine.write_log(len(ctp_order_list))

    # 遍历持仓
    for v in ctp_order_list:
        #engine.write_log(f"pk_id {v.pk_id} name {v.name} code {v.code} buy_or_sell {v.buy_or_sell} open_price {v.open_price} volume {v.volume}")

        slice_tick = engine.get_tick(v.code)
        engine.write_log(f"slice_tick {slice_tick.name} 价格是 {slice_tick.last_price}")
        #engine.write_log(f"slice_tick {slice_tick.name} 价格是 {slice_tick.last_price}")

        # v.open_price 持仓价格
        # tick.last_price 现在价格

        if v.buy_or_sell == "buy":
            target_price = v.open_price + 2

        if v.buy_or_sell == "sell":
            # 下跌2个点后判定为盈利 执行平空
            if v.open_price - 2 >= slice_tick.last_price:
                engine.write_log("执行平空")

                # 平仓
                vt_symbol = v.code
                price = slice_tick.last_price
                volume = v.volume
                order_type = OrderType.LIMIT
                order_id = engine.cover(vt_symbol=vt_symbol, price=price, volume=volume, order_type=order_type)
                engine.write_log(f"order_id {order_id}")

                # 如果平仓失败提示
                if order_id == "":
                    engine.write_log("平仓失败 未返回")
                    return

                # 平仓成功 存储 order_id 用于撤单和确认成交
                engine.write_log("平仓挂单成功 order_id：" + order_id)
                create = pmodel.CTPOrder.create(
                    account=engine.account,
                    order_id=order_id,
                    name=tick.name,
                    code=vt_symbol,
                    price=price,
                    volume=volume,
                    order_type="limit",
                    is_complete=0,
                    complete_volume=0,
                    open_or_close="close",
                    buy_or_sell="buy",
                    slice_id=v.pk_id,
                    create_date=tools.get_now_date_format()
                )
                engine.write_log(create)

# 获得账户动态权益值
def get_dynamic_balance(engine, account):
    account_info = engine.get_account(vt_accountid=account, use_df=False)
    if account_info == None:
        return False
    return account_info.balance

# 存储账户动态权益
def save_account_client_equity(engine, account):
    balance = get_dynamic_balance(engine, f"CTP.{account}")
    # 如果获取余额失败就退出
    if balance == False:
        engine.write_log(f"获取余额失败: {balance}")
        return
    pmodel.AccountDayClientEquity.create(account=account, client_equity=balance, date=tools.get_now_date_format("%Y-%m-%d"), create_date=tools.get_now_date_format())

# 获取今日是否还有未成交订单
def is_today_order_uncomplete(engine):
    now_date_format = tools.get_now_date_format("%Y-%m-%d")
    where = (
        (pmodel.CTPOrder.account == engine.account)
        & (pmodel.CTPOrder.is_close == 0)
        & (pmodel.CTPOrder.open_or_close == "open")
        & (pmodel.CTPOrder.create_date >= f"{now_date_format} 00:00:00")
        & (pmodel.CTPOrder.create_date <= f"{now_date_format} 23:59:59")
    )
    count = pmodel.CTPOrder.select().where(where).count()
    if count > 0:
        return True
    return False

# 获取开仓数量
def get_account_slice_num(engine):
    where = (
        (pmodel.Slice.account == engine.account)
        & (pmodel.Slice.is_close == 0)
    )
    count = pmodel.Slice.select().where(where).count()
    return count

# 存储当前价格
def save_contract_price(name, code, price):
    pmodel.Price.create(name=name, code=code, price=price, create_date=tools.get_now_date_format())

# 更新挂单状态
def update_order(engine):
    now_date_format = tools.get_now_date_format("%Y-%m-%d")
    where = (
        (pmodel.CTPOrder.account == engine.account)
        & (pmodel.CTPOrder.is_close == 0)
        & (pmodel.CTPOrder.create_date >= f"{now_date_format} 00:00:00")
        & (pmodel.CTPOrder.create_date <= f"{now_date_format} 23:59:59")
    )
    select = pmodel.CTPOrder.select().where(where)
    #engine.write_log(f"更新状态数量 {len(select)}")

    # 循环处理未完成订单的状态
    for v in select:
        order = engine.get_order(vt_orderid=v.order_id, use_df=False)
        engine.write_log(order)
        #engine.write_log(tools.get_jd_charge(order.price))

        # 无返回
        if order == None:
            pmodel.CTPOrder.update(is_close=1, note="状态返回为 None, engine.get_order()").where(pmodel.CTPOrder.pk_id == v.pk_id).execute()
            continue
        # 未成交
        if order.status == Status.NOTTRADED:
            #pmodel.CTPOrder.update(note="未成交").where(pmodel.CTPOrder.pk_id==v.pk_id).execute()
            continue
        # 拒单 or 已撤销
        if (order.status == Status.REJECTED) or (order.status == Status.CANCELLED):
            pmodel.CTPOrder.update(is_close=1, complete_volume=order.traded, note="拒单 or 已撤销").where(pmodel.CTPOrder.pk_id == v.pk_id).execute()
            continue
        # 部分成交
        if order.status == Status.PARTTRADED:
            pmodel.CTPOrder.update(complete_volume=order.traded, note="部分成交").where(pmodel.CTPOrder.pk_id == v.pk_id).execute()
            continue
        # 已全部成交
        if order.status == Status.ALLTRADED:
            pmodel.CTPOrder.update(is_close=1, is_complete=1, complete_volume=order.traded, note="已全部成交").where(pmodel.CTPOrder.pk_id == v.pk_id).execute()

            # 如果是开仓
            if v.open_or_close == "open":
                create = pmodel.Slice.create(
                    account=engine.account,
                    buy_or_sell="sell",
                    name=v.name,
                    code=v.code,
                    volume=v.volume,
                    open_price=order.price,
                    open_charge=tools.get_jd_charge(order.price),
                    open_order_id=v.order_id,
                    create_date=tools.get_now_date_format()
                )
                engine.write_log(f"开仓 slice.pk_id {create.pk_id}")
            # 如果是平仓
            if v.open_or_close == "close":
                pmodel.Slice.update(
                    is_close=1,
                    close_order_id=v.order_id,
                    close_price=order.price,
                    close_charge=tools.get_jd_charge(order.price),
                    close_date=tools.get_now_date_format()
                ).where(pmodel.Slice.pk_id == v.slice_id).execute()
                engine.write_log(f"平仓 slice.pk_id {v.slice_id}")
            continue

# 重新挂单机制 simnow 模拟盘不支持市价单 穿透测试服务器可以
def re_order(engine, tick):
    #engine.write_log('re_order()')

    re_order_limit = int(tools.kv_get("re_order_limit"))

    # 获取数据库超时挂单
    where = (
        (pmodel.CTPOrder.account == engine.account)
        & (pmodel.CTPOrder.is_close == 0)
        & (pmodel.CTPOrder.create_date < tools.get_date_format("%Y-%m-%d %H:%M:%S", tools.get_now_time() - re_order_limit))
    )
    select = pmodel.CTPOrder.select().where(where)
    #engine.write_log(select)
    #engine.write_log(f"超时挂单数量 {len(select)}")

    for v in select:
        #engine.write_log(v.pk_id)

        # 取消这个限价挂单
        cancel = engine.cancel_order(vt_orderid=v.order_id)
        engine.write_log(f"取消挂单:{v.order_id}")

        # 关闭数据库限价挂单
        pmodel.CTPOrder.update(is_close=1, note="超时关闭 re_order").where(pmodel.CTPOrder.pk_id == v.pk_id).execute()

        # 新生成的市价平仓 也要检测一下市价是否盈利 不盈利就不开
        # 是否生成新的市价挂单
        if v.open_or_close == "open":
            pass
        if v.open_or_close == "close":
            slice = pmodel.Slice.select(pmodel.Slice.open_price).where(pmodel.Slice.pk_id == v.slice_id).first()
            if v.buy_or_sell == "buy":
                # 如果是 买平
                if slice.open_price - 2 < tick.ask_price_1:
                    engine.write_log(f"市价买平 无法盈利 不执行重挂 open_price:{slice.open_price} ask_price_1:{tick.ask_price_1}")
                    return
            else:
                # 如果是 卖平
                if slice.open_price + 2 > tick.bid_price_1:
                    engine.write_log(f"市价买平 无法盈利 不执行重挂 open_price:{slice.open_price} bid_price_1:{tick.bid_price_1}")
                    return
            pass

        # 生成新的市价挂单
        vt_symbol = v.code
        price = tick.ask_price_1 if v.buy_or_sell == "buy" else tick.bid_price_1
        volume = v.volume - v.complete_volume
        order_type = OrderType.MARKET
        direction = Direction.LONG if v.buy_or_sell == "buy" else Direction.SHORT
        offset = Offset.OPEN if v.open_or_close == "open" else Offset.CLOSE

        engine.write_log(f"re_order market price {price}")

        order_id = engine.send_order(vt_symbol=vt_symbol, price=price, volume=volume, order_type=order_type, direction=direction, offset=offset)
        engine.write_log("re_order_id")
        engine.write_log(order_id)

        # 如果开仓失败提示
        if order_id == "":
            engine.write_log("开仓失败 re_order 未返回 order_id")
            return

        # 存储挂单记录
        create = pmodel.CTPOrder.create(
            account=v.account,
            order_id=order_id,
            name=v.name,
            code=v.code,
            price=price,
            volume=volume,
            order_type="market",
            is_complete=0,
            complete_volume=0,
            open_or_close=v.open_or_close,
            buy_or_sell=v.buy_or_sell,
            slice_id=v.slice_id,
            create_date=tools.get_now_date_format()
        )
        engine.write_log(create)
    pass