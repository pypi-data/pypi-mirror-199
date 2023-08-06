import importlib
import traceback
from ast import List
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from glob import glob
from inspect import getfile
from pathlib import Path
from threading import Thread
from types import ModuleType
from typing import Optional, Dict, Type, Set

from pandas import DataFrame

import vnpy_rq_ctabacktester
from client_server.base_define import APP_rqsdk, APP_backtester
from client_server.object import BuildVtSymbols
from client_server.rqsdk_engine import RqsdkRpcEngine
from vnpy.event import Event, EventEngine
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.converter import OffsetConverter
from vnpy.trader.database import BaseDatabase, get_database, DB_TZ
from vnpy.trader.engine import BaseEngine, MainEngine
from vnpy.trader.object import HistoryRequest, TickData, ContractData, BarData
from vnpy.trader.utility import extract_vt_symbol
from vnpy_rq_ctabacktester.rq_template import RqStrategyTemplate
from .backtesting import (
    BacktestingEngine,
    OptimizationSetting,
)

# from vnpy_ctastrategy.backtesting import (
#     BacktestingEngine,
#     OptimizationSetting,
#     BacktestingMode
# )

EVENT_BACKTESTER_LOG = "eBacktesterLog"
EVENT_BACKTESTER_BACKTESTING_FINISHED = "eBacktesterBacktestingFinished"
EVENT_BACKTESTER_OPTIMIZATION_FINISHED = "eBacktesterOptimizationFinished"


