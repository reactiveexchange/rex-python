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

from copy import deepcopy
from json import dumps, loads
from typing import List

from reactive.platform.domain.util import convert


class Market:

    def __init__(self, symbol="", display="", description="", instr="", venue="", source_id=0,
                 expiry_date=0, default_lots=0, lot_numer=0, lot_denom=0, tick_numer=0,
                 tick_denom=0, price_dp=0, **kwargs):
        self.symbol = convert(symbol, str)
        self.display = convert(display, str)
        self.description = convert(description, str)
        self.instr = convert(instr, str)
        self.venue = convert(venue, str)
        self.source_id = convert(source_id, int)
        self.expiry_date = convert(expiry_date, int)
        self.default_lots = convert(default_lots, int)
        self.lot_numer = convert(lot_numer, int)
        self.lot_denom = convert(lot_denom, int)
        self.tick_numer = convert(tick_numer, int)
        self.tick_denom = convert(tick_denom, int)
        self.price_dp = convert(price_dp, int)

    def __str__(self):
        return "Market(" + f"Symbol:'{self.symbol}'," \
               f"Display:'{self.display}'," + \
               f"Description:'{self.description}'," + \
               f"Instr:'{self.instr}'," + \
               f"Venue:'{self.venue}'," + \
               f"SourceID:{self.source_id}," + \
               f"ExpiryDate:{self.expiry_date}," + \
               f"DefaultLots:{self.default_lots}," + \
               f"LotNumer:{self.lot_numer}," + \
               f"LotDenom:{self.lot_denom}," + \
               f"TickNumer:{self.tick_numer}," + \
               f"TickDenom:{self.tick_denom}," + \
               f"PriceDp:{self.price_dp}" + ")"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())

    def to_json(self, *, indent=None, **kwargs):
        return dumps(self.to_dict(), indent=indent, **kwargs)


class MarketRef:

    def __init__(self, market, instr, venue):
        self.market = market
        self.instr = instr
        self.venue = venue


class MarketRefData:
    """
    MarketRefData represents Market reference data, support to search Market by id or market
    symbol. Dump the market reference to json string or pandas DataFrame.
    """

    MARKET_TABLE_NAME = "market_t"

    def __init__(self, market_dict: dict = None):
        self.__market_dict = market_dict if market_dict is not None \
            else dict()

    def clear(self):

        self.__market_dict = dict()

    def put_market(self, market: Market):

        self.__market_dict[market.symbol] = market

    def market_by_symbol(self, key: str) -> Market:
        return self.__market_dict.get(key, None)

    def to_dict(self):
        return deepcopy(self.__market_dict)

    def to_json(self, *, indent=None, **kwargs):
        markets = list(value.to_dict() for _, value in self.__market_dict.items())
        return dumps(markets, indent=indent, **kwargs)

    @classmethod
    def from_json(cls, market_str: str):
        markets = loads(market_str)
        return cls.load_from_list(markets=markets)

    @classmethod
    def load_from_list(cls, markets: List[dict] = None):
        ref_data = cls()
        if markets is None:
            return ref_data

        for market_dict in markets:
            market = Market(**market_dict)
            ref_data.put_market(market)
        return ref_data
