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
import asyncio
from typing import Callable, Coroutine

from reactive.platform.marketdata.mdclient import MDClient
from reactive.platform.net.websocket import consume, produce


async def run(client: MDClient, app_run: Callable[[MDClient], Coroutine]):
    """
    Consume market data from platform market data gateway. Customize app_run coroutine should be
    implemented for assign new market data callback via `MdClient.register_md_handler` method, or
    subscribe/unsubscribe markets.
    """
    async with client.conn as ws:
        consumer_task = asyncio.ensure_future(consume(ws, client.read))
        producer_task = asyncio.ensure_future(produce(ws, client.write))
        app_task = asyncio.ensure_future(app_run(client))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task, app_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
