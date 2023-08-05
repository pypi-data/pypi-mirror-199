from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Class(_message.Message):
    __slots__ = ['data', 'description', 'id', 'name', 'symbol', 'uri', 'uri_hash']
    DATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    URI_HASH_FIELD_NUMBER: _ClassVar[int]
    data: _any_pb2.Any
    description: str
    id: str
    name: str
    symbol: str
    uri: str
    uri_hash: str

    def __init__(self, id: _Optional[str]=..., name: _Optional[str]=..., symbol: _Optional[str]=..., description: _Optional[str]=..., uri: _Optional[str]=..., uri_hash: _Optional[str]=..., data: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...

class NFT(_message.Message):
    __slots__ = ['class_id', 'data', 'id', 'uri', 'uri_hash']
    CLASS_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    URI_HASH_FIELD_NUMBER: _ClassVar[int]
    class_id: str
    data: _any_pb2.Any
    id: str
    uri: str
    uri_hash: str

    def __init__(self, class_id: _Optional[str]=..., id: _Optional[str]=..., uri: _Optional[str]=..., uri_hash: _Optional[str]=..., data: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...