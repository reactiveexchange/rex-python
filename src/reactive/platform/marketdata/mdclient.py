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

import reactive.platform.fbs.MarketData as fbsmd

from typing import List, AnyStr

from reactive.platform.fbs.Body import Body
from reactive.platform.fbs.MarketDataRequestReject import MarketDataRequestReject
from reactive.platform.fbs.Message import Message
from reactive.platform.fbs.SubReqType import SubReqType

from reactive.platform.marketdata.marketdata import MarketData
from reactive.platform.marketdata.marketdatarequest import build_md_request
from reactive.platform.websocket.client import Client


def md_null_handler(md: MarketData = None):
    pass


class MDClient(Client):
    """
    MDClient is a derived class of Client and handle market data connection, client cloud
    send market data request by subscribe and unsubscribe method and receive market data
    or market data reject. Market data reject will display in the console, and flatbuffers
    formatted market data will be converted into MarketData object and call the callback
    handle. Client must provide handler function which has the contact like handler(MarketData)

    """

    ADDRESS = 'wss://api.platform.reactivemarkets.com/stream'

    def __init__(self, addr: str = None, key: str = None):
        """
        Parameters
        ----------
        addr: str
            web socket server address
        key: str
            platform API token.
        """
        addr = addr if addr is not None else self.ADDRESS
        super().__init__(key=key, addr=addr)
        self.__subCache = dict()

    async def subscribe(self, markets: List[str]):
        for market in markets:
            self.__subCache[market] = True
        await self.send(build_md_request(markets, SubReqType.Subscribe, self.builder))

    async def unsubscribe(self, markets: List[str]):
        for market in markets:
            if market in self.__subCache:
                del self.__subCache[market]
        await self.send(build_md_request(markets, SubReqType.Unsubscribe, self.builder))

    async def _read(self, buf: AnyStr):
        """
        _read overrides the Client _read method, and decoding buffer into fbs.MarketData
        and fbs.MarketDataRequestReject. If Message is fbs.MarketData, convert into MarketData
        object, and call the callback handler, which accepts MarketData object.
        """
        msg = Message.GetRootAsMessage(buf, 0)
        if msg.BodyType() == Body.MarketData:
            fbs_md = fbsmd.MarketData()
            fbs_md.Init(msg.Body().Bytes, msg.Body().Pos)
            md = MarketData.load_from_flat_buffer(0, fbs_md)
            self.handler(md)
        elif msg.BodyType() == Body.MarketDataRequestReject:
            mdrr = MarketDataRequestReject()
            mdrr.Init(msg.Body().Bytes, msg.Body().Pos)
            print("market data request is rejected", mdrr.ErrorCode(), mdrr.ErrorMessage())

    async def run(self, app_run, handler=md_null_handler):
        """
        MDClient expects handler callback method accept MarketData object like
        handler(MarketData), instead of handler(fbs.Message) in base Client.
        """
        await super().run(app_run, handler)
