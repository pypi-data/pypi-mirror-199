"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....stargaze.mint.v1beta1 import mint_pb2 as stargaze_dot_mint_dot_v1beta1_dot_mint__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#stargaze/mint/v1beta1/genesis.proto\x12\x15stargaze.mint.v1beta1\x1a\x14gogoproto/gogo.proto\x1a stargaze/mint/v1beta1/mint.proto"x\n\x0cGenesisState\x123\n\x06minter\x18\x01 \x01(\x0b2\x1d.stargaze.mint.v1beta1.MinterB\x04\xc8\xde\x1f\x00\x123\n\x06params\x18\x02 \x01(\x0b2\x1d.stargaze.mint.v1beta1.ParamsB\x04\xc8\xde\x1f\x00B4Z2github.com/public-awesome/stargaze/v9/x/mint/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.mint.v1beta1.genesis_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z2github.com/public-awesome/stargaze/v9/x/mint/types'
    _GENESISSTATE.fields_by_name['minter']._options = None
    _GENESISSTATE.fields_by_name['minter']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE._serialized_start = 118
    _GENESISSTATE._serialized_end = 238