from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from ethermint.evm.v1 import evm_pb2 as _evm_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class AccessListTx(_message.Message):
    __slots__ = ['accesses', 'chain_id', 'data', 'gas', 'gas_price', 'nonce', 'r', 's', 'to', 'v', 'value']
    ACCESSES_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    GAS_FIELD_NUMBER: _ClassVar[int]
    GAS_PRICE_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    V_FIELD_NUMBER: _ClassVar[int]
    accesses: _containers.RepeatedCompositeFieldContainer[_evm_pb2.AccessTuple]
    chain_id: str
    data: bytes
    gas: int
    gas_price: str
    nonce: int
    r: bytes
    s: bytes
    to: str
    v: bytes
    value: str

    def __init__(self, chain_id: _Optional[str]=..., nonce: _Optional[int]=..., gas_price: _Optional[str]=..., gas: _Optional[int]=..., to: _Optional[str]=..., value: _Optional[str]=..., data: _Optional[bytes]=..., accesses: _Optional[_Iterable[_Union[_evm_pb2.AccessTuple, _Mapping]]]=..., v: _Optional[bytes]=..., r: _Optional[bytes]=..., s: _Optional[bytes]=...) -> None:
        ...

class DynamicFeeTx(_message.Message):
    __slots__ = ['accesses', 'chain_id', 'data', 'gas', 'gas_fee_cap', 'gas_tip_cap', 'nonce', 'r', 's', 'to', 'v', 'value']
    ACCESSES_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    GAS_FEE_CAP_FIELD_NUMBER: _ClassVar[int]
    GAS_FIELD_NUMBER: _ClassVar[int]
    GAS_TIP_CAP_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    V_FIELD_NUMBER: _ClassVar[int]
    accesses: _containers.RepeatedCompositeFieldContainer[_evm_pb2.AccessTuple]
    chain_id: str
    data: bytes
    gas: int
    gas_fee_cap: str
    gas_tip_cap: str
    nonce: int
    r: bytes
    s: bytes
    to: str
    v: bytes
    value: str

    def __init__(self, chain_id: _Optional[str]=..., nonce: _Optional[int]=..., gas_tip_cap: _Optional[str]=..., gas_fee_cap: _Optional[str]=..., gas: _Optional[int]=..., to: _Optional[str]=..., value: _Optional[str]=..., data: _Optional[bytes]=..., accesses: _Optional[_Iterable[_Union[_evm_pb2.AccessTuple, _Mapping]]]=..., v: _Optional[bytes]=..., r: _Optional[bytes]=..., s: _Optional[bytes]=...) -> None:
        ...

class ExtensionOptionsEthereumTx(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class LegacyTx(_message.Message):
    __slots__ = ['data', 'gas', 'gas_price', 'nonce', 'r', 's', 'to', 'v', 'value']
    DATA_FIELD_NUMBER: _ClassVar[int]
    GAS_FIELD_NUMBER: _ClassVar[int]
    GAS_PRICE_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    V_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    gas: int
    gas_price: str
    nonce: int
    r: bytes
    s: bytes
    to: str
    v: bytes
    value: str

    def __init__(self, nonce: _Optional[int]=..., gas_price: _Optional[str]=..., gas: _Optional[int]=..., to: _Optional[str]=..., value: _Optional[str]=..., data: _Optional[bytes]=..., v: _Optional[bytes]=..., r: _Optional[bytes]=..., s: _Optional[bytes]=...) -> None:
        ...

class MsgEthereumTx(_message.Message):
    __slots__ = ['data', 'hash', 'size']
    DATA_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    data: _any_pb2.Any
    hash: str
    size: float

    def __init__(self, data: _Optional[_Union[_any_pb2.Any, _Mapping]]=..., size: _Optional[float]=..., hash: _Optional[str]=..., **kwargs) -> None:
        ...

class MsgEthereumTxResponse(_message.Message):
    __slots__ = ['gas_used', 'hash', 'logs', 'ret', 'vm_error']
    GAS_USED_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    RET_FIELD_NUMBER: _ClassVar[int]
    VM_ERROR_FIELD_NUMBER: _ClassVar[int]
    gas_used: int
    hash: str
    logs: _containers.RepeatedCompositeFieldContainer[_evm_pb2.Log]
    ret: bytes
    vm_error: str

    def __init__(self, hash: _Optional[str]=..., logs: _Optional[_Iterable[_Union[_evm_pb2.Log, _Mapping]]]=..., ret: _Optional[bytes]=..., vm_error: _Optional[str]=..., gas_used: _Optional[int]=...) -> None:
        ...