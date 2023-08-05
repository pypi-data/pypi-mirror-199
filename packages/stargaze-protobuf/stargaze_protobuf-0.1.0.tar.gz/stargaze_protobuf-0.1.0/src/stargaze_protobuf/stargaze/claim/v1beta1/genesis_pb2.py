"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....stargaze.claim.v1beta1 import claim_record_pb2 as stargaze_dot_claim_dot_v1beta1_dot_claim__record__pb2
from ....stargaze.claim.v1beta1 import params_pb2 as stargaze_dot_claim_dot_v1beta1_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$stargaze/claim/v1beta1/genesis.proto\x12$publicawesome.stargaze.claim.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a)stargaze/claim/v1beta1/claim_record.proto\x1a#stargaze/claim/v1beta1/params.proto"\xad\x02\n\x0cGenesisState\x12`\n\x16module_account_balance\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB%\xf2\xde\x1f\x1dyaml:"module_account_balance"\xc8\xde\x1f\x00\x12S\n\x06params\x18\x02 \x01(\x0b2,.publicawesome.stargaze.claim.v1beta1.ParamsB\x15\xf2\xde\x1f\ryaml:"params"\xc8\xde\x1f\x00\x12f\n\rclaim_records\x18\x03 \x03(\x0b21.publicawesome.stargaze.claim.v1beta1.ClaimRecordB\x1c\xf2\xde\x1f\x14yaml:"claim_records"\xc8\xde\x1f\x00B5Z3github.com/public-awesome/stargaze/v9/x/claim/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.claim.v1beta1.genesis_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/public-awesome/stargaze/v9/x/claim/types'
    _GENESISSTATE.fields_by_name['module_account_balance']._options = None
    _GENESISSTATE.fields_by_name['module_account_balance']._serialized_options = b'\xf2\xde\x1f\x1dyaml:"module_account_balance"\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xf2\xde\x1f\ryaml:"params"\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['claim_records']._options = None
    _GENESISSTATE.fields_by_name['claim_records']._serialized_options = b'\xf2\xde\x1f\x14yaml:"claim_records"\xc8\xde\x1f\x00'
    _GENESISSTATE._serialized_start = 213
    _GENESISSTATE._serialized_end = 514