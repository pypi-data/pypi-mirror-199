"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bevmos/erc20/v1/events.proto\x12\x0eevmos.erc20.v1"9\n\x11EventRegisterPair\x12\r\n\x05denom\x18\x01 \x01(\t\x12\x15\n\rerc20_address\x18\x02 \x01(\t"B\n\x1aEventToggleTokenConversion\x12\r\n\x05denom\x18\x01 \x01(\t\x12\x15\n\rerc20_address\x18\x02 \x01(\t"j\n\x10EventConvertCoin\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x10\n\x08receiver\x18\x02 \x01(\t\x12\x0e\n\x06amount\x18\x03 \x01(\t\x12\r\n\x05denom\x18\x04 \x01(\t\x12\x15\n\rerc20_address\x18\x05 \x01(\t"n\n\x11EventConvertERC20\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x10\n\x08receiver\x18\x02 \x01(\t\x12\x0e\n\x06amount\x18\x03 \x01(\t\x12\r\n\x05denom\x18\x04 \x01(\t\x12\x18\n\x10contract_address\x18\x05 \x01(\tB*Z(github.com/evmos/evmos/v12/x/erc20/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.erc20.v1.events_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z(github.com/evmos/evmos/v12/x/erc20/types'
    _EVENTREGISTERPAIR._serialized_start = 47
    _EVENTREGISTERPAIR._serialized_end = 104
    _EVENTTOGGLETOKENCONVERSION._serialized_start = 106
    _EVENTTOGGLETOKENCONVERSION._serialized_end = 172
    _EVENTCONVERTCOIN._serialized_start = 174
    _EVENTCONVERTCOIN._serialized_end = 280
    _EVENTCONVERTERC20._serialized_start = 282
    _EVENTCONVERTERC20._serialized_end = 392