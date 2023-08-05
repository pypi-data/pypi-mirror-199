from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from evmos.erc20.v1 import genesis_pb2 as _genesis_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgConvertCoin(_message.Message):
    __slots__ = ['coin', 'receiver', 'sender']
    COIN_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    coin: _coin_pb2.Coin
    receiver: str
    sender: str

    def __init__(self, coin: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., receiver: _Optional[str]=..., sender: _Optional[str]=...) -> None:
        ...

class MsgConvertCoinResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgConvertERC20(_message.Message):
    __slots__ = ['amount', 'contract_address', 'receiver', 'sender']
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    amount: str
    contract_address: str
    receiver: str
    sender: str

    def __init__(self, contract_address: _Optional[str]=..., amount: _Optional[str]=..., receiver: _Optional[str]=..., sender: _Optional[str]=...) -> None:
        ...

class MsgConvertERC20Response(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgUpdateParams(_message.Message):
    __slots__ = ['authority', 'params']
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    authority: str
    params: _genesis_pb2.Params

    def __init__(self, authority: _Optional[str]=..., params: _Optional[_Union[_genesis_pb2.Params, _Mapping]]=...) -> None:
        ...

class MsgUpdateParamsResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...