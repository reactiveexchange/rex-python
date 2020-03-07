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


from reactive.platform.marketdata.mdclient import MDClient
from reactive.platform.marketdata.marketdata import MarketData

MARKET_LIST = ["EURUSD-REX", "EURGBP-REX", "EURCHF-REX", "EURRON-REX", "USDCAD-REX",
               "USDCHF-REX", "USDJPY-REX", "USDCHF-REX", "EURJPY-REX", "AUDUSD-REX"]


def random_market():
    index = random.randint(0, 9)
    return MARKET_LIST[index]


def md_print_handler(md: MarketData):
    """
    implement a market data callback handler to print best bid and offer.
    """
    best_bid = md.bid_price[0] if len(md.bid_price) > 0 else None
    best_offer = md.offer_price[0] if len(md.offer_price) > 0 else None
    print(md.market, best_bid, best_offer)


async def app_run(c: MDClient):
    """
    implement an application run coroutine to and subscribe or
    unsubscribe markets.
    """

    # unknown markets, expect an reject message
    await c.subscribe(["EURGBP-CME"])
    while True:
        market = random_market()
        print("sub", market)
        await c.subscribe([market])
        await asyncio.sleep(2)
        print("unsub", market)
        await c.unsubscribe([market])
        await asyncio.sleep(2)


if __name__ == "__main__":
    # use default setting
    client = MDClient(addr='ws://127.0.0.1:8989/md')
    run = asyncio.ensure_future(client.run(app_run, md_print_handler))
    asyncio.get_event_loop().run_until_complete(run)
