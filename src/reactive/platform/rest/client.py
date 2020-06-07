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
Client can access trading platform, use auth token can allow clients to access
the platform via python. Accessed data includes reference, trading data and even send requests.

"""


import os
import requests

from reactive.platform.rest.constant import ASSET_PATH, INSTR_PATH, VENUE_PATH, MARKET_PATH
from reactive.platform.domain.asset import AssetRefData
from reactive.platform.domain.instr import InstrRefData
from reactive.platform.domain.market import MarketRefData
from reactive.platform.domain.venue import VenueRefData
from reactive.platform.util.cache import Cached
from reactive.platform.util.error import TokenNotFound


class Client(metaclass=Cached):
    """
    Client represents a client to access reactive exchange platform via Rest API.
    """

    URL = "https://api.platform.reactivemarkets.com"

    def __init__(self, url: str = None, api_key: str = None):
        """
        Create Client.

        Parameters
        ----------
        url: url
            trading platform api url.
        api_key: str
            exchange API token.
        """
        api_key = api_key if api_key is not None else os.getenv("REACTIVE_API_TOKEN")
        if api_key is None:
            raise TokenNotFound("API key not found")

        self.__headers = {'Authorization': 'Bearer ' + api_key}
        self.__url = url if url is not None else self.URL

    def fetch_asset_ref(self) -> AssetRefData:
        """
        Fetch asset reference data.

        Returns
        -------
        AssetRefData: asset reference data.
        """
        r = requests.get(self.__url + ASSET_PATH, headers=self.__headers)
        return AssetRefData.load_from_list(list(r.json()))

    def fetch_instr_ref(self) -> InstrRefData:
        """
        Fetch instrument reference data.

        Returns
        -------
        InstrRefData: instrument reference data.
        """
        r = requests.get(self.__url + INSTR_PATH, headers=self.__headers)
        return InstrRefData.load_from_list(instrs=list(r.json()))

    def fetch_venue_ref(self) -> VenueRefData:
        """
        Fetch venue reference data.

        Returns
        -------
        VenueRefData: venue reference data.
        """
        r = requests.get(self.__url + VENUE_PATH, headers=self.__headers)
        return VenueRefData.load_from_list(venues=list(r.json()))

    def fetch_market_ref(self) -> MarketRefData:
        """
        Fetch market reference data, and market is instrument unique per venue.

        Returns
        -------
        MarketRefData: market reference data.
        """
        r = requests.get(self.__url + MARKET_PATH, headers=self.__headers)
        return MarketRefData.load_from_list(markets=list(r.json()))
