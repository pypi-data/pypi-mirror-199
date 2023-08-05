"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)stargaze/claim/v1beta1/claim_record.proto\x12$publicawesome.stargaze.claim.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x80\x02\n\x0bClaimRecord\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12\x90\x01\n\x18initial_claimable_amount\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBS\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"initial_claimable_amount"\x129\n\x10action_completed\x18\x04 \x03(\x08B\x1f\xf2\xde\x1f\x17yaml:"action_completed"\xc8\xde\x1f\x00*t\n\x06Action\x12\x16\n\x12ActionInitialClaim\x10\x00\x12\x10\n\x0cActionBidNFT\x10\x01\x12\x11\n\rActionMintNFT\x10\x02\x12\x0e\n\nActionVote\x10\x03\x12\x17\n\x13ActionDelegateStake\x10\x04\x1a\x04\x88\xa3\x1e\x00B5Z3github.com/public-awesome/stargaze/v9/x/claim/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.claim.v1beta1.claim_record_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/public-awesome/stargaze/v9/x/claim/types'
    _ACTION._options = None
    _ACTION._serialized_options = b'\x88\xa3\x1e\x00'
    _CLAIMRECORD.fields_by_name['address']._options = None
    _CLAIMRECORD.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _CLAIMRECORD.fields_by_name['initial_claimable_amount']._options = None
    _CLAIMRECORD.fields_by_name['initial_claimable_amount']._serialized_options = b'\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"initial_claimable_amount"'
    _CLAIMRECORD.fields_by_name['action_completed']._options = None
    _CLAIMRECORD.fields_by_name['action_completed']._serialized_options = b'\xf2\xde\x1f\x17yaml:"action_completed"\xc8\xde\x1f\x00'
    _ACTION._serialized_start = 396
    _ACTION._serialized_end = 512
    _CLAIMRECORD._serialized_start = 138
    _CLAIMRECORD._serialized_end = 394