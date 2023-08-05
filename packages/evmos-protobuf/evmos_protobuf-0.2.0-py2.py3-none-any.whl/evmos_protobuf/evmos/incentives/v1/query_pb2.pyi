from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from evmos.incentives.v1 import genesis_pb2 as _genesis_pb2
from evmos.incentives.v1 import incentives_pb2 as _incentives_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryAllocationMeterRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class QueryAllocationMeterResponse(_message.Message):
    __slots__ = ['allocation_meter']
    ALLOCATION_METER_FIELD_NUMBER: _ClassVar[int]
    allocation_meter: _coin_pb2.DecCoin

    def __init__(self, allocation_meter: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]]=...) -> None:
        ...

class QueryAllocationMetersRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryAllocationMetersResponse(_message.Message):
    __slots__ = ['allocation_meters', 'pagination']
    ALLOCATION_METERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    allocation_meters: _containers.RepeatedCompositeFieldContainer[_coin_pb2.DecCoin]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, allocation_meters: _Optional[_Iterable[_Union[_coin_pb2.DecCoin, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryGasMeterRequest(_message.Message):
    __slots__ = ['contract', 'participant']
    CONTRACT_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    contract: str
    participant: str

    def __init__(self, contract: _Optional[str]=..., participant: _Optional[str]=...) -> None:
        ...

class QueryGasMeterResponse(_message.Message):
    __slots__ = ['gas_meter']
    GAS_METER_FIELD_NUMBER: _ClassVar[int]
    gas_meter: int

    def __init__(self, gas_meter: _Optional[int]=...) -> None:
        ...

class QueryGasMetersRequest(_message.Message):
    __slots__ = ['contract', 'pagination']
    CONTRACT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    contract: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, contract: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryGasMetersResponse(_message.Message):
    __slots__ = ['gas_meters', 'pagination']
    GAS_METERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    gas_meters: _containers.RepeatedCompositeFieldContainer[_incentives_pb2.GasMeter]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, gas_meters: _Optional[_Iterable[_Union[_incentives_pb2.GasMeter, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryIncentiveRequest(_message.Message):
    __slots__ = ['contract']
    CONTRACT_FIELD_NUMBER: _ClassVar[int]
    contract: str

    def __init__(self, contract: _Optional[str]=...) -> None:
        ...

class QueryIncentiveResponse(_message.Message):
    __slots__ = ['incentive']
    INCENTIVE_FIELD_NUMBER: _ClassVar[int]
    incentive: _incentives_pb2.Incentive

    def __init__(self, incentive: _Optional[_Union[_incentives_pb2.Incentive, _Mapping]]=...) -> None:
        ...

class QueryIncentivesRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryIncentivesResponse(_message.Message):
    __slots__ = ['incentives', 'pagination']
    INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    incentives: _containers.RepeatedCompositeFieldContainer[_incentives_pb2.Incentive]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, incentives: _Optional[_Iterable[_Union[_incentives_pb2.Incentive, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
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