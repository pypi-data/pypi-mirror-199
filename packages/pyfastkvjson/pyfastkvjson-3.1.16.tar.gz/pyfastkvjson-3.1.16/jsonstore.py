#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Provides a Python class that maps values to/from a JSON file
"""
from __future__ import absolute_import

import json
import os.path
import sys
from collections import OrderedDict
from copy import deepcopy
from tempfile import mktemp
import pyAesCrypt

__all__ = ["JsonStore"]

STRING_TYPES = (str,)
INT_TYPES = (int,)
if sys.version_info < (3,):
    STRING_TYPES += (unicode,)
    INT_TYPES += (long,)

VALUE_TYPES = (bool, int, float, type(None)) + INT_TYPES


class JsonStore(object):
    """A class to provide object based access to a JSON file"""

    def __enter__(self):
        current_state = self.__dict__["_data"]
        self.__dict__["_states"].append(current_state)
        self.__dict__["_data"] = deepcopy(current_state)
        return self

    def __exit__(self, *args):
        previous_state = self.__dict__["_states"].pop()
        if any(args):
            self.__dict__["_data"] = previous_state
        elif not self.__dict__["_states"]:
            self._save()

    def _do_auto_commit(self):
        if self._auto_commit and not self.__dict__["_states"]:
            self._save()

    def _load(self):
        # Check if file exists. Create it if it doesn't
        if not os.path.exists(self._path):
            empty_json_data = "{}".encode(self._encoding)
            if self._secure:
                tempFile = mktemp()
                with open(tempFile, "wb") as tempStore:
                    tempStore.write(empty_json_data)
                pyAesCrypt.encryptFile(tempFile, self._path, self._password, self._bufferSize)
                os.remove(tempFile)
            else:
                with open(self._path, "wb") as store:
                    store.write(empty_json_data)

        # Read the contents of the file
        if self._secure:
            tempFile = mktemp()
            pyAesCrypt.decryptFile(self._path, tempFile, self._password, self._bufferSize)
            with open(tempFile, "rb") as tmp:
                raw_data = tmp.read().decode(self._encoding)
            os.remove(tempFile)
        else:
            with open(self._path, "rb") as store:
                raw_data = store.read().decode(self._encoding)

        if not raw_data:
            data = OrderedDict()
        else:
            data = json.loads(raw_data, object_pairs_hook=OrderedDict)

        if not isinstance(data, dict):
            raise ValueError("Root element is not an object")
        self.__dict__["_data"] = data

    def _save(self):
        temp = self._path + "~"
        tempFile = temp + "2" if self._secure else temp
        with open(temp, "wb") as tempStore:
            jsonStr = json.dumps(self._data, indent=self._indent)
            data = jsonStr.encode(self._encoding)
            tempStore.write(data)

        if self._secure:
            pyAesCrypt.encryptFile(temp, tempFile, self._password, self._bufferSize)
            os.remove(temp)

        if sys.version_info >= (3, 3):
            os.replace(tempFile, self._path)
        elif os.name == "windows":
            os.remove(self._path)
            os.rename(tempFile, self._path)
        else:
            os.rename(tempFile, self._path)

    def get_dump(self):
        return self._data

    def __init__(self, path, indent=2, auto_commit=False, password=None):
        self.__dict__.update(
            {
                "_auto_commit": auto_commit,
                "_data": None,
                "_path": path,
                "_encoding": "utf-8",
                "_secure": True if password else None,
                "_password": password,
                "_bufferSize": 64 * 1024,
                "_indent": indent,
                "_states": [],
            }
        )
        self._load()

    def __getattr__(self, key):
        if key in self._data:
            return deepcopy(self._data[key])
        else:
            raise AttributeError(key)

    def _has_key(self, key: str) -> bool:
        try:
            temp = self._data[key]
            return True
        except KeyError:
            return False

    def _store_object(self, s: dict):
        f = self._flatten_dict(s)
        for key, value in list(f.items()):
            self._data[key] = deepcopy(value)
            self._do_auto_commit()

    @classmethod
    def _flatten_dict(cls, d, parent_key="", sep="."):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(cls._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @classmethod
    def _canonical_key(cls, key):
        """Convert a set/get/del key into the canonical form."""
        if cls._valid_string(key):
            return tuple(key.split("."))

        if isinstance(key, (tuple, list)):
            key = tuple(key)
            if not key:
                raise TypeError("key must be a string or non-empty tuple/list")
            return key

        raise TypeError("key must be a string or non-empty tuple/list")

    @classmethod
    def _valid_object(cls, obj, parents=None):
        """
        Determine if the object can be encoded into JSON
        Raise an exception if the object is not suitable for assignment.
        """
        # pylint: disable=unicode-builtin,long-builtin
        if isinstance(obj, (dict, list)):
            if parents is None:
                parents = []
            elif any(o is obj for o in parents):
                raise ValueError("Cycle detected in list/dictionary")
            parents.append(obj)

        if isinstance(obj, dict):
            return all(
                cls._valid_string(k) and cls._valid_object(v, parents)
                for k, v in obj.items()
            )
        elif isinstance(obj, (list, tuple)):
            return all(cls._valid_object(o, parents) for o in obj)
        else:
            return cls._valid_value(obj)

    @classmethod
    def _valid_value(cls, value):
        if isinstance(value, (bool, int, float, type(None))):
            return True
        elif sys.version_info < (3,) and isinstance(value, long):
            return True
        else:
            return cls._valid_string(value)

    @classmethod
    def _valid_string(cls, value):
        if isinstance(value, str):
            return True
        elif sys.version_info < (3,):
            return isinstance(value, unicode)
        else:
            return False

    def __setattr__(self, key, value):
        self._valid_object(value)
        self._data[key] = deepcopy(value)
        self._do_auto_commit()

    def __delattr__(self, key):
        del self._data[key]

    def __get_obj(self, steps):
        """Returns the object which is under the given path."""
        path = []
        obj = self._data
        for step in steps:
            if isinstance(obj, dict) and not self._valid_string(step):
                # this is necessary because of the JSON serialisation
                raise TypeError("%s is a dict and %s is not a string" % (path, step))
            try:
                obj = obj[step]
            except (KeyError, IndexError, TypeError) as e:
                raise type(e)("unable to get %s from %s: %s" % (step, path, e))
            path.append(step)
        return obj

    def __setitem__(self, key, value):
        steps = self._canonical_key(key)
        path, step = steps[:-1], steps[-1]
        self._valid_object(value)
        container = self.__get_obj(path)
        if isinstance(container, dict) and not self._valid_string(step):
            raise TypeError("%s is a dict and %s is not a string" % (path, step))
        try:
            container[step] = deepcopy(value)
        except (IndexError, TypeError) as e:
            raise type(e)("unable to set %s from %s: %s" % (step, path, e))
        self._do_auto_commit()

    def __getitem__(self, key):
        steps = self._canonical_key(key)
        obj = self.__get_obj(steps)
        return deepcopy(obj)

    def __delitem__(self, key):
        steps = self._canonical_key(key)
        path, step = steps[:-1], steps[-1]
        obj = self.__get_obj(path)
        try:
            del obj[step]
        except (KeyError, IndexError, TypeError) as e:
            raise type(e)("unable to delete %s from %s: %s" % (step, path, e))

    def __contains__(self, key):
        steps = self._canonical_key(key)
        try:
            self.__get_obj(steps)
            return True
        except (KeyError, IndexError, TypeError):
            # this is rather permissive as the types are dynamic
            return False
