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

import reactive.papi.MDSnapshotL2 as Mds
import reactive.papi.PublicTrade as Pt
import reactive.papi.FeedRequestAccept as Fra
import reactive.papi.FeedRequestReject as Frr

from reactive.papi.Body import Body
from reactive.papi.Message import Message

from reactive.platform.feed.feedaccept import FeedRequestAccept
from reactive.platform.feed.feedrequestreject import FeedRequestReject
from reactive.platform.feed.mdsnapshotl2 import MDSnapshotL2
from reactive.platform.feed.publictrade import PublicTrade


def parse_fbs(msg: Message):
    """
    Decode a reactive.papi.Message.
    """
    if msg.BodyType() == Body.MDSnapshotL2:
        fbs_md = Mds.MDSnapshotL2()
        fbs_md.Init(msg.Body().Bytes, msg.Body().Pos)
        return MDSnapshotL2.load_from_fbs(fbs_md)
    elif msg.BodyType() == Body.PublicTrade:
        fbs_trade = Pt.PublicTrade()
        fbs_trade.Init(msg.Body().Bytes, msg.Body().Pos)
        return PublicTrade.load_from_fbs(trade=fbs_trade)
    elif msg.BodyType() == Body.FeedRequestReject:
        frr = Frr.FeedRequestReject()
        frr.Init(msg.Body().Bytes, msg.Body().Pos)
        return FeedRequestReject.load_from_fbs(frr)
    elif msg.BodyType() == Body.FeedRequestAccept:
        fra = Fra.FeedRequestAccept()
        fra.Init(msg.Body().Bytes, msg.Body().Pos)
        return FeedRequestAccept.load_from_fbs(fra)
