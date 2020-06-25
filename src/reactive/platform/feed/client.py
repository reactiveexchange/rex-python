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

import reactive.papi.FeedType as FbsFeedType
import reactive.papi.SubReqType as FbsSrt
import reactive.papi.Message as FbsMessage

from typing import AnyStr, Any, Callable, List

from reactive.platform.feed.decode import load_from_fbs
from reactive.platform.feed.feedrequest import FeedRequest
from reactive.platform.websocket.client import Client


class FeedClient(Client):
    """
    FeedClient is a derived class of Client and handle feed connection, client could send feed
    request by calling subscribe and unsubscribe method and, receive data from platform (level2
    book, trade or feed request reject). The receiving messages are Flatbuffer messages, and
    FeedClient converts into corresponding object and trigger the callback data_handler.
    If want to handle raw flatbuffer message via reactive-papi package, use
    base class Client, instead.
    """

    ADDRESS = 'wss://api.platform.reactivemarkets.com/feed'

    def __init__(self, addr: str = None, api_key: str = None, close_timeout: float = 2.0):
        """
        Parameters
        ----------
        addr: str
            web socket server address
        key: str
            platform API token.
        close_timeout : float
            maximum wait time in seconds for completing the closing handshake and terminating
            the TCP connection.
        """
        addr = addr if addr is not None else self.ADDRESS
        super().__init__(api_key=api_key, addr=addr, close_timeout=close_timeout)
        self.req_id = 0

    async def subscribe(self, markets: List[str],
                        feed_type: int = FbsFeedType.FeedType.Default,
                        depth: int = 10,
                        grouping: int = 1,
                        freq: int = 1):
        """
        subscribe sends a subscription FeedRequest to reactive platform, the default request is
        a market data request.

        Parameters
        ----------
        markets : List[str]
          subscribe market lists.
        feed_type: FeedType, default: FbsFeedType.FeedType.Default
          default type is for subscribing marketdata channel, FeedTypeTrade is for
           subscribing public trade channel.
        depth : int, default 10
          subscribe marketdata l2 orderbook depths, if feed_type is Default, otherwise the field is
          ignored.
        grouping: int, default 1
          subscribe marketdata l2 orderbook grouping ticks per level, if feed_type is Default,
          otherwise the field is ignored.
        freq: int, default 1
          required market data update frequency, if feed_type is Default.
          otherwise the field is ignored by the platform.
        """
        self.req_id += 1
        fr = FeedRequest(req_id=str(self.req_id), grouping=grouping, markets=markets,
                         sub_req_type=FbsSrt.SubReqType.Subscribe, feed_type=feed_type,
                         freq=freq, depth=depth)
        await self.send(fr.build_feed_request(self.builder))

    async def unsubscribe(self, markets: List[str],
                          feed_type: int = FbsFeedType.FeedType.Default,
                          depth: int = 10, grouping: int = 1,
                          freq: int = 1):
        """
        unsubscribe sends a unsubscription FeedRequest to reactive platform, the default request is
        marketdata request.
        """
        self.req_id += 1
        fr = FeedRequest(req_id=str(self.req_id), grouping=grouping, markets=markets,
                         sub_req_type=FbsSrt.SubReqType.Unsubscribe, feed_type=feed_type,
                         freq=freq, depth=depth)
        await self.send(fr.build_feed_request(self.builder))

    async def _read(self, buf: AnyStr):
        """
        _read overrides the Client _read method, and decoding fbs.Message into the
        corresponding object and call the callback data_handler.
        """
        msg = FbsMessage.Message.GetRootAsMessage(buf, 0)
        self.data_handler(load_from_fbs(msg))

    async def run(self, client_handler,
                  data_handler: Callable[[Any], None] = None):
        """
        FeedClient expects handler callback method accept Level2Book object like
        handler(Level2Book), instead of handler(fbs.Message) in base Client.
        """
        await super().run(client_handler=client_handler, data_handler=data_handler)
