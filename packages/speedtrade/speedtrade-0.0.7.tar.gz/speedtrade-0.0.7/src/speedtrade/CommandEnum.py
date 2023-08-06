from enum import Enum

class CommandEnum(Enum):
    Transaction = 0
    Replay = 1
    NewCapital = 2
    NewSimulator = 3
    Select = 4
    Monitor = 5
    OrderAccept = 6
    OrderSold = 7
    OrderCancel = 14
    SignalRInit = 8
    SignalRClose = 9
    Ping = 10
    Pong = 11
    NewSino = 12
    NewKGI = 13
    Error = 15
    ReloadAll = 16
    ReloadCapital = 17
    ReloadSimulator = 18
    ReloadSino = 19
    ReloadKGI = 20
    CloseWindow = 91