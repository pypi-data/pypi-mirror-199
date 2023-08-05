from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
ActionBidNFT: Action
ActionDelegateStake: Action
ActionInitialClaim: Action
ActionMintNFT: Action
ActionVote: Action
DESCRIPTOR: _descriptor.FileDescriptor

class ClaimRecord(_message.Message):
    __slots__ = ['action_completed', 'address', 'initial_claimable_amount']
    ACTION_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_CLAIMABLE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    action_completed: _containers.RepeatedScalarFieldContainer[bool]
    address: str
    initial_claimable_amount: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, address: _Optional[str]=..., initial_claimable_amount: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., action_completed: _Optional[_Iterable[bool]]=...) -> None:
        ...

class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []