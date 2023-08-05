from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from evmos.revenue.v1 import genesis_pb2 as _genesis_pb2
from evmos.revenue.v1 import revenue_pb2 as _revenue_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryDeployerRevenuesRequest(_message.Message):
    __slots__ = ['deployer_address', 'pagination']
    DEPLOYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    deployer_address: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, deployer_address: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryDeployerRevenuesResponse(_message.Message):
    __slots__ = ['contract_addresses', 'pagination']
    CONTRACT_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    contract_addresses: _containers.RepeatedScalarFieldContainer[str]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, contract_addresses: _Optional[_Iterable[str]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _genesis_pb2.Params

    def __init__(self, params: _Optional[_Union[_genesis_pb2.Params, _Mapping]]=...) -> None:
        ...

class QueryRevenueRequest(_message.Message):
    __slots__ = ['contract_address']
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    contract_address: str

    def __init__(self, contract_address: _Optional[str]=...) -> None:
        ...

class QueryRevenueResponse(_message.Message):
    __slots__ = ['revenue']
    REVENUE_FIELD_NUMBER: _ClassVar[int]
    revenue: _revenue_pb2.Revenue

    def __init__(self, revenue: _Optional[_Union[_revenue_pb2.Revenue, _Mapping]]=...) -> None:
        ...

class QueryRevenuesRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryRevenuesResponse(_message.Message):
    __slots__ = ['pagination', 'revenues']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    REVENUES_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    revenues: _containers.RepeatedCompositeFieldContainer[_revenue_pb2.Revenue]

    def __init__(self, revenues: _Optional[_Iterable[_Union[_revenue_pb2.Revenue, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryWithdrawerRevenuesRequest(_message.Message):
    __slots__ = ['pagination', 'withdrawer_address']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    withdrawer_address: str

    def __init__(self, withdrawer_address: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryWithdrawerRevenuesResponse(_message.Message):
    __slots__ = ['contract_addresses', 'pagination']
    CONTRACT_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    contract_addresses: _containers.RepeatedScalarFieldContainer[str]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, contract_addresses: _Optional[_Iterable[str]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...