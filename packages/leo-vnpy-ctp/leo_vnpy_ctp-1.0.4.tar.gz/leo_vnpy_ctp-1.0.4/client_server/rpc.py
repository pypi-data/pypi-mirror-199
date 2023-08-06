from pathlib import Path
from typing import Dict, List

from pandas import DataFrame

from client_server import APP_rqsdk, APP_backtester
from client_server.rqsdk_engine import RqsdkRpcEngine
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy_rpcservice import RpcGateway
from vnpy_rq_ctabacktester import RqBacktesterEngine


class RpcCli(object):
    """
    提供RPC的脚手架,默认直接连接,但不初始化回测框架
    """

    def __init__(self) -> None:
        event_engine = EventEngine()
        self.main_engine = MainEngine(event_engine)
        self.main_engine.add_engine(RqsdkRpcEngine)
        self.main_engine.add_gateway(RpcGateway)
        default_setting: Dict[str, str] = {
            "主动请求地址": "tcp://139.198.114.163:22014",
            "推送订阅地址": "tcp://139.198.114.163:24102"
        }
        self.main_engine.connect(default_setting, "RPC")
        self.rpc: RqsdkRpcEngine = self.main_engine.get_engine(APP_rqsdk)

    """
    初始化回测框架,才支持调用数据, 回测等
        filter: dict = {
            "ma_param": self.maSeting,
            "datetime": {
                "$gte": datetime.strptime(self.start_date, "%Y%m%d").astimezone(DB_TZ),
                "$lte": datetime.strptime(self.end_date, "%Y%m%d").astimezone(DB_TZ),
            }
        }
    """

    def init_backtester(self):
        from vnpy_rq_ctabacktester import CtaRqBacktesterApp
        self.main_engine.add_app(CtaRqBacktesterApp)
        self.backtester: RqBacktesterEngine = self.main_engine.get_engine(APP_backtester)

    """
    通用的加载本地数据方法 aggregate 是否聚合查询
    """

    def load_local_data(self, table_name: str = "", filter: Dict[str, object] = {},
                        aggregate: bool = False) -> DataFrame:
        if not self.backtester:
            print('还未初始化回测框架')
            return
        if aggregate:
            return self.backtester.database.load_aggregate_data(table_name, filter)
        else:
            return self.backtester.database.load_common_data(table_name, filter)

    """
    根据filter, 下载或者更新
     option_daily = []
     for d in list(self.option_symbol_dates.keys()):
        option_daily.append({
            "filter": {
                'name': '单腿卖期权',
                'datetime': datetime(d.year, d.month, d.day),
            },
            "data": {
                **self.option_symbol_dates[d],
                'datetime': datetime(d.year, d.month, d.day),
                'name': '单腿卖期权',
            }
        })

    """

    def download_data(self, table_name: str = "", filter: Dict[str, object] = {}, data: List = []) -> DataFrame:
        if not self.backtester:
            print('还未初始化回测框架')
            return
        save_data = []
        for d in data:
            save_data.append({
                "filter": filter,
                "data": d
            })
        return self.backtester.database.save_common_data(table_name, save_data)

    """
    """
    def start_backtesting(self, strategy: str = "OptionTradingStrategy", path: Path = None, start_date='', end_date='') -> DataFrame:
        self.backtester.init_engine()

        # path2: Path = Path.cwd().joinpath("strategies")
        # 加载自身
        self.backtester.load_strategy_class_from_folder(path, "strategies")

        # 是不是可以做个回调，就从策略算好手续费，跳，金额等，主要是因为合约是不确定的
        result: bool = self.backtester.start_backtesting(
            strategy,
            # vt_symbol,
            interval="1d",
            start=start_date,
            end=end_date,
            rate=0.1,
            slippage=0.1,
            size=10,
            pricetick=0.1,
            capital=1000000,
            setting={
                start_date: start_date, end_date: end_date
            },
            in_thread=False
        )

        print(f'end test ... {result}')
