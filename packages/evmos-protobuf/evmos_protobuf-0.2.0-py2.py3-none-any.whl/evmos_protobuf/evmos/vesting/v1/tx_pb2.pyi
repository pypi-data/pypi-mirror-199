from cosmos.vesting.v1beta1 import vesting_pb2 as _vesting_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgClawback(_message.Message):
    __slots__ = ['account_address', 'dest_address', 'funder_address']
    ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DEST_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FUNDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    account_address: str
    dest_address: str
    funder_address: str

    def __init__(self, funder_address: _Optional[str]=..., account_address: _Optional[str]=..., dest_address: _Optional[str]=...) -> None:
        ...

class MsgClawbackResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgConvertVestingAccount(_message.Message):
    __slots__ = ['vesting_address']
    VESTING_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    vesting_address: str

    def __init__(self, vesting_address: _Optional[str]=...) -> None:
        ...

class MsgConvertVestingAccountResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgCreateClawbackVestingAccount(_message.Message):
    __slots__ = ['from_address', 'lockup_periods', 'merge', 'start_time', 'to_address', 'vesting_periods']
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LOCKUP_PERIODS_FIELD_NUMBER: _ClassVar[int]
    MERGE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    TO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    VESTING_PERIODS_FIELD_NUMBER: _ClassVar[int]
    from_address: str
    lockup_periods: _containers.RepeatedCompositeFieldContainer[_vesting_pb2.Period]
    merge: bool
    start_time: _timestamp_pb2.Timestamp
    to_address: str
    vesting_periods: _containers.RepeatedCompositeFieldContainer[_vesting_pb2.Period]

    def __init__(self, from_address: _Optional[str]=..., to_address: _Optional[str]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., lockup_periods: _Optional[_Iterable[_Union[_vesting_pb2.Period, _Mapping]]]=..., vesting_periods: _Optional[_Iterable[_Union[_vesting_pb2.Period, _Mapping]]]=..., merge: bool=...) -> None:
        ...

class MsgCreateClawbackVestingAccountResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgUpdateVestingFunder(_message.Message):
    __slots__ = ['funder_address', 'new_funder_address', 'vesting_address']
    FUNDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NEW_FUNDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    VESTING_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    funder_address: str
    new_funder_address: str
    vesting_address: str

    def __init__(self, funder_address: _Optional[str]=..., new_funder_address: _Optional[str]=..., vesting_address: _Optional[str]=...) -> None:
        ...

class MsgUpdateVestingFunderResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...