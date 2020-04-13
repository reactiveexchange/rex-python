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
import flatbuffers
import websockets

from typing import AnyStr, Callable
from websockets.http import Headers

from reactive.platform.fbs.feed.Message import Message
from reactive.platform.feed.level2book import Level2Book
from reactive.platform.websocket.websocket import consume, produce


class Client:

    ADDRESS = "wss://api.platform.reactivemarkets.com/stream"

    def __init__(self, addr: str = None, key: str = None):
        """
        Create a web socket client to connect platform.

        Parameters
        ----------
        addr: str
            address for a service, like ws://host:port
        key: str
            key represents API key, which is used for verifying identity.
        """
        self.__addr = addr if addr is not None else self.ADDRESS
        header = Headers(Authorization="Bearer " + key) if key is not None else None
        self.__conn = websockets.connect(self.__addr, extra_headers=header)
        self.__builder = flatbuffers.Builder(1400)
        self.__handler = None
        self.__queue = asyncio.Queue(10)

    @property
    def conn(self):
        return self.__conn

    @property
    def builder(self):
        return self.__builder

    @property
    def handler(self):
        return self.__handler

    def register_handler(self, handler: Callable[[Level2Book], None]):
        self.__handler = handler

    async def send(self, request):
        """
        send sends request to server.

        Parameters
        ----------
        request: fbs.Message
          request message
        """
        await self.__queue.put(request)

    async def _read(self, buf: AnyStr):
        """
        _read decode message into fbs.Message and call callback handler.
        """
        msg = Message.GetRootAsMessage(buf, 0)
        self.__handler(msg)

    async def _write(self):
        return await self.__queue.get()

    async def run(self, app_run, handler=None):
        """
        client run method, will trigger three asyncio tasks running on event loop. Consumer_task is
        reading data from web socket and trigged the callback handler, the second producer_task is
        reading from internal request queue and send to server, and the last task is the app_run
        which is user implemented coroutine has a contact like `func(Client)`. In app_run, user
        has right to re-assign callback handler, and send requests via `send` method.
        """

        self.register_handler(handler)
        if self.handler is None:
            # FIXME: create a specific exception
            raise RuntimeError("no call back handler for the client")
        async with self.conn as ws:
            consumer_task = asyncio.ensure_future(consume(ws, self._read))
            producer_task = asyncio.ensure_future(produce(ws, self._write))
            asyncio.ensure_future(app_run(self))
            done, pending = await asyncio.wait(
                [consumer_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
