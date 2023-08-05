from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from stargaze.claim.v1beta1 import claim_record_pb2 as _claim_record_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ClaimAuthorization(_message.Message):
    __slots__ = ['action', 'contract_address']
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    action: _claim_record_pb2.Action
    contract_address: str

    def __init__(self, contract_address: _Optional[str]=..., action: _Optional[_Union[_claim_record_pb2.Action, str]]=...) -> None:
        ...

class Params(_message.Message):
    __slots__ = ['airdrop_enabled', 'airdrop_start_time', 'allowed_claimers', 'claim_denom', 'duration_of_decay', 'duration_until_decay']
    AIRDROP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    AIRDROP_START_TIME_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_CLAIMERS_FIELD_NUMBER: _ClassVar[int]
    CLAIM_DENOM_FIELD_NUMBER: _ClassVar[int]
    DURATION_OF_DECAY_FIELD_NUMBER: _ClassVar[int]
    DURATION_UNTIL_DECAY_FIELD_NUMBER: _ClassVar[int]
    airdrop_enabled: bool
    airdrop_start_time: _timestamp_pb2.Timestamp
    allowed_claimers: _containers.RepeatedCompositeFieldContainer[ClaimAuthorization]
    claim_denom: str
    duration_of_decay: _duration_pb2.Duration
    duration_until_decay: _duration_pb2.Duration

    def __init__(self, airdrop_enabled: bool=..., airdrop_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., duration_until_decay: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., duration_of_decay: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., claim_denom: _Optional[str]=..., allowed_claimers: _Optional[_Iterable[_Union[ClaimAuthorization, _Mapping]]]=...) -> None:
        ...