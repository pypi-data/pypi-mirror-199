import datetime

gridNum = 1
gridParam = 7

underlying = None
previousDayStr = None
import rqdatac as rq
import pandas as pd

from interval import Interval

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


# ivObj = findIv(iv)
# indexRange,startbuy, startsell
# print(str(ivObj))
def ResetPrice(originalPrice):
    reprice = round(originalPrice, 4)
    return reprice


def refindGG(gg):
    for i in range(0, 10000):
        v = 30 + 10 * i
        if v >= gg:
            return v


def findCurMonthContractss(underlying, type='C', date=None):
    from itertools import groupby
    contracts = rq.options.get_contracts(underlying=underlying, option_type=type, strike=None, trading_date=date)
    i = rq.instruments(contracts)
    insSorted = sorted(i, key=lambda x: (x.maturity_date))
    insGrouped = groupby(insSorted, key=lambda x: (x.maturity_date))
    # list(insGrouped.values)
    checkContractObjs = []
    checkContracts = []
    for key, group in insGrouped:
        checkContractObjs = list(group)
        break
    return [c.order_book_id for c in checkContractObjs]


def findnextmonthContracts(underlying, type='C', date=None):  # underlying 只要写品种名称就行，不用具体到月份
    contracts = rq.options.get_contracts(underlying=underlying, option_type=type, strike=None, trading_date=date)
    # print(contracts)
    m_date = []
    for op in contracts:
        i1 = rq.instruments(op)
        md = i1.maturity_date
        tc = i1.trading_code
        m_date.append({"trading_code": tc, "maturity_date": md})
    m_df = pd.DataFrame(m_date)
    m_df1 = m_df['maturity_date'].unique()
    # print('合约到期日',m_df1)
    nextmonthdate = m_df1[1][2:4] + m_df1[1][5:7]
    nextmonthcontracts = rq.options.get_contracts(underlying=underlying, option_type=type,
                                                  strike=None, maturity=nextmonthdate, trading_date=date)
    return nextmonthcontracts


def findCurMonthContracts(type='C', date=None):
    from itertools import groupby
    contracts = rq.options.get_contracts(underlying=underlying, option_type=type, strike=None, trading_date=date)
    i = rq.instruments(contracts)
    insSorted = sorted(i, key=lambda x: (x.maturity_date))
    insGrouped = groupby(insSorted, key=lambda x: (x.maturity_date))
    # list(insGrouped.values)
    checkContractObjs = []
    checkContracts = []
    for key, group in insGrouped:
        checkContractObjs = list(group)
        break
    return [c.order_book_id for c in checkContractObjs]


def findLastClose(bookId, date):
    # previousDay = rq.get_previous_trading_date(date.replace('-', ''), n=1)
    # previousDayStr = datetime.datetime.strftime(previousDay, '%Y%m%d')
    previousPriceDf = rq.get_price(order_book_ids=bookId, start_date=previousDayStr, end_date=previousDayStr,
                                   frequency='1d', fields='close', adjust_type='none')
    return previousPriceDf.loc[:, ('close')][-1]


def findPingValue(underlyingPrice=None, type='C', date=None):
    contracts = findCurMonthContractss(underlying, type, date)
    # contracts = rq.options.get_contracts(underlying=bd, option_type=type, maturity='2212', strike=None, trading_date=date)
    # 取期权合约的属性
    df = rq.options.get_contract_property(contracts, start_date=date, end_date=date, fields=None, market='cn')

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
    return pingContract


def yesterdayIv(dateStr):
    import pandas as pd
    ivdata = pd.read_excel('50ETFivforzg.xlsx', header=3)
    ivdata.set_index('Date', inplace=True)
    return ivdata.loc[dateStr, 'pre_close']


def findIv(iv):
    print(f'表格里找 pre_close {iv}')
    for ind, item in enumerate(iss.keys()):
        if iv in item:
            return iss[item]
    return {
        "indexRange": 0.03,
        "startbuy": 0,
        "startsell": 500
    }


