from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: Params

    def __init__(self, params: _Optional[_Union[Params, _Mapping]]=...) -> None:
        ...

class Params(_message.Message):
    __slots__ = ['enable_recovery', 'packet_timeout_duration']
    ENABLE_RECOVERY_FIELD_NUMBER: _ClassVar[int]
    PACKET_TIMEOUT_DURATION_FIELD_NUMBER: _ClassVar[int]
    enable_recovery: bool
    packet_timeout_duration: _duration_pb2.Duration

    def __init__(self, enable_recovery: bool=..., packet_timeout_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...