#!/usr/bin/env python3
# encoding: utf-8
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2023 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Alexander Schlemmer <alexander.schlemmer@ds.mpg.de>
#
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
This is the scanner, the original "_crawl" function from crawl.py.
This is just the functionality, that extracts data from the file system.
"""

from __future__ import annotations

import argparse
import importlib
import logging
import os
import sys
import warnings
import yaml

from argparse import RawTextHelpFormatter
from collections import defaultdict
from copy import deepcopy
from enum import Enum
from importlib_resources import files
from jsonschema import validate
from typing import Any, Optional, Type, Union

import caosdb as db

from caosadvancedtools.cache import UpdateCache, Cache
from caosadvancedtools.crawler import Crawler as OldCrawler
from caosdb.apiutils import (compare_entities, EntityMergeConflictError,
                             merge_entities)
from caosdb.common.datatype import is_reference

from .converters import Converter, DirectoryConverter, ConverterValidationError

from .macros import defmacro_constructor, macro_constructor
from .stores import Store, GeneralStore, RecordStore
from .structure_elements import StructureElement, Directory, NoneElement
from .version import check_cfood_version

from caosdb.high_level_api import convert_to_python_object

from .debug_tree import DebugTree

logger = logging.getLogger(__name__)


def load_definition(crawler_definition_path: str):
    """
    Load a cfood from a crawler definition defined by
    crawler definition path and validate it using cfood-schema.yml.
    """

    # Load the cfood from a yaml file:
    with open(crawler_definition_path, "r") as f:
        crawler_definitions = list(yaml.safe_load_all(f))

    crawler_definition = _load_definition_from_yaml_dict(
        crawler_definitions)

    return _resolve_validator_paths(crawler_definition, crawler_definition_path)


def _load_definition_from_yaml_dict(crawler_definitions: list[dict]):
    """Load crawler definitions from a list of (yaml) dicts `crawler_definitions` which
    contains either one or two documents.

    Doesn't resolve the validator paths in the cfood definition, so for
    internal and testing use only.

    """
    if len(crawler_definitions) == 1:
        # Simple case, just one document:
        crawler_definition = crawler_definitions[0]
        metadata = {}
    elif len(crawler_definitions) == 2:
        metadata = crawler_definitions[0]["metadata"] if "metadata" in crawler_definitions[0] else {
        }
        crawler_definition = crawler_definitions[1]
    else:
        raise RuntimeError(
            "Crawler definition must not contain more than two documents.")

    check_cfood_version(metadata)

    # TODO: at this point this function can already load the cfood schema extensions
    #       from the crawler definition and add them to the yaml schema that will be
    #       tested in the next lines of code:

    # Load the cfood schema:
    with open(str(files('caoscrawler').joinpath('cfood-schema.yml')), "r") as f:
        schema = yaml.safe_load(f)

    # Add custom converters to converter enum in schema:
    if "Converters" in crawler_definition:
        for key in crawler_definition["Converters"]:
            schema["cfood"]["$defs"]["converter"]["properties"]["type"]["enum"].append(
                key)
    if len(crawler_definitions) == 2:
        if "Converters" in metadata:
            for key in metadata["Converters"]:
                schema["cfood"]["$defs"]["converter"]["properties"]["type"]["enum"].append(
                    key)

    # Validate the cfood schema:
    validate(instance=crawler_definition, schema=schema["cfood"])

    return crawler_definition


def _resolve_validator_paths(definition: dict, definition_path: str):
    """Resolve path to validation files with respect to the file in which
    the crawler was defined.

    """

    for key, value in definition.items():

        if key == "validate" and isinstance(value, str):
            # Validator is given by a path
            if not value.startswith('/'):
                # Not an absolute path
                definition[key] = os.path.join(os.path.dirname(definition_path), value)
                if not os.path.isfile(definition[key]):
                    # TODO(henrik) capture this in `crawler_main` similar to
                    # `ConverterValidationError`.
                    raise FileNotFoundError(
                        f"Couldn't find validation file {definition[key]}")
        elif isinstance(value, dict):
            # Recursively resolve all validators
            definition[key] = _resolve_validator_paths(value, definition_path)

    return definition


def create_converter_registry(definition: dict):
    """
    Currently the converter registry is a dictionary containing for each converter:
    - key is the short code, abbreviation for the converter class name
    - module is the name of the module to be imported which must be installed
    - class is the converter class to load and associate with this converter entry

    Formerly known as "load_converters".

    all other info for the converter needs to be included in the converter plugin
    directory:
    schema.yml file
    README.md documentation
    """

    # Defaults for the converter registry:
    with open(str(files('caoscrawler').joinpath('default_converters.yml')), "r") as f:
        converter_registry: dict[str, dict[str, str]] = yaml.safe_load(f)

    # More converters from definition file:
    if "Converters" in definition:
        for key, entry in definition["Converters"].items():
            if key in ["Dict", "DictTextElement", "DictIntegerElement", "DictBooleanElement",
                       "DictDictElement", "DictListElement", "DictFloatElement"]:
                warnings.warn(DeprecationWarning(f"{key} is deprecated. Please use the new"
                                                 " variant; without 'Dict' prefix or "
                                                 "'DictElement' in case of 'Dict'"))

            converter_registry[key] = {
                "converter": entry["converter"],
                "package": entry["package"]
            }

    # Load modules and associate classes:
    for key, value in converter_registry.items():
        module = importlib.import_module(value["package"])
        value["class"] = getattr(module, value["converter"])
    return converter_registry


def initialize_converters(crawler_definition: dict, converter_registry: dict):
    """
    takes the cfood as dict (`crawler_definition`) and creates the converter objects that
    are defined on the highest level. Child Converters will in turn be created during the
    initialization of the Converters.
    """
    converters = []

    for key, value in crawler_definition.items():
        # Definitions and Converters are reserved keywords
        # on the top level of the yaml file.
        # TODO: there should also be a top level keyword for the actual
        #       CFood to avoid confusion between top level keywords
        #       and the CFood.
        if key == "Definitions":
            continue
        elif key == "Converters":
            continue
        converters.append(Converter.converter_factory(
            value, key, converter_registry))

    return converters

# --------------------------------------------------------------------------------
# Main scanner function:
# --------------------------------------------------------------------------------


def scanner(items: list[StructureElement],
            converters: list[Converter],
            general_store: Optional[GeneralStore] = None,
            record_store: Optional[RecordStore] = None,
            structure_elements_path: Optional[list[str]] = None,
            converters_path: Optional[list[str]] = None,
            restricted_path: Optional[list[str]] = None,
            crawled_data: Optional[list[db.Record]] = None,
            debug_tree: Optional[DebugTree] = None):
    """
    Crawl a list of StructureElements and apply any matching converters.

    Formerly known as "_crawl".

    items: structure_elements (e.g. files and folders on one level on the hierarchy)
    converters: locally defined converters for
                        treating structure elements. A locally defined converter could be
                        one that is only valid for a specific subtree of the originally
                        cralwed StructureElement structure.
    general_store and record_store: This recursion of the crawl function should only operate on
                                  copies of the global stores of the Crawler object.
    restricted_path: optional, list of strings, traverse the data tree only along the given
                     path. For example, when a directory contains files a, b and c and b is
                     given in restricted_path, a and c will be ignroed by the crawler.
                     When the end of the given path is reached, traverse the full tree as
                     normal. The first element of the list provided by restricted_path should
                     be the name of the StructureElement at this level, i.e. denoting the
                     respective element in the items argument.
    """
    # This path_found variable stores wether the path given by restricted_path was found in the
    # data tree
    path_found = False
    if restricted_path is not None and len(restricted_path) == 0:
        restricted_path = None

    if crawled_data is None:
        crawled_data = []

    if general_store is None:
        general_store = GeneralStore()

    if record_store is None:
        record_store = RecordStore()

    if structure_elements_path is None:
        structure_elements_path = []

    if converters_path is None:
        converters_path = []

    for element in items:
        for converter in converters:

            # type is something like "matches files", replace isinstance with "type_matches"
            # match function tests regexp for example
            if (converter.typecheck(element) and (
                    restricted_path is None or element.name == restricted_path[0])
                    and converter.match(element) is not None):
                path_found = True
                general_store_copy = general_store.create_scoped_copy()
                record_store_copy = record_store.create_scoped_copy()

                # Create an entry for this matched structure element that contains the path:
                general_store_copy[converter.name] = (
                    os.path.join(*(structure_elements_path + [element.get_name()])))

                # extracts values from structure element and stores them in the
                # variable store
                converter.create_values(general_store_copy, element)

                keys_modified = converter.create_records(
                    general_store_copy, record_store_copy, element)

                children = converter.create_children(general_store_copy, element)

                if debug_tree is not None:
                    # add provenance information for each variable
                    debug_tree.debug_tree[str(element)] = (
                        general_store_copy.get_storage(), record_store_copy.get_storage())
                    debug_tree.debug_metadata["copied"][str(element)] = (
                        general_store_copy.get_dict_copied(),
                        record_store_copy.get_dict_copied())
                    debug_tree.debug_metadata["usage"][str(element)].add(
                        "/".join(converters_path + [converter.name]))
                    mod_info = debug_tree.debug_metadata["provenance"]
                    for record_name, prop_name in keys_modified:
                        # TODO: check
                        internal_id = record_store_copy.get_internal_id(
                            record_name)
                        record_identifier = record_name + \
                            "_" + str(internal_id)
                        converter.metadata["usage"].add(record_identifier)
                        mod_info[record_identifier][prop_name] = (
                            structure_elements_path + [element.get_name()],
                            converters_path + [converter.name])

                scanner(children, converter.converters,
                        general_store_copy, record_store_copy,
                        structure_elements_path + [element.get_name()],
                        converters_path + [converter.name],
                        restricted_path[1:] if restricted_path is not None else None,
                        crawled_data, debug_tree)

    if restricted_path and not path_found:
        raise RuntimeError("A 'restricted_path' argument was given that is not contained in "
                           "the data tree")
    # if the crawler is running out of scope, copy all records in
    # the record_store, that were created in this scope
    # to the general update container.
    scoped_records = record_store.get_records_current_scope()
    for record in scoped_records:
        crawled_data.append(record)

    # TODO: the scoped variables should be cleaned up as soon if the variables
    #       are no longer in the current scope. This can be implemented as follows,
    #       but this breaks the test "test_record_structure_generation", because
    #       some debug info is also deleted. This implementation can be used as soon
    #       as the remaining problems with the debug_tree are fixed.
    # Delete the variables that are no longer needed:
    # scoped_names = record_store.get_names_current_scope()
    # for name in scoped_names:
    #     del record_store[name]
    #     del general_store[name]

    return crawled_data


# --------------------------------------------------------------------------------
# Main scanning interface functions:
# --------------------------------------------------------------------------------


def scan_directory(dirname: str, crawler_definition_path: str,
                   restricted_path: Optional[list[str]] = None,
                   debug_tree: Optional[DebugTree] = None):
    """ Crawl a single directory.

    Formerly known as "crawl_directory".

    Convenience function that starts the crawler (calls start_crawling)
    with a single directory as the StructureElement.

    restricted_path: optional, list of strings
            Traverse the data tree only along the given path. When the end of the given path
            is reached, traverse the full tree as normal.
    """

    crawler_definition = load_definition(crawler_definition_path)
    # Load and register converter packages:
    converter_registry = create_converter_registry(crawler_definition)

    if not dirname:
        raise ValueError(
            "You have to provide a non-empty path for crawling.")
    dir_structure_name = os.path.basename(dirname)

    # TODO: needs to be covered somewhere else
    crawled_directory = dirname
    if not dir_structure_name and dirname.endswith('/'):
        if dirname == '/':
            # Crawling the entire file system
            dir_structure_name = "root"
        else:
            # dirname had a trailing '/'
            dir_structure_name = os.path.basename(dirname[:-1])

    return scan_structure_elements(Directory(dir_structure_name,
                                             dirname),
                                   crawler_definition,
                                   converter_registry,
                                   restricted_path=restricted_path,
                                   debug_tree=debug_tree
                                   )


def scan_structure_elements(items: Union[list[StructureElement], StructureElement],
                            crawler_definition: dict,
                            converter_registry: dict,
                            restricted_path: Optional[list[str]] = None,
                            debug_tree: Optional[DebugTree] = None):
    """
    Start point of the crawler recursion.

    Formerly known as "start_crawling".

    Parameters
    ----------
    items: list
         A list of structure elements (or a single StructureElement) that is used for
         generating the initial items for the crawler. This could e.g. be a Directory.
    crawler_definition : dict
         A dictionary representing the crawler definition, possibly from a yaml
         file.
    restricted_path: optional, list of strings
         Traverse the data tree only along the given path. When the end of the given path
         is reached, traverse the full tree as normal.

    Returns
    -------
    crawled_data : list
        the final list with the target state of Records.
    """

    # This function builds the tree of converters out of the crawler definition.
    if not isinstance(items, list):
        items = [items]

    # TODO: needs to be covered somewhere else
    # self.run_id = uuid.uuid1()
    converters = initialize_converters(crawler_definition, converter_registry)

    return scanner(
        items=items,
        converters=converters,
        restricted_path=restricted_path,
        debug_tree=debug_tree
    )
