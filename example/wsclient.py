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
import random
import flatbuffers

from reactive.platform.websocket.client import Client
from reactive.platform.websocket.handler import print_data_handler
from reactive.platform.feed.feedrequest import FeedRequest
from reactive.papi.FeedType import FeedType
from reactive.papi.SubReqType import SubReqType


MARKET_LIST = ["BCHUSD-BFN", "BTCUSD-BFN", "ETHUSD-BFN", "LTCUSD-BFN", "XRPUSD-BFN",
               "BCHUSDT-BIN", "BTCUSDT-BIN", "ETHUSDT-BIN", "LTCUSDT-BIN", "XRPUSDT-BIN",
               "BCHUSD-CNB", "BTCUSD-CNB", "ETHUSD-CNB", "LTCUSD-CNB", "XRPUSD-CNB"]

TOKEN = ""
ADDR = "wss://api.platform.reactivemarkets.com/feed"


def random_market():
    index = random.randint(0, len(MARKET_LIST) - 1)
    return MARKET_LIST[index]


async def client_handler(c: Client):
    """
    implement a client_handle run coroutine to and subscribe or
    unsubscribe market data for a random market.
    """

    builder = flatbuffers.Builder(1400)
    req_id = 0
    while True:
        market = random_market()
        print("sub", market)
        req_id += 1
        feed_request = FeedRequest(str(req_id), [market],
                                   feed_type=FeedType.Default,
                                   sub_req_type=SubReqType.Subscribe)
        await c.send(feed_request.build_feed_request(builder))
        await asyncio.sleep(3)
        print("unsub", market)
        req_id += 1
        feed_request = FeedRequest(str(req_id), [market],
                                   feed_type=FeedType.Default,
                                   sub_req_type=SubReqType.Unsubscribe)
        await c.send(feed_request.build_feed_request(builder))
        await asyncio.sleep(1)


def run():
    client = Client(addr=ADDR, key=TOKEN, close_timeout=1.0)
    run = asyncio.ensure_future(client.run(client_handler=client_handler,
                                           data_handler=print_data_handler))
    asyncio.get_event_loop().run_until_complete(run)


if __name__ == "__main__":
    run()
