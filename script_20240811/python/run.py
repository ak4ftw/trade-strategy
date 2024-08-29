from time import sleep
from vnpy_ctp import CtpGateway
from vnpy_scripttrader import init_cli_trading
from run_script_trader import run

# 运行 可通过控制台运行
def go():
    ctp_setting = {
        "用户名": "",
        "密码": "",
        "经纪商代码": "9999",
        "交易服务器": "180.168.146.187:10202",
        "行情服务器": "180.168.146.187:10212",
        "产品名称": "simnow_client_test",
        "授权编码": "0000000000000000",
    }

    engine = init_cli_trading([CtpGateway])
    engine.connect_gateway(ctp_setting, "CTP")

    sleep(20)
    engine.strategy_active = True
    run(engine)


    engine.write_log("-----------------------------------------------------------")
    engine.write_log("-----------------------------------------------------------")
    engine.write_log("------------------------- 结束运行 -------------------------")
    engine.write_log("-----------------------------------------------------------")
    engine.write_log("-----------------------------------------------------------")

if __name__ == '__main__':
    go()