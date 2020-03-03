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
import reactive.platform.fbs.MarketData as fbsmd

from typing import List, AnyStr, Callable

from reactive.platform.fbs.Body import Body
from reactive.platform.fbs.MarketDataRequestReject import MarketDataRequestReject
from reactive.platform.fbs.Message import Message
from reactive.platform.fbs.SubReqType import SubReqType

from reactive.platform.marketdata.marketdata import MarketData
from reactive.platform.marketdata.marketdatarequest import build_md_request


def md_null_handler(md: MarketData):
    pass


class MDClient:

    ADDRESS = 'ws://localhost:9000/md'

    def __init__(self, addr: str = None,
                 md_handler: Callable[[MarketData], None] = md_null_handler):
        self.__addr = addr if addr is not None else self.ADDRESS
        self.__conn = websockets.connect(self.__addr)
        self.__builder = flatbuffers.Builder(1400)
        self.__handler = md_handler
        self.__subCache = dict()
        self.__queue = asyncio.Queue(10)

    def register_md_handler(self, handler: Callable[[MarketData], None]):
        self.__handler = handler

    @property
    def conn(self):
        return self.__conn

    async def subscribe(self, markets: List[str]):
        for market in markets:
            self.__subCache[market] = True
        await self.__queue.put(build_md_request(markets, SubReqType.Subscribe, self.__builder))

    async def unsubscribe(self, markets: List[str]):
        for market in markets:
            if market in self.__subCache:
                del self.__subCache[market]
        await self.__queue.put(build_md_request(markets, SubReqType.Unsubscribe, self.__builder))

    async def read(self, buf: AnyStr):
        msg = Message.GetRootAsMessage(buf, 0)
        if msg.BodyType() == Body.MarketData:
            fbs_md = fbsmd.MarketData()
            fbs_md.Init(msg.Body().Bytes, msg.Body().Pos)
            md = MarketData.load_from_flat_buffer(0, fbs_md)
            self.__handler(md)
        elif msg.BodyType() == Body.MarketDataRequestReject:
            mdrr = MarketDataRequestReject()
            mdrr.Init(msg.Body().Bytes, msg.Body().Pos)
            print("market data request is rejected", mdrr.ErrorCode(), mdrr.ErrorMessage())

    async def write(self):
        return await self.__queue.get()
