"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....stargaze.alloc.v1beta1 import params_pb2 as stargaze_dot_alloc_dot_v1beta1_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"stargaze/alloc/v1beta1/query.proto\x12$publicawesome.stargaze.alloc.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a#stargaze/alloc/v1beta1/params.proto"\x14\n\x12QueryParamsRequest"Y\n\x13QueryParamsResponse\x12B\n\x06params\x18\x01 \x01(\x0b2,.publicawesome.stargaze.alloc.v1beta1.ParamsB\x04\xc8\xde\x1f\x002\xaf\x01\n\x05Query\x12\xa5\x01\n\x06Params\x128.publicawesome.stargaze.alloc.v1beta1.QueryParamsRequest\x1a9.publicawesome.stargaze.alloc.v1beta1.QueryParamsResponse"&\x82\xd3\xe4\x93\x02 \x12\x1e/stargaze/alloc/v1beta1/paramsB5Z3github.com/public-awesome/stargaze/v9/x/alloc/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.alloc.v1beta1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/public-awesome/stargaze/v9/x/alloc/types'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02 \x12\x1e/stargaze/alloc/v1beta1/params'
    _QUERYPARAMSREQUEST._serialized_start = 165
    _QUERYPARAMSREQUEST._serialized_end = 185
    _QUERYPARAMSRESPONSE._serialized_start = 187
    _QUERYPARAMSRESPONSE._serialized_end = 276
    _QUERY._serialized_start = 279
    _QUERY._serialized_end = 454