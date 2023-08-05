"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1devmos/vesting/v1/events.proto\x12\x10evmos.vesting.v1"v\n!EventCreateClawbackVestingAccount\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\r\n\x05coins\x18\x02 \x01(\t\x12\x12\n\nstart_time\x18\x03 \x01(\t\x12\r\n\x05merge\x18\x04 \x01(\t\x12\x0f\n\x07account\x18\x05 \x01(\t"E\n\rEventClawback\x12\x0e\n\x06funder\x18\x01 \x01(\t\x12\x0f\n\x07account\x18\x02 \x01(\t\x12\x13\n\x0bdestination\x18\x03 \x01(\t"O\n\x18EventUpdateVestingFunder\x12\x0e\n\x06funder\x18\x01 \x01(\t\x12\x0f\n\x07account\x18\x02 \x01(\t\x12\x12\n\nnew_funder\x18\x03 \x01(\tB,Z*github.com/evmos/evmos/v12/x/vesting/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.vesting.v1.events_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z*github.com/evmos/evmos/v12/x/vesting/types'
    _EVENTCREATECLAWBACKVESTINGACCOUNT._serialized_start = 51
    _EVENTCREATECLAWBACKVESTINGACCOUNT._serialized_end = 169
    _EVENTCLAWBACK._serialized_start = 171
    _EVENTCLAWBACK._serialized_end = 240
    _EVENTUPDATEVESTINGFUNDER._serialized_start = 242
    _EVENTUPDATEVESTINGFUNDER._serialized_end = 321