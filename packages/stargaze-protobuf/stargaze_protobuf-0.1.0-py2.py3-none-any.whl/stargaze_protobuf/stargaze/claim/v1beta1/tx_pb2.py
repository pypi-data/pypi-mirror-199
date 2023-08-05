"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....stargaze.claim.v1beta1 import claim_record_pb2 as stargaze_dot_claim_dot_v1beta1_dot_claim__record__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fstargaze/claim/v1beta1/tx.proto\x12$publicawesome.stargaze.claim.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a)stargaze/claim/v1beta1/claim_record.proto"!\n\x0fMsgInitialClaim\x12\x0e\n\x06sender\x18\x01 \x01(\t"\x97\x01\n\x17MsgInitialClaimResponse\x12|\n\x0eclaimed_amount\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBI\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"claimed_amount""l\n\x0bMsgClaimFor\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x0f\n\x07address\x18\x02 \x01(\t\x12<\n\x06action\x18\x03 \x01(\x0e2,.publicawesome.stargaze.claim.v1beta1.Action"\xa4\x01\n\x13MsgClaimForResponse\x12\x0f\n\x07address\x18\x01 \x01(\t\x12|\n\x0eclaimed_amount\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBI\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"claimed_amount"2\x86\x02\n\x03Msg\x12\x84\x01\n\x0cInitialClaim\x125.publicawesome.stargaze.claim.v1beta1.MsgInitialClaim\x1a=.publicawesome.stargaze.claim.v1beta1.MsgInitialClaimResponse\x12x\n\x08ClaimFor\x121.publicawesome.stargaze.claim.v1beta1.MsgClaimFor\x1a9.publicawesome.stargaze.claim.v1beta1.MsgClaimForResponseB5Z3github.com/public-awesome/stargaze/v9/x/claim/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.claim.v1beta1.tx_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/public-awesome/stargaze/v9/x/claim/types'
    _MSGINITIALCLAIMRESPONSE.fields_by_name['claimed_amount']._options = None
    _MSGINITIALCLAIMRESPONSE.fields_by_name['claimed_amount']._serialized_options = b'\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"claimed_amount"'
    _MSGCLAIMFORRESPONSE.fields_by_name['claimed_amount']._options = None
    _MSGCLAIMFORRESPONSE.fields_by_name['claimed_amount']._serialized_options = b'\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"claimed_amount"'
    _MSGINITIALCLAIM._serialized_start = 170
    _MSGINITIALCLAIM._serialized_end = 203
    _MSGINITIALCLAIMRESPONSE._serialized_start = 206
    _MSGINITIALCLAIMRESPONSE._serialized_end = 357
    _MSGCLAIMFOR._serialized_start = 359
    _MSGCLAIMFOR._serialized_end = 467
    _MSGCLAIMFORRESPONSE._serialized_start = 470
    _MSGCLAIMFORRESPONSE._serialized_end = 634
    _MSG._serialized_start = 637
    _MSG._serialized_end = 899