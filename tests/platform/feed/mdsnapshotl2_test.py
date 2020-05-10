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

import numpy as np

import unittest

from reactive.platform.feed.mdsnapshotl2 import MDSnapshotL2


class MDSnapshotL2TestCase(unittest.TestCase):

    def test_depth(self):
        bid_price = np.array([1.0, 0.9])
        bid_qty = np.array([10.0, 11.0, 0.0])
        offer_price = np.array([1.1, 1.2, 1.3])
        offer_qty = np.array([10.0, 9.0, 8.0])

        book = MDSnapshotL2(market="EURUSD-REX", bid_price=bid_price, bid_qty=bid_qty,
                            offer_price=offer_price, offer_qty=offer_qty)
        self.assertEqual(2, book.bid_depth())
        self.assertEqual(3, book.offer_depth())
        self.assertFalse(book.is_empty())

        book = MDSnapshotL2(market="EURUSD-REX", bid_price=np.zeros(1), bid_qty=np.zeros(1),
                            offer_price=np.zeros(1), offer_qty=np.zeros(1))
        self.assertTrue(book.is_empty())
