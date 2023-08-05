#  =============================================================================
#  GNU Lesser General Public License (LGPL)
#
#  Copyright (c) 2022 Qujamlee from www.aztquant.com
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  =============================================================================
class QujamException(Exception):
    _msg = "未知错误"

    @classmethod
    def __err__(cls):
        return cls._msg


# 尚未连接服务
class UnconnectedError(QujamException):
    _msg = "尚未连接服务"


# 服务器连接失败
class ConnectedFailed(QujamException):
    _msg = "服务连接失败"


# 服务器连接中断
class ConnectedBroken(QujamException):
    _msg = "服务连接中断"


# 尚未登录
class NotLoginedError(QujamException):
    _msg = "尚未登录"


# 非交易时间
class NonTradingTimeError(QujamException):
    _msg = "当前非交易时间"


# 时间格式错误
class DatetimeTypeError(QujamException):
    _msg = "时间格式错误"


# 列表格式错误
class ListTypeError(QujamException):
    _msg = "列表格式错误"


# 字典格式错误
class DictTypeError(QujamException):
    _msg = "字典格式错误"


# 参数错误
class ArgsError(QujamException):
    _msg = "参数错误"


# 错误的行情数据
class MarketDataError(QujamException):
    _msg = "错误的行情数据"


# 订阅失败
class SubscribeError(QujamException):
    _msg = "订阅失败"


# 退订失败
class UnsubscribeError(QujamException):
    _msg = "取消订阅失败"


class CloseSocketZmq(QujamException):
    _msg = "主动断开与zmq服务端的连接"


class CloseSocket(QujamException):
    _msg = "主动断开与服务端的连接"
