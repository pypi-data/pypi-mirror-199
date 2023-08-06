import datetime
from queue import Empty, Queue
from threading import Thread
from typing import Any

from client_server.base_define import APP_rqsdk
from vnpy.event import EventEngine
from vnpy.trader.engine import BaseEngine, MainEngine
from vnpy.trader.gateway import BaseGateway


class RqsdkRpcEngine(BaseEngine):
    """
    Provides rpc（rqsdk）function.
    """

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        """"""
        super(RqsdkRpcEngine, self).__init__(main_engine, event_engine, APP_rqsdk)

        self.queue: Queue = Queue()
        self.active: bool = False

    # 有的是异步发起
    def __getattr__(self, name: str) -> Any:
        def start_rpc_request(*args, **kwargs):
            if "thread" in kwargs:
                timeout = kwargs.pop("thread")
                self.thread: Thread = Thread(target=self.run, args=(name, *args), kwargs=kwargs)
                self.start()
            else:
                print("不使用线程")
                # 不需要线程,直接发起
                return self.run(name, *args, **kwargs)

        return start_rpc_request

    def run(self, name, *args, **kwargs) -> None:
        """"""
        # while self.active:
        try:
            gateway: BaseGateway = self.main_engine.get_gateway("RPC")
            print(f"{datetime.datetime.now()} --> 发起客户端rpc请求: {name} ")
            if gateway:
                return getattr(gateway, name)(*args, **kwargs)
        except Empty:
            pass

    def start(self) -> None:
        """"""
        self.active = True
        self.thread.start()

    def close(self) -> None:
        """"""
        if not self.active:
            return

        self.active = False
        self.thread.join()
