from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryBalancesRequest(_message.Message):
    __slots__ = ['address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str

    def __init__(self, address: _Optional[str]=...) -> None:
        ...

class QueryBalancesResponse(_message.Message):
    __slots__ = ['locked', 'unvested', 'vested']
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    UNVESTED_FIELD_NUMBER: _ClassVar[int]
    VESTED_FIELD_NUMBER: _ClassVar[int]
    locked: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    unvested: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    vested: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, locked: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., unvested: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., vested: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...