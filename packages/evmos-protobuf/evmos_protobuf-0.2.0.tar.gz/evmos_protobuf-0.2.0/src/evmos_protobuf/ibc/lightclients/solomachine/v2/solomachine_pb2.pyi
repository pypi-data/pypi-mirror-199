from ibc.core.connection.v1 import connection_pb2 as _connection_pb2
from ibc.core.channel.v1 import channel_pb2 as _channel_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DATA_TYPE_CHANNEL_STATE: DataType
DATA_TYPE_CLIENT_STATE: DataType
DATA_TYPE_CONNECTION_STATE: DataType
DATA_TYPE_CONSENSUS_STATE: DataType
DATA_TYPE_HEADER: DataType
DATA_TYPE_NEXT_SEQUENCE_RECV: DataType
DATA_TYPE_PACKET_ACKNOWLEDGEMENT: DataType
DATA_TYPE_PACKET_COMMITMENT: DataType
DATA_TYPE_PACKET_RECEIPT_ABSENCE: DataType
DATA_TYPE_UNINITIALIZED_UNSPECIFIED: DataType
DESCRIPTOR: _descriptor.FileDescriptor

class ChannelStateData(_message.Message):
    __slots__ = ['channel', 'path']
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    channel: _channel_pb2.Channel
    path: bytes

    def __init__(self, path: _Optional[bytes]=..., channel: _Optional[_Union[_channel_pb2.Channel, _Mapping]]=...) -> None:
        ...

class ClientState(_message.Message):
    __slots__ = ['allow_update_after_proposal', 'consensus_state', 'is_frozen', 'sequence']
    ALLOW_UPDATE_AFTER_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    CONSENSUS_STATE_FIELD_NUMBER: _ClassVar[int]
    IS_FROZEN_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    allow_update_after_proposal: bool
    consensus_state: ConsensusState
    is_frozen: bool
    sequence: int

    def __init__(self, sequence: _Optional[int]=..., is_frozen: bool=..., consensus_state: _Optional[_Union[ConsensusState, _Mapping]]=..., allow_update_after_proposal: bool=...) -> None:
        ...

class ClientStateData(_message.Message):
    __slots__ = ['client_state', 'path']
    CLIENT_STATE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    client_state: _any_pb2.Any
    path: bytes

    def __init__(self, path: _Optional[bytes]=..., client_state: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...

class ConnectionStateData(_message.Message):
    __slots__ = ['connection', 'path']
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    connection: _connection_pb2.ConnectionEnd
    path: bytes

    def __init__(self, path: _Optional[bytes]=..., connection: _Optional[_Union[_connection_pb2.ConnectionEnd, _Mapping]]=...) -> None:
        ...

class ConsensusState(_message.Message):
    __slots__ = ['diversifier', 'public_key', 'timestamp']
    DIVERSIFIER_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    diversifier: str
    public_key: _any_pb2.Any
    timestamp: int

    def __init__(self, public_key: _Optional[_Union[_any_pb2.Any, _Mapping]]=..., diversifier: _Optional[str]=..., timestamp: _Optional[int]=...) -> None:
        ...

class ConsensusStateData(_message.Message):
    __slots__ = ['consensus_state', 'path']
    CONSENSUS_STATE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    consensus_state: _any_pb2.Any
    path: bytes

    def __init__(self, path: _Optional[bytes]=..., consensus_state: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...

class Header(_message.Message):
    __slots__ = ['new_diversifier', 'new_public_key', 'sequence', 'signature', 'timestamp']
    NEW_DIVERSIFIER_FIELD_NUMBER: _ClassVar[int]
    NEW_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    new_diversifier: str
    new_public_key: _any_pb2.Any
    sequence: int
    signature: bytes
    timestamp: int

    def __init__(self, sequence: _Optional[int]=..., timestamp: _Optional[int]=..., signature: _Optional[bytes]=..., new_public_key: _Optional[_Union[_any_pb2.Any, _Mapping]]=..., new_diversifier: _Optional[str]=...) -> None:
        ...

class HeaderData(_message.Message):
    __slots__ = ['new_diversifier', 'new_pub_key']
    NEW_DIVERSIFIER_FIELD_NUMBER: _ClassVar[int]
    NEW_PUB_KEY_FIELD_NUMBER: _ClassVar[int]
    new_diversifier: str
    new_pub_key: _any_pb2.Any

    def __init__(self, new_pub_key: _Optional[_Union[_any_pb2.Any, _Mapping]]=..., new_diversifier: _Optional[str]=...) -> None:
        ...

class Misbehaviour(_message.Message):
    __slots__ = ['client_id', 'sequence', 'signature_one', 'signature_two']
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_ONE_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_TWO_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    sequence: int
    signature_one: SignatureAndData
    signature_two: SignatureAndData

    def __init__(self, client_id: _Optional[str]=..., sequence: _Optional[int]=..., signature_one: _Optional[_Union[SignatureAndData, _Mapping]]=..., signature_two: _Optional[_Union[SignatureAndData, _Mapping]]=...) -> None:
        ...

class NextSequenceRecvData(_message.Message):
    __slots__ = ['next_seq_recv', 'path']
    NEXT_SEQ_RECV_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    next_seq_recv: int
    path: bytes

    def __init__(self, path: _Optional[bytes]=..., next_seq_recv: _Optional[int]=...) -> None:
        ...

class PacketAcknowledgementData(_message.Message):
    __slots__ = ['acknowledgement', 'path']
    ACKNOWLEDGEMENT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    acknowledgement: bytes
    path: bytes

    def __init__(self, path: _Optional[bytes]=..., acknowledgement: _Optional[bytes]=...) -> None:
        ...

class PacketCommitmentData(_message.Message):
    __slots__ = ['commitment', 'path']
    COMMITMENT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    commitment: bytes
    path: bytes

    def __init__(self, path: _Optional[bytes]=..., commitment: _Optional[bytes]=...) -> None:
        ...

class PacketReceiptAbsenceData(_message.Message):
    __slots__ = ['path']
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: bytes

    def __init__(self, path: _Optional[bytes]=...) -> None:
        ...

class SignBytes(_message.Message):
    __slots__ = ['data', 'data_type', 'diversifier', 'sequence', 'timestamp']
    DATA_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DIVERSIFIER_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    data_type: DataType
    diversifier: str
    sequence: int
    timestamp: int

    def __init__(self, sequence: _Optional[int]=..., timestamp: _Optional[int]=..., diversifier: _Optional[str]=..., data_type: _Optional[_Union[DataType, str]]=..., data: _Optional[bytes]=...) -> None:
        ...

class SignatureAndData(_message.Message):
    __slots__ = ['data', 'data_type', 'signature', 'timestamp']
    DATA_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    data_type: DataType
    signature: bytes
    timestamp: int

    def __init__(self, signature: _Optional[bytes]=..., data_type: _Optional[_Union[DataType, str]]=..., data: _Optional[bytes]=..., timestamp: _Optional[int]=...) -> None:
        ...

class TimestampedSignatureData(_message.Message):
    __slots__ = ['signature_data', 'timestamp']
    SIGNATURE_DATA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    signature_data: bytes
    timestamp: int

    def __init__(self, signature_data: _Optional[bytes]=..., timestamp: _Optional[int]=...) -> None:
        ...

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []