from evmos.claims.v1 import claims_pb2 as _claims_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['claims_records', 'params']
    CLAIMS_RECORDS_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    claims_records: _containers.RepeatedCompositeFieldContainer[_claims_pb2.ClaimsRecordAddress]
    params: Params

    def __init__(self, params: _Optional[_Union[Params, _Mapping]]=..., claims_records: _Optional[_Iterable[_Union[_claims_pb2.ClaimsRecordAddress, _Mapping]]]=...) -> None:
        ...

class Params(_message.Message):
    __slots__ = ['airdrop_start_time', 'authorized_channels', 'claims_denom', 'duration_of_decay', 'duration_until_decay', 'enable_claims', 'evm_channels']
    AIRDROP_START_TIME_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    CLAIMS_DENOM_FIELD_NUMBER: _ClassVar[int]
    DURATION_OF_DECAY_FIELD_NUMBER: _ClassVar[int]
    DURATION_UNTIL_DECAY_FIELD_NUMBER: _ClassVar[int]
    ENABLE_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EVM_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    airdrop_start_time: _timestamp_pb2.Timestamp
    authorized_channels: _containers.RepeatedScalarFieldContainer[str]
    claims_denom: str
    duration_of_decay: _duration_pb2.Duration
    duration_until_decay: _duration_pb2.Duration
    enable_claims: bool
    evm_channels: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, enable_claims: bool=..., airdrop_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., duration_until_decay: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., duration_of_decay: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., claims_denom: _Optional[str]=..., authorized_channels: _Optional[_Iterable[str]]=..., evm_channels: _Optional[_Iterable[str]]=...) -> None:
        ...