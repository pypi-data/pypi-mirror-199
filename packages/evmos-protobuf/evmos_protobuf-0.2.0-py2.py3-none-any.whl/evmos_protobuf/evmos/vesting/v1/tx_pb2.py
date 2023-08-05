"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.vesting.v1beta1 import vesting_pb2 as cosmos_dot_vesting_dot_v1beta1_dot_vesting__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19evmos/vesting/v1/tx.proto\x12\x10evmos.vesting.v1\x1a$cosmos/vesting/v1beta1/vesting.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x91\x03\n\x1fMsgCreateClawbackVestingAccount\x12\x14\n\x0cfrom_address\x18\x01 \x01(\t\x12\x12\n\nto_address\x18\x02 \x01(\t\x128\n\nstart_time\x18\x03 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\x90\xdf\x1f\x01\xc8\xde\x1f\x00\x12y\n\x0elockup_periods\x18\x04 \x03(\x0b2\x1e.cosmos.vesting.v1beta1.PeriodBA\xc8\xde\x1f\x00\xaa\xdf\x1f9github.com/cosmos/cosmos-sdk/x/auth/vesting/types.Periods\x12z\n\x0fvesting_periods\x18\x05 \x03(\x0b2\x1e.cosmos.vesting.v1beta1.PeriodBA\xc8\xde\x1f\x00\xaa\xdf\x1f9github.com/cosmos/cosmos-sdk/x/auth/vesting/types.Periods\x12\r\n\x05merge\x18\x06 \x01(\x08:\x04\xe8\xa0\x1f\x00")\n\'MsgCreateClawbackVestingAccountResponse"T\n\x0bMsgClawback\x12\x16\n\x0efunder_address\x18\x01 \x01(\t\x12\x17\n\x0faccount_address\x18\x02 \x01(\t\x12\x14\n\x0cdest_address\x18\x03 \x01(\t"\x15\n\x13MsgClawbackResponse"e\n\x16MsgUpdateVestingFunder\x12\x16\n\x0efunder_address\x18\x01 \x01(\t\x12\x1a\n\x12new_funder_address\x18\x02 \x01(\t\x12\x17\n\x0fvesting_address\x18\x03 \x01(\t" \n\x1eMsgUpdateVestingFunderResponse"3\n\x18MsgConvertVestingAccount\x12\x17\n\x0fvesting_address\x18\x01 \x01(\t""\n MsgConvertVestingAccountResponse2\xa3\x05\n\x03Msg\x12\xca\x01\n\x1cCreateClawbackVestingAccount\x121.evmos.vesting.v1.MsgCreateClawbackVestingAccount\x1a9.evmos.vesting.v1.MsgCreateClawbackVestingAccountResponse"<\x82\xd3\xe4\x93\x026\x124/evmos/vesting/v1/tx/create_clawback_vesting_account\x12w\n\x08Clawback\x12\x1d.evmos.vesting.v1.MsgClawback\x1a%.evmos.vesting.v1.MsgClawbackResponse"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/evmos/vesting/v1/tx/clawback\x12\xa5\x01\n\x13UpdateVestingFunder\x12(.evmos.vesting.v1.MsgUpdateVestingFunder\x1a0.evmos.vesting.v1.MsgUpdateVestingFunderResponse"2\x82\xd3\xe4\x93\x02,\x12*/evmos/vesting/v1/tx/update_vesting_funder\x12\xad\x01\n\x15ConvertVestingAccount\x12*.evmos.vesting.v1.MsgConvertVestingAccount\x1a2.evmos.vesting.v1.MsgConvertVestingAccountResponse"4\x82\xd3\xe4\x93\x02.\x12,/evmos/vesting/v1/tx/convert_vesting_accountB,Z*github.com/evmos/evmos/v12/x/vesting/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.vesting.v1.tx_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z*github.com/evmos/evmos/v12/x/vesting/types'
    _MSGCREATECLAWBACKVESTINGACCOUNT.fields_by_name['start_time']._options = None
    _MSGCREATECLAWBACKVESTINGACCOUNT.fields_by_name['start_time']._serialized_options = b'\x90\xdf\x1f\x01\xc8\xde\x1f\x00'
    _MSGCREATECLAWBACKVESTINGACCOUNT.fields_by_name['lockup_periods']._options = None
    _MSGCREATECLAWBACKVESTINGACCOUNT.fields_by_name['lockup_periods']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f9github.com/cosmos/cosmos-sdk/x/auth/vesting/types.Periods'
    _MSGCREATECLAWBACKVESTINGACCOUNT.fields_by_name['vesting_periods']._options = None
    _MSGCREATECLAWBACKVESTINGACCOUNT.fields_by_name['vesting_periods']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f9github.com/cosmos/cosmos-sdk/x/auth/vesting/types.Periods'
    _MSGCREATECLAWBACKVESTINGACCOUNT._options = None
    _MSGCREATECLAWBACKVESTINGACCOUNT._serialized_options = b'\xe8\xa0\x1f\x00'
    _MSG.methods_by_name['CreateClawbackVestingAccount']._options = None
    _MSG.methods_by_name['CreateClawbackVestingAccount']._serialized_options = b'\x82\xd3\xe4\x93\x026\x124/evmos/vesting/v1/tx/create_clawback_vesting_account'
    _MSG.methods_by_name['Clawback']._options = None
    _MSG.methods_by_name['Clawback']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1f\x12\x1d/evmos/vesting/v1/tx/clawback'
    _MSG.methods_by_name['UpdateVestingFunder']._options = None
    _MSG.methods_by_name['UpdateVestingFunder']._serialized_options = b'\x82\xd3\xe4\x93\x02,\x12*/evmos/vesting/v1/tx/update_vesting_funder'
    _MSG.methods_by_name['ConvertVestingAccount']._options = None
    _MSG.methods_by_name['ConvertVestingAccount']._serialized_options = b'\x82\xd3\xe4\x93\x02.\x12,/evmos/vesting/v1/tx/convert_vesting_account'
    _MSGCREATECLAWBACKVESTINGACCOUNT._serialized_start = 171
    _MSGCREATECLAWBACKVESTINGACCOUNT._serialized_end = 572
    _MSGCREATECLAWBACKVESTINGACCOUNTRESPONSE._serialized_start = 574
    _MSGCREATECLAWBACKVESTINGACCOUNTRESPONSE._serialized_end = 615
    _MSGCLAWBACK._serialized_start = 617
    _MSGCLAWBACK._serialized_end = 701
    _MSGCLAWBACKRESPONSE._serialized_start = 703
    _MSGCLAWBACKRESPONSE._serialized_end = 724
    _MSGUPDATEVESTINGFUNDER._serialized_start = 726
    _MSGUPDATEVESTINGFUNDER._serialized_end = 827
    _MSGUPDATEVESTINGFUNDERRESPONSE._serialized_start = 829
    _MSGUPDATEVESTINGFUNDERRESPONSE._serialized_end = 861
    _MSGCONVERTVESTINGACCOUNT._serialized_start = 863
    _MSGCONVERTVESTINGACCOUNT._serialized_end = 914
    _MSGCONVERTVESTINGACCOUNTRESPONSE._serialized_start = 916
    _MSGCONVERTVESTINGACCOUNTRESPONSE._serialized_end = 950
    _MSG._serialized_start = 953
    _MSG._serialized_end = 1628