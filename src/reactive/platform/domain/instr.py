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

from reactive.platform.domain.asset import Asset
from reactive.platform.domain.util import convert


class Instr:

    def __init__(self, id=0, symbol="", display="", description="",
                 base_asset="", term_ccy="", tenor="", asset_type="",
                 instr_type="", settl_type="", pip_dp=0, pip_digits=0, **kwargs):
        self.id = convert(id, int)
        self.symbol = convert(symbol, str)
        self.display = convert(display, str)
        self.description = convert(description, str)
        self.base_asset = convert(base_asset, str)
        self.term_ccy = convert(term_ccy, str)
        self.tenor = convert(tenor, str)
        self.asset_type = convert(asset_type, str)
        self.instr_type = convert(instr_type, str)
        self.settl_type = convert(settl_type, str)
        self.pip_dp = convert(pip_dp, int)
        self.pip_digits = convert(pip_digits, int)

    def __str__(self):
        return "Instr(" + f"ID:{self.id},Symbol:'{self.symbol}'," + \
               f"Display:'{self.display}'," + \
               f"Description:'{self.description}'," + \
               f"BaseAsset:'{self.base_asset}'," + \
               f"TermCcy:'{self.term_ccy}'," + \
               f"Tenor:'{self.tenor}'," + \
               f"AssetType:'{self.asset_type}'," + \
               f"InstrType:'{self.instr_type}'," + \
               f"SettlType:'{self.settl_type}'," + \
               f"PipDp:{self.pip_dp}," + \
               f"PipDigits:{self.pip_digits}" + ")"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())

    def to_json(self, *, indent=None, **kwargs):
        return dumps(self.to_dict(), indent=indent, **kwargs)


class InstrRef:

    def __init__(self, instr: Instr, base_asset: Asset, term_ccy: Asset):
        self.instr = instr
        self.base_asset = base_asset
        self.term_ccy = term_ccy


class InstrRefData:
    """
    InstrRefData represents instrument reference data, support to search InstrRef by id or instr
    symbol. Dump the instrument reference to json string or pandas DataFrame.
    """

    def __init__(self, instr_dict: dict = None):
        self.__instr_dict = instr_dict if instr_dict is not None \
            else dict()

    def put_instr(self, instr: Instr):
        self.__instr_dict[instr.symbol] = instr

    def clear(self):
        self.__instr_dict = dict()

    def instr_by_symbol(self, key: str) -> Instr:
        return self.__instr_dict.get(key, None)

    def to_dict(self):
        return deepcopy(self.__instr_dict)

    def to_json(self, *, indent=None, **kwargs):
        instrs = list(value.to_dict() for _, value in self.__instr_dict.items())
        return dumps(instrs, indent=indent, **kwargs)

    @classmethod
    def from_json(cls, instrs_str: str):
        instrs = loads(instrs_str)
        return cls.load_from_list(instrs=instrs)

    @classmethod
    def load_from_list(cls, instrs=None):
        ref_data = cls()
        if instrs is None:
            return ref_data

        for instr_dict in instrs:
            instr = Instr(**instr_dict)
            ref_data.put_instr(instr)
        return ref_data
