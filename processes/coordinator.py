from typing import List, Tuple
import logging
import argparse
from concurrent import futures
import grpc
from generated import spec_pb2, spec_pb2_grpc



class Coordinator(spec_pb2_grpc.Coordinator):
    def __init__(self):
        super(Coordinator, self).__init__()
        self.clients: List[Tuple[int, spec_pb2_grpc.NodeStub]] = []

    def Register(self, request: spec_pb2.RegisterRequest, context) -> spec_pb2.RegisterReply:
        if self.clients:
            reply = spec_pb2.RegisterReply(parentPort=self.clients[-1][0])
        else:
            reply = spec_pb2.RegisterReply(parentPort=-1)

        channel = grpc.insecure_channel(f'localhost:{request.port}')
        self.clients.append((request.port, spec_pb2_grpc.NodeStub(channel)))

        print("New Node Added at Port : ", request.port)
        return reply

    def Write(self, request: spec_pb2.WriteRequest, context) -> spec_pb2.WriteReply:

        unreachableClients = []
        for client in self.clients:
            try:
                res = client[1].Write(request)

            except Exception as e:
                # update the Log file
                print("Node was unreadchable : ", client[0])
                print(client[0], "is removed")
                
                unreachableClients.append(client)

        for client in unreachableClients:
            self.clients.remove(client)

        return spec_pb2.WriteReply(success=True)


def serve(args):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    spec_pb2_grpc.add_CoordinatorServicer_to_server(Coordinator(), server)
    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    print("Co-Ordinator Started at port :", args.port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--port", help="Port to run the coordinator process on.", default=5200)
    args = parser.parse_args()
    serve(args)
