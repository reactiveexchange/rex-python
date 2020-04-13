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

import reactive.platform.fbs.feed.Body as Body
import reactive.platform.fbs.feed.Feed as Feed
import reactive.platform.fbs.feed.FeedRequest as Fr
import reactive.platform.fbs.feed.Message as Message
import reactive.platform.fbs.feed.SubReqType as Srt

from time import time_ns
from typing import List


class FeedRequest:

    def __init__(self, req_id: str, grouping: int, markets: List[str],
                 sub_req_type: int = Srt.SubReqType.Subscribe,
                 feed: int = Feed.Feed.Default,
                 conflation: int = 100,
                 depth: int = 5):
        self.req_id = req_id
        self.sub_req_type = sub_req_type
        self.markets = markets
        self.grouping = grouping
        self.sub_req_type = sub_req_type
        self.feed = feed
        self.conflation = conflation
        self.depth = depth

    def build_feed_request(self, builder: flatbuffers.Builder) -> bytearray:

        build_market = []
        size = len(self.markets)
        for market in self.markets:
            build_market.append(builder.CreateString(market))

        Fr.FeedRequestStartMarketsVector(builder, size)
        for b in reversed(build_market):
            builder.PrependUOffsetTRelative(b)
        markets = builder.EndVector(size)

        Fr.FeedRequestStart(builder)
        Fr.FeedRequestAddReqId(builder, self.req_id)
        Fr.FeedRequestAddSubReqType(builder, self.sub_req_type)
        Fr.FeedRequestAddFeed(builder, self.feed)
        Fr.FeedRequestAddGrouping(builder, self.grouping)
        Fr.FeedRequestAddConflation(builder, self.conflation)
        Fr.FeedRequestAddDepth(builder, self.depth)
        Fr.FeedRequestAddMarkets(builder, markets)
        feed_req = Fr.FeedRequestEnd(builder)

        Message.MessageStart(builder)
        Message.MessageAddTts(builder, time_ns())
        Message.MessageAddBodyType(builder, Body.Body.FeedRequest)
        Message.MessageAddBody(builder, feed_req)
        msg = Message.MessageEnd(builder)
        builder.Finish(msg)
        return builder.Output()
