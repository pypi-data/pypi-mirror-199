from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor
PROPOSAL_EXECUTOR_RESULT_FAILURE: ProposalExecutorResult
PROPOSAL_EXECUTOR_RESULT_NOT_RUN: ProposalExecutorResult
PROPOSAL_EXECUTOR_RESULT_SUCCESS: ProposalExecutorResult
PROPOSAL_EXECUTOR_RESULT_UNSPECIFIED: ProposalExecutorResult
PROPOSAL_STATUS_ABORTED: ProposalStatus
PROPOSAL_STATUS_ACCEPTED: ProposalStatus
PROPOSAL_STATUS_REJECTED: ProposalStatus
PROPOSAL_STATUS_SUBMITTED: ProposalStatus
PROPOSAL_STATUS_UNSPECIFIED: ProposalStatus
PROPOSAL_STATUS_WITHDRAWN: ProposalStatus
VOTE_OPTION_ABSTAIN: VoteOption
VOTE_OPTION_NO: VoteOption
VOTE_OPTION_NO_WITH_VETO: VoteOption
VOTE_OPTION_UNSPECIFIED: VoteOption
VOTE_OPTION_YES: VoteOption

class DecisionPolicyWindows(_message.Message):
    __slots__ = ['min_execution_period', 'voting_period']
    MIN_EXECUTION_PERIOD_FIELD_NUMBER: _ClassVar[int]
    VOTING_PERIOD_FIELD_NUMBER: _ClassVar[int]
    min_execution_period: _duration_pb2.Duration
    voting_period: _duration_pb2.Duration

    def __init__(self, voting_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., min_execution_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...

class GroupInfo(_message.Message):
    __slots__ = ['admin', 'created_at', 'id', 'metadata', 'total_weight', 'version']
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    TOTAL_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    admin: str
    created_at: _timestamp_pb2.Timestamp
    id: int
    metadata: str
    total_weight: str
    version: int

    def __init__(self, id: _Optional[int]=..., admin: _Optional[str]=..., metadata: _Optional[str]=..., version: _Optional[int]=..., total_weight: _Optional[str]=..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class GroupMember(_message.Message):
    __slots__ = ['group_id', 'member']
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    member: Member

    def __init__(self, group_id: _Optional[int]=..., member: _Optional[_Union[Member, _Mapping]]=...) -> None:
        ...

class GroupPolicyInfo(_message.Message):
    __slots__ = ['address', 'admin', 'created_at', 'decision_policy', 'group_id', 'metadata', 'version']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DECISION_POLICY_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    address: str
    admin: str
    created_at: _timestamp_pb2.Timestamp
    decision_policy: _any_pb2.Any
    group_id: int
    metadata: str
    version: int

    def __init__(self, address: _Optional[str]=..., group_id: _Optional[int]=..., admin: _Optional[str]=..., metadata: _Optional[str]=..., version: _Optional[int]=..., decision_policy: _Optional[_Union[_any_pb2.Any, _Mapping]]=..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class Member(_message.Message):
    __slots__ = ['added_at', 'address', 'metadata', 'weight']
    ADDED_AT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    added_at: _timestamp_pb2.Timestamp
    address: str
    metadata: str
    weight: str

    def __init__(self, address: _Optional[str]=..., weight: _Optional[str]=..., metadata: _Optional[str]=..., added_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class MemberRequest(_message.Message):
    __slots__ = ['address', 'metadata', 'weight']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    address: str
    metadata: str
    weight: str

    def __init__(self, address: _Optional[str]=..., weight: _Optional[str]=..., metadata: _Optional[str]=...) -> None:
        ...

class PercentageDecisionPolicy(_message.Message):
    __slots__ = ['percentage', 'windows']
    PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    WINDOWS_FIELD_NUMBER: _ClassVar[int]
    percentage: str
    windows: DecisionPolicyWindows

    def __init__(self, percentage: _Optional[str]=..., windows: _Optional[_Union[DecisionPolicyWindows, _Mapping]]=...) -> None:
        ...

class Proposal(_message.Message):
    __slots__ = ['executor_result', 'final_tally_result', 'group_policy_address', 'group_policy_version', 'group_version', 'id', 'messages', 'metadata', 'proposers', 'status', 'submit_time', 'voting_period_end']
    EXECUTOR_RESULT_FIELD_NUMBER: _ClassVar[int]
    FINAL_TALLY_RESULT_FIELD_NUMBER: _ClassVar[int]
    GROUP_POLICY_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    GROUP_POLICY_VERSION_FIELD_NUMBER: _ClassVar[int]
    GROUP_VERSION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PROPOSERS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBMIT_TIME_FIELD_NUMBER: _ClassVar[int]
    VOTING_PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    executor_result: ProposalExecutorResult
    final_tally_result: TallyResult
    group_policy_address: str
    group_policy_version: int
    group_version: int
    id: int
    messages: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    metadata: str
    proposers: _containers.RepeatedScalarFieldContainer[str]
    status: ProposalStatus
    submit_time: _timestamp_pb2.Timestamp
    voting_period_end: _timestamp_pb2.Timestamp

    def __init__(self, id: _Optional[int]=..., group_policy_address: _Optional[str]=..., metadata: _Optional[str]=..., proposers: _Optional[_Iterable[str]]=..., submit_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., group_version: _Optional[int]=..., group_policy_version: _Optional[int]=..., status: _Optional[_Union[ProposalStatus, str]]=..., final_tally_result: _Optional[_Union[TallyResult, _Mapping]]=..., voting_period_end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., executor_result: _Optional[_Union[ProposalExecutorResult, str]]=..., messages: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]]=...) -> None:
        ...

class TallyResult(_message.Message):
    __slots__ = ['abstain_count', 'no_count', 'no_with_veto_count', 'yes_count']
    ABSTAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    NO_COUNT_FIELD_NUMBER: _ClassVar[int]
    NO_WITH_VETO_COUNT_FIELD_NUMBER: _ClassVar[int]
    YES_COUNT_FIELD_NUMBER: _ClassVar[int]
    abstain_count: str
    no_count: str
    no_with_veto_count: str
    yes_count: str

    def __init__(self, yes_count: _Optional[str]=..., abstain_count: _Optional[str]=..., no_count: _Optional[str]=..., no_with_veto_count: _Optional[str]=...) -> None:
        ...

class ThresholdDecisionPolicy(_message.Message):
    __slots__ = ['threshold', 'windows']
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    WINDOWS_FIELD_NUMBER: _ClassVar[int]
    threshold: str
    windows: DecisionPolicyWindows

    def __init__(self, threshold: _Optional[str]=..., windows: _Optional[_Union[DecisionPolicyWindows, _Mapping]]=...) -> None:
        ...

class Vote(_message.Message):
    __slots__ = ['metadata', 'option', 'proposal_id', 'submit_time', 'voter']
    METADATA_FIELD_NUMBER: _ClassVar[int]
    OPTION_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    SUBMIT_TIME_FIELD_NUMBER: _ClassVar[int]
    VOTER_FIELD_NUMBER: _ClassVar[int]
    metadata: str
    option: VoteOption
    proposal_id: int
    submit_time: _timestamp_pb2.Timestamp
    voter: str

    def __init__(self, proposal_id: _Optional[int]=..., voter: _Optional[str]=..., option: _Optional[_Union[VoteOption, str]]=..., metadata: _Optional[str]=..., submit_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class VoteOption(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ProposalStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ProposalExecutorResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []