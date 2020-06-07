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

from reactive.platform.feed.client import FeedClient
from reactive.platform.feed.handler import print_data_handler
from reactive.papi.FeedType import FeedType

API_KEY = ""
ADDR = "wss://api.platform.reactivemarkets.com/feed"


async def feed_client_handler(c: FeedClient):
    """
    implement a feed_client_handler coroutine to send a FeedRequest to subscribe BTCUSD-BFN and
    BTCUSD-CNB trades
    """

    await c.subscribe(["BTCUSD-BFN", "BTCUSD-CNB"], feed_type=FeedType.Trade)


def run():
    client = FeedClient(addr=ADDR, api_key=API_KEY, close_timeout=1.0)
    run = asyncio.ensure_future(client.run(client_handler=feed_client_handler,
                                           data_handler=print_data_handler))
    asyncio.get_event_loop().run_until_complete(run)


if __name__ == "__main__":
    run()
