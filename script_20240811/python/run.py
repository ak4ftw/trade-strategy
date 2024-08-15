from time import sleep
from vnpy_ctp import CtpGateway
from vnpy_scripttrader import ScriptEngine, init_cli_trading


def run():
    ctp_setting = {
        "用户名": "226288",
        "密码": "Tw490216135*",
        "经纪商代码": "9999",
        "交易服务器": "180.168.146.187:10202",
        "行情服务器": "180.168.146.187:10212",
        "产品名称": "simnow_client_test",
        "授权编码": "0000000000000000",
    }

    engine = init_cli_trading([CtpGateway])
    engine.connect_gateway(ctp_setting, "CTP")

    sleep(10)
    vt_symbols = ["jd2409.DCE", "jd2410.DCE"]
    engine.subscribe(vt_symbols=vt_symbols)
    engine.strategy_active = True
    while engine.strategy_active == True:
        tick = engine.get_tick(vt_symbol="jd2409.DCE", use_df=False)
        print(tick)
        sleep(5)
    print("结束运行")

if __name__ == '__main__':
    run()