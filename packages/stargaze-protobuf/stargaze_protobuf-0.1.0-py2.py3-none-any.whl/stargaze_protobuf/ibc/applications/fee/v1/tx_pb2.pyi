from gogoproto import gogo_pb2 as _gogo_pb2
from ibc.applications.fee.v1 import fee_pb2 as _fee_pb2
from ibc.core.channel.v1 import channel_pb2 as _channel_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgPayPacketFee(_message.Message):
    __slots__ = ['fee', 'relayers', 'signer', 'source_channel_id', 'source_port_id']
    FEE_FIELD_NUMBER: _ClassVar[int]
    RELAYERS_FIELD_NUMBER: _ClassVar[int]
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_PORT_ID_FIELD_NUMBER: _ClassVar[int]
    fee: _fee_pb2.Fee
    relayers: _containers.RepeatedScalarFieldContainer[str]
    signer: str
    source_channel_id: str
    source_port_id: str

    def __init__(self, fee: _Optional[_Union[_fee_pb2.Fee, _Mapping]]=..., source_port_id: _Optional[str]=..., source_channel_id: _Optional[str]=..., signer: _Optional[str]=..., relayers: _Optional[_Iterable[str]]=...) -> None:
        ...

class MsgPayPacketFeeAsync(_message.Message):
    __slots__ = ['packet_fee', 'packet_id']
    PACKET_FEE_FIELD_NUMBER: _ClassVar[int]
    PACKET_ID_FIELD_NUMBER: _ClassVar[int]
    packet_fee: _fee_pb2.PacketFee
    packet_id: _channel_pb2.PacketId

    def __init__(self, packet_id: _Optional[_Union[_channel_pb2.PacketId, _Mapping]]=..., packet_fee: _Optional[_Union[_fee_pb2.PacketFee, _Mapping]]=...) -> None:
        ...

class MsgPayPacketFeeAsyncResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgPayPacketFeeResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgRegisterCounterpartyPayee(_message.Message):
    __slots__ = ['channel_id', 'counterparty_payee', 'port_id', 'relayer']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTERPARTY_PAYEE_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    RELAYER_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    counterparty_payee: str
    port_id: str
    relayer: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., relayer: _Optional[str]=..., counterparty_payee: _Optional[str]=...) -> None:
        ...

class MsgRegisterCounterpartyPayeeResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgRegisterPayee(_message.Message):
    __slots__ = ['channel_id', 'payee', 'port_id', 'relayer']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PAYEE_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    RELAYER_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    payee: str
    port_id: str
    relayer: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., relayer: _Optional[str]=..., payee: _Optional[str]=...) -> None:
        ...

class MsgRegisterPayeeResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...