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

import numpy as np
import pandas as pd

from math import isclose
import reactive.papi.MDSnapshotL2 as FbsMD


class MDSnapshotL2:

    def __init__(self, market: str,
                 bid_price: np.array,
                 bid_qty: np.array,
                 offer_price: np.array,
                 offer_qty: np.array,
                 feed_id: int = 0,
                 flag: int = 0,
                 source_ts: int = 0,
                 source: str = None,
                 id: int = None,
                 depth: int = 0,
                 **kwargs):
        """

        Parameters
        ----------
        market: str
          market symbol

        bid_price: np.array[float64]
            Bid price array.
        bid_qty: np.array[float64]
            Bid qty np.array.
        offer_price: np.array[float64]
            Offer price np.array.
        offer_qty: np.array[float64]
            Offer qty np.array.
        feed_id: int
            A unique identifier for a feed view, assigned by server.
        id: int, default None
            Unique book integer identifier, only unique per market and feed_id, not across platfrom.
            default None means id is not specified.
        flag: int
          Bitset describes features of the market-data.
        source_ts : int
          Source timestamp in nanosecond.
        source: str
          Source string.
        """
        self.market = market
        self.feed_id = feed_id
        self.flag = flag
        self.source_ts = source_ts
        self.source = source
        self.id = id
        self.depth = depth

        self.bid_price = bid_price
        self.bid_qty = bid_qty
        self.offer_price = offer_price
        self.offer_qty = offer_qty

    def to_df(self) -> pd.DataFrame:
        """
        Convert order book into a pandas DataFrame.
        """
        df = pd.DataFrame(data={"bid_qty": self.bid_qty,
                                "bid_price": self.bid_price,
                                "offer_price": self.offer_price,
                                "offer_qty": self.offer_price})
        return df

    def bid_depth(self):
        depth = 0
        for qty in self.bid_qty:
            if qty < 0 or isclose(qty, 0.0):
                break
            depth += 1
        return depth

    def offer_depth(self):
        depth = 0
        for qty in self.offer_qty:
            if qty < 0 or isclose(qty, 0.0):
                break
            depth += 1
        return depth

    def is_empty(self) -> bool:
        if self.bid_depth() == 0 and self.offer_depth() == 0:
            return True
        return False

    @classmethod
    def load_from_fbs(cls, md: FbsMD.MDSnapshotL2):
        bid_length = md.BidSideLength()
        bid_price = np.zeros(bid_length, dtype=np.float64)
        bid_qty = np.zeros(bid_length, dtype=np.float64)
        for i in range(0, bid_length):
            level = md.BidSide(i)
            bid_price[i] = level.Price()
            bid_qty[i] = level.Qty()
        offer_length = md.OfferSideLength()
        offer_price = np.zeros(offer_length, dtype=np.float64)
        offer_qty = np.zeros(offer_length, dtype=np.float64)
        for i in range(0, offer_length):
            level = md.OfferSide(i)
            offer_price[i] = level.Price()
            offer_qty[i] = level.Qty()

        return cls(market=md.Market(),
                   bid_price=bid_price,
                   bid_qty=bid_qty,
                   offer_price=offer_price,
                   offer_qty=offer_qty,
                   feed_id=md.FeedId(),
                   id=md.Id(),
                   depth=md.Depth(),
                   flag=md.Flags(),
                   source_ts=md.SourceTs(),
                   source=md.Source())
