"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from .....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from .....tendermint.p2p import types_pb2 as tendermint_dot_p2p_dot_types__pb2
from .....tendermint.types import types_pb2 as tendermint_dot_types_dot_types__pb2
from .....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from .....cosmos.base.tendermint.v1beta1 import types_pb2 as cosmos_dot_base_dot_tendermint_dot_v1beta1_dot_types__pb2
from .....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from .....tendermint.types import block_pb2 as tendermint_dot_types_dot_block__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*cosmos/base/tendermint/v1beta1/query.proto\x12\x1ecosmos.base.tendermint.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19google/protobuf/any.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1atendermint/p2p/types.proto\x1a\x1ctendermint/types/types.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a*cosmos/base/tendermint/v1beta1/types.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1ctendermint/types/block.proto"l\n\x1eGetValidatorSetByHeightRequest\x12\x0e\n\x06height\x18\x01 \x01(\x03\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\xb3\x01\n\x1fGetValidatorSetByHeightResponse\x12\x14\n\x0cblock_height\x18\x01 \x01(\x03\x12=\n\nvalidators\x18\x02 \x03(\x0b2).cosmos.base.tendermint.v1beta1.Validator\x12;\n\npagination\x18\x03 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"Z\n\x1cGetLatestValidatorSetRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\xb1\x01\n\x1dGetLatestValidatorSetResponse\x12\x14\n\x0cblock_height\x18\x01 \x01(\x03\x12=\n\nvalidators\x18\x02 \x03(\x0b2).cosmos.base.tendermint.v1beta1.Validator\x12;\n\npagination\x18\x03 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x8e\x01\n\tValidator\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12%\n\x07pub_key\x18\x02 \x01(\x0b2\x14.google.protobuf.Any\x12\x14\n\x0cvoting_power\x18\x03 \x01(\x03\x12\x19\n\x11proposer_priority\x18\x04 \x01(\x03")\n\x17GetBlockByHeightRequest\x12\x0e\n\x06height\x18\x01 \x01(\x03"\xa9\x01\n\x18GetBlockByHeightResponse\x12+\n\x08block_id\x18\x01 \x01(\x0b2\x19.tendermint.types.BlockID\x12&\n\x05block\x18\x02 \x01(\x0b2\x17.tendermint.types.Block\x128\n\tsdk_block\x18\x03 \x01(\x0b2%.cosmos.base.tendermint.v1beta1.Block"\x17\n\x15GetLatestBlockRequest"\xa7\x01\n\x16GetLatestBlockResponse\x12+\n\x08block_id\x18\x01 \x01(\x0b2\x19.tendermint.types.BlockID\x12&\n\x05block\x18\x02 \x01(\x0b2\x17.tendermint.types.Block\x128\n\tsdk_block\x18\x03 \x01(\x0b2%.cosmos.base.tendermint.v1beta1.Block"\x13\n\x11GetSyncingRequest"%\n\x12GetSyncingResponse\x12\x0f\n\x07syncing\x18\x01 \x01(\x08"\x14\n\x12GetNodeInfoRequest"\x9b\x01\n\x13GetNodeInfoResponse\x12:\n\x11default_node_info\x18\x01 \x01(\x0b2\x1f.tendermint.p2p.DefaultNodeInfo\x12H\n\x13application_version\x18\x02 \x01(\x0b2+.cosmos.base.tendermint.v1beta1.VersionInfo"\xd2\x01\n\x0bVersionInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08app_name\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x12\n\ngit_commit\x18\x04 \x01(\t\x12\x12\n\nbuild_tags\x18\x05 \x01(\t\x12\x12\n\ngo_version\x18\x06 \x01(\t\x12:\n\nbuild_deps\x18\x07 \x03(\x0b2&.cosmos.base.tendermint.v1beta1.Module\x12\x1a\n\x12cosmos_sdk_version\x18\x08 \x01(\t"4\n\x06Module\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x0b\n\x03sum\x18\x03 \x01(\t"M\n\x10ABCIQueryRequest\x12\x0c\n\x04data\x18\x01 \x01(\x0c\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x0e\n\x06height\x18\x03 \x01(\x03\x12\r\n\x05prove\x18\x04 \x01(\x08"\xcd\x01\n\x11ABCIQueryResponse\x12\x0c\n\x04code\x18\x01 \x01(\r\x12\x0b\n\x03log\x18\x03 \x01(\t\x12\x0c\n\x04info\x18\x04 \x01(\t\x12\r\n\x05index\x18\x05 \x01(\x03\x12\x0b\n\x03key\x18\x06 \x01(\x0c\x12\r\n\x05value\x18\x07 \x01(\x0c\x12;\n\tproof_ops\x18\x08 \x01(\x0b2(.cosmos.base.tendermint.v1beta1.ProofOps\x12\x0e\n\x06height\x18\t \x01(\x03\x12\x11\n\tcodespace\x18\n \x01(\tJ\x04\x08\x02\x10\x03"2\n\x07ProofOp\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\x0c\x12\x0c\n\x04data\x18\x03 \x01(\x0c"F\n\x08ProofOps\x12:\n\x03ops\x18\x01 \x03(\x0b2\'.cosmos.base.tendermint.v1beta1.ProofOpB\x04\xc8\xde\x1f\x002\xaf\n\n\x07Service\x12\xa9\x01\n\x0bGetNodeInfo\x122.cosmos.base.tendermint.v1beta1.GetNodeInfoRequest\x1a3.cosmos.base.tendermint.v1beta1.GetNodeInfoResponse"1\x82\xd3\xe4\x93\x02+\x12)/cosmos/base/tendermint/v1beta1/node_info\x12\xa4\x01\n\nGetSyncing\x121.cosmos.base.tendermint.v1beta1.GetSyncingRequest\x1a2.cosmos.base.tendermint.v1beta1.GetSyncingResponse"/\x82\xd3\xe4\x93\x02)\x12\'/cosmos/base/tendermint/v1beta1/syncing\x12\xb6\x01\n\x0eGetLatestBlock\x125.cosmos.base.tendermint.v1beta1.GetLatestBlockRequest\x1a6.cosmos.base.tendermint.v1beta1.GetLatestBlockResponse"5\x82\xd3\xe4\x93\x02/\x12-/cosmos/base/tendermint/v1beta1/blocks/latest\x12\xbe\x01\n\x10GetBlockByHeight\x127.cosmos.base.tendermint.v1beta1.GetBlockByHeightRequest\x1a8.cosmos.base.tendermint.v1beta1.GetBlockByHeightResponse"7\x82\xd3\xe4\x93\x021\x12//cosmos/base/tendermint/v1beta1/blocks/{height}\x12\xd2\x01\n\x15GetLatestValidatorSet\x12<.cosmos.base.tendermint.v1beta1.GetLatestValidatorSetRequest\x1a=.cosmos.base.tendermint.v1beta1.GetLatestValidatorSetResponse"<\x82\xd3\xe4\x93\x026\x124/cosmos/base/tendermint/v1beta1/validatorsets/latest\x12\xda\x01\n\x17GetValidatorSetByHeight\x12>.cosmos.base.tendermint.v1beta1.GetValidatorSetByHeightRequest\x1a?.cosmos.base.tendermint.v1beta1.GetValidatorSetByHeightResponse">\x82\xd3\xe4\x93\x028\x126/cosmos/base/tendermint/v1beta1/validatorsets/{height}\x12\xa4\x01\n\tABCIQuery\x120.cosmos.base.tendermint.v1beta1.ABCIQueryRequest\x1a1.cosmos.base.tendermint.v1beta1.ABCIQueryResponse"2\x82\xd3\xe4\x93\x02,\x12*/cosmos/base/tendermint/v1beta1/abci_queryB4Z2github.com/cosmos/cosmos-sdk/client/grpc/tmserviceb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.base.tendermint.v1beta1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z2github.com/cosmos/cosmos-sdk/client/grpc/tmservice'
    _VALIDATOR.fields_by_name['address']._options = None
    _VALIDATOR.fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _PROOFOPS.fields_by_name['ops']._options = None
    _PROOFOPS.fields_by_name['ops']._serialized_options = b'\xc8\xde\x1f\x00'
    _SERVICE.methods_by_name['GetNodeInfo']._options = None
    _SERVICE.methods_by_name['GetNodeInfo']._serialized_options = b'\x82\xd3\xe4\x93\x02+\x12)/cosmos/base/tendermint/v1beta1/node_info'
    _SERVICE.methods_by_name['GetSyncing']._options = None
    _SERVICE.methods_by_name['GetSyncing']._serialized_options = b"\x82\xd3\xe4\x93\x02)\x12'/cosmos/base/tendermint/v1beta1/syncing"
    _SERVICE.methods_by_name['GetLatestBlock']._options = None
    _SERVICE.methods_by_name['GetLatestBlock']._serialized_options = b'\x82\xd3\xe4\x93\x02/\x12-/cosmos/base/tendermint/v1beta1/blocks/latest'
    _SERVICE.methods_by_name['GetBlockByHeight']._options = None
    _SERVICE.methods_by_name['GetBlockByHeight']._serialized_options = b'\x82\xd3\xe4\x93\x021\x12//cosmos/base/tendermint/v1beta1/blocks/{height}'
    _SERVICE.methods_by_name['GetLatestValidatorSet']._options = None
    _SERVICE.methods_by_name['GetLatestValidatorSet']._serialized_options = b'\x82\xd3\xe4\x93\x026\x124/cosmos/base/tendermint/v1beta1/validatorsets/latest'
    _SERVICE.methods_by_name['GetValidatorSetByHeight']._options = None
    _SERVICE.methods_by_name['GetValidatorSetByHeight']._serialized_options = b'\x82\xd3\xe4\x93\x028\x126/cosmos/base/tendermint/v1beta1/validatorsets/{height}'
    _SERVICE.methods_by_name['ABCIQuery']._options = None
    _SERVICE.methods_by_name['ABCIQuery']._serialized_options = b'\x82\xd3\xe4\x93\x02,\x12*/cosmos/base/tendermint/v1beta1/abci_query'
    _GETVALIDATORSETBYHEIGHTREQUEST._serialized_start = 360
    _GETVALIDATORSETBYHEIGHTREQUEST._serialized_end = 468
    _GETVALIDATORSETBYHEIGHTRESPONSE._serialized_start = 471
    _GETVALIDATORSETBYHEIGHTRESPONSE._serialized_end = 650
    _GETLATESTVALIDATORSETREQUEST._serialized_start = 652
    _GETLATESTVALIDATORSETREQUEST._serialized_end = 742
    _GETLATESTVALIDATORSETRESPONSE._serialized_start = 745
    _GETLATESTVALIDATORSETRESPONSE._serialized_end = 922
    _VALIDATOR._serialized_start = 925
    _VALIDATOR._serialized_end = 1067
    _GETBLOCKBYHEIGHTREQUEST._serialized_start = 1069
    _GETBLOCKBYHEIGHTREQUEST._serialized_end = 1110
    _GETBLOCKBYHEIGHTRESPONSE._serialized_start = 1113
    _GETBLOCKBYHEIGHTRESPONSE._serialized_end = 1282
    _GETLATESTBLOCKREQUEST._serialized_start = 1284
    _GETLATESTBLOCKREQUEST._serialized_end = 1307
    _GETLATESTBLOCKRESPONSE._serialized_start = 1310
    _GETLATESTBLOCKRESPONSE._serialized_end = 1477
    _GETSYNCINGREQUEST._serialized_start = 1479
    _GETSYNCINGREQUEST._serialized_end = 1498
    _GETSYNCINGRESPONSE._serialized_start = 1500
    _GETSYNCINGRESPONSE._serialized_end = 1537
    _GETNODEINFOREQUEST._serialized_start = 1539
    _GETNODEINFOREQUEST._serialized_end = 1559
    _GETNODEINFORESPONSE._serialized_start = 1562
    _GETNODEINFORESPONSE._serialized_end = 1717
    _VERSIONINFO._serialized_start = 1720
    _VERSIONINFO._serialized_end = 1930
    _MODULE._serialized_start = 1932
    _MODULE._serialized_end = 1984
    _ABCIQUERYREQUEST._serialized_start = 1986
    _ABCIQUERYREQUEST._serialized_end = 2063
    _ABCIQUERYRESPONSE._serialized_start = 2066
    _ABCIQUERYRESPONSE._serialized_end = 2271
    _PROOFOP._serialized_start = 2273
    _PROOFOP._serialized_end = 2323
    _PROOFOPS._serialized_start = 2325
    _PROOFOPS._serialized_end = 2395
    _SERVICE._serialized_start = 2398
    _SERVICE._serialized_end = 3725