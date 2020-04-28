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

import unittest

from reactive.platform.domain.asset import AssetRefData
from reactive.platform.domain.instr import InstrRefData
from reactive.platform.domain.market import MarketRefData
from reactive.platform.domain.venue import VenueRefData


class AssetRefDataTestCase(unittest.TestCase):
    asset_str = '[{"id": 6001, "symbol": "AEX", "display": "Netherlands 25 Index", ' \
                '"asset_type": "Index"}, {"id": 36, "symbol": "AUD", "display": ' \
                '"Australia, Dollars", "asset_type": "Ccy"}, {"id": 6002, "symbol": ' \
                '"AXC", "display": "Australian 200 Index", "asset_type": "Index"}]'

    def test_asset_ref(self):
        asset_ref = AssetRefData.from_json(asset_str=self.asset_str)
        asset_dict = asset_ref.to_dict()
        self.assertTrue(isinstance(asset_dict, dict))
        self.assertEqual(len(asset_dict), 3)
        asset = asset_ref.asset_by_symbol('AEX')
        self.assertTrue(asset is not None)
        self.assertEqual(asset.symbol, 'AEX')
        self.assertEqual(asset.id, 6001)
        self.assertEqual(asset.display, "Netherlands 25 Index")
        self.assertEqual(asset.asset_type, "Index")
        # return none if asset not found
        asset = asset_ref.asset_by_symbol('ETC')
        self.assertTrue(asset is None)


class InstrRefDataTestCase(unittest.TestCase):
    instr_str = '[{"id": 45, "symbol": "AEXEUR-CFD", "display": "AEX/EUR CFD", ' \
                '"description": "Netherlands 25 Index CFD", "base_asset": "AEX", ' \
                '"term_ccy": "EUR", "tenor": "", "asset_type": "Index", "instr_type": ' \
                '"CFD", "settl_type": "Cash", "pip_dp": 0, "pip_digits": 2}, {"id": 1, ' \
                '"symbol": "AUDUSD", "display": "AUD/USD", "description": "Aussie Dollar", ' \
                '"base_asset": "AUD", "term_ccy": "USD", "tenor": "Spot", "asset_type": ' \
                '"Ccy", "instr_type": "SpotFwd", "settl_type": "Physical", "pip_dp": 4, ' \
                '"pip_digits": 2}]'

    def test_instr_ref(self):
        instr_ref = InstrRefData.from_json(instrs_str=self.instr_str)
        instr_dict = instr_ref.to_dict()
        self.assertTrue(isinstance(instr_dict, dict))
        self.assertEqual(len(instr_dict), 2)
        instr = instr_ref.instr_by_symbol('AUDUSD')
        self.assertTrue(instr is not None)
        self.assertEqual(instr.symbol, 'AUDUSD')
        self.assertEqual(instr.id, 1)
        self.assertEqual(instr.display, "AUD/USD")
        self.assertEqual(instr.description, "Aussie Dollar")
        self.assertEqual(instr.base_asset, "AUD")
        self.assertEqual(instr.term_ccy, "USD")
        self.assertEqual(instr.tenor, "Spot")
        self.assertEqual(instr.asset_type, "Ccy")
        self.assertEqual(instr.instr_type, "SpotFwd")
        self.assertEqual(instr.settl_type, "Physical")
        self.assertEqual(instr.pip_dp, 4)
        self.assertEqual(instr.pip_digits, 2)
        # return none if instrument not found
        instr = instr_ref.instr_by_symbol('GBPUSD')
        self.assertTrue(instr is None)


class VenueRefDataTestCase(unittest.TestCase):
    venue_str = '[{"id": 15, "symbol": "BIN", "display": "Binance", "flags": 0}, ' \
                '{"id": 2, "symbol": "CMC", "display": "CMC Markets", "flags": 0}, ' \
                '{"id": 3, "symbol": "CME", "display": "CME", "flags": 0}]'

    def test_venue_ref(self):
        venue_ref = VenueRefData.from_json(venue_str=self.venue_str)
        venue_dict = venue_ref.to_dict()
        self.assertTrue(isinstance(venue_dict, dict))
        self.assertEqual(len(venue_dict), 3)
        venue = venue_ref.venue_by_symbol('BIN')
        self.assertTrue(venue is not None)
        self.assertEqual(venue.symbol, 'BIN')
        self.assertEqual(venue.id, 15)
        self.assertEqual(venue.display, "Binance")
        self.assertEqual(venue.flags, 0)
        # return none if venue not found
        venue = venue_ref.venue_by_symbol('LMAX')
        self.assertTrue(venue is None)


class MarketRefDataTestCase(unittest.TestCase):
    market_str = '[{"symbol": "XRPUSD-BIN", "display": "XRP/USD", "description": "Ripple", ' \
                 '"instr": "XRPUSD", "venue": "BIN", "source_id": 983041, "expiry_date": 0, ' \
                 '"default_lots": 1, "lot_numer": 1, "lot_denom": 1, "tick_numer": 1, ' \
                 '"tick_denom": 100000, "price_dp": 5}, {"symbol": "XTSUSD-REX", "display": ' \
                 '"XTS/USD", "description": "Test Instrument", "instr": "XTSUSD", "venue": ' \
                 '"REX", "source_id": 65537, "expiry_date": 0, "default_lots": 1000000, ' \
                 '"lot_numer": 1, "lot_denom": 1, "tick_numer": 1, "tick_denom": 10000, ' \
                 '"price_dp": 4}]'

    def test_market_ref(self):
        market_ref = MarketRefData.from_json(market_str=self.market_str)
        market_dict = market_ref.to_dict()
        self.assertTrue(isinstance(market_dict, dict))
        self.assertEqual(len(market_dict), 2)
        market = market_ref.market_by_symbol('XTSUSD-REX')
        self.assertTrue(market is not None)
        self.assertEqual(market.symbol, 'XTSUSD-REX')
        self.assertEqual(market.display, "XTS/USD")
        self.assertEqual(market.description, "Test Instrument")
        self.assertEqual(market.instr, "XTSUSD")
        self.assertEqual(market.venue, "REX")
        self.assertEqual(market.source_id, 65537)
        self.assertEqual(market.expiry_date, 0)
        self.assertEqual(market.default_lots, 1000000)
        self.assertEqual(market.lot_numer, 1)
        self.assertEqual(market.lot_denom, 1)
        self.assertEqual(market.tick_numer, 1)
        self.assertEqual(market.tick_denom, 10000)
        # return none if market not found
        market = market_ref.market_by_symbol('GBPUSD-REX')
        self.assertTrue(market is None)


if __name__ == '__main__':
    unittest.main()
