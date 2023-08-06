""""""
from datetime import datetime
from typing import List

import pandas as pd
import pytz
from pandas import DataFrame
from pymongo import ASCENDING, MongoClient, ReplaceOne
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.results import DeleteResult

from client_server.object import FutureRuleData, SymbolBasicData
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import BaseDatabase, BarOverview, TickOverview, DB_TZ
from vnpy.trader.object import BarData, TickData
from vnpy.trader.setting import SETTINGS


class MongodbDatabase(BaseDatabase):
    """MongoDB数据库接口"""

    def __init__(self) -> None:
        """"""
        # 读取配置
        self.database: str = SETTINGS["database.database"]
        self.host: str = SETTINGS["database.host"]
        self.port: int = SETTINGS["database.port"]
        self.username: str = SETTINGS["database.user"]
        self.password: str = SETTINGS["database.password"]

        # 创建客户端
        if self.username and self.password:
            self.client: MongoClient = MongoClient(
                host=self.host,
                port=self.port,
                tz_aware=True,
                username=self.username,
                password=self.password,
                tzinfo=DB_TZ
            )
        else:
            self.client: MongoClient = MongoClient(
                host=self.host,
                port=self.port,
                tz_aware=True,
                tzinfo=DB_TZ
            )

        # 初始化数据库
        self.db: Database = self.client[self.database]

        # 初始化K线数据表
        self.bar_collection: Collection = self.db["bar_data"]
        self.bar_collection.create_index(
            [
                ("exchange", ASCENDING),
                ("symbol", ASCENDING),
                ("interval", ASCENDING),
                ("datetime", ASCENDING),
            ],
            unique=True
        )

        # 初始化Tick数据表
        self.tick_collection: Collection = self.db["tick_data"]
        self.tick_collection.create_index(
            [
                ("exchange", ASCENDING),
                ("symbol", ASCENDING),
                ("datetime", ASCENDING),
            ],
            unique=True
        )

        # 初始化K线概览表
        self.bar_overview_collection: Collection = self.db["bar_overview"]
        self.bar_overview_collection.create_index(
            [
                ("exchange", ASCENDING),
                ("symbol", ASCENDING),
                ("interval", ASCENDING),
            ],
            unique=True
        )

        # 初始化Tick概览表
        self.tick_overview_collection: Collection = self.db["tick_overview"]
        self.tick_overview_collection.create_index(
            [
                ("exchange", ASCENDING),
                ("symbol", ASCENDING),
            ],
            unique=True
        )

        # price_tick contract_multiplier 涨跌停板幅度 限价单每笔最大 交易所 品种 underlying_symbol_name
        self.futures_rule: Collection = self.db["futures_rule"]
        # self.symbol_basic_collection.create_index(
        #     [
        #         ("underlying_symbol", ASCENDING),
        #         ("margin_rate_daily", ASCENDING),
        #     ],
        #     unique=True
        # )

        self.symbol_basic_collection: Collection = self.db["symbol_basic"]

    def load_symbol_basic(
            self,
            underlying_symbol: str,
    ) -> dict:
        """读取K线数据"""
        filter: dict = {}
        if underlying_symbol:
            filter: dict = {
                "_id": underlying_symbol,
            }

        c: Cursor = self.symbol_basic_collection.find(filter)

        bars = {}
        for d in c:
            d["underlying_symbol"] = d["_id"]
            d.pop("_id")

            bar = SymbolBasicData(**d)
            # bars.append(bar)
            bars[d["underlying_symbol"]] = bar

        return bars

    def save_common_data(self, table:str, bars: List[dict]) -> bool:
        requests: List[ReplaceOne] = []
        for bar in bars:
            requests.append(ReplaceOne(bar['filter'], bar['data'], upsert=True))
        self.db[table].bulk_write(requests, ordered=False)
        return True

    # 常规查询, 返回pandas dataframe
    def load_common_data(
            self,
            table: str,
            filter: dict
    ) -> DataFrame:
        """读取K线数据"""
        c: Cursor = self.db[table].find(filter)

        # df = pd.DataFrame()
        bars: List[dict] = []

        for d in c:
            if "exchange" in d:
                d["exchange"] = Exchange(d["exchange"])
            if "interval" in d:
                d["interval"] = Interval(d["interval"])

            d["gateway_name"] = "DB"
            d.pop("_id")

            bars.append(d)
            # df = df.append(d, ignore_index=True)
        if len(bars) == 0:
            df = pd.DataFrame(bars, index=[0])
        else:
            df = pd.DataFrame(bars)
        if 'datetime' in df and 'symbol' in df:
            df['datetime'] = df['datetime'].dt.tz_convert('Asia/Shanghai')
            df.set_index(['symbol', 'datetime'], inplace=True)
        bars.clear()
        bars = None
        return df

    # 通过汇总数据查询- 复杂查询
    def load_aggregate_data(
            self,
            table: str,
            filter: List
    ) -> DataFrame:
        """读取K线数据"""
        c: Cursor = self.db[table].aggregate(filter)

        bars: List[dict] = []
        for d in c:
            if "exchange" in d:
                d["exchange"] = Exchange(d["exchange"])
            if "interval" in d:
                d["interval"] = Interval(d["interval"])
            d["gateway_name"] = "DB"
            d.pop("_id")

            bars.append(d)
            # df = df.append(d, ignore_index=True)
        df = pd.DataFrame(bars)
        df['datetime'] = df['datetime'].dt.tz_convert('Asia/Shanghai')
        df.set_index(['symbol', 'datetime'], inplace=True)

        bars.clear()
        bars = None
        return df

    def save_symbol_basic(self, bars: List[FutureRuleData], stream: bool = False) -> bool:
        """保存基础akshare的数据"""
        requests: List[ReplaceOne] = []

        for bar in bars:
            # 逐个插入
            filter: dict = {
                "datetime": bar.datetime,
                "underlying_symbol": bar.underlying_symbol,
            }

            d: dict = {
                "datetime": bar.datetime,
                "underlying_symbol": bar.underlying_symbol,
                "exchange": bar.exchange,
                "underlying_symbol_name": bar.underlying_symbol_name,
                "range": bar.range,
                "limit_volume": bar.limit_volume,
                "contract_multiplier": bar.contract_multiplier,
                "price_tick": bar.price_tick,
                "margin_rate": bar.margin_rate,
                "remark": bar.remark,
            }

            requests.append(ReplaceOne(filter, d, upsert=True))

        self.futures_rule.bulk_write(requests, ordered=False)

        return True

    def futures_rule(self, bars: List[FutureRuleData], stream: bool = False) -> bool:
        """保存基础akshare的数据"""
        requests: List[ReplaceOne] = []

        for bar in bars:
            # 逐个插入
            filter: dict = {
                "datetime": bar.datetime,
                "underlying_symbol": bar.underlying_symbol,
            }

            d: dict = {
                "datetime": bar.datetime,
                "underlying_symbol": bar.underlying_symbol,
                "exchange": bar.exchange,
                "underlying_symbol_name": bar.underlying_symbol_name,
                "range": bar.range,
                "limit_volume": bar.limit_volume,
                "contract_multiplier": bar.contract_multiplier,
                "price_tick": bar.price_tick,
                "margin_rate": bar.margin_rate,
                "remark": bar.remark,
            }

            requests.append(ReplaceOne(filter, d, upsert=True))

        self.futures_rule.bulk_write(requests, ordered=False)

        return True

    def save_bar_data(self, bars: List[BarData], stream: bool = False) -> bool:
        """保存K线数据"""
        requests: List[ReplaceOne] = []

        for bar in bars:
            # 逐个插入
            filter: dict = {
                "symbol": bar.symbol,
                "exchange": bar.exchange.value,
                "datetime": bar.datetime,
                "interval": bar.interval.value,
            }

            d: dict = {
                "symbol": bar.symbol,
                "exchange": bar.exchange.value,
                "datetime": bar.datetime,
                "interval": bar.interval.value,
                "volume": bar.volume,
                "turnover": bar.turnover,
                "open_interest": bar.open_interest,
                "open_price": bar.open_price,
                "high_price": bar.high_price,
                "low_price": bar.low_price,
                "close_price": bar.close_price,
            }

            requests.append(ReplaceOne(filter, d, upsert=True))

        self.bar_collection.bulk_write(requests, ordered=False)

        # 更新汇总
        filter: dict = {
            "symbol": bar.symbol,
            "exchange": bar.exchange.value,
            "interval": bar.interval.value
        }

        overview: dict = self.bar_overview_collection.find_one(filter)

        if not overview:
            overview = {
                "symbol": bar.symbol,
                "exchange": bar.exchange.value,
                "interval": bar.interval.value,
                "count": len(bars),
                "start": bars[0].datetime,
                "end": bars[-1].datetime
            }
        elif stream:
            overview["end"] = bars[-1].datetime
            overview["count"] += len(bars)
        else:
            # 修改时区的问题
            # overview["start"] = min(pytz.timezone('Asia/Shanghai').localize(bars[0].datetime), overview["start"])
            # overview["end"] = max(pytz.timezone('Asia/Shanghai').localize(bars[-1].datetime), overview["end"])
            overview["start"] = min(bars[0].datetime, overview["start"])
            overview["end"] = max(bars[-1].datetime, overview["end"])
            overview["count"] = self.bar_collection.count_documents(filter)

        self.bar_overview_collection.update_one(filter, {"$set": overview}, upsert=True)

        return True

    def save_tick_data(self, ticks: List[TickData], stream: bool = False) -> bool:
        """保存TICK数据"""
        requests: List[ReplaceOne] = []

        for tick in ticks:
            filter: dict = {
                "symbol": tick.symbol,
                "exchange": tick.exchange.value,
                "datetime": tick.datetime,
            }

            d: dict = {
                "symbol": tick.symbol,
                "exchange": tick.exchange.value,
                "datetime": tick.datetime,
                "name": tick.name,
                "volume": tick.volume,
                "turnover": tick.turnover,
                "open_interest": tick.open_interest,
                "last_price": tick.last_price,
                "last_volume": tick.last_volume,
                "limit_up": tick.limit_up,
                "limit_down": tick.limit_down,
                "open_price": tick.open_price,
                "high_price": tick.high_price,
                "low_price": tick.low_price,
                "pre_close": tick.pre_close,
                "bid_price_1": tick.bid_price_1,
                "bid_price_2": tick.bid_price_2,
                "bid_price_3": tick.bid_price_3,
                "bid_price_4": tick.bid_price_4,
                "bid_price_5": tick.bid_price_5,
                "ask_price_1": tick.ask_price_1,
                "ask_price_2": tick.ask_price_2,
                "ask_price_3": tick.ask_price_3,
                "ask_price_4": tick.ask_price_4,
                "ask_price_5": tick.ask_price_5,
                "bid_volume_1": tick.bid_volume_1,
                "bid_volume_2": tick.bid_volume_2,
                "bid_volume_3": tick.bid_volume_3,
                "bid_volume_4": tick.bid_volume_4,
                "bid_volume_5": tick.bid_volume_5,
                "ask_volume_1": tick.ask_volume_1,
                "ask_volume_2": tick.ask_volume_2,
                "ask_volume_3": tick.ask_volume_3,
                "ask_volume_4": tick.ask_volume_4,
                "ask_volume_5": tick.ask_volume_5,
                "localtime": tick.localtime,
            }

            requests.append(ReplaceOne(filter, d, upsert=True))

        self.tick_collection.bulk_write(requests, ordered=False)

        # 更新Tick汇总
        filter: dict = {
            "symbol": tick.symbol,
            "exchange": tick.exchange.value
        }

        overview: dict = self.tick_overview_collection.find_one(filter)

        if not overview:
            overview = {
                "symbol": tick.symbol,
                "exchange": tick.exchange.value,
                "count": len(ticks),
                "start": ticks[0].datetime,
                "end": ticks[-1].datetime
            }
        elif stream:
            overview["end"] = ticks[-1].datetime
            overview["count"] += len(ticks)
        else:
            overview["start"] = min(ticks[0].datetime, overview["start"])
            overview["end"] = max(ticks[-1].datetime, overview["end"])
            overview["count"] = self.bar_collection.count_documents(filter)

        self.tick_overview_collection.update_one(filter, {"$set": overview}, upsert=True)

        return True

    def load_bar_data(
            self,
            symbol: str,
            exchange: Exchange,
            interval: Interval,
            start: datetime,
            end: datetime
    ) -> List[BarData]:
        """读取K线数据"""
        filter: dict = {
            "symbol": symbol,
            "exchange": exchange.value,
            "interval": interval.value,
            "datetime": {
                "$gte": start.astimezone(DB_TZ),
                "$lte": end.astimezone(DB_TZ)
            }
        }

        c: Cursor = self.bar_collection.find(filter)

        bars: List[BarData] = []
        for d in c:
            d["exchange"] = Exchange(d["exchange"])
            d["interval"] = Interval(d["interval"])
            d["gateway_name"] = "DB"
            d.pop("_id")

            bar = BarData(**d)
            bars.append(bar)

        return bars

    def load_tick_data(
            self,
            symbol: str,
            exchange: Exchange,
            start: datetime,
            end: datetime
    ) -> List[TickData]:
        """读取TICK数据"""
        filter: dict = {
            "symbol": symbol,
            "exchange": exchange.value,
            "datetime": {
                "$gte": start.astimezone(DB_TZ),
                "$lte": end.astimezone(DB_TZ)
            }
        }

        c: Cursor = self.tick_collection.find(filter)

        ticks: List[TickData] = []
        for d in c:
            d["exchange"] = Exchange(d["exchange"])
            d["gateway_name"] = "DB"
            d.pop("_id")

            tick: TickData = TickData(**d)
            ticks.append(tick)

        return ticks

    def delete_bar_data(
            self,
            symbol: str,
            exchange: Exchange,
            interval: Interval
    ) -> int:
        """删除K线数据"""
        filter: dict = {
            "symbol": symbol,
            "exchange": exchange.value,
            "interval": interval.value,
        }

        result: DeleteResult = self.bar_collection.delete_many(filter)
        self.bar_overview_collection.delete_one(filter)

        return result.deleted_count

    def delete_tick_data(
            self,
            symbol: str,
            exchange: Exchange
    ) -> int:
        """删除TICK数据"""
        filter: dict = {
            "symbol": symbol,
            "exchange": exchange.value
        }

        result: DeleteResult = self.tick_collection.delete_many(filter)
        self.tick_overview_collection.delete_one(filter)

        return result.deleted_count

    def get_bar_overview(self) -> List[BarOverview]:
        """查询数据库中的K线汇总信息"""
        c: Cursor = self.bar_overview_collection.find()

        overviews: List[BarOverview] = []
        for d in c:
            d["exchange"] = Exchange(d["exchange"])
            d["interval"] = Interval(d["interval"])
            d.pop("_id")

            overview: BarOverview = BarOverview(**d)
            overviews.append(overview)

        return overviews

    def get_tick_overview(self) -> List[TickOverview]:
        """查询数据库中的Tick汇总信息"""
        c: Cursor = self.tick_overview_collection.find()

        overviews: List[TickOverview] = []
        for d in c:
            d["exchange"] = Exchange(d["exchange"])
            d.pop("_id")

            overview: TickOverview = TickOverview(**d)
            overviews.append(overview)

        return overviews
