"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....evmos.revenue.v1 import genesis_pb2 as evmos_dot_revenue_dot_v1_dot_genesis__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19evmos/revenue/v1/tx.proto\x12\x10evmos.revenue.v1\x1a\x17cosmos/msg/v1/msg.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1eevmos/revenue/v1/genesis.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto"z\n\x12MsgRegisterRevenue\x12\x18\n\x10contract_address\x18\x01 \x01(\t\x12\x18\n\x10deployer_address\x18\x02 \x01(\t\x12\x1a\n\x12withdrawer_address\x18\x03 \x01(\t\x12\x0e\n\x06nonces\x18\x04 \x03(\x04:\x04\xe8\xa0\x1f\x00"\x1c\n\x1aMsgRegisterRevenueResponse"h\n\x10MsgUpdateRevenue\x12\x18\n\x10contract_address\x18\x01 \x01(\t\x12\x18\n\x10deployer_address\x18\x02 \x01(\t\x12\x1a\n\x12withdrawer_address\x18\x03 \x01(\t:\x04\xe8\xa0\x1f\x00"\x1a\n\x18MsgUpdateRevenueResponse"L\n\x10MsgCancelRevenue\x12\x18\n\x10contract_address\x18\x01 \x01(\t\x12\x18\n\x10deployer_address\x18\x02 \x01(\t:\x04\xe8\xa0\x1f\x00"\x1a\n\x18MsgCancelRevenueResponse"~\n\x0fMsgUpdateParams\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12.\n\x06params\x18\x02 \x01(\x0b2\x18.evmos.revenue.v1.ParamsB\x04\xc8\xde\x1f\x00:\x0e\x82\xe7\xb0*\tauthority"\x19\n\x17MsgUpdateParamsResponse2\x98\x04\n\x03Msg\x12\x94\x01\n\x0fRegisterRevenue\x12$.evmos.revenue.v1.MsgRegisterRevenue\x1a,.evmos.revenue.v1.MsgRegisterRevenueResponse"-\x82\xd3\xe4\x93\x02\'"%/evmos/revenue/v1/tx/register_revenue\x12\x8c\x01\n\rUpdateRevenue\x12".evmos.revenue.v1.MsgUpdateRevenue\x1a*.evmos.revenue.v1.MsgUpdateRevenueResponse"+\x82\xd3\xe4\x93\x02%"#/evmos/revenue/v1/tx/update_revenue\x12\x8c\x01\n\rCancelRevenue\x12".evmos.revenue.v1.MsgCancelRevenue\x1a*.evmos.revenue.v1.MsgCancelRevenueResponse"+\x82\xd3\xe4\x93\x02%"#/evmos/revenue/v1/tx/cancel_revenue\x12\\\n\x0cUpdateParams\x12!.evmos.revenue.v1.MsgUpdateParams\x1a).evmos.revenue.v1.MsgUpdateParamsResponseB/Z-github.com/evmos/evmos/v12/x/revenue/v1/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.revenue.v1.tx_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/evmos/evmos/v12/x/revenue/v1/types'
    _MSGREGISTERREVENUE._options = None
    _MSGREGISTERREVENUE._serialized_options = b'\xe8\xa0\x1f\x00'
    _MSGUPDATEREVENUE._options = None
    _MSGUPDATEREVENUE._serialized_options = b'\xe8\xa0\x1f\x00'
    _MSGCANCELREVENUE._options = None
    _MSGCANCELREVENUE._serialized_options = b'\xe8\xa0\x1f\x00'
    _MSGUPDATEPARAMS.fields_by_name['authority']._options = None
    _MSGUPDATEPARAMS.fields_by_name['authority']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _MSGUPDATEPARAMS.fields_by_name['params']._options = None
    _MSGUPDATEPARAMS.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _MSGUPDATEPARAMS._options = None
    _MSGUPDATEPARAMS._serialized_options = b'\x82\xe7\xb0*\tauthority'
    _MSG.methods_by_name['RegisterRevenue']._options = None
    _MSG.methods_by_name['RegisterRevenue']._serialized_options = b'\x82\xd3\xe4\x93\x02\'"%/evmos/revenue/v1/tx/register_revenue'
    _MSG.methods_by_name['UpdateRevenue']._options = None
    _MSG.methods_by_name['UpdateRevenue']._serialized_options = b'\x82\xd3\xe4\x93\x02%"#/evmos/revenue/v1/tx/update_revenue'
    _MSG.methods_by_name['CancelRevenue']._options = None
    _MSG.methods_by_name['CancelRevenue']._serialized_options = b'\x82\xd3\xe4\x93\x02%"#/evmos/revenue/v1/tx/cancel_revenue'
    _MSGREGISTERREVENUE._serialized_start = 183
    _MSGREGISTERREVENUE._serialized_end = 305
    _MSGREGISTERREVENUERESPONSE._serialized_start = 307
    _MSGREGISTERREVENUERESPONSE._serialized_end = 335
    _MSGUPDATEREVENUE._serialized_start = 337
    _MSGUPDATEREVENUE._serialized_end = 441
    _MSGUPDATEREVENUERESPONSE._serialized_start = 443
    _MSGUPDATEREVENUERESPONSE._serialized_end = 469
    _MSGCANCELREVENUE._serialized_start = 471
    _MSGCANCELREVENUE._serialized_end = 547
    _MSGCANCELREVENUERESPONSE._serialized_start = 549
    _MSGCANCELREVENUERESPONSE._serialized_end = 575
    _MSGUPDATEPARAMS._serialized_start = 577
    _MSGUPDATEPARAMS._serialized_end = 703
    _MSGUPDATEPARAMSRESPONSE._serialized_start = 705
    _MSGUPDATEPARAMSRESPONSE._serialized_end = 730
    _MSG._serialized_start = 733
    _MSG._serialized_end = 1269