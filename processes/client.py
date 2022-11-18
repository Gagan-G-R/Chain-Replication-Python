import grpc
from generated import spec_pb2, spec_pb2_grpc


class Client():

    def __init__(self, args):

        self.coo_id = args["coordinator"]
        self.node_id = args["read"]
        read_channel = grpc.insecure_channel(f'localhost:{args["read"]}')
        self.read_stub = spec_pb2_grpc.NodeStub(read_channel)

        write_channel = grpc.insecure_channel(
            f'localhost:{args["coordinator"]}')
        self.write_stub = spec_pb2_grpc.CoordinatorStub(write_channel)

    def do_read(self, k):
        """read [KEY]
        Read the value for specified [KEY] from read node."""
        reply = self.read_stub.Read(spec_pb2.ReadRequest(key=k))
        return {reply.key: reply.value}

    def do_write(self, k, v):
        """write [KEY] [VALUE]
        Write the [VALUE] for specified [KEY] to CRAQ store."""

        reply = self.write_stub.Write(spec_pb2.WriteRequest(key=k, value=v))
        print(
            f'Update was {"successful" if reply.success else "unsuccessful"}')
        return True if reply.success else False

    def get_coo(self):
        return self.coo_id

    def get_node(self):
        return self.node_id
