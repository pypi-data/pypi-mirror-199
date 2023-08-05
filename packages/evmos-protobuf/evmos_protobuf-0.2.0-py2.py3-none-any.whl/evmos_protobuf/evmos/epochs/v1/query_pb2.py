"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....evmos.epochs.v1 import genesis_pb2 as evmos_dot_epochs_dot_v1_dot_genesis__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bevmos/epochs/v1/query.proto\x12\x0fevmos.epochs.v1\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x1devmos/epochs/v1/genesis.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto"T\n\x16QueryEpochsInfoRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x88\x01\n\x17QueryEpochsInfoResponse\x120\n\x06epochs\x18\x01 \x03(\x0b2\x1a.evmos.epochs.v1.EpochInfoB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse".\n\x18QueryCurrentEpochRequest\x12\x12\n\nidentifier\x18\x01 \x01(\t"2\n\x19QueryCurrentEpochResponse\x12\x15\n\rcurrent_epoch\x18\x01 \x01(\x032\x9a\x02\n\x05Query\x12\x80\x01\n\nEpochInfos\x12\'.evmos.epochs.v1.QueryEpochsInfoRequest\x1a(.evmos.epochs.v1.QueryEpochsInfoResponse"\x1f\x82\xd3\xe4\x93\x02\x19\x12\x17/evmos/epochs/v1/epochs\x12\x8d\x01\n\x0cCurrentEpoch\x12).evmos.epochs.v1.QueryCurrentEpochRequest\x1a*.evmos.epochs.v1.QueryCurrentEpochResponse"&\x82\xd3\xe4\x93\x02 \x12\x1e/evmos/epochs/v1/current_epochB+Z)github.com/evmos/evmos/v12/x/epochs/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'evmos.epochs.v1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z)github.com/evmos/evmos/v12/x/epochs/types'
    _QUERYEPOCHSINFORESPONSE.fields_by_name['epochs']._options = None
    _QUERYEPOCHSINFORESPONSE.fields_by_name['epochs']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERY.methods_by_name['EpochInfos']._options = None
    _QUERY.methods_by_name['EpochInfos']._serialized_options = b'\x82\xd3\xe4\x93\x02\x19\x12\x17/evmos/epochs/v1/epochs'
    _QUERY.methods_by_name['CurrentEpoch']._options = None
    _QUERY.methods_by_name['CurrentEpoch']._serialized_options = b'\x82\xd3\xe4\x93\x02 \x12\x1e/evmos/epochs/v1/current_epoch'
    _QUERYEPOCHSINFOREQUEST._serialized_start = 175
    _QUERYEPOCHSINFOREQUEST._serialized_end = 259
    _QUERYEPOCHSINFORESPONSE._serialized_start = 262
    _QUERYEPOCHSINFORESPONSE._serialized_end = 398
    _QUERYCURRENTEPOCHREQUEST._serialized_start = 400
    _QUERYCURRENTEPOCHREQUEST._serialized_end = 446
    _QUERYCURRENTEPOCHRESPONSE._serialized_start = 448
    _QUERYCURRENTEPOCHRESPONSE._serialized_end = 498
    _QUERY._serialized_start = 501
    _QUERY._serialized_end = 783