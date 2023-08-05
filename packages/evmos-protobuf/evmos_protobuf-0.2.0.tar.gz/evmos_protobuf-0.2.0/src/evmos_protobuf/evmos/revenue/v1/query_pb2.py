"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....evmos.revenue.v1 import genesis_pb2 as evmos_dot_revenue_dot_v1_dot_genesis__pb2
from ....evmos.revenue.v1 import revenue_pb2 as evmos_dot_revenue_dot_v1_dot_revenue__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cevmos/revenue/v1/query.proto\x12\x10evmos.revenue.v1\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x1eevmos/revenue/v1/genesis.proto\x1a\x1eevmos/revenue/v1/revenue.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto"R\n\x14QueryRevenuesRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x87\x01\n\x15QueryRevenuesResponse\x121\n\x08revenues\x18\x01 \x03(\x0b2\x19.evmos.revenue.v1.RevenueB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"/\n\x13QueryRevenueRequest\x12\x18\n\x10contract_address\x18\x01 \x01(\t"H\n\x14QueryRevenueResponse\x120\n\x07revenue\x18\x01 \x01(\x0b2\x19.evmos.revenue.v1.RevenueB\x04\xc8\xde\x1f\x00"\x14\n\x12QueryParamsRequest"E\n\x13QueryParamsResponse\x12.\n\x06params\x18\x01 \x01(\x0b2\x18.evmos.revenue.v1.ParamsB\x04\xc8\xde\x1f\x00"t\n\x1cQueryDeployerRevenuesRequest\x12\x18\n\x10deployer_address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"x\n\x1dQueryDeployerRevenuesResponse\x12\x1a\n\x12contract_addresses\x18\x01 \x03(\t\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"x\n\x1eQueryWithdrawerRevenuesRequest\x12\x1a\n\x12withdrawer_address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"z\n\x1fQueryWithdrawerRevenuesResponse\x12\x1a\n\x12contract_addresses\x18\x01 \x03(\t\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse2\xf5\x05\n\x05Query\x12\x7f\n\x08Revenues\x12&.evmos.revenue.v1.QueryRevenuesRequest\x1a\'.evmos.revenue.v1.QueryRevenuesResponse""\x82\xd3\xe4\x93\x02\x1c\x12\x1a/evmos/revenue/v1/revenues\x12\x8f\x01\n\x07Revenue\x12%.evmos.revenue.v1.QueryRevenueRequest\x1a&.evmos.revenue.v1.QueryRevenueResponse"5\x82\xd3\xe4\x93\x02/\x12-/evmos/revenue/v1/revenues/{contract_address}\x12w\n\x06Params\x12$.evmos.revenue.v1.QueryParamsRequest\x1a%.evmos.revenue.v1.QueryParamsResponse" \x82\xd3\xe4\x93\x02\x1a\x12\x18/evmos/revenue/v1/params\x12\xaa\x01\n\x10DeployerRevenues\x12..evmos.revenue.v1.QueryDeployerRevenuesRequest\x1a/.evmos.revenue.v1.QueryDeployerRevenuesResponse"5\x82\xd3\xe4\x93\x02/\x12-/evmos/revenue/v1/revenues/{deployer_address}\x12\xb2\x01\n\x12WithdrawerRevenues\x120.evmos.revenue.v1.QueryWithdrawerRevenuesRequest\x1a1.evmos.revenue.v1.QueryWithdrawerRevenuesResponse"7\x82\xd3\xe4\x93\x021\x12//evmos/revenue/v1/revenues/{withdrawer_address}B/Z-github.com/evmos/evmos/v12/x/revenue/v1/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.revenue.v1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/evmos/evmos/v12/x/revenue/v1/types'
    _QUERYREVENUESRESPONSE.fields_by_name['revenues']._options = None
    _QUERYREVENUESRESPONSE.fields_by_name['revenues']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYREVENUERESPONSE.fields_by_name['revenue']._options = None
    _QUERYREVENUERESPONSE.fields_by_name['revenue']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERY.methods_by_name['Revenues']._options = None
    _QUERY.methods_by_name['Revenues']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1c\x12\x1a/evmos/revenue/v1/revenues'
    _QUERY.methods_by_name['Revenue']._options = None
    _QUERY.methods_by_name['Revenue']._serialized_options = b'\x82\xd3\xe4\x93\x02/\x12-/evmos/revenue/v1/revenues/{contract_address}'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1a\x12\x18/evmos/revenue/v1/params'
    _QUERY.methods_by_name['DeployerRevenues']._options = None
    _QUERY.methods_by_name['DeployerRevenues']._serialized_options = b'\x82\xd3\xe4\x93\x02/\x12-/evmos/revenue/v1/revenues/{deployer_address}'
    _QUERY.methods_by_name['WithdrawerRevenues']._options = None
    _QUERY.methods_by_name['WithdrawerRevenues']._serialized_options = b'\x82\xd3\xe4\x93\x021\x12//evmos/revenue/v1/revenues/{withdrawer_address}'
    _QUERYREVENUESREQUEST._serialized_start = 210
    _QUERYREVENUESREQUEST._serialized_end = 292
    _QUERYREVENUESRESPONSE._serialized_start = 295
    _QUERYREVENUESRESPONSE._serialized_end = 430
    _QUERYREVENUEREQUEST._serialized_start = 432
    _QUERYREVENUEREQUEST._serialized_end = 479
    _QUERYREVENUERESPONSE._serialized_start = 481
    _QUERYREVENUERESPONSE._serialized_end = 553
    _QUERYPARAMSREQUEST._serialized_start = 555
    _QUERYPARAMSREQUEST._serialized_end = 575
    _QUERYPARAMSRESPONSE._serialized_start = 577
    _QUERYPARAMSRESPONSE._serialized_end = 646
    _QUERYDEPLOYERREVENUESREQUEST._serialized_start = 648
    _QUERYDEPLOYERREVENUESREQUEST._serialized_end = 764
    _QUERYDEPLOYERREVENUESRESPONSE._serialized_start = 766
    _QUERYDEPLOYERREVENUESRESPONSE._serialized_end = 886
    _QUERYWITHDRAWERREVENUESREQUEST._serialized_start = 888
    _QUERYWITHDRAWERREVENUESREQUEST._serialized_end = 1008
    _QUERYWITHDRAWERREVENUESRESPONSE._serialized_start = 1010
    _QUERYWITHDRAWERREVENUESRESPONSE._serialized_end = 1132
    _QUERY._serialized_start = 1135
    _QUERY._serialized_end = 1892