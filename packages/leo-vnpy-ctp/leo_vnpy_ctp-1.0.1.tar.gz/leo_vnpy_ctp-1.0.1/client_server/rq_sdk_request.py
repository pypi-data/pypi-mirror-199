from dataclasses import dataclass


@dataclass
class RqSdkRequest:
    """
    Request sending to specific gateway for subscribing tick data update.
    """

    method: str
    param: ()

    # def __post_init__(self) -> None:
    #     """"""
    #     self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"
