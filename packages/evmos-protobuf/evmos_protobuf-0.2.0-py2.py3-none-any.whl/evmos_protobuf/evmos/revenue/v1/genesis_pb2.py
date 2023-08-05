"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....evmos.revenue.v1 import revenue_pb2 as evmos_dot_revenue_dot_v1_dot_revenue__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eevmos/revenue/v1/genesis.proto\x12\x10evmos.revenue.v1\x1a\x1eevmos/revenue/v1/revenue.proto\x1a\x14gogoproto/gogo.proto"q\n\x0cGenesisState\x12.\n\x06params\x18\x01 \x01(\x0b2\x18.evmos.revenue.v1.ParamsB\x04\xc8\xde\x1f\x00\x121\n\x08revenues\x18\x02 \x03(\x0b2\x19.evmos.revenue.v1.RevenueB\x04\xc8\xde\x1f\x00"\x8f\x01\n\x06Params\x12\x16\n\x0eenable_revenue\x18\x01 \x01(\x08\x12H\n\x10developer_shares\x18\x02 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12#\n\x1baddr_derivation_cost_create\x18\x03 \x01(\x04B/Z-github.com/evmos/evmos/v12/x/revenue/v1/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.revenue.v1.genesis_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/evmos/evmos/v12/x/revenue/v1/types'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['revenues']._options = None
    _GENESISSTATE.fields_by_name['revenues']._serialized_options = b'\xc8\xde\x1f\x00'
    _PARAMS.fields_by_name['developer_shares']._options = None
    _PARAMS.fields_by_name['developer_shares']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00'
    _GENESISSTATE._serialized_start = 106
    _GENESISSTATE._serialized_end = 219
    _PARAMS._serialized_start = 222
    _PARAMS._serialized_end = 365