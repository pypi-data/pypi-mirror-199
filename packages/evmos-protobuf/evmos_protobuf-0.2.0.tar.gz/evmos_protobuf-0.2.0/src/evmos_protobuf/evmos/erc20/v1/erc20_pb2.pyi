from cosmos.bank.v1beta1 import bank_pb2 as _bank_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor
OWNER_EXTERNAL: Owner
OWNER_MODULE: Owner
OWNER_UNSPECIFIED: Owner

class ProposalMetadata(_message.Message):
    __slots__ = ['metadata']
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[_bank_pb2.Metadata]

    def __init__(self, metadata: _Optional[_Iterable[_Union[_bank_pb2.Metadata, _Mapping]]]=...) -> None:
        ...

class RegisterCoinProposal(_message.Message):
    __slots__ = ['description', 'metadata', 'title']
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    description: str
    metadata: _containers.RepeatedCompositeFieldContainer[_bank_pb2.Metadata]
    title: str

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., metadata: _Optional[_Iterable[_Union[_bank_pb2.Metadata, _Mapping]]]=...) -> None:
        ...

class RegisterERC20Proposal(_message.Message):
    __slots__ = ['description', 'erc20addresses', 'title']
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ERC20ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    description: str
    erc20addresses: _containers.RepeatedScalarFieldContainer[str]
    title: str

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., erc20addresses: _Optional[_Iterable[str]]=...) -> None:
        ...

class ToggleTokenConversionProposal(_message.Message):
    __slots__ = ['description', 'title', 'token']
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    description: str
    title: str
    token: str

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., token: _Optional[str]=...) -> None:
        ...

class TokenPair(_message.Message):
    __slots__ = ['contract_owner', 'denom', 'enabled', 'erc20_address']
    CONTRACT_OWNER_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ERC20_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    contract_owner: Owner
    denom: str
    enabled: bool
    erc20_address: str

    def __init__(self, erc20_address: _Optional[str]=..., denom: _Optional[str]=..., enabled: bool=..., contract_owner: _Optional[_Union[Owner, str]]=...) -> None:
        ...

class Owner(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []