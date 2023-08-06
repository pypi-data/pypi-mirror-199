from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

from vnpy.trader.constant import Interval


@dataclass
class SymbolBasicData:
    """
    """
    underlying_symbol: str
    price_tick: float = 0
    contract_multiplier: float = 0
    limit_volume: float = 0

# 提前算好合约的回测数据结构
@dataclass
class BuildVtSymbols:
    vt_symbols: List[str]
    interval: Interval
    start: datetime
    end: datetime
    rates: Dict[str, float]
    slippages: Dict[str, float]
    sizes: Dict[str, float]
    priceticks: Dict[str, float]
    capital: int = 0
    risk_free: float = 0


@dataclass
class FutureRuleData:
    """
    """
    # 交易所
    exchange: str
    datetime: datetime
    # 品种
    underlying_symbol: str
    # 品种
    underlying_symbol_name: str
    # 涨跌停板幅度
    range: float = 0
    # 限价单每笔最大
    limit_volume: float = 0
    # 合约乘数
    contract_multiplier: float = 0
    # 最小变动价位
    price_tick: float = 0
    # 交易保证金比例
    margin_rate: float = 0
    remark: str = 0

    def __init__(self) -> None:
        pass
