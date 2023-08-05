from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class DistributionProportions(_message.Message):
    __slots__ = ['developer_rewards', 'nft_incentives']
    DEVELOPER_REWARDS_FIELD_NUMBER: _ClassVar[int]
    NFT_INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    developer_rewards: str
    nft_incentives: str

    def __init__(self, nft_incentives: _Optional[str]=..., developer_rewards: _Optional[str]=...) -> None:
        ...

class Params(_message.Message):
    __slots__ = ['distribution_proportions', 'weighted_developer_rewards_receivers']
    DISTRIBUTION_PROPORTIONS_FIELD_NUMBER: _ClassVar[int]
    WEIGHTED_DEVELOPER_REWARDS_RECEIVERS_FIELD_NUMBER: _ClassVar[int]
    distribution_proportions: DistributionProportions
    weighted_developer_rewards_receivers: _containers.RepeatedCompositeFieldContainer[WeightedAddress]

    def __init__(self, distribution_proportions: _Optional[_Union[DistributionProportions, _Mapping]]=..., weighted_developer_rewards_receivers: _Optional[_Iterable[_Union[WeightedAddress, _Mapping]]]=...) -> None:
        ...

class WeightedAddress(_message.Message):
    __slots__ = ['address', 'weight']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    address: str
    weight: str

    def __init__(self, address: _Optional[str]=..., weight: _Optional[str]=...) -> None:
        ...