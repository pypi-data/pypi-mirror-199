import traceback
from inspect import *
from typing import Dict, Optional, List

from rqdatac.services import options, calendar, basic, future, get_price

from vnpy.event import Event, EventEngine
from vnpy.rpc import RpcServer
from vnpy.trader.constant import Interval
from vnpy.trader.database import BaseDatabase, get_database
from vnpy.trader.datafeed import get_datafeed, BaseDatafeed
from vnpy.trader.engine import BaseEngine, MainEngine
from vnpy.trader.event import EVENT_TIMER
from vnpy.trader.object import LogData, HistoryRequest, BarData
from vnpy.trader.utility import load_json, save_json

APP_NAME = "RpcService"

EVENT_RPC_LOG = "eRpcLog"


class RpcEngine(BaseEngine):
    """
    VeighNa的rpc服务引擎。
    """
    setting_filename: str = "rpc_service_setting.json"

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        """构造函数"""
        super().__init__(main_engine, event_engine, APP_NAME)

        self.rep_address: str = "tcp://*:2014"
        self.pub_address: str = "tcp://*:4102"

        self.server: Optional[RpcServer] = None

        self.datafeed: BaseDatafeed = get_datafeed()
        self.database: BaseDatabase = get_database()
        self.init_server()
        self.load_setting()
        self.register_event()

    def init_server(self) -> None:
        """初始化服务器"""
        self.server = RpcServer()
        # self.rqsdk_rpc = RqsdkRpcEngine()
        # RqsdkRpcEngine
        # 这里是是vnpy默认的常规查询
        self.server.register(self.main_engine.subscribe)
        self.server.register(self.main_engine.send_order)
        self.server.register(self.main_engine.cancel_order)
        self.server.register(self.main_engine.query_history)

        self.server.register(self.main_engine.get_tick)
        self.server.register(self.main_engine.get_order)
        self.server.register(self.main_engine.get_trade)
        self.server.register(self.main_engine.get_position)
        self.server.register(self.main_engine.get_account)
        self.server.register(self.main_engine.get_contract)
        self.server.register(self.main_engine.get_all_ticks)
        self.server.register(self.main_engine.get_all_orders)
        self.server.register(self.main_engine.get_all_trades)
        self.server.register(self.main_engine.get_all_positions)
        self.server.register(self.main_engine.get_all_accounts)
        self.server.register(self.main_engine.get_all_contracts)
        self.server.register(self.main_engine.get_all_active_orders)
        # 米筐默认的接口
        # 注解get_price
        for a in dir(get_price):
            if a and callable(get_price.__dict__[a]) and '@export_as_api' in getsource(get_price.__dict__[a]):
                print(f'注册了回调接口get_price  {get_price.__dict__[a]}')
                self.server.register(get_price.__dict__[a])
        # 期货的接口
        for a in dir(future):
            if a and callable(future.__dict__[a]) and '@export_as_api' in getsource(future.__dict__[a]):
                print(f'注册了回调接口future {future.__dict__[a]}')
                self.server.register(future.__dict__[a])
        # 期权接口
        for a in dir(options):
            if a and callable(options.__dict__[a]) and '@export_as_api' in getsource(options.__dict__[a]):
                print(f'注册了回调接口options {options.__dict__[a]}')
                self.server.register(options.__dict__[a])
        # 日历
        for a in dir(calendar):
            if a and callable(calendar.__dict__[a]) and '@export_as_api' in getsource(calendar.__dict__[a]):
                print(f'注册了回调接口calendar {calendar.__dict__[a]}')
                self.server.register(calendar.__dict__[a])
        # 基础的
        for a in dir(basic):
            if a and callable(basic.__dict__[a]) and '@export_as_api' in getsource(basic.__dict__[a]):
                print(f'注册了回调接口basic  {basic.__dict__[a]}')
                self.server.register(basic.__dict__[a])

        # for a in dir(api_base):
        #     try:
        #         if a and callable(api_base.__dict__[a]) and '@export_as_api' in getsource(api_base.__dict__[a]):
        #             print(f'注册了回调接口4  {api_base.__dict__[a]}')
        #             self.server.register(api_base.__dict__[a])
        #     except Exception:
        #         pass
        # self.server.register(api_base.history_bars)
        # leo vnpy rqdataDatafeed 的查询接口，比如
        # self.server.register(self.datafeed.query_bar_history)
        self.server.register(self.datafeed.query_tick_history)
        self.server.register(self.query_bar_history)
        self.server.register(self.get_contracts_option)

    def get_contracts_option(self, underlying, option_type=None, maturity=None, strike=None, trading_date=None) -> List:
        return self.datafeed.rq_options_method("get_contracts", (underlying, option_type, maturity, strike, trading_date))

    def query_bar_history(self, req: HistoryRequest) -> List[BarData]:
        data: List[BarData] = self.datafeed.query_bar_history(req)
        if req.interval == Interval.TICK:
            self.database.save_tick_data(data)
        else:
            self.database.save_bar_data(data)
        return data

    # def query_rqsdk(self, req: RqSdkRequest, gateway_name: str) -> None:
    #     print("客户端发起请求, 服务端现在查找米筐!!!")
    #     dd = self.datafeed.rq_options_method(req.method, req.param)
    #
    #     # dd = self.datafeed.get_contract_property()(
    #     #     ['10002752'], start_date='20210115', end_date='20210118')
    #     print(dd)
    #     event: Event = Event("RQSDKCallBack", dd)
    #     #  server上需要处理event线程？
    #     self.event_engine.put(event)
    #     return dd

    def load_setting(self) -> None:
        """读取配置文件"""
        setting: Dict[str, str] = load_json(self.setting_filename)
        self.rep_address = setting.get("rep_address", self.rep_address)
        self.pub_address = setting.get("pub_address", self.pub_address)

    def save_setting(self) -> None:
        """保存配置文件"""
        setting: Dict[str, str] = {
            "rep_address": self.rep_address,
            "pub_address": self.pub_address
        }
        save_json(self.setting_filename, setting)

    def start(self, rep_address: str, pub_address: str) -> bool:
        """启动rpc服务"""
        if self.server.is_active():
            self.write_log("RPC服务运行中")
            return False

        self.rep_address = rep_address
        self.pub_address = pub_address

        try:
            self.server.start(rep_address, pub_address)
        except:  # noqa
            msg: str = traceback.format_exc()
            self.write_log(f"RPC服务启动失败：{msg}")
            return False

        self.save_setting()
        self.write_log("RPC服务启动成功")
        return True

    def stop(self) -> bool:
        """停止rpc服务"""
        if not self.server.is_active():
            self.write_log("RPC服务未启动")
            return False

        self.server.stop()
        self.server.join()
        self.write_log("RPC服务已停止")
        return True

    def close(self) -> None:
        """关闭rpc服务"""
        self.stop()

    def register_event(self) -> None:
        """注册事件"""
        self.event_engine.register_general(self.process_event)

    def process_event(self, event: Event) -> None:
        """调用事件"""
        if self.server.is_active():
            if event.type == EVENT_TIMER:
                return
            self.server.publish("", event)

    def write_log(self, msg: str) -> None:
        """输出日志"""
        log: LogData = LogData(msg=msg, gateway_name=APP_NAME)
        event: Event = Event(EVENT_RPC_LOG, log)
        self.event_engine.put(event)
