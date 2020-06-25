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
Liquidation order data structures.

"""

import reactive.papi.LiquidationOrder as FbsLo


class LiquidationOrder:

    def __init__(self, market: str, side: int, qty: float, price: float,
                 source_ts: int = 0, source: str = "", feed_id: int = 0,
                 order_id: str = "", flags: int = 0, exec_venue: str = ""):
        self.source_ts = source_ts
        self.source = source
        self.market = market
        self.feed_id = feed_id
        self.order_id = order_id
        self.flags = flags
        self.side = side
        self.qty = qty
        self.price = price
        self.exec_venue = exec_venue

    @classmethod
    def load_from_fbs(cls, liquidation: FbsLo.LiquidationOrder):
        return cls(market=liquidation.Market(), side=liquidation.Side(), qty=liquidation.Qty(),
                   price=liquidation.Qty(), source_ts=liquidation.SourceTs(),
                   source=liquidation.Source(), feed_id=liquidation.FeedId(),
                   order_id=liquidation.OrderId(), flags=liquidation.Flags(),
                   exec_venue=liquidation.ExecVenue())
