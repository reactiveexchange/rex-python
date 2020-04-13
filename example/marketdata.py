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

from reactive.platform.feed.feedclient import FeedClient
from reactive.platform.feed.level2book import Level2Book

MARKET_LIST = ["EURUSD-REX", "EURGBP-REX", "EURCHF-REX", "EURRON-REX", "USDCAD-REX",
               "USDCHF-REX", "USDJPY-REX", "USDCHF-REX", "EURJPY-REX", "AUDUSD-REX",
               "BCHUSD-BFN", "BTCUSD-BFN", "ETHUSD-BFN", "LTCUSD-BFN", "XRPUSD-BFN",
               "BCHUSD-BIN", "BTCUSD-BIN", "ETHUSD-BIN", "LTCUSD-BIN", "XRPUSD-BIN",
               "BCHUSD-CNB", "BTCUSD-CNB", "ETHUSD-CNB", "LTCUSD-CNB", "XRPUSD-CNB"]
TOKEN = ""
ADDR = "wss://api.platform.reactivemarkets.com/feed"


def random_market():
    index = random.randint(0, len(MARKET_LIST) - 1)
    return MARKET_LIST[index]


def md_print_handler(md: Level2Book):
    """
    implement a market data callback handler to print best bid and offer.
    """
    best_bid = md.bid_side[0] if len(md.bid_side) > 0 else None
    best_offer = md.offer_side[0] if len(md.offer_side) > 0 else None
    print(md.market, best_bid.price, best_offer.price)


async def app_run(c: FeedClient):
    """
    implement an application run coroutine to and subscribe or
    unsubscribe markets.
    """

    # unknown markets, expect an reject message
    await c.subscribe(["BTCUSD-CME"])
    while True:
        market = random_market()
        print("sub", market)
        await c.subscribe([market])
        await asyncio.sleep(3)
        print("unsub", market)
        await c.unsubscribe([market])
        await asyncio.sleep(1)


if __name__ == "__main__":
    # use default setting
    client = FeedClient(addr=ADDR, key=TOKEN)
    run = asyncio.ensure_future(client.run(app_run, md_print_handler))
    asyncio.get_event_loop().run_until_complete(run)
