"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....stargaze.claim.v1beta1 import claim_record_pb2 as stargaze_dot_claim_dot_v1beta1_dot_claim__record__pb2
from ....stargaze.claim.v1beta1 import params_pb2 as stargaze_dot_claim_dot_v1beta1_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"stargaze/claim/v1beta1/query.proto\x12$publicawesome.stargaze.claim.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a)stargaze/claim/v1beta1/claim_record.proto\x1a#stargaze/claim/v1beta1/params.proto""\n QueryModuleAccountBalanceRequest"\x9e\x01\n!QueryModuleAccountBalanceResponse\x12y\n\x14moduleAccountBalance\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB@\xf2\xde\x1f\x0cyaml:"coins"\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins"\x14\n\x12QueryParamsRequest"Y\n\x13QueryParamsResponse\x12B\n\x06params\x18\x01 \x01(\x0b2,.publicawesome.stargaze.claim.v1beta1.ParamsB\x04\xc8\xde\x1f\x00"=\n\x17QueryClaimRecordRequest\x12"\n\x07address\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender""\x80\x01\n\x18QueryClaimRecordResponse\x12d\n\x0cclaim_record\x18\x01 \x01(\x0b21.publicawesome.stargaze.claim.v1beta1.ClaimRecordB\x1b\xf2\xde\x1f\x13yaml:"claim_record"\xc8\xde\x1f\x00"\x96\x01\n\x1eQueryClaimableForActionRequest\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12O\n\x06action\x18\x02 \x01(\x0e2,.publicawesome.stargaze.claim.v1beta1.ActionB\x11\xf2\xde\x1f\ryaml:"action""\x8d\x01\n\x1fQueryClaimableForActionResponse\x12j\n\x05coins\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB@\xf2\xde\x1f\x0cyaml:"coins"\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins"A\n\x1aQueryTotalClaimableRequest\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address""\x89\x01\n\x1bQueryTotalClaimableResponse\x12j\n\x05coins\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB@\xf2\xde\x1f\x0cyaml:"coins"\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins2\x98\x08\n\x05Query\x12\xdf\x01\n\x14ModuleAccountBalance\x12F.publicawesome.stargaze.claim.v1beta1.QueryModuleAccountBalanceRequest\x1aG.publicawesome.stargaze.claim.v1beta1.QueryModuleAccountBalanceResponse"6\x82\xd3\xe4\x93\x020\x12./stargaze/claim/v1beta1/module_account_balance\x12\xa5\x01\n\x06Params\x128.publicawesome.stargaze.claim.v1beta1.QueryParamsRequest\x1a9.publicawesome.stargaze.claim.v1beta1.QueryParamsResponse"&\x82\xd3\xe4\x93\x02 \x12\x1e/stargaze/claim/v1beta1/params\x12\xc4\x01\n\x0bClaimRecord\x12=.publicawesome.stargaze.claim.v1beta1.QueryClaimRecordRequest\x1a>.publicawesome.stargaze.claim.v1beta1.QueryClaimRecordResponse"6\x82\xd3\xe4\x93\x020\x12./stargaze/claim/v1beta1/claim_record/{address}\x12\xea\x01\n\x12ClaimableForAction\x12D.publicawesome.stargaze.claim.v1beta1.QueryClaimableForActionRequest\x1aE.publicawesome.stargaze.claim.v1beta1.QueryClaimableForActionResponse"G\x82\xd3\xe4\x93\x02A\x12?/stargaze/claim/v1beta1/claimable_for_action/{address}/{action}\x12\xd0\x01\n\x0eTotalClaimable\x12@.publicawesome.stargaze.claim.v1beta1.QueryTotalClaimableRequest\x1aA.publicawesome.stargaze.claim.v1beta1.QueryTotalClaimableResponse"9\x82\xd3\xe4\x93\x023\x121/stargaze/claim/v1beta1/total_claimable/{address}B5Z3github.com/public-awesome/stargaze/v9/x/claim/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.claim.v1beta1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/public-awesome/stargaze/v9/x/claim/types'
    _QUERYMODULEACCOUNTBALANCERESPONSE.fields_by_name['moduleAccountBalance']._options = None
    _QUERYMODULEACCOUNTBALANCERESPONSE.fields_by_name['moduleAccountBalance']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"coins"\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYCLAIMRECORDREQUEST.fields_by_name['address']._options = None
    _QUERYCLAIMRECORDREQUEST.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _QUERYCLAIMRECORDRESPONSE.fields_by_name['claim_record']._options = None
    _QUERYCLAIMRECORDRESPONSE.fields_by_name['claim_record']._serialized_options = b'\xf2\xde\x1f\x13yaml:"claim_record"\xc8\xde\x1f\x00'
    _QUERYCLAIMABLEFORACTIONREQUEST.fields_by_name['address']._options = None
    _QUERYCLAIMABLEFORACTIONREQUEST.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _QUERYCLAIMABLEFORACTIONREQUEST.fields_by_name['action']._options = None
    _QUERYCLAIMABLEFORACTIONREQUEST.fields_by_name['action']._serialized_options = b'\xf2\xde\x1f\ryaml:"action"'
    _QUERYCLAIMABLEFORACTIONRESPONSE.fields_by_name['coins']._options = None
    _QUERYCLAIMABLEFORACTIONRESPONSE.fields_by_name['coins']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"coins"\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _QUERYTOTALCLAIMABLEREQUEST.fields_by_name['address']._options = None
    _QUERYTOTALCLAIMABLEREQUEST.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _QUERYTOTALCLAIMABLERESPONSE.fields_by_name['coins']._options = None
    _QUERYTOTALCLAIMABLERESPONSE.fields_by_name['coins']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"coins"\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _QUERY.methods_by_name['ModuleAccountBalance']._options = None
    _QUERY.methods_by_name['ModuleAccountBalance']._serialized_options = b'\x82\xd3\xe4\x93\x020\x12./stargaze/claim/v1beta1/module_account_balance'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02 \x12\x1e/stargaze/claim/v1beta1/params'
    _QUERY.methods_by_name['ClaimRecord']._options = None
    _QUERY.methods_by_name['ClaimRecord']._serialized_options = b'\x82\xd3\xe4\x93\x020\x12./stargaze/claim/v1beta1/claim_record/{address}'
    _QUERY.methods_by_name['ClaimableForAction']._options = None
    _QUERY.methods_by_name['ClaimableForAction']._serialized_options = b'\x82\xd3\xe4\x93\x02A\x12?/stargaze/claim/v1beta1/claimable_for_action/{address}/{action}'
    _QUERY.methods_by_name['TotalClaimable']._options = None
    _QUERY.methods_by_name['TotalClaimable']._serialized_options = b'\x82\xd3\xe4\x93\x023\x121/stargaze/claim/v1beta1/total_claimable/{address}'
    _QUERYMODULEACCOUNTBALANCEREQUEST._serialized_start = 240
    _QUERYMODULEACCOUNTBALANCEREQUEST._serialized_end = 274
    _QUERYMODULEACCOUNTBALANCERESPONSE._serialized_start = 277
    _QUERYMODULEACCOUNTBALANCERESPONSE._serialized_end = 435
    _QUERYPARAMSREQUEST._serialized_start = 437
    _QUERYPARAMSREQUEST._serialized_end = 457
    _QUERYPARAMSRESPONSE._serialized_start = 459
    _QUERYPARAMSRESPONSE._serialized_end = 548
    _QUERYCLAIMRECORDREQUEST._serialized_start = 550
    _QUERYCLAIMRECORDREQUEST._serialized_end = 611
    _QUERYCLAIMRECORDRESPONSE._serialized_start = 614
    _QUERYCLAIMRECORDRESPONSE._serialized_end = 742
    _QUERYCLAIMABLEFORACTIONREQUEST._serialized_start = 745
    _QUERYCLAIMABLEFORACTIONREQUEST._serialized_end = 895
    _QUERYCLAIMABLEFORACTIONRESPONSE._serialized_start = 898
    _QUERYCLAIMABLEFORACTIONRESPONSE._serialized_end = 1039
    _QUERYTOTALCLAIMABLEREQUEST._serialized_start = 1041
    _QUERYTOTALCLAIMABLEREQUEST._serialized_end = 1106
    _QUERYTOTALCLAIMABLERESPONSE._serialized_start = 1109
    _QUERYTOTALCLAIMABLERESPONSE._serialized_end = 1246
    _QUERY._serialized_start = 1249
    _QUERY._serialized_end = 2297