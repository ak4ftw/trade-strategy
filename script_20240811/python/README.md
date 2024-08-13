# 交易策略 分仓每日空
### python 版本  
### pip 镜像设置 
```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
### pip 依赖
```
pip install mysql-connector pymysql peewee
```


### q&a
q:配置文件路径
a:配置文件路径 C:\Users\49021\.vntrader

q:使用方法
a:
    1.打开phpstudy 启动mysql8.0; 
    2.打开VeighNa Station;
    3.勾选交易接口.CTP; 勾选ScriptTrader; 启动
    4.在新页面选择 系统 > 连接CTP, 输入信息, 连接;
    5.功能 > 脚本策略, 新页面点击打开, 选择 run_script_trader.py 文件, 启动;
    6.收盘后点击停止;

q: 修改触发时间
a: 修改数据库vnpy中表 kv.key= target_time 的value值为 14:55:00

q: 修改每次开仓手数
a: 修改数据库vnpy中表 kv.key= open_code 的value值为 jd2409.DCE (合约代码.交易所缩写)

q: 修改分仓最大数量
a: 修改数据库vnpy中表 kv.key= slice_num 的value值为 15

q: 修改是否开启市价重挂机制 (simnow模拟盘不支持市价单需要关闭)
a: 修改数据库vnpy中表kv.key= is_open_re_order 的value值为 1

q: 修改是否开启市价重挂机制
a: 修改数据库vnpy中表kv.key= re_order_limit 的value值为 60 (限价单(a)秒后不成交自动取消该挂单, 上架市价单)

