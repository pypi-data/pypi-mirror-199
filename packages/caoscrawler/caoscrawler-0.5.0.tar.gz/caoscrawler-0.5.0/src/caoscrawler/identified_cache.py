#!/usr/bin/env python3
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2021 Henrik tom Wörden <h.tomwoerden@indiscale.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#


"""
see class docstring
"""

from .identifiable import Identifiable
import caosdb as db


class IdentifiedCache(object):
    """
    This class is like a dictionary where the keys are Identifiables. When you check whether an
    Identifiable exists as key this class returns True not only if that exact Python object is
    used as a key, but if an Identifiable is used as key that is **equal** to the one being
    considered (see __eq__ function of Identifiable). Similarly, if you do `cache[identifiable]`
    you get the Record where the key is an Identifiable that is equal to the one in the rectangular
    brackets.

    This class is used for Records where we checked the existence in a remote server using
    identifiables. If the Record was found, this means that we identified the corresponding Record
    in the remote server and the ID of the local object can be set.
    To prevent querying the server again and again for the same objects, this cache allows storing
    Records that were found on a remote server and those that were not (typically in separate
    caches).
    """

    def __init__(self):
        self._cache = {}
        self._identifiables = []

    def __contains__(self, identifiable: Identifiable):
        return identifiable in self._identifiables

    def __getitem__(self, identifiable: db.Record):
        index = self._identifiables.index(identifiable)
        return self._cache[id(self._identifiables[index])]

    def add(self, record: db.Record, identifiable: Identifiable):
        self._cache[id(identifiable)] = record
        self._identifiables.append(identifiable)
