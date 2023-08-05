from evmos.revenue.v1 import revenue_pb2 as _revenue_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['params', 'revenues']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    REVENUES_FIELD_NUMBER: _ClassVar[int]
    params: Params
    revenues: _containers.RepeatedCompositeFieldContainer[_revenue_pb2.Revenue]

    def __init__(self, params: _Optional[_Union[Params, _Mapping]]=..., revenues: _Optional[_Iterable[_Union[_revenue_pb2.Revenue, _Mapping]]]=...) -> None:
        ...

class Params(_message.Message):
    __slots__ = ['addr_derivation_cost_create', 'developer_shares', 'enable_revenue']
    ADDR_DERIVATION_COST_CREATE_FIELD_NUMBER: _ClassVar[int]
    DEVELOPER_SHARES_FIELD_NUMBER: _ClassVar[int]
    ENABLE_REVENUE_FIELD_NUMBER: _ClassVar[int]
    addr_derivation_cost_create: int
    developer_shares: str
    enable_revenue: bool

    def __init__(self, enable_revenue: bool=..., developer_shares: _Optional[str]=..., addr_derivation_cost_create: _Optional[int]=...) -> None:
        ...