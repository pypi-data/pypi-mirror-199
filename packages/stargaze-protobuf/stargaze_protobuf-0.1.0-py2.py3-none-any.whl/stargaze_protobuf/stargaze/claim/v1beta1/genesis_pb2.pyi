from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from stargaze.claim.v1beta1 import claim_record_pb2 as _claim_record_pb2
from stargaze.claim.v1beta1 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['claim_records', 'module_account_balance', 'params']
    CLAIM_RECORDS_FIELD_NUMBER: _ClassVar[int]
    MODULE_ACCOUNT_BALANCE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    claim_records: _containers.RepeatedCompositeFieldContainer[_claim_record_pb2.ClaimRecord]
    module_account_balance: _coin_pb2.Coin
    params: _params_pb2.Params

    def __init__(self, module_account_balance: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., params: _Optional[_Union[_params_pb2.Params, _Mapping]]=..., claim_records: _Optional[_Iterable[_Union[_claim_record_pb2.ClaimRecord, _Mapping]]]=...) -> None:
        ...