"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1devmos/revenue/v1/events.proto\x12\x10evmos.revenue.v1"h\n\x14EventRegisterRevenue\x12\x18\n\x10deployer_address\x18\x01 \x01(\t\x12\x18\n\x10contract_address\x18\x02 \x01(\t\x12\x1c\n\x14effective_withdrawer\x18\x03 \x01(\t"d\n\x12EventUpdateRevenue\x12\x18\n\x10contract_address\x18\x01 \x01(\t\x12\x18\n\x10deployer_address\x18\x02 \x01(\t\x12\x1a\n\x12withdrawer_address\x18\x03 \x01(\t"H\n\x12EventCancelRevenue\x12\x18\n\x10deployer_address\x18\x01 \x01(\t\x12\x18\n\x10contract_address\x18\x02 \x01(\t"f\n\x16EventDistributeRevenue\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x10\n\x08contract\x18\x02 \x01(\t\x12\x1a\n\x12withdrawer_address\x18\x03 \x01(\t\x12\x0e\n\x06amount\x18\x04 \x01(\tB/Z-github.com/evmos/evmos/v12/x/revenue/v1/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.revenue.v1.events_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/evmos/evmos/v12/x/revenue/v1/types'
    _EVENTREGISTERREVENUE._serialized_start = 51
    _EVENTREGISTERREVENUE._serialized_end = 155
    _EVENTUPDATEREVENUE._serialized_start = 157
    _EVENTUPDATEREVENUE._serialized_end = 257
    _EVENTCANCELREVENUE._serialized_start = 259
    _EVENTCANCELREVENUE._serialized_end = 331
    _EVENTDISTRIBUTEREVENUE._serialized_start = 333
    _EVENTDISTRIBUTEREVENUE._serialized_end = 435