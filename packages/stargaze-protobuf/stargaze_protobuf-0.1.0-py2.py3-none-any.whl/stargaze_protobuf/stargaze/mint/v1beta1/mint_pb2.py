"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n stargaze/mint/v1beta1/mint.proto\x12\x15stargaze.mint.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto"o\n\x06Minter\x12e\n\x11annual_provisions\x18\x01 \x01(\tBJ\xf2\xde\x1f\x18yaml:"annual_provisions"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00"\x82\x03\n\x06Params\x12\x12\n\nmint_denom\x18\x01 \x01(\t\x12M\n\nstart_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1d\x90\xdf\x1f\x01\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x12u\n\x19initial_annual_provisions\x18\x03 \x01(\tBR\xf2\xde\x1f yaml:"initial_annual_provisions"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12c\n\x10reduction_factor\x18\x04 \x01(\tBI\xf2\xde\x1f\x17yaml:"reduction_factor"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x123\n\x0fblocks_per_year\x18\x05 \x01(\x04B\x1a\xf2\xde\x1f\x16yaml:"blocks_per_year":\x04\x98\xa0\x1f\x00B4Z2github.com/public-awesome/stargaze/v9/x/mint/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.mint.v1beta1.mint_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z2github.com/public-awesome/stargaze/v9/x/mint/types'
    _MINTER.fields_by_name['annual_provisions']._options = None
    _MINTER.fields_by_name['annual_provisions']._serialized_options = b'\xf2\xde\x1f\x18yaml:"annual_provisions"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00'
    _PARAMS.fields_by_name['start_time']._options = None
    _PARAMS.fields_by_name['start_time']._serialized_options = b'\x90\xdf\x1f\x01\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"'
    _PARAMS.fields_by_name['initial_annual_provisions']._options = None
    _PARAMS.fields_by_name['initial_annual_provisions']._serialized_options = b'\xf2\xde\x1f yaml:"initial_annual_provisions"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00'
    _PARAMS.fields_by_name['reduction_factor']._options = None
    _PARAMS.fields_by_name['reduction_factor']._serialized_options = b'\xf2\xde\x1f\x17yaml:"reduction_factor"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00'
    _PARAMS.fields_by_name['blocks_per_year']._options = None
    _PARAMS.fields_by_name['blocks_per_year']._serialized_options = b'\xf2\xde\x1f\x16yaml:"blocks_per_year"'
    _PARAMS._options = None
    _PARAMS._serialized_options = b'\x98\xa0\x1f\x00'
    _MINTER._serialized_start = 114
    _MINTER._serialized_end = 225
    _PARAMS._serialized_start = 228
    _PARAMS._serialized_end = 614