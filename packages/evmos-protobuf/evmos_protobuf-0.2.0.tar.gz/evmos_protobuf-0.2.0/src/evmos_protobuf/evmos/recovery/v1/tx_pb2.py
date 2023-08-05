"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....evmos.recovery.v1 import genesis_pb2 as evmos_dot_recovery_dot_v1_dot_genesis__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aevmos/recovery/v1/tx.proto\x12\x11evmos.recovery.v1\x1a\x17cosmos/msg/v1/msg.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1fevmos/recovery/v1/genesis.proto\x1a\x14gogoproto/gogo.proto"\x7f\n\x0fMsgUpdateParams\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12/\n\x06params\x18\x02 \x01(\x0b2\x19.evmos.recovery.v1.ParamsB\x04\xc8\xde\x1f\x00:\x0e\x82\xe7\xb0*\tauthority"\x19\n\x17MsgUpdateParamsResponse2e\n\x03Msg\x12^\n\x0cUpdateParams\x12".evmos.recovery.v1.MsgUpdateParams\x1a*.evmos.recovery.v1.MsgUpdateParamsResponseB-Z+github.com/evmos/evmos/v12/x/recovery/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.recovery.v1.tx_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z+github.com/evmos/evmos/v12/x/recovery/types'
    _MSGUPDATEPARAMS.fields_by_name['authority']._options = None
    _MSGUPDATEPARAMS.fields_by_name['authority']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _MSGUPDATEPARAMS.fields_by_name['params']._options = None
    _MSGUPDATEPARAMS.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _MSGUPDATEPARAMS._options = None
    _MSGUPDATEPARAMS._serialized_options = b'\x82\xe7\xb0*\tauthority'
    _MSGUPDATEPARAMS._serialized_start = 156
    _MSGUPDATEPARAMS._serialized_end = 283
    _MSGUPDATEPARAMSRESPONSE._serialized_start = 285
    _MSGUPDATEPARAMSRESPONSE._serialized_end = 310
    _MSG._serialized_start = 312
    _MSG._serialized_end = 413