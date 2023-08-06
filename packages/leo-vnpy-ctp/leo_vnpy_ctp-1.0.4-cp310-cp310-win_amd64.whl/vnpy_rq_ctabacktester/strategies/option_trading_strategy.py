import os
from datetime import datetime
from typing import Dict, Any

import pandas as pd
import quantstats as qs
from pandas import DataFrame

from client_server.object import BuildVtSymbols
from vnpy.trader.constant import Interval, Offset
from vnpy.trader.object import BarData, TradeData
from vnpy_rq_ctabacktester.myutils2 import OptionUtils
from vnpy_rq_ctabacktester.rq_template import RqStrategyTemplate


class OptionTradingStrategy(RqStrategyTemplate):
    """"""

    author = "期权分钟交易!!!"

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
    # start_date = '20210101'
    # end_date = '20230101'
    start_date = '20220726'
    end_date = '20220801'
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
            strategy_engine: Any,
            strategy_name: str,
            setting: dict
    ):
        """"""
        super().__init__(strategy_engine, strategy_name, setting)
        self.trades = []
        self.m = None
        # self.trades = []
        print(f'开始加载回测时间: {datetime.now()}')
        self.active = 1

    #
    def on_build(self):
        self.write_log("可在此函数里面找对应和合约以及组装因子数据，一次性算好有助于提高回测性能")
        # 返回合约列表，合约乘数的结构对象
        self.m = OptionUtils(self.rpc_engine, self.backtester_engine, self.start_date, self.end_date)
        # m.download2('IM2306', Interval.MINUTE, datetime.strptime('20230314', '%Y%m%d'), datetime.strptime('20230315', '%Y%m%d'))
        # b: BuildVtSymbols = self.m.findAllSymbols(underlying='CU', interval=Interval.MINUTE)
        # self.m.download_symbol()
        b: BuildVtSymbols = self.m.find_symbol_fromdb(Interval.MINUTE)
        # self.m.update_ma(Interval.DAILY, 60)
        # m.checkTradeSymbolByDate()
        return b

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化完成: 是在bar数据加载完毕后调用, 看还有啥要做的")

        # self.strategy_engine.main_engine.subscribe()
        self.load_bars(1)

    def before_trade(self, dt: datetime) -> None:
        """
        开盘前
        """
        print(f'开盘前回调 {dt}')
        self.active = 1
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

    def on_complete(self, daily_df: DataFrame,
                    statistics: dict) -> None:
        print(f'{self.orders}')
        daily_df.index = pd.to_datetime(daily_df.index)

        pwd = os.path.dirname(__file__)
        path = pwd + '\\abbb.xlsx'
        # 三个同时导出
        writer = self.export_trades(filename=path)
        self.export_orders(filename=path, writer=writer)
        self.export_daily_results(filename=path, writer=writer, df=daily_df)
        # 最后保存一次即可
        writer.save()

        qs.reports.html(daily_df['return'], output='stats.html', title='Options Sentiment')
        pass

    def on_bars(self, bars: Dict[str, BarData]):
        # print(f'持仓 {self.pos} 合约：{str(bars)}  ')
        cur_d_time = bars[list(bars.keys())[0]].datetime
        # print(f'到bar时间: {cur_d_time}')
        # 当前持仓判断止损
        if cur_d_time.time() == datetime(2022, 7, 30, 0, 55, 0).time():
            pass
        # if cur_d_time.time() == datetime(2022, 7, 27, 9, 30, 0).time():
        #     pass
        if cur_d_time.date() == datetime(2022, 11, 28).date():
            pass
        # 凌晨3点到9点之间数据不处理
        # if cur_d_time.hour < 9:
        #     return
        if cur_d_time.hour == 9 and cur_d_time.minute < 30:
            return

        # 查看是否成交，根据订单合计卖开合约
        if self.active != 1:
            # 当日不激活，一般是平仓了数据
            # print(f'{cur_d_time} 未激活，当日操作过？ {self.active}')
            return

        # 判断 止损
        for vt_symbol in list(self.pos.keys()):
            count = self.get_pos(vt_symbol)
            if count == 0:
                continue
            end_days = (datetime.strptime(self.m.option_symbol_data[vt_symbol]['maturity_date'],
                                          "%Y-%m-%d").date() - cur_d_time.date()).days
            if vt_symbol not in bars:
                continue
            b = bars[vt_symbol]
            if end_days == 0:
                print(f'到期日止损平仓=>  {vt_symbol} {b.close_price} {abs(count)}')
                self.cover(vt_symbol, b.close_price, abs(count))
                self.active = 0
                return
            # 判断是否超过止损
            trade = list(filter(lambda x: x.symbol == vt_symbol.split('.')[0] and x.offset == Offset.OPEN, self.trades))
            # print(f'分钟收盘价：{ b.close_price} 3倍下单时候的合约价格： {3 * trade[0].price}')
            if count != 0 and len(trade) > 0 and b.close_price > 3 * trade[0].price:
                # 大于三倍止损
                print(f"{cur_d_time} 大于三倍止损 {vt_symbol} 止损价格 {b.close_price} 数量 {count}")
                self.cover(vt_symbol, b.close_price, abs(count))
                self.active = 0
                return

        if cur_d_time.date() not in self.m.option_symbol_dates:
            return

        cur_open_data = self.m.option_symbol_dates[cur_d_time.date()]

        if 'option_code' not in cur_open_data or str(cur_open_data['option_code']) == 'nan':
            # print(f'{cur_d_time.date()} option_code 不在 m.cur_open_data 或者nan')
            return
        # 只要有持仓就不开仓，一直等到止损或者行权
        # 所有的持仓数量，为0 则都不持仓
        has_pos_count = 0
        for s in self.pos:
            has_pos_count += abs(self.get_pos(s))

        if has_pos_count == 0:
            for s in bars:
                # 要卖开的合约
                # if s in bars:
                b: BarData = bars[s]
                # 找到这天应该开仓得合约是啥
                if 'option_code' in cur_open_data and cur_open_data['option_code'] == b.vt_symbol and self.get_pos(
                        cur_open_data['option_code']) == 0:
                    # 模拟指定开仓时间 if cur_d_time.hour == 9
                    if cur_d_time.hour == 9:
                        # 卖开
                        print(
                            f'{cur_d_time}==> 卖开 {cur_open_data["option_code"]}, 分钟收盘价：{b.close_price} 开仓时间: {cur_d_time}')
                        self.short(cur_open_data["option_code"], b.close_price, 1)
                        self.active = 0

        self.put_event()

    def on_trade(self, trade: TradeData, symbol: str):
        """
        Callback of new trade data update.
        """
        print(f' on_trade {trade}')
        # self.active = 0
        # if trade.offset != Offset.CLOSE:
        if trade:
            self.trades.append(trade)
        # date = trade.datetime.date()
        # # 'maturity_date': c_maturity_date,
        # # 'end_days': (datetime.strptime(c_maturity_date, "%Y-%m-%d").date() - d).days,  # 结束日期
        # # 成交的订单
        # self.trades.append({
        #     **trade.__dict__,
        #     'c_maturity_date': self.m.option_symbol_dates[date].c_maturity_date,
        # })
        # trade.vt_symbol
        # self.orders
        self.put_event()
