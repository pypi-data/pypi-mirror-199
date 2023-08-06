from dataclasses import dataclass
from datetime import datetime
from typing import Any
from .CommandEnum import CommandEnum

@dataclass
class CommandStructure:
    command_id: str
    command: str
    symbol: str
    action: CommandEnum
    parameter: str
    time_stamp: datetime
    trade_date: datetime
    account: str
    take_benefit: str
    stop_loss: str
    strategy_out: str

    def clone(self) -> Any:
        return CommandStructure(
            command_id=self.command_id,
            command=self.command,
            symbol=self.symbol,
            action=self.action,
            parameter=self.parameter,
            time_stamp=self.time_stamp,
            trade_date=self.trade_date,
            account=self.account,
            take_benefit=self.take_benefit,
            stop_loss=self.stop_loss,
            strategy_out=self.strategy_out
        )

    def __init__(self, command_id, command, symbol, action, parameter, time_stamp, trade_date, account, take_benefit, stop_loss, strategy_out):
        self.command_id = command_id
        self.command = command
        self.symbol = symbol
        self.action = action
        self.parameter = parameter
        self.time_stamp = time_stamp
        self.trade_date = trade_date
        self.account = account
        self.take_benefit = take_benefit
        self.stop_loss = stop_loss
        self.strategy_out = strategy_out

    def to_dict(self):
        return {
            'commandid': self.command_id,
            'command': self.command,
            'symbol': self.symbol,
            'action': self.action.value,
            'parameter': self.parameter,
            'timestamp': self.time_stamp.isoformat(),
            'tradedate': self.trade_date.isoformat(),
            'account': self.account,
            'takebenefit': self.take_benefit,
            'stoploss': self.stop_loss,
            'strategyout': self.strategy_out,
        }

    def clone(self):
        return CommandStructure(**self.to_dict())
    
    
    def send_command(self, zmq_handler):
        import json
        source = "PythonClient"
        destination = "PythonClient"
        serialized_metadata = json.dumps(self.to_dict())

        zmq_handler.send_command(source, destination, serialized_metadata)
        return
        
    @staticmethod
    def create(CommandId, Symbol, Account, TakeBEnefit, StopLoss, Action=CommandEnum.NewSimulator):     
        import json   
        # Create an instance of CommandStructure
        command_instance_sub = CommandStructure(
            command_id=CommandId,
            command='SomeCommand',
            symbol=Symbol,
            action=CommandEnum.Select,
            parameter='SomeParameter',
            time_stamp=datetime.now(),
            trade_date=datetime.now(),
            account=Account,
            take_benefit=TakeBEnefit,
            stop_loss=StopLoss,
            strategy_out='SomeStrategyOut'
        )

        command_instance = CommandStructure(
            command_id=CommandId,
            command='SomeCommand',
            symbol=Symbol,
            action=Action,
            parameter='SomeParameter',
            time_stamp=datetime.now(),
            trade_date=datetime.now(),
            account=Account,
            take_benefit=TakeBEnefit,
            stop_loss=StopLoss,
            strategy_out='SomeStrategyOut'
        )

        command_instance.parameter = json.dumps(command_instance_sub.to_dict())
        return command_instance