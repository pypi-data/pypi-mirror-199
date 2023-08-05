from gogoproto import gogo_pb2 as _gogo_pb2
from ibc.applications.fee.v1 import fee_pb2 as _fee_pb2
from ibc.core.channel.v1 import channel_pb2 as _channel_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class FeeEnabledChannel(_message.Message):
    __slots__ = ['channel_id', 'port_id']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=...) -> None:
        ...

class ForwardRelayerAddress(_message.Message):
    __slots__ = ['address', 'packet_id']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PACKET_ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    packet_id: _channel_pb2.PacketId

    def __init__(self, address: _Optional[str]=..., packet_id: _Optional[_Union[_channel_pb2.PacketId, _Mapping]]=...) -> None:
        ...

class GenesisState(_message.Message):
    __slots__ = ['fee_enabled_channels', 'forward_relayers', 'identified_fees', 'registered_counterparty_payees', 'registered_payees']
    FEE_ENABLED_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    FORWARD_RELAYERS_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIED_FEES_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_COUNTERPARTY_PAYEES_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_PAYEES_FIELD_NUMBER: _ClassVar[int]
    fee_enabled_channels: _containers.RepeatedCompositeFieldContainer[FeeEnabledChannel]
    forward_relayers: _containers.RepeatedCompositeFieldContainer[ForwardRelayerAddress]
    identified_fees: _containers.RepeatedCompositeFieldContainer[_fee_pb2.IdentifiedPacketFees]
    registered_counterparty_payees: _containers.RepeatedCompositeFieldContainer[RegisteredCounterpartyPayee]
    registered_payees: _containers.RepeatedCompositeFieldContainer[RegisteredPayee]

    def __init__(self, identified_fees: _Optional[_Iterable[_Union[_fee_pb2.IdentifiedPacketFees, _Mapping]]]=..., fee_enabled_channels: _Optional[_Iterable[_Union[FeeEnabledChannel, _Mapping]]]=..., registered_payees: _Optional[_Iterable[_Union[RegisteredPayee, _Mapping]]]=..., registered_counterparty_payees: _Optional[_Iterable[_Union[RegisteredCounterpartyPayee, _Mapping]]]=..., forward_relayers: _Optional[_Iterable[_Union[ForwardRelayerAddress, _Mapping]]]=...) -> None:
        ...

class RegisteredCounterpartyPayee(_message.Message):
    __slots__ = ['channel_id', 'counterparty_payee', 'relayer']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTERPARTY_PAYEE_FIELD_NUMBER: _ClassVar[int]
    RELAYER_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    counterparty_payee: str
    relayer: str

    def __init__(self, channel_id: _Optional[str]=..., relayer: _Optional[str]=..., counterparty_payee: _Optional[str]=...) -> None:
        ...

class RegisteredPayee(_message.Message):
    __slots__ = ['channel_id', 'payee', 'relayer']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PAYEE_FIELD_NUMBER: _ClassVar[int]
    RELAYER_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    payee: str
    relayer: str

    def __init__(self, channel_id: _Optional[str]=..., relayer: _Optional[str]=..., payee: _Optional[str]=...) -> None:
        ...