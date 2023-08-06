# VeighNa框架的CTP底层接口
## 改动过，针对rpc做扩展
- 支持远程rpc到server，查询米筐数据
- 除了get_contract_option方法自定义了，其他方法和米筐使用方式一样
- 需要手动装下talib  ![img.png](img.png)
```
from client_server.rpc import RpcCli
cli = RpcCli()
df = cli.rpc.get_contract_property(order_book_ids=['10002752'], start_date='20200101',end_date='20210118')
cli.rpc.get_price('000001.XSHE', start_date='2015-04-01', end_date='2015-04-03', adjust_type='none',expect_df=True)


cli.init_backtester()
filter = {"ma_param":60}
cli.load_local_data(table_name='symbol_ma', filter=filter)
```

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-6.6.7.0-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.7|3.8|3.9|3.10-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## 说明

基于CTP期货版的6.6.7接口封装开发，接口中自带的是【穿透式实盘环境】的dll文件。

## 安装

安装环境推荐基于3.3.0版本以上的【[**VeighNa Studio**](https://www.vnpy.com)】。

直接使用pip命令：

```
pip install vnpy_ctp
```


或者下载源代码后，解压后在cmd中运行：

```
pip install .
```

使用源代码安装时需要进行C++编译，因此在执行上述命令之前请确保已经安装了【Visual Studio（Windows）】或者【GCC（Linux）】编译器。

## 使用

以脚本方式启动（script/run.py）：

```
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctp import CtpGateway


def main():
    """主入口函数"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(CtpGateway)
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
```
