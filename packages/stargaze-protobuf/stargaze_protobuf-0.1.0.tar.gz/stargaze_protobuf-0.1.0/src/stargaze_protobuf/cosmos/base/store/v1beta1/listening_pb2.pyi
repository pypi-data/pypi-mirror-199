from tendermint.abci import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class BlockMetadata(_message.Message):
    __slots__ = ['deliver_txs', 'request_begin_block', 'request_end_block', 'response_begin_block', 'response_commit', 'response_end_block']

    class DeliverTx(_message.Message):
        __slots__ = ['request', 'response']
        REQUEST_FIELD_NUMBER: _ClassVar[int]
        RESPONSE_FIELD_NUMBER: _ClassVar[int]
        request: _types_pb2.RequestDeliverTx
        response: _types_pb2.ResponseDeliverTx

        def __init__(self, request: _Optional[_Union[_types_pb2.RequestDeliverTx, _Mapping]]=..., response: _Optional[_Union[_types_pb2.ResponseDeliverTx, _Mapping]]=...) -> None:
            ...
    DELIVER_TXS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BEGIN_BLOCK_FIELD_NUMBER: _ClassVar[int]
    REQUEST_END_BLOCK_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_BEGIN_BLOCK_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_COMMIT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_END_BLOCK_FIELD_NUMBER: _ClassVar[int]
    deliver_txs: _containers.RepeatedCompositeFieldContainer[BlockMetadata.DeliverTx]
    request_begin_block: _types_pb2.RequestBeginBlock
    request_end_block: _types_pb2.RequestEndBlock
    response_begin_block: _types_pb2.ResponseBeginBlock
    response_commit: _types_pb2.ResponseCommit
    response_end_block: _types_pb2.ResponseEndBlock

    def __init__(self, request_begin_block: _Optional[_Union[_types_pb2.RequestBeginBlock, _Mapping]]=..., response_begin_block: _Optional[_Union[_types_pb2.ResponseBeginBlock, _Mapping]]=..., deliver_txs: _Optional[_Iterable[_Union[BlockMetadata.DeliverTx, _Mapping]]]=..., request_end_block: _Optional[_Union[_types_pb2.RequestEndBlock, _Mapping]]=..., response_end_block: _Optional[_Union[_types_pb2.ResponseEndBlock, _Mapping]]=..., response_commit: _Optional[_Union[_types_pb2.ResponseCommit, _Mapping]]=...) -> None:
        ...

class StoreKVPair(_message.Message):
    __slots__ = ['delete', 'key', 'store_key', 'value']
    DELETE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    STORE_KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    delete: bool
    key: bytes
    store_key: str
    value: bytes

    def __init__(self, store_key: _Optional[str]=..., delete: bool=..., key: _Optional[bytes]=..., value: _Optional[bytes]=...) -> None:
        ...