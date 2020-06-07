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
import reactive.papi.Message as FbsMessage

from typing import AnyStr, Callable
from websockets.http import Headers

from reactive.platform.websocket.websocket import read, write


class Client:
    """
    Client handles websocket connection with reactive platform. The data_handler must accept
    an reactive.papi.Message.Message type, which is in platform Flatbuffer message type in
    reactive-papi package. See more support message type in reactive-papi package.
    """

    ADDRESS = "wss://api.platform.reactivemarkets.com/stream"
    IO_TIMEOUT = 2.0

    def __init__(self, addr: str = None, api_key: str = None, close_timeout: float = IO_TIMEOUT):
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
        self.__api_key = api_key
        self.header = Headers(Authorization="Bearer " + api_key) if api_key is not None else None
        self.close_timeout = close_timeout

        self.__builder = flatbuffers.Builder(1400)
        self.__data_handler = None
        self.__queue = asyncio.Queue(10)

    @property
    def builder(self):
        return self.__builder

    @property
    def data_handler(self):
        return self.__data_handler

    def register_data_handler(self, data_handler: Callable[[FbsMessage.Message], None]):
        self.__data_handler = data_handler

    def get_conn(self):
        """
        get_conn initialize a new connection, and return the connection.
        """
        return websockets.connect(self.__addr, extra_headers=self.header)

    async def send(self, request: AnyStr):
        """
        Sends a request message.

        Parameters
        ----------
        request: fbs.Message
          feed.Message with feed request
        """
        await self.__queue.put(request)

    async def _read(self, buf: AnyStr):
        """
        _read decode message into fbs.Message and call callback handler.
        """
        # TODO: change _read method to a decorator
        msg = FbsMessage.Message.GetRootAsMessage(buf, 0)
        self.__data_handler(msg)

    async def _write(self):
        return await self.__queue.get()

    async def run(self, client_handler, data_handler: Callable[[FbsMessage.Message], None] = None):
        """
        run runs a coroutine to trigger three asyncio futures running on event loop. The
        consumer_task is reading data from web socket and trigger the user defined callback handler,
        the second producer_task is reading from internal request queue and send requests to server,
        and the last task is the client_handler which is user implemented coroutine has a contact:
        `func(Client)`.

        Parameters
        ----------
        client_handler : callable[[Client], None]
            client_handler is a user defined coroutine, which will be wrapped into a future,
            and running with read / write futures together in the event_loop.
            In the client_handler, user can use Client object to send request messages via
            `send` method, or execute any codes with the Client object.

        data_handler: callable[[Message], None]
            callback handler handles message read from web sockets.

        """
        if data_handler is not None:
            self.register_data_handler(data_handler)
        if self.__data_handler is None:
            raise RuntimeError("no call back data handler for the client")
        try:
            conn = self.get_conn()
            # do not use `with conn as ws:` this is because cannot set close_timeout.
            ws = await asyncio.wait_for(conn, timeout=self.close_timeout)
            consumer_task = asyncio.ensure_future(read(ws, self._read))
            producer_task = asyncio.ensure_future(write(ws, self._write))
            asyncio.ensure_future(client_handler(self))
            done, pending = await asyncio.wait(
                [consumer_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
        except Exception:
            raise
        else:
            conn.ws_client.close()
