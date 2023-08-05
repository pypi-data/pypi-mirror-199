"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#stargaze/alloc/v1beta1/params.proto\x12$publicawesome.stargaze.alloc.v1beta1\x1a\x14gogoproto/gogo.proto"\x87\x01\n\x0fWeightedAddress\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12O\n\x06weight\x18\x02 \x01(\tB?\xf2\xde\x1f\ryaml:"weight"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00"\xe1\x01\n\x17DistributionProportions\x12_\n\x0enft_incentives\x18\x01 \x01(\tBG\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x15yaml:"nft_incentives"\xc8\xde\x1f\x00\x12e\n\x11developer_rewards\x18\x02 \x01(\tBJ\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x18yaml:"developer_rewards"\xc8\xde\x1f\x00"\x80\x02\n\x06Params\x12e\n\x18distribution_proportions\x18\x01 \x01(\x0b2=.publicawesome.stargaze.alloc.v1beta1.DistributionProportionsB\x04\xc8\xde\x1f\x00\x12\x8e\x01\n$weighted_developer_rewards_receivers\x18\x02 \x03(\x0b25.publicawesome.stargaze.alloc.v1beta1.WeightedAddressB)\xf2\xde\x1f!yaml:"developer_rewards_receiver"\xc8\xde\x1f\x00B5Z3github.com/public-awesome/stargaze/v9/x/alloc/typesb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stargaze.alloc.v1beta1.params_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/public-awesome/stargaze/v9/x/alloc/types'
    _WEIGHTEDADDRESS.fields_by_name['address']._options = None
    _WEIGHTEDADDRESS.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _WEIGHTEDADDRESS.fields_by_name['weight']._options = None
    _WEIGHTEDADDRESS.fields_by_name['weight']._serialized_options = b'\xf2\xde\x1f\ryaml:"weight"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00'
    _DISTRIBUTIONPROPORTIONS.fields_by_name['nft_incentives']._options = None
    _DISTRIBUTIONPROPORTIONS.fields_by_name['nft_incentives']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x15yaml:"nft_incentives"\xc8\xde\x1f\x00'
    _DISTRIBUTIONPROPORTIONS.fields_by_name['developer_rewards']._options = None
    _DISTRIBUTIONPROPORTIONS.fields_by_name['developer_rewards']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x18yaml:"developer_rewards"\xc8\xde\x1f\x00'
    _PARAMS.fields_by_name['distribution_proportions']._options = None
    _PARAMS.fields_by_name['distribution_proportions']._serialized_options = b'\xc8\xde\x1f\x00'
    _PARAMS.fields_by_name['weighted_developer_rewards_receivers']._options = None
    _PARAMS.fields_by_name['weighted_developer_rewards_receivers']._serialized_options = b'\xf2\xde\x1f!yaml:"developer_rewards_receiver"\xc8\xde\x1f\x00'
    _WEIGHTEDADDRESS._serialized_start = 100
    _WEIGHTEDADDRESS._serialized_end = 235
    _DISTRIBUTIONPROPORTIONS._serialized_start = 238
    _DISTRIBUTIONPROPORTIONS._serialized_end = 463
    _PARAMS._serialized_start = 466
    _PARAMS._serialized_end = 722