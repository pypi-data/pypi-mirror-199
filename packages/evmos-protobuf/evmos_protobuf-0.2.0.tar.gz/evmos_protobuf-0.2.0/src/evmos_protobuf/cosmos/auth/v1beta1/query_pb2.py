"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....cosmos.auth.v1beta1 import auth_pb2 as cosmos_dot_auth_dot_v1beta1_dot_auth__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fcosmos/auth/v1beta1/query.proto\x12\x13cosmos.auth.v1beta1\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x14gogoproto/gogo.proto\x1a\x19google/protobuf/any.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1ecosmos/auth/v1beta1/auth.proto\x1a\x19cosmos_proto/cosmos.proto"R\n\x14QueryAccountsRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x8a\x01\n\x15QueryAccountsResponse\x124\n\x08accounts\x18\x01 \x03(\x0b2\x14.google.protobuf.AnyB\x0c\xca\xb4-\x08AccountI\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"J\n\x13QueryAccountRequest\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString:\x08\xe8\xa0\x1f\x00\x88\xa0\x1f\x00"K\n\x14QueryAccountResponse\x123\n\x07account\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyB\x0c\xca\xb4-\x08AccountI"\x14\n\x12QueryParamsRequest"H\n\x13QueryParamsResponse\x121\n\x06params\x18\x01 \x01(\x0b2\x1b.cosmos.auth.v1beta1.ParamsB\x04\xc8\xde\x1f\x00"\x1c\n\x1aQueryModuleAccountsRequest"Y\n\x1bQueryModuleAccountsResponse\x12:\n\x08accounts\x18\x01 \x03(\x0b2\x14.google.protobuf.AnyB\x12\xca\xb4-\x0eModuleAccountI"/\n\x1fQueryModuleAccountByNameRequest\x12\x0c\n\x04name\x18\x01 \x01(\t"]\n QueryModuleAccountByNameResponse\x129\n\x07account\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyB\x12\xca\xb4-\x0eModuleAccountI"\x15\n\x13Bech32PrefixRequest"-\n\x14Bech32PrefixResponse\x12\x15\n\rbech32_prefix\x18\x01 \x01(\t"4\n\x1bAddressBytesToStringRequest\x12\x15\n\raddress_bytes\x18\x01 \x01(\x0c"6\n\x1cAddressBytesToStringResponse\x12\x16\n\x0eaddress_string\x18\x01 \x01(\t"5\n\x1bAddressStringToBytesRequest\x12\x16\n\x0eaddress_string\x18\x01 \x01(\t"5\n\x1cAddressStringToBytesResponse\x12\x15\n\raddress_bytes\x18\x01 \x01(\x0c",\n\x1eQueryAccountAddressByIDRequest\x12\n\n\x02id\x18\x01 \x01(\x03"T\n\x1fQueryAccountAddressByIDResponse\x121\n\x0faccount_address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString2\xaa\x0b\n\x05Query\x12\x88\x01\n\x08Accounts\x12).cosmos.auth.v1beta1.QueryAccountsRequest\x1a*.cosmos.auth.v1beta1.QueryAccountsResponse"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/cosmos/auth/v1beta1/accounts\x12\x8f\x01\n\x07Account\x12(.cosmos.auth.v1beta1.QueryAccountRequest\x1a).cosmos.auth.v1beta1.QueryAccountResponse"/\x82\xd3\xe4\x93\x02)\x12\'/cosmos/auth/v1beta1/accounts/{address}\x12\xb0\x01\n\x12AccountAddressByID\x123.cosmos.auth.v1beta1.QueryAccountAddressByIDRequest\x1a4.cosmos.auth.v1beta1.QueryAccountAddressByIDResponse"/\x82\xd3\xe4\x93\x02)\x12\'/cosmos/auth/v1beta1/address_by_id/{id}\x12\x80\x01\n\x06Params\x12\'.cosmos.auth.v1beta1.QueryParamsRequest\x1a(.cosmos.auth.v1beta1.QueryParamsResponse"#\x82\xd3\xe4\x93\x02\x1d\x12\x1b/cosmos/auth/v1beta1/params\x12\xa1\x01\n\x0eModuleAccounts\x12/.cosmos.auth.v1beta1.QueryModuleAccountsRequest\x1a0.cosmos.auth.v1beta1.QueryModuleAccountsResponse",\x82\xd3\xe4\x93\x02&\x12$/cosmos/auth/v1beta1/module_accounts\x12\xb7\x01\n\x13ModuleAccountByName\x124.cosmos.auth.v1beta1.QueryModuleAccountByNameRequest\x1a5.cosmos.auth.v1beta1.QueryModuleAccountByNameResponse"3\x82\xd3\xe4\x93\x02-\x12+/cosmos/auth/v1beta1/module_accounts/{name}\x12\x88\x01\n\x0cBech32Prefix\x12(.cosmos.auth.v1beta1.Bech32PrefixRequest\x1a).cosmos.auth.v1beta1.Bech32PrefixResponse"#\x82\xd3\xe4\x93\x02\x1d\x12\x1b/cosmos/auth/v1beta1/bech32\x12\xb0\x01\n\x14AddressBytesToString\x120.cosmos.auth.v1beta1.AddressBytesToStringRequest\x1a1.cosmos.auth.v1beta1.AddressBytesToStringResponse"3\x82\xd3\xe4\x93\x02-\x12+/cosmos/auth/v1beta1/bech32/{address_bytes}\x12\xb1\x01\n\x14AddressStringToBytes\x120.cosmos.auth.v1beta1.AddressStringToBytesRequest\x1a1.cosmos.auth.v1beta1.AddressStringToBytesResponse"4\x82\xd3\xe4\x93\x02.\x12,/cosmos/auth/v1beta1/bech32/{address_string}B+Z)github.com/cosmos/cosmos-sdk/x/auth/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.auth.v1beta1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z)github.com/cosmos/cosmos-sdk/x/auth/types'
    _QUERYACCOUNTSRESPONSE.fields_by_name['accounts']._options = None
    _QUERYACCOUNTSRESPONSE.fields_by_name['accounts']._serialized_options = b'\xca\xb4-\x08AccountI'
    _QUERYACCOUNTREQUEST.fields_by_name['address']._options = None
    _QUERYACCOUNTREQUEST.fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _QUERYACCOUNTREQUEST._options = None
    _QUERYACCOUNTREQUEST._serialized_options = b'\xe8\xa0\x1f\x00\x88\xa0\x1f\x00'
    _QUERYACCOUNTRESPONSE.fields_by_name['account']._options = None
    _QUERYACCOUNTRESPONSE.fields_by_name['account']._serialized_options = b'\xca\xb4-\x08AccountI'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYMODULEACCOUNTSRESPONSE.fields_by_name['accounts']._options = None
    _QUERYMODULEACCOUNTSRESPONSE.fields_by_name['accounts']._serialized_options = b'\xca\xb4-\x0eModuleAccountI'
    _QUERYMODULEACCOUNTBYNAMERESPONSE.fields_by_name['account']._options = None
    _QUERYMODULEACCOUNTBYNAMERESPONSE.fields_by_name['account']._serialized_options = b'\xca\xb4-\x0eModuleAccountI'
    _QUERYACCOUNTADDRESSBYIDRESPONSE.fields_by_name['account_address']._options = None
    _QUERYACCOUNTADDRESSBYIDRESPONSE.fields_by_name['account_address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _QUERY.methods_by_name['Accounts']._options = None
    _QUERY.methods_by_name['Accounts']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1f\x12\x1d/cosmos/auth/v1beta1/accounts'
    _QUERY.methods_by_name['Account']._options = None
    _QUERY.methods_by_name['Account']._serialized_options = b"\x82\xd3\xe4\x93\x02)\x12'/cosmos/auth/v1beta1/accounts/{address}"
    _QUERY.methods_by_name['AccountAddressByID']._options = None
    _QUERY.methods_by_name['AccountAddressByID']._serialized_options = b"\x82\xd3\xe4\x93\x02)\x12'/cosmos/auth/v1beta1/address_by_id/{id}"
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1d\x12\x1b/cosmos/auth/v1beta1/params'
    _QUERY.methods_by_name['ModuleAccounts']._options = None
    _QUERY.methods_by_name['ModuleAccounts']._serialized_options = b'\x82\xd3\xe4\x93\x02&\x12$/cosmos/auth/v1beta1/module_accounts'
    _QUERY.methods_by_name['ModuleAccountByName']._options = None
    _QUERY.methods_by_name['ModuleAccountByName']._serialized_options = b'\x82\xd3\xe4\x93\x02-\x12+/cosmos/auth/v1beta1/module_accounts/{name}'
    _QUERY.methods_by_name['Bech32Prefix']._options = None
    _QUERY.methods_by_name['Bech32Prefix']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1d\x12\x1b/cosmos/auth/v1beta1/bech32'
    _QUERY.methods_by_name['AddressBytesToString']._options = None
    _QUERY.methods_by_name['AddressBytesToString']._serialized_options = b'\x82\xd3\xe4\x93\x02-\x12+/cosmos/auth/v1beta1/bech32/{address_bytes}'
    _QUERY.methods_by_name['AddressStringToBytes']._options = None
    _QUERY.methods_by_name['AddressStringToBytes']._serialized_options = b'\x82\xd3\xe4\x93\x02.\x12,/cosmos/auth/v1beta1/bech32/{address_string}'
    _QUERYACCOUNTSREQUEST._serialized_start = 238
    _QUERYACCOUNTSREQUEST._serialized_end = 320
    _QUERYACCOUNTSRESPONSE._serialized_start = 323
    _QUERYACCOUNTSRESPONSE._serialized_end = 461
    _QUERYACCOUNTREQUEST._serialized_start = 463
    _QUERYACCOUNTREQUEST._serialized_end = 537
    _QUERYACCOUNTRESPONSE._serialized_start = 539
    _QUERYACCOUNTRESPONSE._serialized_end = 614
    _QUERYPARAMSREQUEST._serialized_start = 616
    _QUERYPARAMSREQUEST._serialized_end = 636
    _QUERYPARAMSRESPONSE._serialized_start = 638
    _QUERYPARAMSRESPONSE._serialized_end = 710
    _QUERYMODULEACCOUNTSREQUEST._serialized_start = 712
    _QUERYMODULEACCOUNTSREQUEST._serialized_end = 740
    _QUERYMODULEACCOUNTSRESPONSE._serialized_start = 742
    _QUERYMODULEACCOUNTSRESPONSE._serialized_end = 831
    _QUERYMODULEACCOUNTBYNAMEREQUEST._serialized_start = 833
    _QUERYMODULEACCOUNTBYNAMEREQUEST._serialized_end = 880
    _QUERYMODULEACCOUNTBYNAMERESPONSE._serialized_start = 882
    _QUERYMODULEACCOUNTBYNAMERESPONSE._serialized_end = 975
    _BECH32PREFIXREQUEST._serialized_start = 977
    _BECH32PREFIXREQUEST._serialized_end = 998
    _BECH32PREFIXRESPONSE._serialized_start = 1000
    _BECH32PREFIXRESPONSE._serialized_end = 1045
    _ADDRESSBYTESTOSTRINGREQUEST._serialized_start = 1047
    _ADDRESSBYTESTOSTRINGREQUEST._serialized_end = 1099
    _ADDRESSBYTESTOSTRINGRESPONSE._serialized_start = 1101
    _ADDRESSBYTESTOSTRINGRESPONSE._serialized_end = 1155
    _ADDRESSSTRINGTOBYTESREQUEST._serialized_start = 1157
    _ADDRESSSTRINGTOBYTESREQUEST._serialized_end = 1210
    _ADDRESSSTRINGTOBYTESRESPONSE._serialized_start = 1212
    _ADDRESSSTRINGTOBYTESRESPONSE._serialized_end = 1265
    _QUERYACCOUNTADDRESSBYIDREQUEST._serialized_start = 1267
    _QUERYACCOUNTADDRESSBYIDREQUEST._serialized_end = 1311
    _QUERYACCOUNTADDRESSBYIDRESPONSE._serialized_start = 1313
    _QUERYACCOUNTADDRESSBYIDRESPONSE._serialized_end = 1397
    _QUERY._serialized_start = 1400
    _QUERY._serialized_end = 2850