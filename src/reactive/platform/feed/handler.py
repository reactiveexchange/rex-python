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

from typing import Union

from reactive.platform.feed.feedaccept import FeedRequestAccept
from reactive.platform.feed.feedrequestreject import FeedRequestReject
from reactive.platform.feed.mdsnapshotl2 import MDSnapshotL2
from reactive.platform.feed.publictrade import PublicTrade


def print_data_handler(obj: Union[FeedRequestAccept, FeedRequestReject,
                                  MDSnapshotL2, PublicTrade]):
    """
    implement a print callback handler for FeedClient.

    Parameters
    ----------
    obj: object
        a object of FeedRequestAccept, FeedRequestReject, MDSnapshotL2 or PublicTrade class.
    """
    if isinstance(obj, MDSnapshotL2):
        md = obj
        best_bid = md.bid_price[0] if md.bid_price.size > 0 else None
        best_offer = md.offer_price[0] if md.offer_price.size > 0 else None
        print(md.market, best_bid, best_offer)
        print("market depth: ", md.depth)
    elif isinstance(obj, PublicTrade):
        trade = obj
        print(trade.market, trade.exec_venue, trade.price, trade.qty, trade.side)
    elif isinstance(obj, FeedRequestReject):
        reject = obj
        print(f"feed request {reject.req_id} is rejected: {reject.error_code},"
              f"{reject.error_message}")
    elif isinstance(obj, FeedRequestAccept):
        ack = obj
        print(f"feed ack, req_id: {ack.req_id} feed_id: {ack.feed_id}")
    else:
        print("unknown object")
