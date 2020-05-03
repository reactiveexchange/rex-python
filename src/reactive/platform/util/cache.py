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
"""

__author__ = ['fzhao']


import hashlib
from weakref import WeakValueDictionary


class Cached(type):
    """
    Metaclass Hook for Cached instances of a class type.
    The same inputs of `__init__`  method will return the same object from cache.
    """

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.__cache = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        params = {'args': args}
        params.update(kwargs)
        _id = str(sorted(list(params.items())))
        h = hashlib.new('ripemd160')
        h.update(_id.encode())
        hash_id = h.hexdigest()

        if hash_id in cls.__cache:
            return cls.__cache[hash_id]
        else:
            obj = super().__call__(*args, **kwargs)
            cls.__cache[hash_id] = obj
            return obj


if __name__ == "__main__":
    import doctest

    doctest.testmod()
