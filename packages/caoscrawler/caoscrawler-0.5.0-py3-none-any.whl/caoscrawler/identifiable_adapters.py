#!/usr/bin/env python3
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021-2022 Henrik tom Wörden
#               2021-2022 Alexander Schlemmer
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

from __future__ import annotations
import yaml

from datetime import datetime
from typing import Any
from .identifiable import Identifiable
import caosdb as db
import logging
from abc import abstractmethod, ABCMeta
from .utils import has_parent

logger = logging.getLogger(__name__)


def convert_value(value: Any):
    """ Returns a string representation of the value that is suitable
    to be used in the query
    looking for the identified record.

    Parameters
    ----------
    value : Any type, the value that shall be returned and potentially converted.

    Returns
    -------
    out : the string reprensentation of the value

    """

    if isinstance(value, db.Entity):
        return str(value.id)
    elif isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, bool):
        return str(value).upper()
    elif isinstance(value, str):
        # replace single quotes, otherwise they may break the queries
        return value.replace("\'", "\\'")
    else:
        return str(value)


class IdentifiableAdapter(metaclass=ABCMeta):
    """
    Base class for identifiable adapters.

    Some terms:
    - Registered identifiable is the definition of an identifiable which is:
      - A record type as the parent
      - A list of properties
      - A list of referenced by statements

    - Identifiable is the concrete identifiable, e.g. the Record based on
      the registered identifiable with all the values filled in.

    - Identified record is the result of retrieving a record based on the
      identifiable from the database.

    General question to clarify:
    Do we want to support multiple identifiables per RecordType?
    Current implementation supports only one identifiable per RecordType.

    The list of referenced by statements is currently not implemented.

    The IdentifiableAdapter can be used to retrieve the three above mentioned objects (registred
    identifiabel, identifiable and identified record) for a Record.
    """

    @staticmethod
    def create_query_for_identifiable(ident: Identifiable):
        """
        This function is taken from the old crawler:
        caosdb-advanced-user-tools/src/caosadvancedtools/crawler.py

        uses the properties of ident to create a query that can determine
        whether the required record already exists.
        """

        query_string = "FIND RECORD "
        if ident.record_type is not None:
            query_string += ident.record_type
        for ref in ident.backrefs:
            eid = ref
            if isinstance(ref, db.Entity):
                eid = ref.id
            query_string += (" WHICH IS REFERENCED BY " + str(eid) + " AND")

        query_string += " WITH "

        if ident.name is not None:
            query_string += "name='{}'".format(ident.name)
            if len(ident.properties) > 0:
                query_string += " AND "

        query_string += IdentifiableAdapter.create_property_query(ident)
        return query_string

    @staticmethod
    def create_property_query(entity: Identifiable):
        query_string = ""
        for pname, pvalue in entity.properties.items():
            if pvalue is None:
                query_string += "'" + pname + "' IS NULL AND "
            elif isinstance(pvalue, list):
                for v in pvalue:
                    query_string += ("'" + pname + "'='" +
                                     convert_value(v) + "' AND ")

            # TODO: (for review)
            #       This code would allow for more complex identifiables with
            #       subproperties being checked directly.
            #       we currently do not need them and they could introduce
            #       problems in the local caching mechanism.
            #       However, it could be discussed to implement a similar mechanism.
            # elif isinstance(p.value, db.Entity):
            #     query_string += ("'" + p.name + "' WITH (" +
            #                      IdentifiableAdapter.create_property_query(p.value) +
            #                      ") AND ")
            else:
                query_string += ("'" + pname + "'='" +
                                 convert_value(pvalue) + "' AND ")
        # remove the last AND
        return query_string[:-4]

    @abstractmethod
    def get_registered_identifiable(self, record: db.Record):
        """
        Check whether an identifiable is registered for this record and return its definition.
        If there is no identifiable registered, return None.
        """
        pass

    @abstractmethod
    def resolve_reference(self, record: db.Record):
        pass

    @abstractmethod
    def get_file(self, identifiable: db.File):
        """
        Retrieve the file object for a (File) identifiable.
        """
        pass

    def get_identifiable(self, record: db.Record, referencing_entities=None):
        """
        retrieve the registred identifiable and fill the property values to create an
        identifiable

        Args:
            record: the record for which the Identifiable shall be created.
            referencing_entities: a dictionary (Type: dict[int, dict[str, list[db.Entity]]]), that
              allows to look up entities with a certain RecordType, that reference ``record``

        Returns:
            Identifiable, the identifiable for record.
        """

        registered_identifiable = self.get_registered_identifiable(record)

        if referencing_entities is None:
            referencing_entities = {}

        property_name_list_A = []
        property_name_list_B = []
        identifiable_props = {}
        identifiable_backrefs = []

        if registered_identifiable is not None:
            # fill the values:
            for prop in registered_identifiable.properties:
                if prop.name == "name":
                    # The name can be an identifiable, but it isn't a property
                    continue
                # problem: what happens with multi properties?
                # case A: in the registered identifiable
                # case B: in the identifiable

                # TODO: similar to the Identifiable class, Registred Identifiable should be a
                # separate class too
                if prop.name.lower() == "is_referenced_by":
                    for rtname in prop.value:
                        if (id(record) in referencing_entities
                                and rtname in referencing_entities[id(record)]):
                            identifiable_backrefs.extend(referencing_entities[id(record)][rtname])
                        else:
                            # TODO: is this the appropriate error?
                            raise NotImplementedError(
                                f"The following record is missing an identifying property:"
                                f"RECORD\n{record}\nIdentifying PROPERTY\n{prop.name}"
                            )
                    continue

                record_prop = record.get_property(prop.name)
                if record_prop is None:
                    # TODO: how to handle missing values in identifiables
                    #       raise an exception?
                    # TODO: is this the appropriate error?
                    raise NotImplementedError(
                        f"The following record is missing an identifying property:"
                        f"RECORD\n{record}\nIdentifying PROPERTY\n{prop.name}"
                    )
                identifiable_props[record_prop.name] = record_prop.value
                property_name_list_A.append(prop.name)

            # check for multi properties in the record:
            for prop in property_name_list_A:
                property_name_list_B.append(prop)
            if (len(set(property_name_list_B)) != len(property_name_list_B) or len(
                    set(property_name_list_A)) != len(property_name_list_A)):
                raise RuntimeError(
                    "Multi properties used in identifiables could cause unpredictable results and "
                    "are not allowed. You might want to consider a Property with a list as value.")

        # use the RecordType of the registred Identifiable if it exists
        # We do not use parents of Record because it might have multiple
        return Identifiable(
            record_id=record.id,
            record_type=(registered_identifiable.parents[0].name
                         if registered_identifiable else None),
            name=record.name,
            properties=identifiable_props,
            path=record.path,
            backrefs=identifiable_backrefs
        )

    @abstractmethod
    def retrieve_identified_record_for_identifiable(self, identifiable: Identifiable):
        """
        Retrieve identifiable record for a given identifiable.

        This function will return None if there is either no identifiable registered
        or no corresponding identified record in the database for a given record.

        Warning: this function is not expected to work correctly for file identifiables.
        """
        pass

    # TODO: remove side effect
    # TODO: use ID if record has one?
    def retrieve_identified_record_for_record(self, record: db.Record, referencing_entities=None):
        """
        This function combines all functionality of the IdentifierAdapter by
        returning the identifiable after having checked for an appropriate
        registered identifiable.

        In case there was no appropriate registered identifiable or no identifiable could
        be found return value is None.
        """
        identifiable = self.get_identifiable(record, referencing_entities=referencing_entities)

        if identifiable.path is not None:
            return self.get_file(identifiable)

        return self.retrieve_identified_record_for_identifiable(identifiable)


class LocalStorageIdentifiableAdapter(IdentifiableAdapter):
    """
    Identifiable adapter which can be used for unit tests.
    """

    def __init__(self):
        self._registered_identifiables = dict()
        self._records = []

    def register_identifiable(self, name: str, definition: db.RecordType):
        self._registered_identifiables[name] = definition

    def get_records(self):
        return self._records

    def get_file(self, identifiable: Identifiable):
        """
        Just look in records for a file with the same path.
        """
        candidates = []
        for record in self._records:
            if record.role == "File" and record.path == identifiable.path:
                candidates.append(record)
        if len(candidates) > 1:
            raise RuntimeError("Identifiable was not defined unambigiously.")
        if len(candidates) == 0:
            return None
        return candidates[0]

    def store_state(self, filename):
        with open(filename, "w") as f:
            f.write(db.common.utils.xml2str(
                db.Container().extend(self._records).to_xml()))

    def restore_state(self, filename):
        with open(filename, "r") as f:
            self._records = db.Container().from_xml(f.read())

    # TODO: move to super class?
    def is_identifiable_for_record(self, registered_identifiable: db.RecordType, record: db.Record):
        """
        Check whether this registered_identifiable is an identifiable for the record.

        That means:
        - The properties of the registered_identifiable are a subset of the properties of record.
        - One of the parents of record is the parent of registered_identifiable.

        Return True in that case and False otherwise.
        """
        if len(registered_identifiable.parents) != 1:
            raise RuntimeError(
                "Multiple parents for identifiables not supported.")

        if not has_parent(record, registered_identifiable.parents[0].name):
            return False

        for prop in registered_identifiable.properties:
            if record.get_property(prop.name) is None:
                return False
        return True

    def get_registered_identifiable(self, record: db.Record):
        identifiable_candidates = []
        for _, definition in self._registered_identifiables.items():
            if self.is_identifiable_for_record(definition, record):
                identifiable_candidates.append(definition)
        if len(identifiable_candidates) > 1:
            raise RuntimeError(
                "Multiple candidates for an identifiable found.")
        if len(identifiable_candidates) == 0:
            return None
        return identifiable_candidates[0]

    def check_record(self, record: db.Record, identifiable: Identifiable):
        """
        Check for a record from the local storage (named "record") if it is
        the identified record for an identifiable which was created by
        a run of the crawler.

        Naming of the parameters could be confusing:
        record is the record from the local database to check against.
        identifiable is the record that was created during the crawler run.
        """
        if (identifiable.record_type is not None
                and not has_parent(record, identifiable.record_type)):
            return False
        for propname, propvalue in identifiable.properties.items():
            prop_record = record.get_property(propname)
            if prop_record is None:
                return False

            # if prop is an entity, it needs to be resolved first.
            # there are two different cases:
            # a) prop_record.value has a registered identifiable:
            #      in this case, fetch the identifiable and set the value accordingly
            if isinstance(propvalue, db.Entity):  # lists are not checked here
                otherid = prop_record.value
                if isinstance(prop_record.value, db.Entity):
                    otherid = prop_record.value.id
                if propvalue.id != otherid:
                    return False

            elif propvalue != prop_record.value:
                return False
        return True

    def retrieve_identified_record_for_identifiable(self, identifiable: Identifiable):
        candidates = []
        for record in self._records:
            if self.check_record(record, identifiable):
                candidates.append(record)
        if len(candidates) > 1:
            raise RuntimeError(
                f"Identifiable was not defined unambigiously. Possible candidates are {candidates}")
        if len(candidates) == 0:
            return None
        return candidates[0]

    def resolve_reference(self, value: db.Record):
        if self.get_registered_identifiable(value) is None:
            raise NotImplementedError("Non-identifiable references cannot"
                                      " be used as properties in identifiables.")
            # TODO: just resolve the entity

        value_identifiable = self.retrieve_identified_record_for_record(value)
        if value_identifiable is None:
            raise RuntimeError("The identifiable which is used as property"
                               " here has to be inserted first.")

        if value_identifiable.id is None:
            raise RuntimeError("The entity has not been assigned an ID.")

        return value_identifiable.id


