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

import reactive.platform.fbs.feed.FeedType as FeedType
import reactive.platform.fbs.feed.MDSnapshotL2 as Ms
import reactive.platform.fbs.feed.SubReqType as Srt

from typing import List, AnyStr

from reactive.platform.fbs.feed.Body import Body
from reactive.platform.fbs.feed.FeedRequestReject import FeedRequestReject
from reactive.platform.fbs.feed.FeedRequestAck import FeedRequestAck
from reactive.platform.fbs.feed.Message import Message

from reactive.platform.feed.level2book import Level2Book
from reactive.platform.feed.feedrequest import FeedRequest
from reactive.platform.websocket.client import Client


def md_null_handler(md: Level2Book = None):
    pass


class FeedClient(Client):
    """
    FeedClient is a derived class of Client and handle feed connection, client cloud
    send feed request by subscribe and unsubscribe method and receive level2 book
    or feed request reject. Feed request reject will display in the console, and flatbuffers
    formatted Level2Snapshot will be converted into Level2Book object and trigger the callback
    handle. Client must provide handler function which has the contract like handler(Level2book)

    """

    ADDRESS = 'wss://api.platform.reactivemarkets.com/feed'

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
        self.req_id = 0

    async def subscribe(self, markets: List[str], grouping: int = 0,
                        feed_type: int = FeedType.FeedType.Default,
                        frequency: int = 1,
                        depth: int = 10):
        # FIXME: check if market is already subscribed and only subscribe new markets.
        for market in markets:
            self.__subCache[market] = True
        fr = FeedRequest(req_id=str(++self.req_id), grouping=grouping, markets=markets,
                         sub_req_type=Srt.SubReqType.Subscribe, feed_type=feed_type,
                         frequency=frequency, depth=depth)
        await self.send(fr.build_feed_request(self.builder))

    async def unsubscribe(self, markets: List[str], grouping: int = 0,
                          feed_type: int = FeedType.FeedType.Default,
                          frequency: int = 1, depth: int = 10):
        for market in markets:
            if market in self.__subCache:
                self.__subCache[market] = False
        fr = FeedRequest(req_id=str(++self.req_id), grouping=grouping, markets=markets,
                         sub_req_type=Srt.SubReqType.Unsubscribe, feed_type=feed_type,
                         frequency=frequency, depth=depth)
        await self.send(fr.build_feed_request(self.builder))

    async def _read(self, buf: AnyStr):
        """
        _read overrides the Client _read method, and decoding buffer into fbs.Feed.MDSnapshotL2
        and fbs.Feed.FeedRequestReject. If Message is fbs.Feed.MDSnapshotL2, convert into Level2Book
        object, and call the callback handler, which accepts Level2Book object.
        """
        msg = Message.GetRootAsMessage(buf, 0)
        if msg.BodyType() == Body.MDSnapshotL2:
            fbs_md = Ms.MDSnapshotL2()
            fbs_md.Init(msg.Body().Bytes, msg.Body().Pos)
            md = Level2Book.load_from_flat_buffer(fbs_md)
            self.handler(md)
        elif msg.BodyType() == Body.FeedRequestReject:
            frr = FeedRequestReject()
            frr.Init(msg.Body().Bytes, msg.Body().Pos)
            print("market data request is rejected", frr.ErrorCode(), frr.ErrorMessage())
        elif msg.BodyType() == Body.FeedRequestAck:
            fra = FeedRequestAck()
            fra.Init(msg.Body().Bytes, msg.Body().Pos)
            print("feed ack, req_id: ", fra.ReqId(), " feed_id: ", fra.FeedId())

    async def run(self, app_run, handler=md_null_handler):
        """
        FeedClient expects handler callback method accept Level2Book object like
        handler(Level2Book), instead of handler(fbs.Message) in base Client.
        """
        await super().run(app_run, handler)
