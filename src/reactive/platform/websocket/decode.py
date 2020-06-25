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


from typing import Union, Tuple

from reactive.papi.Body import Body
from reactive.papi.FeedRequestAccept import FeedRequestAccept
from reactive.papi.FeedRequestReject import FeedRequestReject
from reactive.papi.LiquidationOrder import LiquidationOrder
from reactive.papi.MDSnapshotL2 import MDSnapshotL2
from reactive.papi.Message import Message
from reactive.papi.PublicTrade import PublicTrade


def decode_fbs(msg: Message) -> Tuple[Body, Union[MDSnapshotL2,
                                                  PublicTrade,
                                                  LiquidationOrder,
                                                  FeedRequestReject,
                                                  FeedRequestAccept,
                                                  None]]:
    """
    Decode a reactive.papi.Message into the Msg BodyType and body object.
    """
    if msg.BodyType() == Body.MDSnapshotL2:
        fbs_md = MDSnapshotL2()
        fbs_md.Init(msg.Body().Bytes, msg.Body().Pos)
        return Body.MDSnapshotL2, fbs_md
    elif msg.BodyType() == Body.PublicTrade:
        fbs_trade = PublicTrade()
        fbs_trade.Init(msg.Body().Bytes, msg.Body().Pos)
        return Body.PublicTrade, fbs_trade
    elif msg.BodyType() == Body.FeedRequestReject:
        frr = FeedRequestReject()
        frr.Init(msg.Body().Bytes, msg.Body().Pos)
        return Body.FeedRequestReject, frr
    elif msg.BodyType() == Body.FeedRequestAccept:
        fra = FeedRequestAccept()
        fra.Init(msg.Body().Bytes, msg.Body().Pos)
        return Body.FeedRequestAccept, fra
    elif msg.BodyType() == Body.LiquidationOrder:
        lo = LiquidationOrder()
        lo.Init(msg.Body().Bytes, msg.Body().Pos)
        return Body.LiquidationOrder, lo
    else:
        return Body.NONE, None
