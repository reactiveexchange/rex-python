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


class Asset:

    def __init__(self, id=0, symbol="", display="", asset_type=0, **kwargs):
        self.id = convert(id, int)
        self.symbol = convert(symbol, str)
        self.display = convert(display, str)
        self.asset_type = convert(asset_type, str)

    def __str__(self):
        return "Asset(" + "id:{0},symbol:'{1}',Display:'{2}',asset_type:'{3}'".\
            format(self.id, self.symbol, self.display, self.asset_type) + ")"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())

    def to_json(self, *, indent=None, **kwargs):
        return dumps(self.to_dict(), indent=indent, **kwargs)


AssetRef = Asset


class AssetRefData:
    """
    AssetRefData represents assets reference data, support to search asset by id or asset
    symbol. Dump the asset reference to json string or pandas DataFrame.
    """

    def __init__(self, asset_dict: dict = None):
        self.__asset_dict = asset_dict if asset_dict is not None \
            else dict()

    def put_asset(self, asset: Asset):
        self.__asset_dict[asset.symbol] = asset

    def clear(self):
        self.__asset_dict = dict()

    def asset_by_symbol(self, key: str) -> Asset:
        return self.__asset_dict.get(key, None)

    def to_dict(self):
        return deepcopy(self.__asset_dict)

    def to_json(self, *, indent=None, **kwargs):
        assets = list(value.to_dict() for _, value in self.__asset_dict.items())
        return dumps(assets, indent=indent, **kwargs)

    @classmethod
    def from_json(cls, asset_str: str):
        assets = loads(asset_str)
        return cls.load_from_list(assets)

    @classmethod
    def load_from_list(cls, assets: List[dict] = None):
        ref_data = cls()
        if assets is None:
            return ref_data

        for asset_dict in assets:
            asset = Asset(**asset_dict)
            ref_data.put_asset(asset)
        return ref_data
