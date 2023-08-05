"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....evmos.erc20.v1 import genesis_pb2 as evmos_dot_erc20_dot_v1_dot_genesis__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17evmos/erc20/v1/tx.proto\x12\x0eevmos.erc20.v1\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x17cosmos/msg/v1/msg.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1cevmos/erc20/v1/genesis.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto"a\n\x0eMsgConvertCoin\x12-\n\x04coin\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x12\x10\n\x08receiver\x18\x02 \x01(\t\x12\x0e\n\x06sender\x18\x03 \x01(\t"\x18\n\x16MsgConvertCoinResponse"\x8d\x01\n\x0fMsgConvertERC20\x12\x18\n\x10contract_address\x18\x01 \x01(\t\x12>\n\x06amount\x18\x02 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00\x12\x10\n\x08receiver\x18\x03 \x01(\t\x12\x0e\n\x06sender\x18\x04 \x01(\t"\x19\n\x17MsgConvertERC20Response"|\n\x0fMsgUpdateParams\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12,\n\x06params\x18\x02 \x01(\x0b2\x16.evmos.erc20.v1.ParamsB\x04\xc8\xde\x1f\x00:\x0e\x82\xe7\xb0*\tauthority"\x19\n\x17MsgUpdateParamsResponse2\xe4\x02\n\x03Msg\x12~\n\x0bConvertCoin\x12\x1e.evmos.erc20.v1.MsgConvertCoin\x1a&.evmos.erc20.v1.MsgConvertCoinResponse"\'\x82\xd3\xe4\x93\x02!\x12\x1f/evmos/erc20/v1/tx/convert_coin\x12\x82\x01\n\x0cConvertERC20\x12\x1f.evmos.erc20.v1.MsgConvertERC20\x1a\'.evmos.erc20.v1.MsgConvertERC20Response"(\x82\xd3\xe4\x93\x02"\x12 /evmos/erc20/v1/tx/convert_erc20\x12X\n\x0cUpdateParams\x12\x1f.evmos.erc20.v1.MsgUpdateParams\x1a\'.evmos.erc20.v1.MsgUpdateParamsResponseB*Z(github.com/evmos/evmos/v12/x/erc20/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.erc20.v1.tx_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z(github.com/evmos/evmos/v12/x/erc20/types'
    _MSGCONVERTCOIN.fields_by_name['coin']._options = None
    _MSGCONVERTCOIN.fields_by_name['coin']._serialized_options = b'\xc8\xde\x1f\x00'
    _MSGCONVERTERC20.fields_by_name['amount']._options = None
    _MSGCONVERTERC20.fields_by_name['amount']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00'
    _MSGUPDATEPARAMS.fields_by_name['authority']._options = None
    _MSGUPDATEPARAMS.fields_by_name['authority']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _MSGUPDATEPARAMS.fields_by_name['params']._options = None
    _MSGUPDATEPARAMS.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _MSGUPDATEPARAMS._options = None
    _MSGUPDATEPARAMS._serialized_options = b'\x82\xe7\xb0*\tauthority'
    _MSG.methods_by_name['ConvertCoin']._options = None
    _MSG.methods_by_name['ConvertCoin']._serialized_options = b'\x82\xd3\xe4\x93\x02!\x12\x1f/evmos/erc20/v1/tx/convert_coin'
    _MSG.methods_by_name['ConvertERC20']._options = None
    _MSG.methods_by_name['ConvertERC20']._serialized_options = b'\x82\xd3\xe4\x93\x02"\x12 /evmos/erc20/v1/tx/convert_erc20'
    _MSGCONVERTCOIN._serialized_start = 209
    _MSGCONVERTCOIN._serialized_end = 306
    _MSGCONVERTCOINRESPONSE._serialized_start = 308
    _MSGCONVERTCOINRESPONSE._serialized_end = 332
    _MSGCONVERTERC20._serialized_start = 335
    _MSGCONVERTERC20._serialized_end = 476
    _MSGCONVERTERC20RESPONSE._serialized_start = 478
    _MSGCONVERTERC20RESPONSE._serialized_end = 503
    _MSGUPDATEPARAMS._serialized_start = 505
    _MSGUPDATEPARAMS._serialized_end = 629
    _MSGUPDATEPARAMSRESPONSE._serialized_start = 631
    _MSGUPDATEPARAMSRESPONSE._serialized_end = 656
    _MSG._serialized_start = 659
    _MSG._serialized_end = 1015