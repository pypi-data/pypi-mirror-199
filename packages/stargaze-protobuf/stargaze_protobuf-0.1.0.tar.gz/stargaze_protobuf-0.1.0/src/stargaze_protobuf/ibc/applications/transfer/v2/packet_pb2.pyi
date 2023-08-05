from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class FungibleTokenPacketData(_message.Message):
    __slots__ = ['amount', 'denom', 'memo', 'receiver', 'sender']
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    MEMO_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    amount: str
    denom: str
    memo: str
    receiver: str
    sender: str

    def __init__(self, denom: _Optional[str]=..., amount: _Optional[str]=..., sender: _Optional[str]=..., receiver: _Optional[str]=..., memo: _Optional[str]=...) -> None:
        ...