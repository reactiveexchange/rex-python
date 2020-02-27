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

from rex.util.cache import Cached
from unittest import TestCase, main


class CachedTestClass(metaclass=Cached):

    def __init__(self, x, y=10):
        pass


class TestCached(TestCase):

    def test_cached_class(self):
        res = CachedTestClass(x=10, y=30)
        res2 = CachedTestClass(x=10, y=30)
        res3 = CachedTestClass(11)
        res4 = CachedTestClass(15, y=9)
        self.assertTrue(res is res2)
        self.assertFalse(res3 is res)
        self.assertFalse(res4 is res)


if __name__ == "__main__":
    main()