class CaosDBIdentifiableAdapter(IdentifiableAdapter):
    """
    Identifiable adapter which can be used for production.
    """

    # TODO: don't store registered identifiables locally

    def __init__(self):
        self._registered_identifiables = dict()

    def load_from_yaml_definition(self, path: str):
        """Load identifiables defined in a yaml file"""
        with open(path, 'r') as yaml_f:
            identifiable_data = yaml.safe_load(yaml_f)

        for key, value in identifiable_data.items():
            rt = db.RecordType().add_parent(key)
            for prop_name in value:
                if isinstance(prop_name, str):
                    rt.add_property(name=prop_name)
                elif isinstance(prop_name, dict):
                    for k, v in prop_name.items():
                        rt.add_property(name=k, value=v)
                else:
                    NotImplementedError("YAML is not structured correctly")

            self.register_identifiable(key, rt)

    def register_identifiable(self, name: str, definition: db.RecordType):
        self._registered_identifiables[name] = definition

    def get_file(self, identifiable: Identifiable):
        if identifiable.path is None:
            raise RuntimeError("Path must not be None for File retrieval.")
        candidates = db.execute_query("FIND File which is stored at '{}'".format(
            identifiable.path))
        if len(candidates) > 1:
            raise RuntimeError("Identifiable was not defined unambigiously.")
        if len(candidates) == 0:
            return None
        return candidates[0]

    def get_registered_identifiable(self, record: db.Record):
        """
        returns the registred identifiable for the given Record

        It is assumed, that there is exactly one identifiable for each RecordType. Only the first
        parent of the given Record is considered; others are ignored
        """
        if len(record.parents) == 0:
            return None
        # TODO We need to treat the case where multiple parents exist properly.
        rt_name = record.parents[0].name
        for name, definition in self._registered_identifiables.items():
            if definition.parents[0].name.lower() == rt_name.lower():
                return definition

    def resolve_reference(self, record: db.Record):
        """
        Current implementation just sets the id for this record
        as a value. It needs to be verified that references all contain an ID.
        """
        if record.id is None:
            return record
        return record.id

    def retrieve_identified_record_for_identifiable(self, identifiable: Identifiable):
        query_string = self.create_query_for_identifiable(identifiable)
        candidates = db.execute_query(query_string)
        if len(candidates) > 1:
            raise RuntimeError(
                f"Identifiable was not defined unambigiously.\n{query_string}\nReturned the "
                f"following {candidates}."
                f"Identifiable:\n{identifiable.record_type}{identifiable.properties}")
        if len(candidates) == 0:
            return None
        return candidates[0]
