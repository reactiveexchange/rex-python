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


async def read(ws: websockets.WebSocketClientProtocol, handler: Callable[[AnyStr], Coroutine]):
    """
    read read data from websocket and handle the raw message via callback handler.
    Running read as a task or future.
    """
    async for message in ws:
        await handler(message)


async def write(ws: websockets.WebSocketClientProtocol, writer: Callable[[], Coroutine]):
    """
    write gets a message from writer handler, and send the message via websocket.

    sends a message to the other side, which reads from writer(), via websocket.
    """
    while True:
        message = await writer()
        await ws.send(message)


async def ws_conn_handler(ws: websockets.WebSocketClientProtocol,
                          read_handler: Callable[[AnyStr], Coroutine],
                          write_handler: Callable[[], Coroutine],
                          return_when=asyncio.ALL_COMPLETED):
    """
    ws_conn_handler handles a websocket connection, reads data from
    websocket via read asyncoi.future with consumer_handler callback function, sends
    message via write asyncoi.future with producer_handler callback function.

    """
    consumer_task = asyncio.ensure_future(read(ws, read_handler))
    producer_task = asyncio.ensure_future(write(ws, write_handler))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=return_when,
    )
    for task in pending:
        task.cancel()


def ws_address(host: str, port: int, path: str) -> str:
    return "ws://" + host + ":" + str(port) + "/" + path