class RqBacktesterEngine(BaseEngine):
    """
    For running CTA strategy backtesting.
    """

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        """"""
        super().__init__(main_engine, event_engine, APP_backtester)

        self.strategy_data: Dict[str, Dict] = {}

        self.classes: Dict[str, Type[RqStrategyTemplate]] = {}
        self.strategies: Dict[str, RqStrategyTemplate] = {}

        self.symbol_strategy_map: Dict[str, List[RqStrategyTemplate]] = defaultdict(list)
        self.orderid_strategy_map: Dict[str, RqStrategyTemplate] = {}

        self.init_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)

        self.vt_tradeids: Set[str] = set()

        self.offset_converter: OffsetConverter = OffsetConverter(self.main_engine)

        self.database: BaseDatabase = get_database()

        # leo
        self.rpc_engine: RqsdkRpcEngine = self.main_engine.get_engine(APP_rqsdk)
        # dd = self.rpc_engine.get_contract_property(order_book_ids=['10002752'], start_date=self.start_date,
        #                                            end_date='20210118')
        # print(dd)

        self.classes: dict = {}
        self.backtesting_engine: BacktestingEngine = None
        self.thread: Thread = None

        # self.datafeed: BaseDatafeed = get_datafeed()
        self.database: BaseDatabase = get_database()

        # Backtesting reuslt
        self.result_df: DataFrame = None
        self.result_statistics: dict = None

        # Optimization result
        self.result_values: list = None

    def init_engine(self) -> None:
        """"""
        self.write_log("初始化米筐的CTA回测引擎")

        self.backtesting_engine = BacktestingEngine(self.main_engine, self.event_engine)
        # Redirect log from backtesting engine outside.
        self.backtesting_engine.output = self.write_log

        self.load_strategy_class()
        # self.load_strategy_setting()
        # self.load_strategy_data()
        # self.register_event()
        self.write_log("策略文件加载完成, 数据源通过rpc进行初始化")

        # self.init_datafeed()

    # def register_event(self) -> None:
    #     """"""
    #     self.event_engine.register(EVENT_TICK, self.process_tick_event)
    #     self.event_engine.register(EVENT_ORDER, self.process_order_event)
    #     self.event_engine.register(EVENT_TRADE, self.process_trade_event)
    #     self.event_engine.register(EVENT_POSITION, self.process_position_event)
    #
    # def init_datafeed(self) -> None:
    #     """
    #     Init datafeed client.
    #     """
    #     result: bool = self.datafeed.init()
    #     if result:
    #         self.write_log("数据服务初始化成功")

    def write_log(self, msg: str, logout=False) -> None:
        """"""
        if logout:
            print(f'日志：' + msg)
        event: Event = Event(EVENT_BACKTESTER_LOG)
        event.data = msg
        self.event_engine.put(event)

    def load_strategy_class(self) -> None:
        """
        Load strategy class from source code.
        """
        app_path: Path = Path(vnpy_rq_ctabacktester.__file__).parent
        path1: Path = app_path.joinpath("strategies")
        self.load_strategy_class_from_folder(path1, "vnpy_rq_ctabacktester.strategies")

        # 自带window路径下
        path2: Path = Path.cwd().joinpath("strategies")
        self.load_strategy_class_from_folder(path2, "strategies")

    def load_strategy_class_from_folder(self, path: Path, module_name: str = "") -> None:
        """
        Load strategy class from certain folder.
        """
        # print(f"load_strategy_class_from_folder  {path}  {module_name}")
        for suffix in ["py", "pyd", "so"]:
            pathname: str = str(path.joinpath(f"*.{suffix}"))
            for filepath in glob(pathname):
                filename: str = Path(filepath).stem
                name: str = f"{module_name}.{filename}"
                self.load_strategy_class_from_module(name)

    def load_strategy_class_from_module(self, module_name: str) -> None:
        """
        Load strategy class from module file.
        """
        try:
            module: ModuleType = importlib.import_module(module_name)
            # 重载模块，确保如果策略文件中有任何修改，能够立即生效。
            importlib.reload(module)
            for name in dir(module):
                value = getattr(module, name)
                if (isinstance(value, type) and issubclass(value,
                                                           RqStrategyTemplate) and value is not RqStrategyTemplate):
                    self.classes[value.__name__] = value
        except:  # noqa
            msg: str = f"策略文件{module_name}加载失败，触发异常：\n{traceback.format_exc()}"
            self.write_log(msg)

        # try:
        #     module: ModuleType = importlib.import_module(module_name)
        #
        #     # 重载模块，确保如果策略文件中有任何修改，能够立即生效。
        #     importlib.reload(module)
        #
        #     for name in dir(module):
        #         value = getattr(module, name)
        #         if (isinstance(value, type) and issubclass(value, CtaTemplate) and value is not CtaTemplate):
        #             self.classes[value.__name__] = value
        # except:  # noqa
        #     msg: str = f"策略文件{module_name}加载失败，触发异常：\n{traceback.format_exc()}"
        #     self.write_log(msg)

    def reload_strategy_class(self) -> None:
        """"""
        self.classes.clear()
        self.load_strategy_class()
        self.write_log("策略文件重载刷新完成")

    def get_strategy_class_names(self) -> list:
        """"""
        return list(self.classes.keys())

    # 组合策略得合约指定在策略代码中指定
    def start_backtesting(
            self,
            class_name: str,
            interval: str,
            start: datetime,
            end: datetime,
            rate: float,
            slippage: float,
            size: int,
            pricetick: float,
            capital: int,
            setting: dict,
            in_thread: bool = True
    ) -> bool:
        if not in_thread:
            # 先粗暴这么写吧
            self.run_backtesting(class_name=class_name, interval=interval, start=start, end=end, rate=rate,
                                 slippage=slippage, size=size, pricetick=pricetick, capital=capital, setting=setting)
        else:
            if self.thread:
                self.write_log("已有任务在运行中，请等待完成")
                return False

            self.write_log("-" * 40)
            self.thread = Thread(
                target=self.run_backtesting,
                args=(
                    class_name,
                    # vt_symbols,
                    interval,
                    start,
                    end,
                    rate,
                    slippage,
                    size,
                    pricetick,
                    capital,
                    setting
                )
            )
            self.thread.start()

        return True

    # 关键回测点, 线程中
    def run_backtesting(
            self,
            class_name: str,
            # vt_symbols: List[str],
            interval: str,
            start: datetime,
            end: datetime,
            rate: float,
            slippage: float,
            size: int,
            pricetick: float,
            capital: int,
            setting: dict
    ) -> None:
        """"""
        self.result_df = None
        self.result_statistics = None
        engine: BacktestingEngine = self.backtesting_engine
        engine.clear_data()

        try:
            strategy_class: type = self.classes[class_name]
            engine.add_strategy(
                strategy_class,
                setting
            )
            build_symbols: BuildVtSymbols = engine.build_strategy_symbols()
            # TODO 先加载策略，让策略先算好合约，去获取策略数据
            engine.set_parameters(**build_symbols.__dict__)
            # self.write_log('--- 尝试自动检查数据完整性 --- ')
            # engine.check_data(True)
            self.write_log('--- 检查更新完毕 --- ', logout=True)
            engine.load_data()
            self.write_log('历史数据加载完毕', logout=True)

            engine.run_backtesting()
        except Exception:
            msg: str = f"策略回测失败，触发异常：\n{traceback.format_exc()}"
            print(msg)
            self.write_log(msg)

            self.thread = None
            return

        self.result_df = engine.calculate_result()
        self.result_statistics = engine.calculate_statistics(output=False)

        # Clear thread object handler.
        self.thread = None

        # Put backtesting done event
        # 发送回测策略完成的事件
        event: Event = Event(EVENT_BACKTESTER_BACKTESTING_FINISHED)
        self.event_engine.put(event)

    def get_result_df(self) -> DataFrame:
        """"""
        return self.result_df

    def get_result_statistics(self) -> dict:
        """"""
        return self.result_statistics

    def get_result_values(self) -> list:
        """"""
        return self.result_values

    def get_default_setting(self, class_name: str) -> dict:
        """"""
        strategy_class: type = self.classes[class_name]
        return strategy_class.get_class_parameters()

    def run_optimization(
            self,
            class_name: str,
            vt_symbol: str,
            interval: str,
            start: datetime,
            end: datetime,
            rate: float,
            slippage: float,
            size: int,
            pricetick: float,
            capital: int,
            optimization_setting: OptimizationSetting,
            use_ga: bool
    ) -> None:
        """"""
        self.result_values = None

        engine: BacktestingEngine = self.backtesting_engine
        engine.clear_data()

        engine.set_parameters(
            vt_symbols=["AU2304.SHFE", "AG2303.SHFE"],
            interval=Interval.MINUTE,
            start=start,
            end=end,
            rates={
                "AU2304.SHFE": 0 / 10000,
                "AG2303.SHFE": 0 / 10000
            },
            slippages={
                "AU2304.SHFE": 0,
                "AG2303.SHFE": 0
            },
            sizes={
                "AU2304.SHFE": 10,
                "AG2303.SHFE": 10
            },
            priceticks={
                "AU2304.SHFE": 1,
                "AG2303.SHFE": 1
            },
            capital=1_000_000,
        )

        strategy_class: type = self.classes[class_name]
        engine.add_strategy(
            strategy_class,
            {}
        )

        if use_ga:
            self.result_values = engine.run_ga_optimization(
                optimization_setting,
                output=False
            )
        else:
            self.result_values = engine.run_bf_optimization(
                optimization_setting,
                output=False
            )

        # Clear thread object handler.
        self.thread = None
        self.write_log("多进程参数优化完成")

        # Put optimization done event
        event: Event = Event(EVENT_BACKTESTER_OPTIMIZATION_FINISHED)
        self.event_engine.put(event)

    def start_optimization(
            self,
            class_name: str,
            vt_symbol: str,
            interval: str,
            start: datetime,
            end: datetime,
            rate: float,
            slippage: float,
            size: int,
            pricetick: float,
            capital: int,
            optimization_setting: OptimizationSetting,
            use_ga: bool
    ) -> bool:
        if self.thread:
            self.write_log("已有任务在运行中，请等待完成")
            return False

        self.write_log("-" * 40)
        self.thread = Thread(
            target=self.run_optimization,
            args=(
                class_name,
                vt_symbol,
                interval,
                start,
                end,
                rate,
                slippage,
                size,
                pricetick,
                capital,
                optimization_setting,
                use_ga
            )
        )
        self.thread.start()

        return True

    # def download_basic(
    #         self,
    #         dates
    # ) -> None:
    #     for d in dates:
    #         # 每天的保证金占有率 每一跳可能不同
    #         try:
    #             df = ak.futures_rule(date=d.strftime("%Y%m%d"))
    #             bars = []
    #             for row in df.itertuples():
    #                 b: FutureRuleData = FutureRuleData()
    #                 b.datetime = datetime.strptime(str(d), '%Y-%m-%d')
    #                 b.exchange = row[1]
    #                 b.underlying_symbol_name = row[2]
    #                 b.underlying_symbol = row[3]
    #                 b.margin_rate = row[4]
    #                 b.range = row[5]
    #                 b.contract_multiplier = row[6]
    #                 b.price_tick = row[7]
    #                 b.limit_volume = row[8]
    #                 b.remark = row[9]
    #
    #                 bars.append(b)
    #             # a = futures_rule_df.loc[
    #             #     futures_rule_df['代码'] == ins.underlying_symbol, ['交易保证金比例', '合约乘数', '最小变动价位']]
    #             # self.symbol_dict[symbol][d] = {}
    #             # self.symbol_dict[symbol][d]['margin_rate_daily'] = float(a['交易保证金比例'][0]) / 100
    #             # self.symbol_dict[symbol][d]['price_tick'] = a['最小变动价位'][0]
    #             self.database.save_basic(bars)
    #         except:
    #             print(traceback.format_exc())

    # for d in dates:
    #     try:
    #         self.database.save_basic(data)
    #
    #     except Exception:
    #         msg: str = f"数据下载失败，触发异常：\n{traceback.format_exc()}"
    #         self.write_log(msg)
    #
    # # Clear thread object handler.
    # self.thread = None

    def download_bar_history(
            self,
            vt_symbol: str,
            interval: str,
            start: datetime,
            end: datetime,
            saveLocal: bool = False
    ) -> None:
        """
                执行下载任务
                """
        self.write_log(f"{vt_symbol}-{interval}开始下载历史数据")

        try:
            symbol, exchange = extract_vt_symbol(vt_symbol)
        except ValueError:
            self.write_log(f"{vt_symbol}解析失败，请检查交易所后缀")
            self.thread = None
            return

        req: HistoryRequest = HistoryRequest(
            symbol=symbol,
            exchange=exchange,
            interval=Interval(interval),
            start=start,
            end=end
        )

        try:
            if interval == "tick":
                dd = self.rpc_engine.query_tick_history(req)
                print(dd)
                # data: List[TickData] = self.datafeed.query_tick_history(req)
                data: List[TickData] = self.rpc_engine.query_tick_history(req)
                for d in data:
                    d.exchange = Exchange(d.exchange)
            else:
                data: List[BarData] = self.rpc_engine.query_bar_history(req)
                for d in data:
                    d.exchange = Exchange(d.exchange)
                    d.interval = Interval(d.interval)
                    # 怀疑是这里的时间问题
                    d.datetime = d.datetime.replace(tzinfo=DB_TZ)

                # contract: Optional[ContractData] = self.main_engine.get_contract(vt_symbol)
                #
                # # If history data provided in gateway, then query
                # if contract and contract.history_data:
                #     data: List[BarData] = self.main_engine.query_history(
                #         req, contract.gateway_name
                #     )
                # # Otherwise use RQData to query data
                # else:
                #     # data: List[BarData] = self.datafeed.query_bar_history(req)
                #     #
                #     data: List[BarData] = self.rpc_engine.query_bar_history(req)

            if data:
                self.write_log(f'远程数据下载完成等待从库同步完成', logout=True)
                pass

            if saveLocal:
                if interval == "tick":
                    self.database.save_tick_data(data)
                else:
                    self.database.save_bar_data(data)

                self.write_log(f"{vt_symbol}-{interval}历史数据下载完成")
            else:
                self.write_log(f"数据下载失败，无法获取{vt_symbol}的历史数据")

        except Exception:
            msg: str = f"数据下载失败，触发异常：\n{traceback.format_exc()}"
            self.write_log(msg, True)

        # Clear thread object handler.
        self.thread = None

    def run_downloading(
            self,
            vt_symbol: str,
            interval: str,
            start: datetime,
            end: datetime
    ) -> None:
        """
        执行下载任务
        """
        self.write_log(f"{vt_symbol}-{interval}开始下载历史数据")

        try:
            symbol, exchange = extract_vt_symbol(vt_symbol)
        except ValueError:
            self.write_log(f"{vt_symbol}解析失败，请检查交易所后缀")
            self.thread = None
            return

        req: HistoryRequest = HistoryRequest(
            symbol=symbol,
            exchange=exchange,
            interval=Interval(interval),
            start=start,
            end=end
        )

        try:
            if interval == "tick":
                dd = self.rpc_engine.query_tick_history(req)
                print(dd)
                # data: List[TickData] = self.datafeed.query_tick_history(req)
                data: List[TickData] = self.rpc_engine.query_tick_history(req)
            else:
                contract: Optional[ContractData] = self.main_engine.get_contract(vt_symbol)

                # If history data provided in gateway, then query
                if contract and contract.history_data:
                    data: List[BarData] = self.main_engine.query_history(
                        req, contract.gateway_name
                    )
                # Otherwise use RQData to query data
                else:
                    # data: List[BarData] = self.datafeed.query_bar_history(req)
                    #
                    data: List[BarData] = self.rpc_engine.query_bar_history(req)

            if data:
                if interval == "tick":
                    self.database.save_tick_data(data)
                else:
                    # TODO 这里可能要改成服务端下载
                    self.database.save_bar_data(data)

                self.write_log(f"{vt_symbol}-{interval}历史数据下载完成")
            else:
                self.write_log(f"数据下载失败，无法获取{vt_symbol}的历史数据")
        except Exception:
            msg: str = f"数据下载失败，触发异常：\n{traceback.format_exc()}"
            self.write_log(msg)

        # Clear thread object handler.
        self.thread = None

    def start_downloading(
            self,
            vt_symbol: str,
            interval: str,
            start: datetime,
            end: datetime
    ) -> bool:
        if self.thread:
            self.write_log("已有任务在运行中，请等待完成")
            return False

        self.write_log("-" * 40)
        self.thread = Thread(
            target=self.run_downloading,
            args=(
                vt_symbol,
                interval,
                start,
                end
            )
        )
        self.thread.start()

        return True

    def get_all_trades(self) -> list:
        """"""
        return self.backtesting_engine.get_all_trades()

    def get_all_orders(self) -> list:
        """"""
        return self.backtesting_engine.get_all_orders()

    def get_all_daily_results(self) -> list:
        """"""
        return self.backtesting_engine.get_all_daily_results()

    def get_history_data(self) -> list:
        """"""
        return self.backtesting_engine.history_data

    def get_strategy_class_file(self, class_name: str) -> str:
        """"""
        strategy_class: type = self.classes[class_name]
        file_path: str = getfile(strategy_class)
        return file_path
