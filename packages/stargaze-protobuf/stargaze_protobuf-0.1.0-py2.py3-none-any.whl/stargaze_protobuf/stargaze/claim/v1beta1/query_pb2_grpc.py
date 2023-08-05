"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from ....stargaze.claim.v1beta1 import query_pb2 as stargaze_dot_claim_dot_v1beta1_dot_query__pb2

class QueryStub(object):
    """Query defines the gRPC querier service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ModuleAccountBalance = channel.unary_unary('/publicawesome.stargaze.claim.v1beta1.Query/ModuleAccountBalance', request_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryModuleAccountBalanceRequest.SerializeToString, response_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryModuleAccountBalanceResponse.FromString)
        self.Params = channel.unary_unary('/publicawesome.stargaze.claim.v1beta1.Query/Params', request_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString, response_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString)
        self.ClaimRecord = channel.unary_unary('/publicawesome.stargaze.claim.v1beta1.Query/ClaimRecord', request_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimRecordRequest.SerializeToString, response_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimRecordResponse.FromString)
        self.ClaimableForAction = channel.unary_unary('/publicawesome.stargaze.claim.v1beta1.Query/ClaimableForAction', request_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimableForActionRequest.SerializeToString, response_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimableForActionResponse.FromString)
        self.TotalClaimable = channel.unary_unary('/publicawesome.stargaze.claim.v1beta1.Query/TotalClaimable', request_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryTotalClaimableRequest.SerializeToString, response_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryTotalClaimableResponse.FromString)

class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def ModuleAccountBalance(self, request, context):
        """this line is used by starport scaffolding # 2
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Params(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClaimRecord(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClaimableForAction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TotalClaimable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'ModuleAccountBalance': grpc.unary_unary_rpc_method_handler(servicer.ModuleAccountBalance, request_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryModuleAccountBalanceRequest.FromString, response_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryModuleAccountBalanceResponse.SerializeToString), 'Params': grpc.unary_unary_rpc_method_handler(servicer.Params, request_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryParamsRequest.FromString, response_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryParamsResponse.SerializeToString), 'ClaimRecord': grpc.unary_unary_rpc_method_handler(servicer.ClaimRecord, request_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimRecordRequest.FromString, response_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimRecordResponse.SerializeToString), 'ClaimableForAction': grpc.unary_unary_rpc_method_handler(servicer.ClaimableForAction, request_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimableForActionRequest.FromString, response_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimableForActionResponse.SerializeToString), 'TotalClaimable': grpc.unary_unary_rpc_method_handler(servicer.TotalClaimable, request_deserializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryTotalClaimableRequest.FromString, response_serializer=stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryTotalClaimableResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('publicawesome.stargaze.claim.v1beta1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class Query(object):
    """Query defines the gRPC querier service.
    """

    @staticmethod
    def ModuleAccountBalance(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/publicawesome.stargaze.claim.v1beta1.Query/ModuleAccountBalance', stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryModuleAccountBalanceRequest.SerializeToString, stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryModuleAccountBalanceResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Params(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/publicawesome.stargaze.claim.v1beta1.Query/Params', stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString, stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClaimRecord(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/publicawesome.stargaze.claim.v1beta1.Query/ClaimRecord', stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimRecordRequest.SerializeToString, stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimRecordResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClaimableForAction(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/publicawesome.stargaze.claim.v1beta1.Query/ClaimableForAction', stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimableForActionRequest.SerializeToString, stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryClaimableForActionResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TotalClaimable(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/publicawesome.stargaze.claim.v1beta1.Query/TotalClaimable', stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryTotalClaimableRequest.SerializeToString, stargaze_dot_claim_dot_v1beta1_dot_query__pb2.QueryTotalClaimableResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)