import datetime

gridNum = 1
gridParam = 7

underlying = None
previousDayStr = None

from interval import Interval


class BuildSymbols():
    iss = {
        Interval(0, 20, lower_closed=True): {
            "indexRange": 0.015,
            "startbuy": 4,
            "startsell": 500
        },
        Interval(20, 25, lower_closed=True, upper_closed=False): {
            "indexRange": 0.02,
            "startbuy": 3,
            "startsell": 500
        },
        Interval(25, 30, lower_closed=True, upper_closed=False): {
            "indexRange": 0.03,
            "startbuy": 1,
            "startsell": 500
        },
        Interval(30, 40, lower_closed=True, upper_closed=False): {
            "indexRange": 0.03,
            "startbuy": 500,
            "startsell": 500
        },
    }

    def __init__(self, datafeed) -> None:
        super().__init__()
        self.datafeed = datafeed
        # # dd = rq.options.get_contract_property(contracts, start_date=date, end_date=date, fields=None, market='cn')
        # dd = self.datafeed.get_contract_property()(
        #     ['10004497', '10004498', '10004499', '10004500', '10004501', '10004502', '10004503', '10004504', '10004505',
        #      '10004587'], start_date='20221010', end_date='20221020')
        # print('111', dd)
        # dd = self.datafeed.get_contract_property()(
        #     ['10002752'], start_date='20210115', end_date='20210118')
        # print('112', dd)

    # ivObj = findIv(iv)
    # indexRange,startbuy, startsell
    # print(str(ivObj))
    def resetPrice(self, originalPrice):
        reprice = round(originalPrice, 4)
        return reprice

    def refindGG(self, gg):
        for i in range(0, 10000):
            v = 30 + 10 * i
            if v >= gg:
                return v

    def findCurMonthContracts(self, type='C', date=None):
        from itertools import groupby
        contracts = self.datafeed.get_contracts()(underlying=underlying, option_type=type, strike=None,
                                                  trading_date=date)
        i = self.datafeed.instruments()(contracts)
        insSorted = sorted(i, key=lambda x: (x.maturity_date))
        insGrouped = groupby(insSorted, key=lambda x: (x.maturity_date))
        # list(insGrouped.values)
        checkContractObjs = []
        checkContracts = []
        for key, group in insGrouped:
            checkContractObjs = list(group)
            break
        return [c.order_book_id for c in checkContractObjs]

    def findLastClose(self, bookId, date):
        # previousDay = rq.get_previous_trading_date(date.replace('-', ''), n=1)
        # previousDayStr = datetime.datetime.strftime(previousDay, '%Y%m%d')
        previousPriceDf = self.datafeed.get_price()(order_book_ids=bookId, start_date=previousDayStr,
                                                    end_date=previousDayStr,
                                                    frequency='1d', fields='close', adjust_type='none')
        return previousPriceDf.loc[:, ('close')][-1]

    def findPingValue(self, underlyingPrice=None, type='C', date=None):
        contracts = self.findCurMonthContracts(type, date)
        # contracts = rq.options.get_contracts(underlying=bd, option_type=type, maturity='2212', strike=None, trading_date=date)
        # 取期权合约的属性
        # print(f'找平直： {contracts} 日期：{date}')
        df = self.datafeed.get_contract_property()(contracts, start_date=date, end_date=date, fields=None, market='cn')
        # time.sleep(2)
        df['diff'] = df.apply(lambda x: abs(float(x['strike_price']) - float(underlyingPrice)), axis=1)
        # 排序找到平值合约
        df2 = df.sort_values(by='diff', ascending=True, axis=0)
        pingContract = df2.index[0][0]
        print(f'{type} 平值合约：{pingContract}')
        # 方便找到临近的实值和虚值
        df.sort_values(by='strike_price', ascending=True, axis=0, inplace=True)
        df.reset_index(inplace=True)
        pingIndex = df[df['order_book_id'] == pingContract].index[0]
        # df
        return pingIndex, pingContract, df

    def yesterdayIv(self, dateStr):
        import pandas as pd
        ivdata = pd.read_excel('D:\workspace\\vnpy_ctp-main2\\vnpy_ctastrategy\\50ETFivforzg.xlsx', header=3)
        ivdata.set_index('Date', inplace=True)
        return ivdata.loc[dateStr, 'pre_close']

    def findIv(self, iv):
        print(f'表格里找 pre_close {iv}')
        for ind, item in enumerate(self.iss.keys()):
            if iv in item:
                return self.iss[item]
        return {
            "indexRange": 0.03,
            "startbuy": 0,
            "startsell": 500
        }

    def build4Contracts(self, bd, date):
        ivObj = self.findIv(self.yesterdayIv(date))
        global underlying
        underlying = bd

        previousDay = self.datafeed.get_previous_trading_date()(date.replace('-', ''), n=1)
        global previousDayStr
        previousDayStr = datetime.datetime.strftime(previousDay, '%Y%m%d')
        print(f'前一交易日{previousDayStr}')
        pricedf = self.datafeed.get_price()(order_book_ids=underlying, start_date=previousDayStr,
                                            end_date=previousDayStr,
                                            adjust_type='none')
        underlyingPrice = pricedf['close'][0]
        print('标的收盘价', underlyingPrice)

        subCodes = []
        cIndex, cContract, df = self.findPingValue(underlyingPrice, 'C', date.replace('-', ''))
        # df[pingIndex-1:pingIndex]['']
        print(f'认购平值索引{cIndex}, 平值合约{cContract}')
        subCodes = [{
            # 实值一档
            'code': df[cIndex - 1:cIndex]['order_book_id'].iloc[-1],
            "type": 'itm',
            'date': date,
            "direct": 0
        }, {
            # 虚值一档
            'code': df[cIndex + 1:cIndex + 2]['order_book_id'].iloc[-1],
            "direct": 0,
            'date': date,
            "type": 'otm'
        }]
        # print(f'认购：{df}')
        # print('1111', df[cIndex:cIndex]['order_book_id'][0])

        pIndex, pContract, df = self.findPingValue(underlyingPrice, 'P', date)
        # print(f'认沽：{df}')
        print(f'认沽平值索引{pIndex}, 平值合约{pContract}')

        subCodes.extend([{
            # 虚值一档
            'code': df[pIndex - 1:pIndex]['order_book_id'].iloc[-1],
            "direct": 1,
            'date': date,
            "type": 'otm'
        }, {
            # 实值一档
            'code': df[pIndex + 1:pIndex + 2]['order_book_id'].iloc[-1],
            "direct": 1,
            'date': date,
            "type": 'itm'
        }])
        greeks = self.datafeed.get_greeks()([i['code'] for i in subCodes], start_date=date, end_date=date)
        bdLastClose = self.findLastClose(underlying, date)
        if greeks is None:
            print(f'请检查合约列表 {[i["code"] for i in subCodes]} 查询时间{date}')
            return []
        for c in subCodes:
            # previousPriceDf = self.datafeed.get_price(order_book_ids=s['code'], start_date=previousDayStr, end_date=previousDayStr, frequency='1d', fields='close')
            c['lastClose'] = self.findLastClose(c['code'], date)
            c['optionDelta'] = greeks.loc[c['code'], ('delta')][-1]
            c['startbuy'] = ivObj['startbuy']
            c['startsell'] = ivObj['startsell']
            c['indexRange'] = ivObj['indexRange']
            c['start'] = 0
            c['lever'] = self.refindGG(bdLastClose / c['lastClose'] * abs(c['optionDelta']))
            c['gridPrice'] = c['lastClose'] * ivObj['indexRange'] * c['lever'] / gridParam
            # print('==> gridPrice',c['gridPrice'],'lever',c['lever'] )
            if c['type'] == 'otm':
                # H标记在高位 L在低位 closeOrderId 用来记住平仓单的id orderPosStatus 0 未成交 1 成交
                c['gridPriceList'] = [
                    {"ind": i, "prices": [], "closeOrderId": None, "enterStatus": 0, "active": 0, "closeStatus": 0,
                     "orderPos": "H",
                     "price": self.resetPrice(c['lastClose'] + c['gridPrice'] * (ivObj['startsell'] + (i + 1)))}
                    for i in range(0, gridNum)]
            else:
                c['gridPriceList'] = [{"ind": i, "closeOrderId": None, "enterStatus": 0, "orderPos": "H", "active": 0,
                                       "price": self.resetPrice(
                                           c['lastClose'] + c['gridPrice'] * (ivObj['startbuy'] + (i + 1)))}
                                      for i in range(0, gridNum)]

            # print("gridpricelist",c['gridPriceList'])
        # for s in subCodes:
        #     filter(lambda x: x['code'] == )
        # print(f'找到合约{subCodes}')
        return subCodes

    # '20160505'
    def buildBackTestContracts(self, bd, startDate='2016-05-05', endDate='2016-05-15'):

        dates = self.datafeed.get_trading_dates()(start_date=startDate, end_date=endDate)
        print('==========', dates)
        allSubCodes = []
        for d in dates:
            allSubCodes.extend(self.build4Contracts(bd, str(d)))
        return allSubCodes

# codes = buildBackTestContracts('510500.XSHG', '20220505', '20220515')
# print(codes)
