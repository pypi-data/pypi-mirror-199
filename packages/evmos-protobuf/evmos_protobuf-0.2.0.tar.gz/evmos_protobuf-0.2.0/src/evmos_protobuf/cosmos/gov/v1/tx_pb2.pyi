from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.gov.v1 import gov_pb2 as _gov_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgDeposit(_message.Message):
    __slots__ = ['amount', 'depositor', 'proposal_id']
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DEPOSITOR_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    amount: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    depositor: str
    proposal_id: int

    def __init__(self, proposal_id: _Optional[int]=..., depositor: _Optional[str]=..., amount: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class MsgDepositResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgExecLegacyContent(_message.Message):
    __slots__ = ['authority', 'content']
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    authority: str
    content: _any_pb2.Any

    def __init__(self, content: _Optional[_Union[_any_pb2.Any, _Mapping]]=..., authority: _Optional[str]=...) -> None:
        ...

class MsgExecLegacyContentResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSubmitProposal(_message.Message):
    __slots__ = ['initial_deposit', 'messages', 'metadata', 'proposer']
    INITIAL_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_FIELD_NUMBER: _ClassVar[int]
    initial_deposit: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    messages: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    metadata: str
    proposer: str

    def __init__(self, messages: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]]=..., initial_deposit: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., proposer: _Optional[str]=..., metadata: _Optional[str]=...) -> None:
        ...

class MsgSubmitProposalResponse(_message.Message):
    __slots__ = ['proposal_id']
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    proposal_id: int

    def __init__(self, proposal_id: _Optional[int]=...) -> None:
        ...

class MsgVote(_message.Message):
    __slots__ = ['metadata', 'option', 'proposal_id', 'voter']
    METADATA_FIELD_NUMBER: _ClassVar[int]
    OPTION_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    VOTER_FIELD_NUMBER: _ClassVar[int]
    metadata: str
    option: _gov_pb2.VoteOption
    proposal_id: int
    voter: str

    def __init__(self, proposal_id: _Optional[int]=..., voter: _Optional[str]=..., option: _Optional[_Union[_gov_pb2.VoteOption, str]]=..., metadata: _Optional[str]=...) -> None:
        ...

class MsgVoteResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgVoteWeighted(_message.Message):
    __slots__ = ['metadata', 'options', 'proposal_id', 'voter']
    METADATA_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    VOTER_FIELD_NUMBER: _ClassVar[int]
    metadata: str
    options: _containers.RepeatedCompositeFieldContainer[_gov_pb2.WeightedVoteOption]
    proposal_id: int
    voter: str

    def __init__(self, proposal_id: _Optional[int]=..., voter: _Optional[str]=..., options: _Optional[_Iterable[_Union[_gov_pb2.WeightedVoteOption, _Mapping]]]=..., metadata: _Optional[str]=...) -> None:
        ...

class MsgVoteWeightedResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...