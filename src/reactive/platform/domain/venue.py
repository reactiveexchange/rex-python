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

from reactive.platform.domain.util import convert


class Venue:

    def __init__(self, id=0, symbol="", display="", flags=0, **kwargs):
        self.id = convert(id, int)
        self.symbol = convert(symbol, str)
        self.display = convert(display, str)
        self.flags = convert(flags, int)

    def __str__(self):
        return "Venue{" + "id:{0},symbol:'{1}',Display:'{2}',flags:{3}".\
            format(self.id, self.symbol, self.display, self.flags) + "}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())

    def to_json(self, *, indent=None, **kwargs):
        return dumps(self.to_dict(), indent=indent, **kwargs)


VenueRef = Venue


class VenueRefData:
    """
    VenueRefData represents venue reference data, support to search venue by id or venue
    symbol. Dump the venue reference to json string or pandas DataFrame.
    """

    Venue_TABLE_NAME = "venue_t"

    def __init__(self, venue_dict: dict = None):
        self.__venue_dict = venue_dict if venue_dict is not None \
            else dict()

    def put_venue(self, venue: Venue):
        self.__venue_dict[venue.symbol] = venue

    def venue_by_symbol(self, key: str) -> Venue:
        return self.__venue_dict.get(key, None)

    def clear(self):
        self.__venue_dict = dict()

    def to_dict(self):
        return deepcopy(self.__venue_dict)

    def to_json(self):
        venues = list(value.to_dict() for _, value in self.__venue_dict.items())
        return dumps(venues)

    @classmethod
    def from_json(cls, venue_str: str):
        venues = loads(venue_str)
        return cls.load_from_list(venues)

    @classmethod
    def load_from_list(cls, venues=None):
        ref_data = cls()
        if venues is None:
            return ref_data

        for venue_dict in venues:
            venue = Venue(**venue_dict)
            ref_data.put_venue(venue)
        return ref_data
