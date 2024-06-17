import asyncio
import functools
import logging
import queue

import grpc
import example.generated.helloworld_pb2 as helloworld_pb2
import example.generated.helloworld_pb2_grpc as helloworld_pb2_grpc


async def run() -> None:
    try:
        channel = grpc.insecure_channel("localhost:50051")
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        # Read from an async generator
        send_queue = queue.SimpleQueue()
        stream = stub.Greeting(iter(send_queue.get, None))

        send_greetings_task = asyncio.create_task(send_greetings(send_queue), name="sending task")
        send_greetings_task.add_done_callback(functools.partial(_callback))
        receive_greetings_task = asyncio.create_task(receive_greetings(stream), name="receiving task")
        receive_greetings_task.add_done_callback(functools.partial(_callback))

        logging.info("gathering tasks...")
        await asyncio.gather(send_greetings_task, receive_greetings_task)
    except Exception as e:
        logging.exception("Something broke", e)


async def send_greetings(send_queue):
    logging.info("Sending greetings...")
    for i in range(0, 3):
        message = f"Test {i}"
        logging.info(f"Sending: {message}")
        msg = helloworld_pb2.ClientGreeting(message=message)
        send_queue.put(msg)
        logging.info(f"Sent: {message}")
        await asyncio.sleep(0)


async def receive_greetings(stream):
    logging.info("Receiving greetings...")
    for response in stream:
        logging.info(f"Received greeting: {response.message}")
        await asyncio.sleep(0)


def _callback(task):
    if task.cancelled():
        logging.error(
            f"Task {task.get_name()} was cancelled",
        )
    elif task.exception():
        logging.error(
            f"Exception found for task {task.get_name()}: {task.exception()}",
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the client")
    asyncio.run(run())