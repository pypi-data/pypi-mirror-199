from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from evmos.inflation.v1 import genesis_pb2 as _genesis_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryCirculatingSupplyRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryCirculatingSupplyResponse(_message.Message):
    __slots__ = ['circulating_supply']
    CIRCULATING_SUPPLY_FIELD_NUMBER: _ClassVar[int]
    circulating_supply: _coin_pb2.DecCoin

    def __init__(self, circulating_supply: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]]=...) -> None:
        ...

class QueryEpochMintProvisionRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryEpochMintProvisionResponse(_message.Message):
    __slots__ = ['epoch_mint_provision']
    EPOCH_MINT_PROVISION_FIELD_NUMBER: _ClassVar[int]
    epoch_mint_provision: _coin_pb2.DecCoin

    def __init__(self, epoch_mint_provision: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]]=...) -> None:
        ...

class QueryInflationRateRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryInflationRateResponse(_message.Message):
    __slots__ = ['inflation_rate']
    INFLATION_RATE_FIELD_NUMBER: _ClassVar[int]
    inflation_rate: str

    def __init__(self, inflation_rate: _Optional[str]=...) -> None:
        ...

class QueryParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _genesis_pb2.Params

    def __init__(self, params: _Optional[_Union[_genesis_pb2.Params, _Mapping]]=...) -> None:
        ...

class QueryPeriodRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryPeriodResponse(_message.Message):
    __slots__ = ['period']
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    period: int

    def __init__(self, period: _Optional[int]=...) -> None:
        ...

class QuerySkippedEpochsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QuerySkippedEpochsResponse(_message.Message):
    __slots__ = ['skipped_epochs']
    SKIPPED_EPOCHS_FIELD_NUMBER: _ClassVar[int]
    skipped_epochs: int

    def __init__(self, skipped_epochs: _Optional[int]=...) -> None:
        ...