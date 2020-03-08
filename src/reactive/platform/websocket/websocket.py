# -*- coding: utf-8 -*-
# Copyright (C) 2020 Reactive Markets Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import websockets

from typing import Callable, AnyStr, Coroutine

HOST = "ws://localhost:8989/md"


async def consume(ws: websockets.WebSocketClientProtocol, handler: Callable[[AnyStr], Coroutine]):
    """
    consumer read data from web socket and handle the message via callback function handler
    """
    async for message in ws:
        await handler(message)


async def produce(ws: websockets.WebSocketClientProtocol, handler: Callable[[], Coroutine]):
    while True:
        message = await handler()
        await ws.send(message)


async def run_consume_produce(ws, consumer_handler, producer_handler,
                              return_when=asyncio.ALL_COMPLETED):
    consumer_task = asyncio.ensure_future(consume(ws, consumer_handler))
    producer_task = asyncio.ensure_future(produce(ws, producer_handler))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=return_when,
    )
    for task in pending:
        task.cancel()


async def print_consumer_handler(msg):
    print(msg)


async def null_producer_handler():
    return ""


def ws_address(host: str, port: int, path: str) -> str:
    return "ws://" + host + ":" + str(port) + "/" + path
