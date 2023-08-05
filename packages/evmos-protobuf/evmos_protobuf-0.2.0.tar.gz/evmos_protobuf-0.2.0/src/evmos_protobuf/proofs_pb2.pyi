from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
BITCOIN: HashOp
DESCRIPTOR: _descriptor.FileDescriptor
FIXED32_BIG: LengthOp
FIXED32_LITTLE: LengthOp
FIXED64_BIG: LengthOp
FIXED64_LITTLE: LengthOp
KECCAK: HashOp
NO_HASH: HashOp
NO_PREFIX: LengthOp
REQUIRE_32_BYTES: LengthOp
REQUIRE_64_BYTES: LengthOp
RIPEMD160: HashOp
SHA256: HashOp
SHA512: HashOp
SHA512_256: HashOp
VAR_PROTO: LengthOp
VAR_RLP: LengthOp

class BatchEntry(_message.Message):
    __slots__ = ['exist', 'nonexist']
    EXIST_FIELD_NUMBER: _ClassVar[int]
    NONEXIST_FIELD_NUMBER: _ClassVar[int]
    exist: ExistenceProof
    nonexist: NonExistenceProof

    def __init__(self, exist: _Optional[_Union[ExistenceProof, _Mapping]]=..., nonexist: _Optional[_Union[NonExistenceProof, _Mapping]]=...) -> None:
        ...

class BatchProof(_message.Message):
    __slots__ = ['entries']
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[BatchEntry]

    def __init__(self, entries: _Optional[_Iterable[_Union[BatchEntry, _Mapping]]]=...) -> None:
        ...

class CommitmentProof(_message.Message):
    __slots__ = ['batch', 'compressed', 'exist', 'nonexist']
    BATCH_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    EXIST_FIELD_NUMBER: _ClassVar[int]
    NONEXIST_FIELD_NUMBER: _ClassVar[int]
    batch: BatchProof
    compressed: CompressedBatchProof
    exist: ExistenceProof
    nonexist: NonExistenceProof

    def __init__(self, exist: _Optional[_Union[ExistenceProof, _Mapping]]=..., nonexist: _Optional[_Union[NonExistenceProof, _Mapping]]=..., batch: _Optional[_Union[BatchProof, _Mapping]]=..., compressed: _Optional[_Union[CompressedBatchProof, _Mapping]]=...) -> None:
        ...

class CompressedBatchEntry(_message.Message):
    __slots__ = ['exist', 'nonexist']
    EXIST_FIELD_NUMBER: _ClassVar[int]
    NONEXIST_FIELD_NUMBER: _ClassVar[int]
    exist: CompressedExistenceProof
    nonexist: CompressedNonExistenceProof

    def __init__(self, exist: _Optional[_Union[CompressedExistenceProof, _Mapping]]=..., nonexist: _Optional[_Union[CompressedNonExistenceProof, _Mapping]]=...) -> None:
        ...

class CompressedBatchProof(_message.Message):
    __slots__ = ['entries', 'lookup_inners']
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    LOOKUP_INNERS_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[CompressedBatchEntry]
    lookup_inners: _containers.RepeatedCompositeFieldContainer[InnerOp]

    def __init__(self, entries: _Optional[_Iterable[_Union[CompressedBatchEntry, _Mapping]]]=..., lookup_inners: _Optional[_Iterable[_Union[InnerOp, _Mapping]]]=...) -> None:
        ...

class CompressedExistenceProof(_message.Message):
    __slots__ = ['key', 'leaf', 'path', 'value']
    KEY_FIELD_NUMBER: _ClassVar[int]
    LEAF_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: bytes
    leaf: LeafOp
    path: _containers.RepeatedScalarFieldContainer[int]
    value: bytes

    def __init__(self, key: _Optional[bytes]=..., value: _Optional[bytes]=..., leaf: _Optional[_Union[LeafOp, _Mapping]]=..., path: _Optional[_Iterable[int]]=...) -> None:
        ...

