# Bug demo

### Description

This repo exists to provide a (relatively) minimal reproduction of a bug (https://github.com/grpc/grpc/issues/36950) I noticed when trying to build a Python protobuf client.

The issue seems to be that using `grpc.aio.*_channel()` instead of just `grpc.*_channel()` puts something on the event loop that blocks indefinitely.

Combined with bi-directional streaming, this eventually hangs the client program, as the "send" and "receive" tasks must each periodically yield control, and eventually _something_ grabs control but never reliquishes it.

### Protobuf 
The minimal protobuf file is in `.proto/helloworld.proto`

Python code generated from this proto file is included in `example/generated`, and was created with `scripts/generate.sh`, through `make generate`

### How to run
To demonstrate the issue:
1. clone this repo
2. run `make install`
3. in one terminal tab, run `bin/python example/server.py`
4. in a second terminal tab, run `bin/python example/client.py`
5. You will see a bunch of output, demonstrating that the client sends and receives messages
6. in a third terminal tab, run `bin/python example/async_client.py`
7. You will _not_ see much output. The last line will indicate that the async tasks were "gathered", but they never actually execute.
8. Run `diff example/client.py example/async_client.py`
9. You will see that the only difference between these is that one uses `grpc` and the other uses `grpc.aio`
