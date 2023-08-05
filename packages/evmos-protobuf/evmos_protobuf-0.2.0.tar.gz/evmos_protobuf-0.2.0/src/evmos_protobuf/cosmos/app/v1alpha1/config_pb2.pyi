from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Config(_message.Message):
    __slots__ = ['modules']
    MODULES_FIELD_NUMBER: _ClassVar[int]
    modules: _containers.RepeatedCompositeFieldContainer[ModuleConfig]

    def __init__(self, modules: _Optional[_Iterable[_Union[ModuleConfig, _Mapping]]]=...) -> None:
        ...

class ModuleConfig(_message.Message):
    __slots__ = ['config', 'name']
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    config: _any_pb2.Any
    name: str

    def __init__(self, name: _Optional[str]=..., config: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...