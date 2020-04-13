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
"""
Summary
-------
Level 2 order book data structures.

"""

from typing import List

from reactive.platform.fbs.feed.MDSnapshotL2 import MDSnapshotL2


class MDLevel2:

    def __init__(self, qty, price):
        self.qty = qty
        self.price = price


class Level2Book:

    def __init__(self, market: str, flag: int, bid_side: List[MDLevel2],
                 offer_side: List[MDLevel2], **kwargs):
        """

        Parameters
        ----------
        market: str
          market symbol
        flag: int
          bitset describes features of the market-data.
        bid_side: List[MDLevel2]
          bid side of the book
        offer_side: List[MDLevel2]
          offer side of the book
        kwargs: dict
        """
        self.market = market
        self.flag = flag
        self.bid_side = bid_side
        self.offer_side = offer_side

        if "source_ts" in kwargs:
            self.source_ts = kwargs["source_ts"]
        if "source" in kwargs:
            self.source = kwargs["soruce"]
        if "id" in kwargs:
            self.id = kwargs["id"]

    @classmethod
    def load_from_flat_buffer(cls, md: MDSnapshotL2):
        bid_side = list()
        for i in range(0, md.BidSideLength()):
            level = md.BidSide(i)
            bid_side.append(MDLevel2(qty=level.Qty(), price=level.Price()))

        offer_side = list()
        for i in range(0, md.OfferSideLength()):
            level = md.OfferSide(i)
            offer_side.append(MDLevel2(qty=level.Qty(), price=level.Price()))

        return Level2Book(market=md.Market(), flag=md.Flags(), bid_side=bid_side,
                          offer_side=offer_side)
