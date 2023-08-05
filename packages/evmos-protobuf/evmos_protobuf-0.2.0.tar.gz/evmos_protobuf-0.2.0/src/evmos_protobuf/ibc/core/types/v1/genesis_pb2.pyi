from gogoproto import gogo_pb2 as _gogo_pb2
from ibc.core.client.v1 import genesis_pb2 as _genesis_pb2
from ibc.core.connection.v1 import genesis_pb2 as _genesis_pb2_1
from ibc.core.channel.v1 import genesis_pb2 as _genesis_pb2_1_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['channel_genesis', 'client_genesis', 'connection_genesis']
    CHANNEL_GENESIS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_GENESIS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_GENESIS_FIELD_NUMBER: _ClassVar[int]
    channel_genesis: _genesis_pb2_1_1.GenesisState
    client_genesis: _genesis_pb2.GenesisState
    connection_genesis: _genesis_pb2_1.GenesisState

    def __init__(self, client_genesis: _Optional[_Union[_genesis_pb2.GenesisState, _Mapping]]=..., connection_genesis: _Optional[_Union[_genesis_pb2_1.GenesisState, _Mapping]]=..., channel_genesis: _Optional[_Union[_genesis_pb2_1_1.GenesisState, _Mapping]]=...) -> None:
        ...