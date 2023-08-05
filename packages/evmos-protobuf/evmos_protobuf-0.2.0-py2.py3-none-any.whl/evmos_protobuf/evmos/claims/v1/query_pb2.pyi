from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from evmos.claims.v1 import claims_pb2 as _claims_pb2
from evmos.claims.v1 import genesis_pb2 as _genesis_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryClaimsRecordRequest(_message.Message):
    __slots__ = ['address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str

    def __init__(self, address: _Optional[str]=...) -> None:
        ...

class QueryClaimsRecordResponse(_message.Message):
    __slots__ = ['claims', 'initial_claimable_amount']
    CLAIMS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_CLAIMABLE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    claims: _containers.RepeatedCompositeFieldContainer[_claims_pb2.Claim]
    initial_claimable_amount: str

    def __init__(self, initial_claimable_amount: _Optional[str]=..., claims: _Optional[_Iterable[_Union[_claims_pb2.Claim, _Mapping]]]=...) -> None:
        ...

class QueryClaimsRecordsRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryClaimsRecordsResponse(_message.Message):
    __slots__ = ['claims', 'pagination']
    CLAIMS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    claims: _containers.RepeatedCompositeFieldContainer[_claims_pb2.ClaimsRecordAddress]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, claims: _Optional[_Iterable[_Union[_claims_pb2.ClaimsRecordAddress, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
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

class QueryTotalUnclaimedRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryTotalUnclaimedResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...