class CompressedNonExistenceProof(_message.Message):
    __slots__ = ['key', 'left', 'right']
    KEY_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    key: bytes
    left: CompressedExistenceProof
    right: CompressedExistenceProof

    def __init__(self, key: _Optional[bytes]=..., left: _Optional[_Union[CompressedExistenceProof, _Mapping]]=..., right: _Optional[_Union[CompressedExistenceProof, _Mapping]]=...) -> None:
        ...

class ExistenceProof(_message.Message):
    __slots__ = ['key', 'leaf', 'path', 'value']
    KEY_FIELD_NUMBER: _ClassVar[int]
    LEAF_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: bytes
    leaf: LeafOp
    path: _containers.RepeatedCompositeFieldContainer[InnerOp]
    value: bytes

    def __init__(self, key: _Optional[bytes]=..., value: _Optional[bytes]=..., leaf: _Optional[_Union[LeafOp, _Mapping]]=..., path: _Optional[_Iterable[_Union[InnerOp, _Mapping]]]=...) -> None:
        ...

class InnerOp(_message.Message):
    __slots__ = ['hash', 'prefix', 'suffix']
    HASH_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    hash: HashOp
    prefix: bytes
    suffix: bytes

    def __init__(self, hash: _Optional[_Union[HashOp, str]]=..., prefix: _Optional[bytes]=..., suffix: _Optional[bytes]=...) -> None:
        ...

class InnerSpec(_message.Message):
    __slots__ = ['child_order', 'child_size', 'empty_child', 'hash', 'max_prefix_length', 'min_prefix_length']
    CHILD_ORDER_FIELD_NUMBER: _ClassVar[int]
    CHILD_SIZE_FIELD_NUMBER: _ClassVar[int]
    EMPTY_CHILD_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    MAX_PREFIX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MIN_PREFIX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    child_order: _containers.RepeatedScalarFieldContainer[int]
    child_size: int
    empty_child: bytes
    hash: HashOp
    max_prefix_length: int
    min_prefix_length: int

    def __init__(self, child_order: _Optional[_Iterable[int]]=..., child_size: _Optional[int]=..., min_prefix_length: _Optional[int]=..., max_prefix_length: _Optional[int]=..., empty_child: _Optional[bytes]=..., hash: _Optional[_Union[HashOp, str]]=...) -> None:
        ...

class LeafOp(_message.Message):
    __slots__ = ['hash', 'length', 'prefix', 'prehash_key', 'prehash_value']
    HASH_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    PREHASH_KEY_FIELD_NUMBER: _ClassVar[int]
    PREHASH_VALUE_FIELD_NUMBER: _ClassVar[int]
    hash: HashOp
    length: LengthOp
    prefix: bytes
    prehash_key: HashOp
    prehash_value: HashOp

    def __init__(self, hash: _Optional[_Union[HashOp, str]]=..., prehash_key: _Optional[_Union[HashOp, str]]=..., prehash_value: _Optional[_Union[HashOp, str]]=..., length: _Optional[_Union[LengthOp, str]]=..., prefix: _Optional[bytes]=...) -> None:
        ...

class NonExistenceProof(_message.Message):
    __slots__ = ['key', 'left', 'right']
    KEY_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    key: bytes
    left: ExistenceProof
    right: ExistenceProof

    def __init__(self, key: _Optional[bytes]=..., left: _Optional[_Union[ExistenceProof, _Mapping]]=..., right: _Optional[_Union[ExistenceProof, _Mapping]]=...) -> None:
        ...

class ProofSpec(_message.Message):
    __slots__ = ['inner_spec', 'leaf_spec', 'max_depth', 'min_depth']
    INNER_SPEC_FIELD_NUMBER: _ClassVar[int]
    LEAF_SPEC_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    MIN_DEPTH_FIELD_NUMBER: _ClassVar[int]
    inner_spec: InnerSpec
    leaf_spec: LeafOp
    max_depth: int
    min_depth: int

    def __init__(self, leaf_spec: _Optional[_Union[LeafOp, _Mapping]]=..., inner_spec: _Optional[_Union[InnerSpec, _Mapping]]=..., max_depth: _Optional[int]=..., min_depth: _Optional[int]=...) -> None:
        ...

class HashOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class LengthOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []