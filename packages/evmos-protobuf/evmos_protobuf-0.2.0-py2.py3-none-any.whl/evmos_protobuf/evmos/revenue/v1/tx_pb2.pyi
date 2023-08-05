from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from evmos.revenue.v1 import genesis_pb2 as _genesis_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgCancelRevenue(_message.Message):
    __slots__ = ['contract_address', 'deployer_address']
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    contract_address: str
    deployer_address: str

    def __init__(self, contract_address: _Optional[str]=..., deployer_address: _Optional[str]=...) -> None:
        ...

class MsgCancelRevenueResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgRegisterRevenue(_message.Message):
    __slots__ = ['contract_address', 'deployer_address', 'nonces', 'withdrawer_address']
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NONCES_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    contract_address: str
    deployer_address: str
    nonces: _containers.RepeatedScalarFieldContainer[int]
    withdrawer_address: str

    def __init__(self, contract_address: _Optional[str]=..., deployer_address: _Optional[str]=..., withdrawer_address: _Optional[str]=..., nonces: _Optional[_Iterable[int]]=...) -> None:
        ...

class MsgRegisterRevenueResponse(_message.Message):
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

class MsgUpdateRevenue(_message.Message):
    __slots__ = ['contract_address', 'deployer_address', 'withdrawer_address']
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    contract_address: str
    deployer_address: str
    withdrawer_address: str

    def __init__(self, contract_address: _Optional[str]=..., deployer_address: _Optional[str]=..., withdrawer_address: _Optional[str]=...) -> None:
        ...

class MsgUpdateRevenueResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...