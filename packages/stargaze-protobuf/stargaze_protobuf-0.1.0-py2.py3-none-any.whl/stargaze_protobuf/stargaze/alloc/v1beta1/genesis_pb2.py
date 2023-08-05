"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....stargaze.alloc.v1beta1 import params_pb2 as stargaze_dot_alloc_dot_v1beta1_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$stargaze/alloc/v1beta1/genesis.proto\x12$publicawesome.stargaze.alloc.v1beta1\x1a\x14gogoproto/gogo.proto\x1a#stargaze/alloc/v1beta1/params.proto"R\n\x0cGenesisState\x12B\n\x06params\x18\x01 \x01(\x0b2,.publicawesome.stargaze.alloc.v1beta1.ParamsB\x04\xc8\xde\x1f\x00B5Z3github.com/public-awesome/stargaze/v9/x/alloc/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.alloc.v1beta1.genesis_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/public-awesome/stargaze/v9/x/alloc/types'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE._serialized_start = 137
    _GENESISSTATE._serialized_end = 219