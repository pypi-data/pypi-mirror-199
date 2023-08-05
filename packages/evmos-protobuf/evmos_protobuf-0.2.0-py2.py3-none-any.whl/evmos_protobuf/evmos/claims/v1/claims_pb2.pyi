from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union
ACTION_DELEGATE: Action
ACTION_EVM: Action
ACTION_IBC_TRANSFER: Action
ACTION_UNSPECIFIED: Action
ACTION_VOTE: Action
DESCRIPTOR: _descriptor.FileDescriptor

class Claim(_message.Message):
    __slots__ = ['action', 'claimable_amount', 'completed']
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CLAIMABLE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    action: Action
    claimable_amount: str
    completed: bool

    def __init__(self, action: _Optional[_Union[Action, str]]=..., completed: bool=..., claimable_amount: _Optional[str]=...) -> None:
        ...

class ClaimsRecord(_message.Message):
    __slots__ = ['actions_completed', 'initial_claimable_amount']
    ACTIONS_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    INITIAL_CLAIMABLE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    actions_completed: _containers.RepeatedScalarFieldContainer[bool]
    initial_claimable_amount: str

    def __init__(self, initial_claimable_amount: _Optional[str]=..., actions_completed: _Optional[_Iterable[bool]]=...) -> None:
        ...

class ClaimsRecordAddress(_message.Message):
    __slots__ = ['actions_completed', 'address', 'initial_claimable_amount']
    ACTIONS_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_CLAIMABLE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    actions_completed: _containers.RepeatedScalarFieldContainer[bool]
    address: str
    initial_claimable_amount: str

    def __init__(self, address: _Optional[str]=..., initial_claimable_amount: _Optional[str]=..., actions_completed: _Optional[_Iterable[bool]]=...) -> None:
        ...

class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []