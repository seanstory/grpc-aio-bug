import asyncio
import logging

import grpc
from example.generated.helloworld_pb2 import ServerGreeting
from example.generated.helloworld_pb2_grpc import GreeterServicer
from example.generated.helloworld_pb2_grpc import add_GreeterServicer_to_server


NUMBER_OF_REPLY = 10


class Greeter(GreeterServicer):
    async def Greeting(
            self, requestStream, context: grpc.aio.ServicerContext
    ) -> ServerGreeting:
        logging.info("Reading requests...")
        async for request in requestStream:
            logging.info("Serving request %s", request)
            for i in range(NUMBER_OF_REPLY):
                yield ServerGreeting(message=f"Hello number {i}, {request.message}!")


async def serve() -> None:
    server = grpc.aio.server()
    add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
