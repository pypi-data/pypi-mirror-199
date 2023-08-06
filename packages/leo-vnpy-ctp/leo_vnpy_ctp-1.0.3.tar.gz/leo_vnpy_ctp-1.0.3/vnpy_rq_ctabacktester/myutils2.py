import traceback
from datetime import datetime, timedelta
from itertools import groupby
from typing import List

import numpy
import pandas as pd
import talib
from pandas import DataFrame
from rqalpha.model import Instrument

from client_server.object import SymbolBasicData, BuildVtSymbols
from client_server.rqsdk_engine import RqsdkRpcEngine
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import DB_TZ
from vnpy.trader.object import BarData
from vnpy_rq_ctabacktester import RqBacktesterEngine


class OptionUtils:
    deltaseting = 0.25
    maSeting = 60
    savename = "变实值or3倍止损_均线" + str(maSeting) + "_delta0.25.csv"

    def __init__(self, rpc, backtester, start_date, end_date) -> None:
        self.dates = None
        # 所有合约-只有期权
        self.all_instruments = None
        self.all_instruments_pd = None
        # 期权合约列表， 但只是作为订阅用，不作为下单用，每日下单得看option_symbol_dates[d]['option_code']
        self.option_symbol = []
        # 标的
        self.underlying_order_book_ids = []
        # 期权按日期得数据组合
        self.option_symbol_dates = {}
        self.option_symbol_data = {}
        # 对应标的所有均线数据
        # self.underlying_ma_period = {}
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.rpc_engine: RqsdkRpcEngine = rpc
        self.backtester_engine: RqBacktesterEngine = backtester

    # 找1个月内的合约
    def findCurDayInstruments(self, ins_grouped: dict, cur_date: datetime, interval: int = 1) -> List[Instrument]:
        for index, key in enumerate(ins_grouped):
            groupd_date = datetime.strptime(key, '%Y-%m-%d')
            if cur_date.year == groupd_date.year and cur_date.month == groupd_date.month:
                if cur_date.day <= groupd_date.day:
                    #      还未到到期日，取本月合约
                    return ins_grouped[key]
                else:
                    # 已到到期日，取下个月合约
                    return ins_grouped[list(ins_grouped.keys())[index + interval]]

    def findCPByDelta(self, subcall_df: DataFrame, type) -> tuple:
        a = subcall_df.loc[(subcall_df["diff"] > 0) & (subcall_df["option_type"] == type), :]
        # print(a)
        if not a.empty:  # 如果有，筛选diff最小的合约
            a1 = a.sort_values(by="diff")
            atmopc = a1["code"].iloc[0]
            c_delta = a1["option_delta"].iloc[0]
        #        atmopc1=a1["code"].iloc[1]
        else:  # 若没有，就选取delta最小的合约
            a1 = subcall_df.sort_values(by="option_delta")
            atmopc = a1["code"].iloc[0]
            c_delta = a1["option_delta"].iloc[0]
        return atmopc + '.' + a1["exchange"].iloc[0], c_delta, a1["maturity_date"].iloc[0], a1["strike_price"].iloc[0],

    # def checkOpen(self, bar_time: datetime, symbol: str, pos_count: int, pre_open_interest: int):
    #     self.option_symbol_dates[bar_time]
    #     return None

    # 交易前一日的日期, 传入datetime
    def find_last_trade_day(self, d: datetime):
        for ind, da in enumerate(self.dates):
            if da == d.date():
                return self.dates[ind - 1]

    def findAllSymbols(self, underlying, interval: Interval):
        # 认购
        call_contracts = self.rpc_engine.get_contracts_option(underlying, option_type='C', strike=None)
        # 认沽
        put_contracts = self.rpc_engine.get_contracts_option(underlying, option_type='P', strike=None)

        self.all_instruments = self.rpc_engine.instruments(call_contracts + put_contracts)
        # 先用这个暂存数据, 后续把上面的去掉都用pandas处理
        self.all_instruments_pd = pd.DataFrame([x.__dict__ for x in self.all_instruments])
        self.all_instruments_pd.set_index('order_book_id', inplace=True)

        insSorted = sorted(self.all_instruments, key=lambda x: (x.maturity_date))
        insGrouped = groupby(insSorted, key=lambda x: (x.maturity_date))
        gg = {}
        for maturity_date, group in insGrouped:
            gg[maturity_date] = list(group)
        # break
        # 通过greek找到delta的值
        greeks = self.rpc_engine.get_greeks(call_contracts + put_contracts, self.start_date, self.end_date)
        self.dates: List[datetime] = self.rpc_engine.get_trading_dates(start_date=self.start_date, end_date=self.end_date)

        filter: dict = {
            "ma_param": self.maSeting,
            "datetime": {
                "$gte": datetime.strptime(self.start_date, "%Y%m%d").astimezone(DB_TZ),
                "$lte": datetime.strptime(self.end_date, "%Y%m%d").astimezone(DB_TZ),
            }
        }
        pd_ma_list = self.backtester_engine.database.load_common_data('symbol_ma', filter)
        # 查找每天9.30的标的分钟数据

        for d in self.dates:
            subcall = []
            # 根据当前日期查找到期月份内，还未到期的合约列表
            curDayInstruments = self.findCurDayInstruments(gg, d, 1)
            # print(f'{d} {todayInstruments}')
            # 当前日期的标的 如CU2211， 后面用于计算标的的60日均线
            curDayCode = None
            for instrument in curDayInstruments:
                if not curDayCode:
                    curDayCode = instrument.underlying_order_book_id + '.' + instrument.exchange
                multi_index = (instrument.order_book_id, d.strftime("%Y-%m-%d 00:00:00"))
                if multi_index in greeks.index:
                    option_delta = greeks.loc[multi_index, "delta"]
                    diff = self.deltaseting - abs(option_delta)
                    subcall.append(
                        {"code": instrument.order_book_id, "exchange": instrument.exchange,
                         "option_type": instrument.option_type, "diff": diff,
                         "strike_price": instrument.strike_price,
                         "option_delta": abs(option_delta), "maturity_date": instrument.maturity_date})
            # option_delta = greeks.delta[0]
            # diff = deltaseting - option_delta
            subcall_df = pd.DataFrame(subcall)
            # a = subcall_df.loc[(subcall_df["diff"] > 0) & (subcall_df["option_type"] == 'C'),:]
            if not subcall_df.empty:
                atmopc, c_delta, c_maturity_date, c_strike_price = self.findCPByDelta(subcall_df, 'C')
                atmopp, p_delta, p_maturity_date, p_strike_price = self.findCPByDelta(subcall_df, 'P')
                print(f'当前时间 :' + str(d), atmopc, c_delta, atmopp, p_delta)
                self.option_symbol_dates[d] = {
                    'C': atmopc,
                    'P': atmopp,
                    # 'c_strike_price': c_strike_price,
                    # 'p_strike_price': p_strike_price,
                    'maturity_date': c_maturity_date,
                    'end_days': (datetime.strptime(c_maturity_date, "%Y-%m-%d").date() - d).days,  # 结束日期
                    'underlying_order_book_id': curDayCode
                }
                self.option_symbol_data[atmopc] = {
                    'maturity_date': c_maturity_date
                }
                self.option_symbol_data[atmopp] = {
                    'maturity_date': c_maturity_date
                }
                self.option_symbol.extend([atmopc, atmopp])
            else:
                print(f'当前时间 :' + str(d), "没有delta数据，请检查")

            try:
                if d in self.option_symbol_dates:
                    ma = pd_ma_list.loc[
                         (self.option_symbol_dates[d]['underlying_order_book_id'].split('.')[0], pd.Timestamp(d)), :]
                    self.option_symbol_dates[d]['ma_value'] = ma['ma_value']
                    self.option_symbol_dates[d]['ma_param'] = int(ma['ma_param'])
                    if 'close_price' in ma:
                        self.option_symbol_dates[d]['close_price'] = ma['close_price']
                    if 'open_price' in ma:
                        self.option_symbol_dates[d]['open_price'] = ma['open_price']
            except Exception as e:
                # 有的数据可能没有导致异常
                rep: list = [False, traceback.format_exc()]
                print(rep)

        self.option_symbol = list(set(self.option_symbol))
        # 查找以天为单位的合约的持仓量
        print(f' 准备加载期权合约天的数据，为了拿open_intervest...{datetime.now()}')
        option_volumn_pandas = self.backtester_engine.database.load_common_data('bar_data', {
            "interval": 'd',
            "symbol": {
                "$in": [x.split(".")[0] for x in self.option_symbol],
            },
            "datetime": {
                "$gte": datetime.strptime(self.start_date, "%Y%m%d").astimezone(DB_TZ),
                "$lte": datetime.strptime(self.end_date, "%Y%m%d").astimezone(DB_TZ),
            }
        })
        # option_volumn_pandas = pd.DataFrame(option_volumn)
        print(f' 完成加载 期权合约天的数据...{datetime.now()}')
        # option_volumn_pandas['datetime'] = option_volumn_pandas['datetime'].dt.tz_convert('Asia/Shanghai')
        # option_volumn_pandas.set_index(['symbol', 'datetime'], inplace=True)

        self.underlying_order_book_ids = list(
            set([v['underlying_order_book_id'] for v in self.option_symbol_dates.values()]))
        print(f'准备加载9.29标的数据...{datetime.now()}')
        pd_min_data = self.backtester_engine.database.load_aggregate_data('bar_data', [
            {
                "$match": {
                    "symbol": {
                        "$in": [x.split(".")[0] for x in self.underlying_order_book_ids],
                    },
                    "interval": "1m",
                    "datetime": {
                        "$gte": datetime.strptime(self.start_date, "%Y%m%d").astimezone(DB_TZ),
                        "$lte": datetime.strptime(self.end_date, "%Y%m%d").astimezone(DB_TZ),
                    }
                }
            }, {
                "$project": {
                    "_id": - 1,
                    "symbol": 1,
                    "interval": 1,
                    "open_price": 1,
                    "close_price": 1,
                    "high_price": 1,
                    "low_price": 1,
                    "open_interest": 1,
                    "datetime": 1,
                    "time": {
                        "$dateToString": {
                            "format": "%H:%M",
                            "date": '$datetime'
                        }
                    }
                }
            }, {
                "$match": {
                    "time": '01:29'
                }
            }
        ])
        # pd_min_data = pd.DataFrame(underlying_min_data)
        # pd_min_data['datetime'] = pd_min_data['datetime'].dt.tz_convert('Asia/Shanghai')
        # pd_min_data.set_index(['symbol', 'datetime'], inplace=True)
        print(f'完成 加载9.29标的数据 ...{datetime.now()}')
        for ind, d in enumerate(self.dates):
            if d in self.option_symbol_dates:
                final_data = self.option_symbol_dates[d]
                # 9：30 标的的分钟数据
                try:
                    ss = pd_min_data.loc[
                         (final_data['underlying_order_book_id'].split('.')[0],
                          pd.Timestamp(datetime(d.year, d.month, d.day, 9, 30, 0))),
                         :]
                    # print(f'标的9.30的数据：{final_data["underlying_order_book_id"]}:  收盘价: {ss["close_price"]}')

                    if ind > 0:
                        # 查找前一日的持仓量
                        c_daily = option_volumn_pandas.loc[
                                  (final_data['C'].split('.')[0], pd.Timestamp(self.dates[ind - 1])),
                                  :]
                        # and (final_data['P'].split('.')[0], self.dates[ind - 1]) in option_volumn_pandas:
                        p_daily = option_volumn_pandas.loc[
                                  (final_data['P'].split('.')[0], pd.Timestamp(self.dates[ind - 1])),
                                  :]
                        # print(option_volumn)
                        if 3 < final_data['end_days'] < 30:
                            # 结束时间段内判断 and 对应期权的合约持仓量是否满足条件 300
                            if ss['close_price'] > final_data['ma_value'] and not p_daily.empty:
                                self.option_symbol_dates[d]['open'] = 'sell_open'
                                self.option_symbol_dates[d]['open_interest'] = p_daily['open_interest']
                                if p_daily['open_interest'] > 300:
                                    # 标的1分钟前收盘价大于60日均线，并且此合约前一日的持仓量大于300
                                    self.option_symbol_dates[d]['option_code'] = final_data['P']
                                else:
                                    print(f'{self.option_symbol_dates[d]} 做认沽,持仓量不达标')
                                    # self.option_symbol_dates[d]['option_code'] = final_data['P']
                            elif not c_daily.empty:
                                self.option_symbol_dates[d]['open_interest'] = c_daily['open_interest']
                                self.option_symbol_dates[d]['open'] = 'sell_open'
                                if c_daily['open_interest'] > 300:
                                    self.option_symbol_dates[d]['option_code'] = final_data['C']
                                else:
                                    print(f'{self.option_symbol_dates[d]} 做认购, 持仓量不达标')
                except Exception as e:
                    rep: list = [False, traceback.format_exc()]
                    print(e)

        # 将数据临时存入mongo 用于下次提取，省事
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

        self.backtester_engine.database.save_common_data('tmp_option_daily', option_daily)
        tmp_option_symbol = [{
            "filter": {
                'name':'单腿卖期权',
                'start_date': self.start_date,
                'end_date': self.end_date
            },
            "data": {
                'name': '单腿卖期权',
                'start_date': self.start_date,
                'end_date': self.end_date,
                'symbols': self.option_symbol
            }
        }]

        self.backtester_engine.database.save_common_data('tmp_option_symbol', tmp_option_symbol)
        # 组装数据返回
        # self.find_symbol_fromdb()
        return self.build_paramer(interval)

    def find_symbol_fromdb(self, interval: Interval):

        self.dates: List[datetime] = self.rpc_engine.get_trading_dates(start_date=self.start_date, end_date=self.end_date)
        filter: dict = {
            'name': '单腿卖期权',
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        tmp_option_symbol = self.backtester_engine.database.load_common_data('tmp_option_symbol', filter)
        if not tmp_option_symbol.empty:
            self.option_symbol = tmp_option_symbol.loc[0, :].symbols

        tmp_option_daily = self.backtester_engine.database.load_common_data('tmp_option_daily', {
            # 'name': '单腿卖期权',
            "datetime": {
                "$gte": datetime.strptime(self.start_date, "%Y%m%d").astimezone(DB_TZ),
                "$lte": datetime.strptime(self.end_date, "%Y%m%d").astimezone(DB_TZ),
            }
        })
        if not tmp_option_daily.empty:
            tmp_option_daily['datetime'] = tmp_option_daily['datetime'].dt.tz_convert('Asia/Shanghai')
            tmp_option_daily.sort_values(by='datetime', ascending=True, axis=0)
            tmp_option_daily.set_index('datetime', inplace=True)
            for index, row in tmp_option_daily.iterrows():
                # print(index, row)
                dd = row.to_dict()
                self.option_symbol_dates[index.date()] = dd
                self.option_symbol_data[dd['C']] = {
                    'maturity_date': dd['maturity_date']
                }
                self.option_symbol_data[dd['P']] = {
                    'maturity_date': dd['maturity_date']
                }

        tmp_instruments = self.backtester_engine.database.load_common_data('tmp_instruments', {

        })
        if not tmp_instruments.empty:
            self.all_instruments_pd = tmp_instruments
            self.all_instruments_pd.set_index('order_book_id', inplace=True)

        return self.build_paramer(interval)
            # tmp_option_daily.index
            # self.option_symbol = option_symbols.loc[0, :].symbols

    def build_paramer(self, interval: Interval):
        # 根据找到的合约计算BuildVtSymbols
        symbol_basic: List[SymbolBasicData] = self.backtester_engine.database.load_symbol_basic(underlying_symbol=None)
        sizes = {}
        priceticks = {}
        slippages = {}
        rates = {}
        for symbol in self.option_symbol:
            ins = self.get_symbol_params(symbol.split('.')[0])
            sizes[symbol] = ins.contract_multiplier
            if ins.type == 'Option':
                # 期权的跳和期货的略有不同要注意
                priceticks[symbol] = symbol_basic[ins.underlying_symbol + '_O'].price_tick
            else:
                priceticks[symbol] = symbol_basic[ins.underlying_symbol].price_tick
            slippages[symbol] = 1
            rates[symbol] = 0.001

        return BuildVtSymbols(vt_symbols=self.option_symbol,
                              interval=interval,
                              start=datetime.strptime(self.start_date, "%Y%m%d").astimezone(DB_TZ),
                              end=datetime.strptime(self.end_date, "%Y%m%d").astimezone(DB_TZ),
                              rates=rates,
                              sizes=sizes,
                              slippages=slippages,
                              priceticks=priceticks,
                              capital=1000000,
                              risk_free=0
                              )

    def get_symbol_params(self, symbol: str):
        # 返回Series
        return self.all_instruments_pd.loc[symbol, :]
        #     for i in self.all_instruments:
        #         if i.order_book_id == symbol:
        #             return i

    # 保存MA平均数，
    def update_ma(self, interval: Interval, ma_param):

        self.dates: List[datetime] = self.rpc_engine.get_trading_dates(start_date=self.start_date, end_date=self.end_date)
        # 认购
        call_contracts = self.rpc_engine.get_contracts_option('CU', option_type='C', strike=None)
        # 认沽
        put_contracts = self.rpc_engine.get_contracts_option('CU', option_type='P', strike=None)

        self.all_instruments = self.rpc_engine.instruments(call_contracts + put_contracts)
        # 临时存储好了
        self.save_tmp_all_instruments()

        insSorted = sorted(self.all_instruments, key=lambda x: (x.maturity_date))
        insGrouped = groupby(insSorted, key=lambda x: (x.maturity_date))
        gg = {}
        for key, group in insGrouped:
            gg[key] = list(group)
        unerlying_ids = []
        for d in self.dates:
            curDayInstruments = self.findCurDayInstruments(gg, d, 1)
            # print(f'{d} {todayInstruments}')
            # 当前日期的标的 如CU2211， 后面用于计算标的的60日均线
            curDayCode = None
            for instrument in curDayInstruments:
                if not curDayCode:
                    curDayCode = instrument.underlying_order_book_id + '.' + instrument.exchange
                    unerlying_ids.append(curDayCode)

        self.underlying_order_book_ids = list(
            set(unerlying_ids))

        ##### 以上特定添加的 ########

        start_datep = datetime.strptime(self.start_date, "%Y%m%d")
        end_datep = datetime.strptime(self.end_date, "%Y%m%d")
        print(f'当前标的: {len(self.underlying_order_book_ids)}  {self.underlying_order_book_ids}')

        ma_data: List[dict] = []
        for symbol in self.underlying_order_book_ids:
            print(f'MA 当前计算: {symbol}')
            # 因为要60日均线，所以往前要半年数据基本上能够覆盖
            ma_start = start_datep + timedelta(days=-120)
            bar1: List[BarData] = self.backtester_engine.database.load_bar_data(
                symbol.split('.')[0], Exchange.SHFE, interval, ma_start, end_datep
            )
            if len(bar1) == 0:
                raise Exception(f"标的 {symbol} 不存在1d 数据，请先下载")

            bar_date = []
            bar_close_price = []
            bar_open_price = []

            for ind, b in enumerate(bar1):
                bar_date.append(b.datetime)
                bar_close_price.append(b.close_price)
                bar_open_price.append(b.open_price)

            # 这个合约标的的60日均线
            mas = talib.MA(numpy.array(bar_close_price), ma_param)
            # 能否将平均线数据存储到mongodb
            for ind, ma in enumerate(mas):
                if not pd.isna(ma):
                    ma_data.append({
                        "filter": {
                            "symbol": symbol.split('.')[0],
                            'datetime': bar_date[ind],
                            "ma_param": ma_param,
                        },
                        "data": {
                            "symbol": symbol.split('.')[0],
                            'datetime': bar_date[ind],
                            "ma_param": ma_param,
                            "close_price": bar_close_price[ind],
                            "open_price": bar_open_price[ind],
                            "ma_value": ma,

                        }
                    })

        self.backtester_engine.database.save_common_data('symbol_ma', ma_data)

        # filter: dict = {
        #     "ma_param": ma_param,
        #     "datetime": {
        #         "$gte": datetime.strptime(self.start_date, "%Y%m%d").astimezone(DB_TZ),
        #         "$lte": datetime.strptime(self.end_date, "%Y%m%d").astimezone(DB_TZ),
        #     }
        # }
        # ret = backtester_engine.database.load_common_data('symbol_ma', filter)
        print(f'移动平均线数据已存储 ')

    def download_symbol(self):
        # 拼接合约 合约加上交易所编号
        # 下载期权合约
        # backtester_engine.backtesting_engine.download_symbol(self.option_symbol, Interval.MINUTE,
        #                                                      datetime.strptime(self.start_date, "%Y%m%d"),
        #                                                      datetime.strptime(self.end_date, "%Y%m%d"), True)
        # # 下载标的日线
        # backtester_engine.backtesting_engine.download_symbol(self.underlying_order_book_ids, Interval.DAILY,
        #                                                      datetime.strptime(self.start_date, "%Y%m%d"),
        #                                                      datetime.strptime(self.end_date, "%Y%m%d"), True)
        # # 下载标的分钟线
        # backtester_engine.backtesting_engine.download_symbol(self.underlying_order_book_ids, Interval.MINUTE,
        #                                                      datetime.strptime(self.start_date, "%Y%m%d"),
        #                                                      datetime.strptime(self.end_date, "%Y%m%d"), True)

        self.backtester_engine.backtesting_engine.download_symbol(['CU2209C62000.SHFE'], Interval.MINUTE,
                                                             datetime.strptime(self.start_date, "%Y%m%d"),
                                                             datetime.strptime(self.end_date, "%Y%m%d"), True)

        print(f'已全部下载完毕....')

    def save_tmp_all_instruments(self):
        option_daily = []
        for d in self.all_instruments:
            option_daily.append({
                "filter": {
                    'symbol': d.order_book_id,
                },
                "data": {
                    **d.__dict__
                }
            })

        self.backtester_engine.database.save_common_data('tmp_instruments', option_daily)
