from datetime import datetime
from typing import Dict

import pandas as pd
import quantstats as qs
from pandas import DataFrame

from client_server.rqsdk_engine import RqsdkRpcEngine
from vnpy.trader.object import TickData, BarData
from vnpy.trader.utility import BarGenerator
from vnpy_rq_ctabacktester import RqBacktesterEngine
from vnpy_rq_ctabacktester.base_define import APP_rqsdk
from vnpy_rq_ctabacktester.rq_template import RqStrategyTemplate


class TlTradingStrategy(RqStrategyTemplate):
    """"""

    author = "套利交易，日级别-问题在于合约比较难以成交"

    price_add = 5
    boll_window = 20
    boll_dev = 2
    fixed_size = 1
    leg1_ratio = 1
    leg2_ratio = 1

    leg1_symbol = ""
    leg2_symbol = ""
    current_spread = 0.0
    boll_mid = 0.0
    boll_down = 0.0
    boll_up = 0.0
    start_date = '20220101'
    end_date = '20230227'
    symbol = "CU"
    domNextData = {}
    diff = None

    parameters = [
        "price_add",
        "boll_window",
        "boll_dev",
        "fixed_size",
        "leg1_ratio",
        "leg2_ratio",
    ]
    variables = [
        "leg1_symbol",
        "leg2_symbol",
        "current_spread",
        "boll_mid",
        "boll_down",
        "boll_up",
    ]

    def __init__(
            self,
            strategy_engine: RqBacktesterEngine,
            strategy_name: str,
            setting: dict
    ):
        """"""
        super().__init__(strategy_engine, strategy_name, setting)

        self.rpc_engine: RqsdkRpcEngine = self.strategy_engine.main_engine.get_engine(APP_rqsdk)

        last_td_date = self.rpc_engine.get_previous_trading_date(self.start_date)
        # dates = [last_td_date]
        dates = self.rpc_engine.get_trading_dates(start_date=self.start_date, end_date=self.end_date)
        # dates.extends(dates2)
        print('==========', dates)

        # self.download_basic(dates)
        dictSymbols = []
        allContracts = []
        for d in dates:
            ctr_list = self.rpc_engine.get_contracts(self.symbol, date=d.strftime("%Y%m%d"))
            if len(ctr_list) >= 2:
                allContracts.extend(ctr_list)
        allContracts = list(set(allContracts))

        # 提取各个持仓量
        positions_list = self.rpc_engine.get_price(
            order_book_ids=allContracts,
            start_date=last_td_date,
            end_date=self.end_date,
            frequency="1d",
            fields=["open_interest", "close"],
            expect_df=True,
        )
        positions_list = positions_list.reset_index().set_index("order_book_id")
        df = positions_list.sort_values(by="date", ascending=True)
        symbols = []

        for ind, d in enumerate(dates):
            # 前一天是不是周五
            # da = d + timedelta(days=-1)
            # if da.weekday() not in [0, 1, 2, 3, 4]:
            #     da = d + timedelta(days=-3)
            da = None
            if ind == 0:
                # da = datetime.strptime().strftime("%Y%m%d")
                da = last_td_date
            else:
                da = dates[ind - 1]
            pos_sorted = df[df['date'] == str(da)].sort_values(by='open_interest', ascending=False)

            today_sorted = df[df['date'] == str(d)].sort_values(by='open_interest', ascending=False)
            if len(list(pos_sorted.index)) >= 2:
                # 提取主力、次主力合约
                dom_ctr = pos_sorted.index[0]
                next_ctr = pos_sorted.index[1]
                dn = [dom_ctr, next_ctr]
                diff = pos_sorted['close'][dom_ctr] - pos_sorted['close'][next_ctr]

                self.domNextData[d] = {
                    "date_base": da,
                    "dom": dom_ctr,
                    "next": next_ctr,
                    "diff": diff,
                    "dom_price": today_sorted['close'][dom_ctr],
                    "next_price": today_sorted['close'][next_ctr],
                }
                symbols.extend(dn)

        # 拿到要回测的合约属性
        instruments = self.get_instruments(list(set(symbols)), dates)

        for x in self.domNextData:
            s = self.domNextData[x]
            for i in instruments:
                if s['dom'] == i.order_book_id:
                    s['dom'] += '.' + i.exchange
                elif s['next'] == i.order_book_id:
                    s['next'] += '.' + i.exchange

        print(f"订阅所有主力合约 {self.vt_symbols}")

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")

        # self.strategy_engine.main_engine.subscribe()
        self.load_bars(1)

    def before_trade(self, dt: datetime) -> None:
        """
        开盘前
        """
        # self.output(f'开盘前回调 {dt}')
        pass

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        if (
                self.last_tick_time
                and self.last_tick_time.minute != tick.datetime.minute
        ):
            bars = {}
            for vt_symbol, bg in self.bgs.items():
                bars[vt_symbol] = bg.generate()
            self.on_bars(bars)

        bg: BarGenerator = self.bgs[tick.vt_symbol]
        bg.update_tick(tick)

        self.last_tick_time = tick.datetime

    def on_complete(self, daily_df: DataFrame,
                    statistics: dict) -> None:
        daily_df.index = pd.to_datetime(daily_df.index)

        qs.reports.html(daily_df['return'], output='stats.html', title='Stock Sentiment')
        pass

    def on_bars(self, bars: Dict[str, BarData]):
        # print(f'持仓 {self.pos} 合约：{str(bars)}  ')
        if bars[list(bars.keys())[0]].datetime.date() not in self.domNextData:
            print(f'跳过一天 {bars[list(bars.keys())[0]].datetime.date()}')
            return
        dom_next_data = self.domNextData[bars[list(bars.keys())[0]].datetime.date()]
        dom_ctr = dom_next_data['dom']
        next_ctr = dom_next_data['next']
        dom_price = dom_next_data['dom_price']
        next_price = dom_next_data['next_price']

        # 主力合约 >0 : long   <0 : short
        dom_num = self.get_pos(dom_ctr)
        # 次主力合约
        next_num = self.get_pos(next_ctr)
        bar = bars[dom_ctr]
        for symbol in self.pos.keys():
            if symbol not in [dom_ctr, next_ctr]:
                # 合约换月 平仓
                num = self.get_pos(symbol)
                if num > 0:
                    print(f'合约换月11 {symbol} 平多头 {num}')
                    self.sell(symbol, bar.close_price, num)
                    # next_num = 0

                if num < 0:
                    print(f'合约换月11 {symbol} 平空头 {num}')
                    self.cover(symbol, bar.close_price, abs(num))
                    # dom_num = 0

        if dom_next_data['diff'] <= -150:
            # print(f' 主力次主力合约： {dom_next_data}')
            # 做多价差
            if dom_num == 0 and next_num == 0 and bar.close_price:
                self.buy(dom_ctr, dom_price, 1)
                self.short(next_ctr, next_price, 1)

                print(
                    f'做多价差 {dom_ctr} 时间 {bar.datetime.date()}  收盘价 {dom_price} . 做空合约 {next_ctr} 收盘价 {next_price} ')
            # 平空价差
            elif next_num > 0 and dom_num < 0:
                self.cover(dom_ctr, dom_price, abs(dom_num))
                self.sell(next_ctr, next_price, abs(next_num))
                print(
                    f'平空价差: 卖空： {dom_ctr} 时间 {bar.datetime.date()} 收盘价 {dom_price} . 卖多合约 {next_ctr} 收盘价 {next_price} ')
        elif dom_next_data['diff'] >= 150:
            # 做空价差
            if dom_num == 0 and next_num == 0 and bar.close_price:
                self.short(dom_ctr, dom_price, 1)
                # self.short(dom_ctr, bar.low_price, 1)
                self.buy(next_ctr, next_price, 1)

                print(
                    f'做空价差 {dom_ctr} 时间 {bar.datetime.date()}  收盘价 {dom_price} . 做多合约 {next_ctr} 收盘价 {next_price} ')
            # 平多价差
            elif dom_num > 0 and next_num < 0 and bar.close_price:
                self.sell(dom_ctr, dom_price, abs(dom_num))
                self.cover(next_ctr, next_price, abs(next_num))
                print(
                    f'平空价差: 卖多： {dom_ctr} 时间 {bar.datetime.date()} 收盘价 {dom_price} . 卖空合约 {next_ctr} 收盘价 {next_price} ')

        # for b in bars:
        #     bar = bars[b]
        #     dom_next_data = self.domNextData[bar.datetime.date()]
        #     longSymbol = dom_next_data['dom']
        #     shortSymbol = dom_next_data['next']
        #
        #     # 主力合约 >0 : long   <0 : short
        #     dom_num = self.get_pos(longSymbol)
        #     # 次主力合约
        #     next_num = self.get_pos(shortSymbol)
        #     # print(f' {str(dom_next_data)}')
        #     if dom_next_data['diff'] <= -150:
        #         print(f' eeee {dom_next_data}')
        #         # 做多价差
        #         if dom_num == 0 and next_num == 0 and bar.close_price:
        #             self.buy(longSymbol, bar.close_price, 1)
        #             self.short(shortSymbol, bar.close_price, 1)
        #
        #             print(f'做多价差 {longSymbol} 时间 {bar.datetime.date()}  收盘价 {bar.close_price} . 做空合约 {shortSymbol} 收盘价 {bar.close_price} ')
        #         # 平空价差
        #         elif next_num > 0 and dom_num < 0:
        #             self.sell(longSymbol, bar.close_price, abs(dom_num))
        #             self.cover(shortSymbol, bar.close_price, abs(next_num))
        #             print(f'平空价差: 卖多： {longSymbol} 时间 {bar.datetime.date()} 收盘价 {bar.close_price} . 卖空合约 {shortSymbol} 收盘价 {bar.close_price} ')
        #         pass
        """"""
        # self.cancel_all()
        # print(f' all bars== {bars}')
        # # Return if one leg data is missing
        # if self.leg1_symbol not in bars or self.leg2_symbol not in bars:
        #     return
        #
        # # Calculate current spread
        # leg1_bar = bars[self.leg1_symbol]
        # leg2_bar = bars[self.leg2_symbol]
        #
        # # Filter time only run every 5 minutes
        # if (leg1_bar.datetime.minute + 1) % 5:
        #     return
        #
        # self.current_spread = (
        #     leg1_bar.close_price * self.leg1_ratio - leg2_bar.close_price * self.leg2_ratio
        # )
        #
        # # Update to spread array
        # self.spread_data[:-1] = self.spread_data[1:]
        # self.spread_data[-1] = self.current_spread
        #
        # self.spread_count += 1
        # if self.spread_count <= self.boll_window:
        #     return
        #
        # # Calculate boll value
        # buf: np.array = self.spread_data[-self.boll_window:]
        #
        # std = buf.std()
        # self.boll_mid = buf.mean()
        # self.boll_up = self.boll_mid + self.boll_dev * std
        # self.boll_down = self.boll_mid - self.boll_dev * std
        #
        # # Calculate new target position
        # leg1_pos = self.get_pos(self.leg1_symbol)
        #
        # if not leg1_pos:
        #     if self.current_spread >= self.boll_up:
        #         self.targets[self.leg1_symbol] = -1
        #         self.targets[self.leg2_symbol] = 1
        #     elif self.current_spread <= self.boll_down:
        #         self.targets[self.leg1_symbol] = 1
        #         self.targets[self.leg2_symbol] = -1
        # elif leg1_pos > 0:
        #     if self.current_spread >= self.boll_mid:
        #         self.targets[self.leg1_symbol] = 0
        #         self.targets[self.leg2_symbol] = 0
        # else:
        #     if self.current_spread <= self.boll_mid:
        #         self.targets[self.leg1_symbol] = 0
        #         self.targets[self.leg2_symbol] = 0
        #
        # # Execute orders
        # for vt_symbol in self.vt_symbols:
        #     target_pos = self.targets[vt_symbol]
        #     current_pos = self.get_pos(vt_symbol)
        #
        #     pos_diff = target_pos - current_pos
        #     volume = abs(pos_diff)
        #     bar = bars[vt_symbol]
        #
        #     if pos_diff > 0:
        #         price = bar.close_price + self.price_add
        #
        #         if current_pos < 0:
        #             self.cover(vt_symbol, price, volume)
        #         else:
        #             self.buy(vt_symbol, price, volume)
        #     elif pos_diff < 0:
        #         price = bar.close_price - self.price_add
        #
        #         if current_pos > 0:
        #             self.sell(vt_symbol, price, volume)
        #         else:
        #             self.short(vt_symbol, price, volume)

        self.put_event()
