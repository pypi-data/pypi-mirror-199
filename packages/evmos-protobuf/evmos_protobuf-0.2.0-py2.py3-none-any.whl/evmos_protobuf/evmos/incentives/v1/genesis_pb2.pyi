from evmos.incentives.v1 import incentives_pb2 as _incentives_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['gas_meters', 'incentives', 'params']
    GAS_METERS_FIELD_NUMBER: _ClassVar[int]
    INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    gas_meters: _containers.RepeatedCompositeFieldContainer[_incentives_pb2.GasMeter]
    incentives: _containers.RepeatedCompositeFieldContainer[_incentives_pb2.Incentive]
    params: Params

    def __init__(self, params: _Optional[_Union[Params, _Mapping]]=..., incentives: _Optional[_Iterable[_Union[_incentives_pb2.Incentive, _Mapping]]]=..., gas_meters: _Optional[_Iterable[_Union[_incentives_pb2.GasMeter, _Mapping]]]=...) -> None:
        ...

class Params(_message.Message):
    __slots__ = ['allocation_limit', 'enable_incentives', 'incentives_epoch_identifier', 'reward_scaler']
    ALLOCATION_LIMIT_FIELD_NUMBER: _ClassVar[int]
    ENABLE_INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    INCENTIVES_EPOCH_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    REWARD_SCALER_FIELD_NUMBER: _ClassVar[int]
    allocation_limit: str
    enable_incentives: bool
    incentives_epoch_identifier: str
    reward_scaler: str

    def __init__(self, enable_incentives: bool=..., allocation_limit: _Optional[str]=..., incentives_epoch_identifier: _Optional[str]=..., reward_scaler: _Optional[str]=...) -> None:
        ...