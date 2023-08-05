from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class Revenue(_message.Message):
    __slots__ = ['contract_address', 'deployer_address', 'withdrawer_address']
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    contract_address: str
    deployer_address: str
    withdrawer_address: str

    def __init__(self, contract_address: _Optional[str]=..., deployer_address: _Optional[str]=..., withdrawer_address: _Optional[str]=...) -> None:
        ...