from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from stargaze.claim.v1beta1 import claim_record_pb2 as _claim_record_pb2
from stargaze.claim.v1beta1 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryClaimRecordRequest(_message.Message):
    __slots__ = ['address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str

    def __init__(self, address: _Optional[str]=...) -> None:
        ...

class QueryClaimRecordResponse(_message.Message):
    __slots__ = ['claim_record']
    CLAIM_RECORD_FIELD_NUMBER: _ClassVar[int]
    claim_record: _claim_record_pb2.ClaimRecord

    def __init__(self, claim_record: _Optional[_Union[_claim_record_pb2.ClaimRecord, _Mapping]]=...) -> None:
        ...

class QueryClaimableForActionRequest(_message.Message):
    __slots__ = ['action', 'address']
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    action: _claim_record_pb2.Action
    address: str

    def __init__(self, address: _Optional[str]=..., action: _Optional[_Union[_claim_record_pb2.Action, str]]=...) -> None:
        ...

class QueryClaimableForActionResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryModuleAccountBalanceRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryModuleAccountBalanceResponse(_message.Message):
    __slots__ = ['moduleAccountBalance']
    MODULEACCOUNTBALANCE_FIELD_NUMBER: _ClassVar[int]
    moduleAccountBalance: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, moduleAccountBalance: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=...) -> None:
        ...

class QueryTotalClaimableRequest(_message.Message):
    __slots__ = ['address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str

    def __init__(self, address: _Optional[str]=...) -> None:
        ...

class QueryTotalClaimableResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...