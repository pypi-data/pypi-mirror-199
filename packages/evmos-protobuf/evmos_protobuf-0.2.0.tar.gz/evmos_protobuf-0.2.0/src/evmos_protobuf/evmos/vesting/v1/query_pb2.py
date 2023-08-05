"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cevmos/vesting/v1/query.proto\x12\x10evmos.vesting.v1\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto"\'\n\x14QueryBalancesRequest\x12\x0f\n\x07address\x18\x01 \x01(\t"\xb0\x02\n\x15QueryBalancesResponse\x12[\n\x06locked\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12]\n\x08unvested\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12[\n\x06vested\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins2\x93\x01\n\x05Query\x12\x89\x01\n\x08Balances\x12&.evmos.vesting.v1.QueryBalancesRequest\x1a\'.evmos.vesting.v1.QueryBalancesResponse",\x82\xd3\xe4\x93\x02&\x12$/evmos/vesting/v1/balances/{address}B,Z*github.com/evmos/evmos/v12/x/vesting/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.vesting.v1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z*github.com/evmos/evmos/v12/x/vesting/types'
    _QUERYBALANCESRESPONSE.fields_by_name['locked']._options = None
    _QUERYBALANCESRESPONSE.fields_by_name['locked']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _QUERYBALANCESRESPONSE.fields_by_name['unvested']._options = None
    _QUERYBALANCESRESPONSE.fields_by_name['unvested']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _QUERYBALANCESRESPONSE.fields_by_name['vested']._options = None
    _QUERYBALANCESRESPONSE.fields_by_name['vested']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _QUERY.methods_by_name['Balances']._options = None
    _QUERY.methods_by_name['Balances']._serialized_options = b'\x82\xd3\xe4\x93\x02&\x12$/evmos/vesting/v1/balances/{address}'
    _QUERYBALANCESREQUEST._serialized_start = 134
    _QUERYBALANCESREQUEST._serialized_end = 173
    _QUERYBALANCESRESPONSE._serialized_start = 176
    _QUERYBALANCESRESPONSE._serialized_end = 480
    _QUERY._serialized_start = 483
    _QUERY._serialized_end = 630