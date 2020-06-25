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

from reactive.papi.Message import Message
from reactive.papi.Body import Body
from reactive.platform.websocket.decode import decode_fbs


async def print_read_handler(msg):
    print(msg)


async def null_writer_handler():
    return ""


def print_data_handler(msg: Message):
    """
    implement a print callback handler for Client.
    """
    body_type, body = decode_fbs(msg)
    if body_type == Body.MDSnapshotL2:
        market = body.Market()
        bid_length = body.BidSideLength()
        best_bid = None if bid_length == 0 else body.BidSide(0).Price()
        offer_length = body.OfferSideLength()
        best_offer = None if offer_length == 0 else body.OfferSide(0).Price()
        print("market data:", market, best_bid, best_offer)
    elif body_type == Body.PublicTrade:
        print("public trade:", body.Market(), body.ExecVenue(), body.Price(), body.Qty(),
              body.Side())
    elif body_type == Body.LiquidationOrder:
        print("liquidation:", body.Market(), body.ExecVenue(), body.Price(), body.Qty(),
              body.Side())
    elif body_type == Body.FeedRequestReject:
        print(f"feed request {body.ReqId()} is rejected: {body.ErrorCode()},"
              f"{body.ErrorMessage()}")
    elif body_type == Body.FeedRequestAccept:
        print(f"feed ack, req_id: {body.ReqId()} feed_id: {body.FeedId()}")
    else:
        print("unknown object")
