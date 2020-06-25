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

import flatbuffers

import reactive.papi.Body as FbsBody
import reactive.papi.FeedType as FbsFeedType
import reactive.papi.FeedRequest as FbsFr
import reactive.papi.Message as FbsMessage
import reactive.papi.SubReqType as FbsSrt

from time import time_ns
from typing import List


class FeedRequest:
    """
    FeedRequest class is responsible for creating a feed.FeedRequest FlatBuffer message.
    """
    def __init__(self, req_id: str, markets: List[str],
                 feed_type: int = FbsFeedType.FeedType.Default,
                 depth: int = 10,
                 grouping: int = 1,
                 sub_req_type: int = FbsSrt.SubReqType.Subscribe,
                 freq: int = 1):
        """
        Parameters
        ----------
        req_id : str
          Feed request from client, should be echo back in FeedAccept message.
        markets : List[str]
          list of markets to subscribe.
        feed_type : int
          FeedType : 0 (Default for market data)
                     1 (Trade)
                     2 (Liquidation)
        depth : int
          order book depth, if feed_type is 0, otherwise, this field is ignored.
        grouping : int
          grouping in aggregate algo on order book, if feed_type is 0, otherwise, this
          field is ignore.
        sub_req_type : int
           1: subscribe
           2: unsubscribe
        freq : int
          book update frequency in milliseconds, if feed_type is 0, otherwise, this field is
          ignored.
        """
        self.req_id = req_id
        self.markets = markets
        self.sub_req_type = sub_req_type
        self.grouping = grouping
        self.feed_type = feed_type
        self.freq = freq
        self.depth = depth

    def build_feed_request(self, builder: flatbuffers.Builder) -> bytearray:

        build_market = []
        size = len(self.markets)
        for market in self.markets:
            build_market.append(builder.CreateString(market))
        req_id_string = builder.CreateString(self.req_id)

        FbsFr.FeedRequestStartMarketsVector(builder, size)
        for b in reversed(build_market):
            builder.PrependUOffsetTRelative(b)
        markets = builder.EndVector(size)

        FbsFr.FeedRequestStart(builder)
        FbsFr.FeedRequestAddReqId(builder, req_id_string)
        FbsFr.FeedRequestAddSubReqType(builder, self.sub_req_type)
        FbsFr.FeedRequestAddFeedType(builder, self.feed_type)
        FbsFr.FeedRequestAddGrouping(builder, self.grouping)
        FbsFr.FeedRequestAddDepth(builder, self.depth)
        FbsFr.FeedRequestAddFrequency(builder, self.freq)
        FbsFr.FeedRequestAddMarkets(builder, markets)
        feed_req = FbsFr.FeedRequestEnd(builder)

        FbsMessage.MessageStart(builder)
        FbsMessage.MessageAddTts(builder, time_ns())
        FbsMessage.MessageAddBodyType(builder, FbsBody.Body.FeedRequest)
        FbsMessage.MessageAddBody(builder, feed_req)
        msg = FbsMessage.MessageEnd(builder)
        builder.Finish(msg)
        return builder.Output()
