from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Minter(_message.Message):
    __slots__ = ['annual_provisions']
    ANNUAL_PROVISIONS_FIELD_NUMBER: _ClassVar[int]
    annual_provisions: str

    def __init__(self, annual_provisions: _Optional[str]=...) -> None:
        ...

class Params(_message.Message):
    __slots__ = ['blocks_per_year', 'initial_annual_provisions', 'mint_denom', 'reduction_factor', 'start_time']
    BLOCKS_PER_YEAR_FIELD_NUMBER: _ClassVar[int]
    INITIAL_ANNUAL_PROVISIONS_FIELD_NUMBER: _ClassVar[int]
    MINT_DENOM_FIELD_NUMBER: _ClassVar[int]
    REDUCTION_FACTOR_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    blocks_per_year: int
    initial_annual_provisions: str
    mint_denom: str
    reduction_factor: str
    start_time: _timestamp_pb2.Timestamp

    def __init__(self, mint_denom: _Optional[str]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., initial_annual_provisions: _Optional[str]=..., reduction_factor: _Optional[str]=..., blocks_per_year: _Optional[int]=...) -> None:
        ...