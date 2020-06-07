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

from reactive.platform.rest.client import Client

API_KEY = "xxx"
URL = "https://api.platform.reactivemarkets.com"


if __name__ == "__main__":

    rc = Client(url=URL, api_key=API_KEY)
    asset_ref = rc.fetch_asset_ref()
    # json format assets reference data
    assets = asset_ref.to_json()
    print("asset reference:\n", assets)
    # dict format assets
    assets_dict = asset_ref.to_dict()
    print("assets dict:\n", assets)

    # instr reference
    instr_ref = rc.fetch_instr_ref()
    instrs = instr_ref.to_json()
    print("instrument reference:\n", instrs)

    # venue reference
    venue_ref = rc.fetch_venue_ref()
    venues = venue_ref.to_json()
    print("venue reference:\n", venues)

    # market reference
    market_ref = rc.fetch_market_ref()
    markets = market_ref.to_json()
    print("market reference:\n", venues)