def build4Contracts(bd, date):
    ivObj = findIv(yesterdayIv(date))
    global underlying
    underlying = bd

    previousDay = rq.get_previous_trading_date(date.replace('-', ''), n=1)
    global previousDayStr
    previousDayStr = datetime.datetime.strftime(previousDay, '%Y%m%d')
    print(f'前一交易日{previousDayStr}')
    pricedf = rq.get_price(order_book_ids=underlying, start_date=previousDayStr, end_date=previousDayStr,
                           adjust_type='none')
    underlyingPrice = pricedf['close'][0]
    print('标的收盘价', underlyingPrice)

    subCodes = []
    cIndex, cContract, df = findPingValue(underlyingPrice, 'C', date)
    # df[pingIndex-1:pingIndex]['']
    print(f'认购平值索引{cIndex}, 平值合约{cContract}')
    # print(f'认购：{df}')
    # print('1111', df[cIndex:cIndex]['order_book_id'][0])
    subCodes = [{
        # 实值一档
        'code': df[cIndex - 1:cIndex]['order_book_id'].iloc[-1],
        "type": 'itm',
        "direct": 0
    }, {
        # 虚值一档
        'code': df[cIndex + 1:cIndex + 2]['order_book_id'].iloc[-1],
        "direct": 0,
        "type": 'otm'
    }, {
        'code': cContract,
        "direct": 0,
        "type": 'atm'
    }
    ]

    pIndex, pContract, df = findPingValue(underlyingPrice, 'P', date)
    # print(f'认沽：{df}')
    print(f'认沽平值索引{pIndex}, 平值合约{pContract}')

    subCodes.extend([{
        # 虚值一档
        'code': df[pIndex - 1:pIndex]['order_book_id'].iloc[-1],
        "direct": 1,
        "type": 'otm'
    }, {
        # 实值一档
        'code': df[pIndex + 1:pIndex + 2]['order_book_id'].iloc[-1],
        "direct": 1,
        "type": 'itm'
    }, {
        'code': pContract,
        "direct": 0,
        "type": 'atm'
    }])
    greeks = rq.options.get_greeks([i['code'] for i in subCodes], start_date=date, end_date=date)
    bdLastClose = findLastClose(underlying, date)
    if greeks is None:
        print(f'请检查合约列表 {[i["code"] for i in subCodes]} 查询时间{date}')
        return []
    for c in subCodes:
        # previousPriceDf = rq.get_price(order_book_ids=s['code'], start_date=previousDayStr, end_date=previousDayStr, frequency='1d', fields='close')
        c['lastClose'] = findLastClose(c['code'], date)
        c['optionDelta'] = greeks.loc[c['code'], ('delta')][-1]
        c['startbuy'] = ivObj['startbuy']
        c['startsell'] = ivObj['startsell']
        c['indexRange'] = ivObj['indexRange']
        c['start'] = 0
        c['lever'] = refindGG(bdLastClose / c['lastClose'] * abs(c['optionDelta']))
        c['gridPrice'] = c['lastClose'] * ivObj['indexRange'] * c['lever'] / gridParam
        # print('==> gridPrice',c['gridPrice'],'lever',c['lever'] )
        if c['type'] == 'otm':
            # H标记在高位 L在低位 closeOrderId 用来记住平仓单的id orderPosStatus 0 未成交 1 成交
            c['gridPriceList'] = [
                {"ind": i, "prices": [], "closeOrderId": None, "enterStatus": 0, "active": 0, "closeStatus": 0,
                 "orderPos": "H", "price": ResetPrice(c['lastClose'] + c['gridPrice'] * (ivObj['startsell'] + (i + 1)))}
                for i in range(0, gridNum)]
        else:
            c['gridPriceList'] = [{"ind": i, "closeOrderId": None, "enterStatus": 0, "orderPos": "H", "active": 0,
                                   "price": ResetPrice(c['lastClose'] + c['gridPrice'] * (ivObj['startbuy'] + (i + 1)))}
                                  for i in range(0, gridNum)]

        # print("gridpricelist",c['gridPriceList'])
    # for s in subCodes:
    #     filter(lambda x: x['code'] == )
    # print(f'找到合约{subCodes}')
    return subCodes
