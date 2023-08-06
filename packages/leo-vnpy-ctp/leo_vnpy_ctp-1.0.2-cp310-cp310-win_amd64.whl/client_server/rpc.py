from typing import Dict

from client_server.rqsdk_engine import RqsdkRpcEngine
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy_rpcservice import RpcGateway


class RpcCli(object):
    """
    Provides rpc（rqsdk）function.
    """

    def __init__(self) -> None:
        event_engine = EventEngine()
        main_engine = MainEngine(event_engine)
        main_engine.add_engine(RqsdkRpcEngine)
        main_engine.add_gateway(RpcGateway)
        default_setting: Dict[str, str] = {
            "主动请求地址": "tcp://139.198.114.163:22014",
            "推送订阅地址": "tcp://139.198.114.163:24102"
        }
        main_engine.connect(default_setting, "RPC")
        self.rpc: RqsdkRpcEngine = main_engine.get_engine("RqsdkEngine")


