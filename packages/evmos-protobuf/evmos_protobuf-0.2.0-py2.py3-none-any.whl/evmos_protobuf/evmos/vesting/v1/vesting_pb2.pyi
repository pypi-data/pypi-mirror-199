from cosmos.vesting.v1beta1 import vesting_pb2 as _vesting_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ClawbackVestingAccount(_message.Message):
    __slots__ = ['base_vesting_account', 'funder_address', 'lockup_periods', 'start_time', 'vesting_periods']
    BASE_VESTING_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    FUNDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LOCKUP_PERIODS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    VESTING_PERIODS_FIELD_NUMBER: _ClassVar[int]
    base_vesting_account: _vesting_pb2.BaseVestingAccount
    funder_address: str
    lockup_periods: _containers.RepeatedCompositeFieldContainer[_vesting_pb2.Period]
    start_time: _timestamp_pb2.Timestamp
    vesting_periods: _containers.RepeatedCompositeFieldContainer[_vesting_pb2.Period]

    def __init__(self, base_vesting_account: _Optional[_Union[_vesting_pb2.BaseVestingAccount, _Mapping]]=..., funder_address: _Optional[str]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., lockup_periods: _Optional[_Iterable[_Union[_vesting_pb2.Period, _Mapping]]]=..., vesting_periods: _Optional[_Iterable[_Union[_vesting_pb2.Period, _Mapping]]]=...) -> None:
        ...