from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class EventClawback(_message.Message):
    __slots__ = ['account', 'destination', 'funder']
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    FUNDER_FIELD_NUMBER: _ClassVar[int]
    account: str
    destination: str
    funder: str

    def __init__(self, funder: _Optional[str]=..., account: _Optional[str]=..., destination: _Optional[str]=...) -> None:
        ...

class EventCreateClawbackVestingAccount(_message.Message):
    __slots__ = ['account', 'coins', 'merge', 'sender', 'start_time']
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    MERGE_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    account: str
    coins: str
    merge: str
    sender: str
    start_time: str

    def __init__(self, sender: _Optional[str]=..., coins: _Optional[str]=..., start_time: _Optional[str]=..., merge: _Optional[str]=..., account: _Optional[str]=...) -> None:
        ...

class EventUpdateVestingFunder(_message.Message):
    __slots__ = ['account', 'funder', 'new_funder']
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    FUNDER_FIELD_NUMBER: _ClassVar[int]
    NEW_FUNDER_FIELD_NUMBER: _ClassVar[int]
    account: str
    funder: str
    new_funder: str

    def __init__(self, funder: _Optional[str]=..., account: _Optional[str]=..., new_funder: _Optional[str]=...) -> None:
        ...