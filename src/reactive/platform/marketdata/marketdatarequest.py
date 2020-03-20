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

from time import time_ns
from typing import List

from reactive.platform.fbs.Body import Body
import reactive.platform.fbs.MarketDataRequest as MarketDataRequest
import reactive.platform.fbs.Message as Message


def build_md_request(markets: List[str], sub_type: int, builder: flatbuffers.Builder):
    """
    Create flatbuffer market data request message.

    Parameters
    ----------
    markets: List[str]
        list of market string
    sub_type: int
        1: Subscribe
        2: unsubscribe

    builder: flatbuffers.Builder

    Returns
    -------
    bytearray:
        market data request message byte array.
    """
    build_market = []
    size = len(markets)
    for market in markets:
        build_market.append(builder.CreateString(market))
    MarketDataRequest.MarketDataRequestStartMarketsVector(builder, size)
    for b in reversed(build_market):
        builder.PrependUOffsetTRelative(b)
    markets = builder.EndVector(size)
    MarketDataRequest.MarketDataRequestStart(builder)
    MarketDataRequest.MarketDataRequestAddSubReqType(builder, sub_type)
    MarketDataRequest.MarketDataRequestAddMarkets(builder, markets)
    md_req = MarketDataRequest.MarketDataRequestEnd(builder)

    Message.MessageStart(builder)
    Message.MessageAddTts(builder, time_ns())
    Message.MessageAddRts(builder, time_ns())
    Message.MessageAddSid(builder, 0)
    Message.MessageAddOptions(builder, 0)
    Message.MessageAddBodyType(builder, Body.MarketDataRequest)
    Message.MessageAddBody(builder, md_req)
    msg = Message.MessageEnd(builder)
    builder.Finish(msg)
    return builder.Output()
