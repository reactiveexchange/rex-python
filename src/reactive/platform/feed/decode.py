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

from reactive.papi.Body import Body
from reactive.papi.Message import Message

from reactive.platform.feed.feedaccept import FeedRequestAccept
from reactive.platform.feed.feedrequestreject import FeedRequestReject
from reactive.platform.feed.liquidation import LiquidationOrder
from reactive.platform.feed.mdsnapshotl2 import MDSnapshotL2
from reactive.platform.feed.publictrade import PublicTrade

from reactive.platform.websocket.decode import decode_fbs


def load_from_fbs(msg: Message) -> Union[MDSnapshotL2, FeedRequestAccept,
                                         FeedRequestReject, PublicTrade]:
    """
    load a reactive.papi.Message into feed object.
    """
    body_type, body = decode_fbs(msg)

    if body_type == Body.FeedRequestAccept:
        return FeedRequestAccept.load_from_fbs(body)
    elif body_type == Body.FeedRequestReject:
        return FeedRequestReject.load_from_fbs(body)
    elif body_type == Body.MDSnapshotL2:
        return MDSnapshotL2.load_from_fbs(body)
    elif body_type == Body.PublicTrade:
        return PublicTrade.load_from_fbs(body)
    elif body_type == Body.LiquidationOrder:
        return LiquidationOrder.load_from_fbs(body)
