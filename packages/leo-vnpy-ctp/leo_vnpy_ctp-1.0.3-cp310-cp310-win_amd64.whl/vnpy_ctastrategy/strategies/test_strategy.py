from client_server.base_define import APP_rqsdk
from client_server.rqsdk_engine import RqsdkRpcEngine
from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)


class TestStrategy(CtaTemplate):
    """"""

    author = "用Python的交易员"

    boll_window = 18
    boll_dev = 3.4
    cci_window = 10
    atr_window = 30
    sl_multiplier = 5.2
    fixed_size = 1
    start_date = '20210115'

    boll_up = 0
    boll_down = 0
    cci_value = 0
    atr_value = 0

    intra_trade_high = 0
    intra_trade_low = 0
    long_stop = 0
    short_stop = 0

    parameters = [
        "boll_window",
        "boll_dev",
        "cci_window",
        "atr_window",
        "sl_multiplier",
        "fixed_size",
        "start_date",
    ]
    variables = [
        "boll_up",
        "boll_down",
        "cci_value",
        "atr_value",
        "intra_trade_high",
        "intra_trade_low",
        "long_stop",
        "short_stop"
    ]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        startDate = '2020-10-10'
        endDate = '2022-10-12'
        # self.write_log('123123123123')
        # rq.init()
        # date = '20221010'
        # contracts = ['10004497', '10004498', '10004499', '10004500', '10004501', '10004502', '10004503', '10004504',
        #              '10004505', '10004587']
        # # # dd = rq.options.get_contract_property(contracts, start_date=date, end_date=date, fields=None, market='cn')
        # dd = self.query_datafeed().query_contract_property(contracts, start_date=date, end_date=None, fields=None, market='cn')
        # print(dd)
        # global buildSymbols
        # 试着从RQSDK的引擎中远程获取数据
        self.rpc_engine: RqsdkRpcEngine = self.main_engine.get_engine(APP_rqsdk)
        dd = self.rpc_engine.get_contract_property(order_book_ids=['10002752'], start_date=self.start_date, end_date='20210118')
        print(dd)
        # 默认米筐目前会过滤掉这几种，所以要注意 '510050.XSHG', '510300.XSHG', '159919.XSHE'
        # print(f'vt_symbol: {vt_symbol}')
        # super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        # print(f"###############1")
        # self.buildSymbols = BuildSymbols(self.query_datafeed())
        # codes = self.buildSymbols.buildBackTestContracts('510050.XSHG', startDate, endDate)
        # self.update_symbols([c['code'] for c in codes])
        self.load_bar(10)
        print(f"###############2")
        #
        # # self.write_log(str(codes))
        # print(f'回测得所有合约 {codes}')
        self.bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)
        self.am = ArrayManager()

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化!!!!!!!!!!!!!!")
        self.load_bar(10)

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
        print(f'on_tick {tick}')
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        print(f'on_bar: {bar}')
        self.bg.update_bar(bar)

    def on_15min_bar(self, bar: BarData):
        print(f'on_15min_bar: {bar}')
        """"""
        self.cancel_all()

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        self.boll_up, self.boll_down = am.boll(self.boll_window, self.boll_dev)
        self.cci_value = am.cci(self.cci_window)
        self.atr_value = am.atr(self.atr_window)

        if self.pos == 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = bar.low_price

            if self.cci_value > 0:
                self.buy(self.boll_up, self.fixed_size, True)
            elif self.cci_value < 0:
                self.short(self.boll_down, self.fixed_size, True)

        elif self.pos > 0:
            self.intra_trade_high = max(self.intra_trade_high, bar.high_price)
            self.intra_trade_low = bar.low_price

            self.long_stop = self.intra_trade_high - self.atr_value * self.sl_multiplier
            self.sell(self.long_stop, abs(self.pos), True)

        elif self.pos < 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = min(self.intra_trade_low, bar.low_price)

            self.short_stop = self.intra_trade_low + self.atr_value * self.sl_multiplier
            self.cover(self.short_stop, abs(self.pos), True)

        self.put_event()

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass