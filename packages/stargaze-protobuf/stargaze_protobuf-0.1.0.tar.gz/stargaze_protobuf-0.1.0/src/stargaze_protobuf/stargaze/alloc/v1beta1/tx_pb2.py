"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fstargaze/alloc/v1beta1/tx.proto\x12$publicawesome.stargaze.alloc.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\xb9\x02\n\x17MsgCreateVestingAccount\x12-\n\x0cfrom_address\x18\x01 \x01(\tB\x17\xf2\xde\x1f\x13yaml:"from_address"\x12)\n\nto_address\x18\x02 \x01(\tB\x15\xf2\xde\x1f\x11yaml:"to_address"\x12[\n\x06amount\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12)\n\nstart_time\x18\x04 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"start_time"\x12%\n\x08end_time\x18\x05 \x01(\x03B\x13\xf2\xde\x1f\x0fyaml:"end_time"\x12\x0f\n\x07delayed\x18\x06 \x01(\x08:\x04\xe8\xa0\x1f\x01"!\n\x1fMsgCreateVestingAccountResponse"\x8c\x01\n\x13MsgFundFairburnPool\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12[\n\x06amount\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins:\x08\xe8\xa0\x1f\x00\x88\xa0\x1f\x00"\x1d\n\x1bMsgFundFairburnPoolResponse2\xb7\x02\n\x03Msg\x12\x9c\x01\n\x14CreateVestingAccount\x12=.publicawesome.stargaze.alloc.v1beta1.MsgCreateVestingAccount\x1aE.publicawesome.stargaze.alloc.v1beta1.MsgCreateVestingAccountResponse\x12\x90\x01\n\x10FundFairburnPool\x129.publicawesome.stargaze.alloc.v1beta1.MsgFundFairburnPool\x1aA.publicawesome.stargaze.alloc.v1beta1.MsgFundFairburnPoolResponseB5Z3github.com/public-awesome/stargaze/v9/x/alloc/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.alloc.v1beta1.tx_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/public-awesome/stargaze/v9/x/alloc/types'
    _MSGCREATEVESTINGACCOUNT.fields_by_name['from_address']._options = None
    _MSGCREATEVESTINGACCOUNT.fields_by_name['from_address']._serialized_options = b'\xf2\xde\x1f\x13yaml:"from_address"'
    _MSGCREATEVESTINGACCOUNT.fields_by_name['to_address']._options = None
    _MSGCREATEVESTINGACCOUNT.fields_by_name['to_address']._serialized_options = b'\xf2\xde\x1f\x11yaml:"to_address"'
    _MSGCREATEVESTINGACCOUNT.fields_by_name['amount']._options = None
    _MSGCREATEVESTINGACCOUNT.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGCREATEVESTINGACCOUNT.fields_by_name['start_time']._options = None
    _MSGCREATEVESTINGACCOUNT.fields_by_name['start_time']._serialized_options = b'\xf2\xde\x1f\x11yaml:"start_time"'
    _MSGCREATEVESTINGACCOUNT.fields_by_name['end_time']._options = None
    _MSGCREATEVESTINGACCOUNT.fields_by_name['end_time']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"end_time"'
    _MSGCREATEVESTINGACCOUNT._options = None
    _MSGCREATEVESTINGACCOUNT._serialized_options = b'\xe8\xa0\x1f\x01'
    _MSGFUNDFAIRBURNPOOL.fields_by_name['amount']._options = None
    _MSGFUNDFAIRBURNPOOL.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGFUNDFAIRBURNPOOL._options = None
    _MSGFUNDFAIRBURNPOOL._serialized_options = b'\xe8\xa0\x1f\x00\x88\xa0\x1f\x00'
    _MSGCREATEVESTINGACCOUNT._serialized_start = 128
    _MSGCREATEVESTINGACCOUNT._serialized_end = 441
    _MSGCREATEVESTINGACCOUNTRESPONSE._serialized_start = 443
    _MSGCREATEVESTINGACCOUNTRESPONSE._serialized_end = 476
    _MSGFUNDFAIRBURNPOOL._serialized_start = 479
    _MSGFUNDFAIRBURNPOOL._serialized_end = 619
    _MSGFUNDFAIRBURNPOOLRESPONSE._serialized_start = 621
    _MSGFUNDFAIRBURNPOOLRESPONSE._serialized_end = 650
    _MSG._serialized_start = 653
    _MSG._serialized_end = 964