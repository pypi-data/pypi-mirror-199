from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class ExtensionOptionsWeb3Tx(_message.Message):
    __slots__ = ['fee_payer', 'fee_payer_sig', 'typed_data_chain_id']
    FEE_PAYER_FIELD_NUMBER: _ClassVar[int]
    FEE_PAYER_SIG_FIELD_NUMBER: _ClassVar[int]
    TYPED_DATA_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    fee_payer: str
    fee_payer_sig: bytes
    typed_data_chain_id: int

    def __init__(self, typed_data_chain_id: _Optional[int]=..., fee_payer: _Optional[str]=..., fee_payer_sig: _Optional[bytes]=...) -> None:
        ...