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
feed ack data structures.
"""

import reactive.papi.FeedRequestAccept as FbsFra


class FeedRequestAccept:

    def __init__(self, feed_id: int, req_id: str = ""):
        self.feed_id = feed_id
        self.req_id = req_id

    @classmethod
    def load_from_fbs(cls, ack: FbsFra.FeedRequestAccept):
        return cls(feed_id=ack.FeedId(), req_id=ack.ReqId())
