"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ....stargaze.claim.v1beta1 import claim_record_pb2 as stargaze_dot_claim_dot_v1beta1_dot_claim__record__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#stargaze/claim/v1beta1/params.proto\x12$publicawesome.stargaze.claim.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a)stargaze/claim/v1beta1/claim_record.proto"\x9c\x01\n\x12ClaimAuthorization\x125\n\x10contract_address\x18\x01 \x01(\tB\x1b\xf2\xde\x1f\x17yaml:"contract_address"\x12O\n\x06action\x18\x02 \x01(\x0e2,.publicawesome.stargaze.claim.v1beta1.ActionB\x11\xf2\xde\x1f\ryaml:"action""\xa5\x04\n\x06Params\x12\x17\n\x0fairdrop_enabled\x18\x01 \x01(\x08\x12]\n\x12airdrop_start_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampB%\x90\xdf\x1f\x01\xc8\xde\x1f\x00\xf2\xde\x1f\x19yaml:"airdrop_start_time"\x12\x82\x01\n\x14duration_until_decay\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationBI\xc8\xde\x1f\x00\x98\xdf\x1f\x01\xea\xde\x1f\x1eduration_until_decay,omitempty\xf2\xde\x1f\x1byaml:"duration_until_decay"\x12y\n\x11duration_of_decay\x18\x04 \x01(\x0b2\x19.google.protobuf.DurationBC\xc8\xde\x1f\x00\x98\xdf\x1f\x01\xea\xde\x1f\x1bduration_of_decay,omitempty\xf2\xde\x1f\x18yaml:"duration_of_decay"\x12\x13\n\x0bclaim_denom\x18\x05 \x01(\t\x12\x87\x01\n\x10allowed_claimers\x18\x06 \x03(\x0b28.publicawesome.stargaze.claim.v1beta1.ClaimAuthorizationB3\xc8\xde\x1f\x00\xea\xde\x1f\x10allowed_claimers\xf2\xde\x1f\x17yaml:"allowed_claimers":\x04\x98\xa0\x1f\x00B5Z3github.com/public-awesome/stargaze/v9/x/claim/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.claim.v1beta1.params_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/public-awesome/stargaze/v9/x/claim/types'
    _CLAIMAUTHORIZATION.fields_by_name['contract_address']._options = None
    _CLAIMAUTHORIZATION.fields_by_name['contract_address']._serialized_options = b'\xf2\xde\x1f\x17yaml:"contract_address"'
    _CLAIMAUTHORIZATION.fields_by_name['action']._options = None
    _CLAIMAUTHORIZATION.fields_by_name['action']._serialized_options = b'\xf2\xde\x1f\ryaml:"action"'
    _PARAMS.fields_by_name['airdrop_start_time']._options = None
    _PARAMS.fields_by_name['airdrop_start_time']._serialized_options = b'\x90\xdf\x1f\x01\xc8\xde\x1f\x00\xf2\xde\x1f\x19yaml:"airdrop_start_time"'
    _PARAMS.fields_by_name['duration_until_decay']._options = None
    _PARAMS.fields_by_name['duration_until_decay']._serialized_options = b'\xc8\xde\x1f\x00\x98\xdf\x1f\x01\xea\xde\x1f\x1eduration_until_decay,omitempty\xf2\xde\x1f\x1byaml:"duration_until_decay"'
    _PARAMS.fields_by_name['duration_of_decay']._options = None
    _PARAMS.fields_by_name['duration_of_decay']._serialized_options = b'\xc8\xde\x1f\x00\x98\xdf\x1f\x01\xea\xde\x1f\x1bduration_of_decay,omitempty\xf2\xde\x1f\x18yaml:"duration_of_decay"'
    _PARAMS.fields_by_name['allowed_claimers']._options = None
    _PARAMS.fields_by_name['allowed_claimers']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x10allowed_claimers\xf2\xde\x1f\x17yaml:"allowed_claimers"'
    _PARAMS._options = None
    _PARAMS._serialized_options = b'\x98\xa0\x1f\x00'
    _CLAIMAUTHORIZATION._serialized_start = 208
    _CLAIMAUTHORIZATION._serialized_end = 364
    _PARAMS._serialized_start = 367
    _PARAMS._serialized_end = 916