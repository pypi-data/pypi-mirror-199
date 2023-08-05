"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....stargaze.mint.v1beta1 import mint_pb2 as stargaze_dot_mint_dot_v1beta1_dot_mint__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!stargaze/mint/v1beta1/query.proto\x12\x15stargaze.mint.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a stargaze/mint/v1beta1/mint.proto"\x14\n\x12QueryParamsRequest"J\n\x13QueryParamsResponse\x123\n\x06params\x18\x01 \x01(\x0b2\x1d.stargaze.mint.v1beta1.ParamsB\x04\xc8\xde\x1f\x00"\x1e\n\x1cQueryAnnualProvisionsRequest"j\n\x1dQueryAnnualProvisionsResponse\x12I\n\x11annual_provisions\x18\x01 \x01(\x0cB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x002\xc2\x02\n\x05Query\x12\x86\x01\n\x06Params\x12).stargaze.mint.v1beta1.QueryParamsRequest\x1a*.stargaze.mint.v1beta1.QueryParamsResponse"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/stargaze/mint/v1beta1/params\x12\xaf\x01\n\x10AnnualProvisions\x123.stargaze.mint.v1beta1.QueryAnnualProvisionsRequest\x1a4.stargaze.mint.v1beta1.QueryAnnualProvisionsResponse"0\x82\xd3\xe4\x93\x02*\x12(/stargaze/mint/v1beta1/annual_provisionsB4Z2github.com/public-awesome/stargaze/v9/x/mint/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.mint.v1beta1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z2github.com/public-awesome/stargaze/v9/x/mint/types'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYANNUALPROVISIONSRESPONSE.fields_by_name['annual_provisions']._options = None
    _QUERYANNUALPROVISIONSRESPONSE.fields_by_name['annual_provisions']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1f\x12\x1d/stargaze/mint/v1beta1/params'
    _QUERY.methods_by_name['AnnualProvisions']._options = None
    _QUERY.methods_by_name['AnnualProvisions']._serialized_options = b'\x82\xd3\xe4\x93\x02*\x12(/stargaze/mint/v1beta1/annual_provisions'
    _QUERYPARAMSREQUEST._serialized_start = 146
    _QUERYPARAMSREQUEST._serialized_end = 166
    _QUERYPARAMSRESPONSE._serialized_start = 168
    _QUERYPARAMSRESPONSE._serialized_end = 242
    _QUERYANNUALPROVISIONSREQUEST._serialized_start = 244
    _QUERYANNUALPROVISIONSREQUEST._serialized_end = 274
    _QUERYANNUALPROVISIONSRESPONSE._serialized_start = 276
    _QUERYANNUALPROVISIONSRESPONSE._serialized_end = 382
    _QUERY._serialized_start = 385
    _QUERY._serialized_end = 707