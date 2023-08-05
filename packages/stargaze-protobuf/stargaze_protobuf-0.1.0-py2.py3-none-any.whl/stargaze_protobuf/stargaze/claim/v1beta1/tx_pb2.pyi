from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from stargaze.claim.v1beta1 import claim_record_pb2 as _claim_record_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgClaimFor(_message.Message):
    __slots__ = ['action', 'address', 'sender']
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    action: _claim_record_pb2.Action
    address: str
    sender: str

    def __init__(self, sender: _Optional[str]=..., address: _Optional[str]=..., action: _Optional[_Union[_claim_record_pb2.Action, str]]=...) -> None:
        ...

class MsgClaimForResponse(_message.Message):
    __slots__ = ['address', 'claimed_amount']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CLAIMED_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    address: str
    claimed_amount: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, address: _Optional[str]=..., claimed_amount: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class MsgInitialClaim(_message.Message):
    __slots__ = ['sender']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    sender: str

    def __init__(self, sender: _Optional[str]=...) -> None:
        ...

class MsgInitialClaimResponse(_message.Message):
    __slots__ = ['claimed_amount']
    CLAIMED_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    claimed_amount: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, claimed_amount: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...