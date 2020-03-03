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

# FIXME: current do not have message header in python, add tts in MarketData.


class MarketData:

    def __init__(self):
        # FIXME: use numpy array instead of python list
        self.tts = 0

        self.accnt = None
        self.market = None
        self.id = None
        self.request_id = None
        self.flags = None
        self.last_ts = 0
        self.last_side = None
        self.last_qty = None
        self.last_price = None
        self.bid_qty = []
        self.bid_price = []
        self.bid_count = []
        self.offer_qty = []
        self.offer_price = []
        self.offer_count = []

    @classmethod
    def load_from_flat_buffer(cls, tts, md):
        res = cls()
        res.tts = tts
        res.accnt = str(md.Accnt())
        res.market = str(md.Market())
        res.id = str(md.Id())
        res.request_id = md.RequestId()
        res.flags = md.Flags()
        last_trade = md.LastTrade()
        if last_trade is not None:
            res.last_ts = last_trade.TransTs()
            res.last_side = last_trade.Side()
            res.last_qty = last_trade.Qty()
            res.last_price = last_trade.Price()

        for i in range(0, md.BidL2Length()):
            level = md.BidL2(i)
            res.bid_qty.append(level.Qty())
            res.bid_count.append(level.Count())
            res.bid_price.append(level.Price())

        for i in range(0, md.OfferL2Length()):
            level = md.OfferL2(i)
            res.offer_qty.append(level.Qty())
            res.offer_count.append(level.Count())
            res.offer_price.append(level.Price())
        return res
