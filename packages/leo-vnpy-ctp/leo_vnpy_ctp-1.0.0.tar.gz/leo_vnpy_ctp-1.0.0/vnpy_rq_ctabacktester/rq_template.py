""""""
from abc import ABC
from collections import defaultdict
from copy import copy
from datetime import datetime
from typing import Dict, Set, List, Optional, Any

import numpy as np
import pandas as pd
from openpyxl.utils import get_column_letter
from pandas import DataFrame, ExcelWriter

from client_server.base_define import APP_backtester, APP_rqsdk
from client_server.object import BuildVtSymbols
from client_server.rqsdk_engine import RqsdkRpcEngine
from vnpy.trader.constant import Interval, Direction, Offset
from vnpy.trader.object import BarData, TickData, OrderData, TradeData
from vnpy.trader.utility import virtual

class RqStrategyTemplate(ABC):
    """"""

    author: str = ""
    parameters: list = []
    variables: list = []

    def __init__(
            self,
            # 实际上是backtester
            strategy_engine: Any,
            strategy_name: str,
            setting: dict,
    ) -> None:
        """"""
        self.dates = None
        self.instruments = None
        self.symbol_dict = {}
        self.strategy_engine: Any = strategy_engine
        self.strategy_name: str = strategy_name
        self.vt_symbols: List[str] = []

        self.inited: bool = False
        self.trading: bool = False
        self.pos: Dict[str, int] = defaultdict(int)

        self.orders: Dict[str, OrderData] = {}
        self.active_orderids: Set[str] = set()

        self.rpc_engine: RqsdkRpcEngine = self.strategy_engine.main_engine.get_engine(APP_rqsdk)
        self.backtester_engine = self.strategy_engine.main_engine.get_engine(APP_backtester)

        # Copy a new variables list here to avoid duplicate insert when multiple
        # strategy instances are created with the same strategy class.
        self.variables: list = copy(self.variables)
        self.variables.insert(0, "inited")
        self.variables.insert(1, "trading")
        self.variables.insert(2, "pos")

        self.update_setting(setting)

    # def download_future_rules(self, dates: List[datetime]):
    #     backtester_engine: BaseEngine = self.strategy_engine.main_engine.get_engine("RqCtaBacktester")
    #     return backtester_engine.download_future_rules(dates)

    # def rpc(self):
    #     rpc_engine: RqsdkRpcEngine = self.strategy_engine.main_engine.get_engine(APP_rqsdk)
    #     return rpc_engine
    #
    # def backtester(self):
    #     backtester_engine = self.strategy_engine.main_engine.get_engine(APP_backtester)
    #     return backtester_engine

    def to_excel_auto_column_weight(self, df: pd.DataFrame, writer: ExcelWriter, sheet_name="Shee1"):
        """DataFrame保存为excel并自动设置列宽"""
        # 数据 to 写入器，并指定sheet名称
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        #  计算每列表头的字符宽度
        column_widths = (
            df.columns.to_series().apply(lambda x: len(str(x).encode('gbk'))).values
        )
        #  计算每列的最大字符宽度
        max_widths = (
            df.astype(str).applymap(lambda x: len(str(x).encode('gbk'))).agg(max).values
        )
        # 取前两者中每列的最大宽度
        widths = np.max([column_widths, max_widths], axis=0)
        # 指定sheet，设置该sheet的每列列宽
        worksheet = writer.sheets[sheet_name]
        for i, width in enumerate(widths, 1):
            # openpyxl引擎设置字符宽度时会缩水0.5左右个字符，所以干脆+2使左右都空出一个字宽。
            worksheet.column_dimensions[get_column_letter(i)].width = width + 5


    def export_daily_results(self, writer: ExcelWriter = None, filename = None, df: DataFrame  = None, save=False):
        if not writer:
            writer = pd.ExcelWriter(filename)
        self.to_excel_auto_column_weight(df, writer, '每日盈亏计算')
        if save:
            writer.save()
        return writer

    def export_trades(self, writer: ExcelWriter = None, filename='', save=False):
        trades = self.backtester_engine.get_all_trades()

        dd = []
        for t in trades:
            s = t.__dict__
            s['exchange'] = t.exchange.value
            s['direction'] = t.direction.value
            s['offset'] = t.offset.value
            # 去掉时区方便导出
            s['datetime'] = s['datetime'].replace(tzinfo=None)
            dd.append(s)

        # , mode='a', if_sheet_exists='replace'
        if not writer:
            writer = pd.ExcelWriter(filename)
        trades_pd = pd.DataFrame(dd)
        self.to_excel_auto_column_weight(trades_pd, writer, '交易')
        # trades_pd.to_excel(writer, sheet_name='交易')
        if save:
            writer.save()
        return writer

    def export_orders(self, writer: ExcelWriter = None, filename = None, save=False):
        dd = []
        orders = self.backtester_engine.get_all_orders()
        dd.clear()
        for t in orders:
            s = t.__dict__
            s['exchange'] = t.exchange.value
            s['direction'] = t.direction.value
            s['offset'] = t.offset.value
            s['type'] = t.type.value
            s['status'] = t.status.value
            # 去掉时区方便导出
            s['datetime'] = s['datetime'].replace(tzinfo=None)
            dd.append(s)
        if not writer:
            writer = pd.ExcelWriter(filename)
        orders_pd = pd.DataFrame(dd)
        self.to_excel_auto_column_weight(orders_pd, writer, '委托')
        # orders_pd.to_excel(writer, sheet_name='委托')
        # writer1.save()
        if save:
            writer.save()
        return writer

    # 自定义，获取合约合集的的时候，自动把这些合约信息对应从开始到结束时间的手续费，保证金占比信息填充完毕
    def get_instruments(self, symbols: List[str], dates: List[datetime]):
        self.dates = dates
        instruments, self.vt_symbols = self.strategy_engine.calc_symbol_dict(symbols, dates)
        return instruments

    # def update_symbols(self, vt_symbols: List[str], dates: List[datetime]):
    #     self.vt_symbols: List[str] = vt_symbols
    #     self.strategy_engine.update_symbols(self.vt_symbols, dates)

    def update_setting(self, setting: dict) -> None:
        """
        Update strategy parameter wtih value in setting dict.
        """
        for name in self.parameters:
            if name in setting:
                setattr(self, name, setting[name])

    @classmethod
    def get_class_parameters(cls) -> Dict:
        """
        Get default parameters dict of strategy class.
        """
        class_parameters: dict = {}
        for name in cls.parameters:
            class_parameters[name] = getattr(cls, name)
        return class_parameters

    def get_parameters(self) -> Dict:
        """
        Get strategy parameters dict.
        """
        strategy_parameters: dict = {}
        for name in self.parameters:
            strategy_parameters[name] = getattr(self, name)
        return strategy_parameters

    def get_variables(self) -> Dict:
        """
        Get strategy variables dict.
        """
        strategy_variables: dict = {}
        for name in self.variables:
            strategy_variables[name] = getattr(self, name)
        return strategy_variables

    def get_data(self) -> Dict:
        """
        Get strategy data.
        """
        strategy_data: dict = {
            "strategy_name": self.strategy_name,
            "vt_symbols": self.vt_symbols,
            "class_name": self.__class__.__name__,
            "author": self.author,
            "parameters": self.get_parameters(),
            "variables": self.get_variables(),
        }
        return strategy_data

    @virtual
    def on_build(self) -> BuildVtSymbols:
        """
        Callback build symbols.
        """
        pass

    @virtual
    def on_init(self) -> None:
        """
        Callback when strategy is inited.
        """
        pass

    @virtual
    def on_start(self) -> None:
        """
        Callback when strategy is started.
        """
        pass

    @virtual
    def after_trade(self, dt: datetime) -> None:
        """
        开盘后
        """
        pass

    @virtual
    def before_trade(self, dt: datetime) -> None:
        """
        开盘前
        """
        pass

    @virtual
    def on_stop(self) -> None:
        """
        Callback when strategy is stopped.
        """
        pass

    @virtual
    def on_tick(self, tick: TickData) -> None:
        """
        Callback of new tick data update.
        """
        pass

    @virtual
    def on_bars(self, bars: Dict[str, BarData]) -> None:
        """
        Callback of new bar data update.
        """
        pass

    @virtual
    def on_complete(self, daily_df: DataFrame,
                    statistics: dict) -> None:
        """
        Callback of new bar data update.
        """
        pass

    @virtual
    def on_trade(self, trade: TradeData, symbol: str) -> None:
        """
        Callback of new bar data update.
        如果trade为None说明撮合失败
        """
        pass

    def update_trade(self, trade: TradeData) -> None:
        """
        Callback of new trade data update.
        """
        if trade.direction == Direction.LONG:
            self.pos[trade.vt_symbol] += trade.volume
        else:
            self.pos[trade.vt_symbol] -= trade.volume

    def update_order(self, order: OrderData) -> None:
        """
        Callback of new order data update.
        """
        self.orders[order.vt_orderid] = order

        if not order.is_active() and order.vt_orderid in self.active_orderids:
            self.active_orderids.remove(order.vt_orderid)

    def buy(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> List[str]:
        """
        Send buy order to open a long position.
        """
        return self.send_order(vt_symbol, Direction.LONG, Offset.OPEN, price, volume, lock, net)

    def sell(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> List[str]:
        """
        Send sell order to close a long position.
        """
        return self.send_order(vt_symbol, Direction.SHORT, Offset.CLOSE, price, volume, lock, net)

    def short(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> List[str]:
        """
        Send short order to open as short position.
        """
        return self.send_order(vt_symbol, Direction.SHORT, Offset.OPEN, price, volume, lock, net)

    def cover(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> List[str]:
        """
        Send cover order to close a short position.
        """
        return self.send_order(vt_symbol, Direction.LONG, Offset.CLOSE, price, volume, lock, net)

    def send_order(
            self,
            vt_symbol: str,
            direction: Direction,
            offset: Offset,
            price: float,
            volume: float,
            lock: bool = False,
            net: bool = False,
    ) -> List[str]:
        """
        Send a new order.
        """
        if self.trading:
            vt_orderids: list = self.strategy_engine.send_order(
                self, vt_symbol, direction, offset, price, volume, lock, net
            )

            for vt_orderid in vt_orderids:
                self.active_orderids.add(vt_orderid)

            return vt_orderids
        else:
            return []

    def cancel_order(self, vt_orderid: str) -> None:
        """
        Cancel an existing order.
        """
        if self.trading:
            self.strategy_engine.cancel_order(self, vt_orderid)

    def cancel_all(self) -> None:
        """
        Cancel all orders sent by strategy.
        """
        for vt_orderid in list(self.active_orderids):
            self.cancel_order(vt_orderid)

    def get_pos(self, vt_symbol: str) -> int:
        """"""
        return self.pos.get(vt_symbol, 0)

    def get_order(self, vt_orderid: str) -> Optional[OrderData]:
        """"""
        return self.orders.get(vt_orderid, None)

    def get_all_active_orderids(self) -> List[OrderData]:
        """"""
        return list(self.active_orderids)

    def write_log(self, msg: str) -> None:
        """
        Write a log message.写日志
        """
        self.strategy_engine.write_log(msg, self)

    def get_pricetick(self, vt_symbol) -> float:
        """
        Return pricetick data of trading contract.
        """
        return self.strategy_engine.get_pricetick(self, vt_symbol)

    def load_bars(self, days: int, interval: Interval = Interval.MINUTE) -> None:
        """
        Load historical bar data for initializing strategy.
        """
        self.strategy_engine.load_bars(self, days, interval)

    def put_event(self) -> None:
        """
        Put an strategy data event for ui update.
        """
        if self.inited:
            self.strategy_engine.put_strategy_event(self)

    def send_email(self, msg) -> None:
        """
        Send email to default receiver.
        """
        if self.inited:
            self.strategy_engine.send_email(msg, self)

    def sync_data(self):
        """
        Sync strategy variables value into disk storage.
        """
        if self.trading:
            self.strategy_engine.sync_strategy_data(self)
