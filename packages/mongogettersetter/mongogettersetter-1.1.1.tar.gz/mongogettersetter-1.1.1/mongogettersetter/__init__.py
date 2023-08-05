import sys
import json

sys.setrecursionlimit(64)


class MongoDictWrapper(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prepare(self, _key, _collection, _filter_query):
        self._filter_query = _filter_query
        self._collection = _collection
        self._key = _key[0]
        self._keys = _key
        path = ".".join(self._keys)
        # print(f"__prepare__ you are at: {path}")

    def __setattr__(self, _key, value):
        if _key in ["_filter_query", "_collection", "_key", "_keys"]:
            self.__dict__[_key] = value
        else:
            # Call the parent __setitem__ method to actually set the value in the dictionary
            path = ".".join(self._keys)
            # Execute your function here
            # # print(f"Dictionary updated: {path}.{_key}={value}")
            update = {"$set": {"{}.{}".format(path, _key): value}}
            result = self._collection.update_one(self._filter_query, update)
            nested_dict = self._collection.find_one(self._filter_query)
            for k in self._keys:
                nested_dict = nested_dict[k]
            # print(f"__setitem__ {str(nested_dict)}")
            super().update(nested_dict)

    def __getattr__(self, _key):
        if _key in self.__dict__:
            return self.__dict__[_key]
        else:
            path = ".".join(self._keys)
            # print(f"__getitem__ you are at: {path}")
            nested_dict = self._collection.find_one(self._filter_query)
            for k in self._keys:
                nested_dict = nested_dict[k]
            super().update(nested_dict)
            # print(f"__getitem__ {str(nested_dict)}")
            if isinstance(nested_dict[_key], dict):
                dictwrapper = MongoDictWrapper(nested_dict[_key])
                dictwrapper.prepare(
                    self._keys + [_key], self._collection, self._filter_query
                )
                return dictwrapper
            elif isinstance(nested_dict[_key], list):
                datawrapper = MongoDataWrapper(
                    self._keys + [_key], self._collection, self._filter_query
                )
                return datawrapper
            else:
                return nested_dict[_key]

    def __getitem__(self, _key):
        path = ".".join(self._keys)
        # print(f"__getitem__ you are at: {path}")
        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        super().update(nested_dict)
        # print(f"__getitem__ {str(nested_dict)}")
        if isinstance(nested_dict[_key], dict):
            dictwrapper = MongoDictWrapper(nested_dict[_key])
            dictwrapper.prepare(
                self._keys + [_key], self._collection, self._filter_query
            )
            return dictwrapper
        elif isinstance(nested_dict[_key], list):
            datawrapper = MongoDataWrapper(
                self._keys + [_key], self._collection, self._filter_query
            )
            return datawrapper
        else:
            return nested_dict[_key]

    def __setitem__(self, _key, value):
        # Call the parent __setitem__ method to actually set the value in the dictionary
        path = ".".join(self._keys)
        # Execute your function here
        # # print(f"Dictionary updated: {path}.{_key}={value}")
        update = {"$set": {"{}.{}".format(path, _key): value}}
        result = self._collection.update_one(self._filter_query, update)
        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        # print(f"__setitem__ {str(nested_dict)}")
        super().update(nested_dict)

    def __delitem__(self, _key):
        super().__delitem__(_key)
        path = ".".join(self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )

    def get(self, _key, default=None):
        if _key in self:
            return self[_key]
        else:
            return default

    def pop(self, _key, default=None):
        value = super().pop(_key, default)
        path = ".".join(self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
        return value

    def update(self, other):
        super().update(other)
        d = dict(self)
        other.update(d)
        path = ".".join(self._keys)
        update = {"$set": {path: other}}
        self._collection.update_one(self._filter_query, update, upsert=True)

    def clear(self):
        # print("__clear__ ")
        path = ".".join(self._keys)
        update = {"$set": {path: {}}}
        self._collection.update_one(self._filter_query, update)
        super().clear()


class MongoDataWrapper:
    def __init__(self, _key, _collection, _filter_query):
        self._filter_query = _filter_query
        self._collection = _collection
        self._key = _key[0]
        self._keys = _key

    def get(self, _key=None):
        """Get the original representation of the document as it exists without MongoGetterSetter Wrappers.
        If no arguments are passed, then return the whole data.
        If _key is passed, it will return the specific value w.r.t the key.

        Args:
            _key (any|None, optional):  Defaults to None.

        Returns:
            any: Original Data without Wrapper
        """

        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        if _key is None:
            return nested_dict
        else:
            return nested_dict[_key]

    def inArray(self, value):
        path = ".".join(self._keys)
        return self._collection.find_one({path: {"$in": [value]}})

    def append(self, *value):
        return self.push(*value)

    def push(self, *values, maximum=0):
        path = ".".join(self._keys)
        if maximum == 0:
            return (
                self._collection.update_one(
                    self._filter_query, {"$push": {path: {"$each": values}}}
                ).modified_count
                > 0
            )
        else:
            update_operation = {"$push": {path: {"$each": values, "$slice": -maximum}}}

            return (
                self._collection.update_one(
                    self._filter_query, update_operation
                ).modified_count
                > 0
            )

    def addToSet(self, value):
        path = ".".join(self._keys)
        return (
            self._collection.update_one(
                self._filter_query, {"$addToSet": {path: value}}
            ).modified_count
            > 0
        )

    def pop(self, direction=1):
        path = ".".join(self._keys)
        return (
            self._collection.update_one(
                self._filter_query, {"$pop": {path: direction}}
            ).modified_count
            > 0
        )

    def remove(self, item):
        return self.pull(item)

    def count(self):
        return self.__len__()

    def pull(self, value):
        path = ".".join(self._keys)
        return (
            self._collection.update_one(
                self._filter_query, {"$pull": {path: value}}
            ).modified_count
            > 0
        )

    def insert(self, index, value):
        path = ".".join(self._keys)
        insert_query = {"$push": {path: {"$each": [value], "$position": index}}}
        return (
            self._collection.update_one(self._filter_query, insert_query).modified_count
            > 0
        )

    def pullAll(self, *values):
        path = ".".join(self._keys)
        return (
            self._collection.update_one(
                self._filter_query, {"$pullAll": {path: values}}
            ).modified_count
            > 0
        )

    def matchSize(self, value):
        path = ".".join(self._keys)
        return bool(self._collection.find_one({path: {"$size": value}}))

    def elemMatch(self, **kvalues):
        path = ".".join(self._keys)
        return bool(self._collection.find_one({path: {"$elemMatch": kvalues}}))

    def matchAll(self, *values):
        path = ".".join(self._keys)
        return bool(self._collection.find_one({path: {"$all": values}}))

    def update(self, field, match, **kvalues):
        path = ".".join(self._keys)
        _filter_query = dict(self._filter_query)
        update_query = {
            path + f".$[elem]." + _key: value for _key, value in kvalues.items()
        }
        _filter_query[path + "." + field] = match
        return (
            self._collection.update_one(
                self._filter_query,
                {"$set": update_query},
                array_filters=[{f"elem.{field}": match}],
                upsert=True,
            ).modified_count
            > 0
        )

    def __len__(self):
        return len(self.get())

    def __str__(self):
        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return json.dumps(nested_dict, indent=4, default=str)

    def __repr__(self):
        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return str(nested_dict)

    def __int__(self):
        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return int(nested_dict)

    def __float__(self):
        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return float(nested_dict)

    def __bool__(self):
        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return bool(nested_dict)

    def __getitem__(self, _key):
        data = self.get(_key)
        # return data[_key]
        if isinstance(data, dict):
            dictwrapper = MongoDictWrapper(data)
            dictwrapper.prepare(
                self._keys + [_key], self._collection, self._filter_query
            )
            return dictwrapper
        elif isinstance(data, list):
            datawrapper = MongoDataWrapper(
                self._keys + [_key], self._collection, self._filter_query
            )
            return datawrapper
        else:
            return data

    def __getattr__(self, _key):
        if _key in self.__dict__:
            return self.__dict__[_key]
        else:
            data = self.get(_key)
            # return data[_key]
            if isinstance(data, dict):
                dictwrapper = MongoDictWrapper(data)
                dictwrapper.prepare(
                    self._keys + [_key], self._collection, self._filter_query
                )
                return dictwrapper
            elif isinstance(data, list):
                datawrapper = MongoDataWrapper(
                    self._keys + [_key], self._collection, self._filter_query
                )
                return datawrapper
            else:
                return data

    def __setattr__(self, _key, value):
        if _key in ["_filter_query", "_collection", "_key", "_keys"]:
            self.__dict__[_key] = value
        else:
            path = ".".join(self._keys)
            self._collection.update_one(
                self._filter_query, {"$set": {path + "." + _key: value}}
            )
            # # print("__setattr__", _key, value)

    def __setitem__(self, index, value):
        path = ".".join(self._keys)
        update_query = {path + "." + str(index): value}
        self._collection.update_one(self._filter_query, {"$set": update_query})

    def __delitem__(self, _key):
        path = ".".join(self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )

    def __delattr__(self, _key):
        path = ".".join(self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )


class MongoGetterSetter(type):
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.__class__ = type(
            "PyMongoGetterSetter",
            (cls,),
            {
                "__getattr__": cls.PyMongoGetterSetter.__getattr__,
                "__getitem__": cls.PyMongoGetterSetter.__getitem__,
                "__setattr__": cls.PyMongoGetterSetter.__setattr__,
                "__setitem__": cls.PyMongoGetterSetter.__setitem__,
                "__contains__": cls.PyMongoGetterSetter.__contains__,
                "__str__": cls.PyMongoGetterSetter.__str__,
                "__repr__": cls.PyMongoGetterSetter.__repr__,
                "__delattr__": cls.PyMongoGetterSetter.__delattr__,
                "__delitem__": cls.PyMongoGetterSetter.__delitem__,
            },
        )
        return instance

    class PyMongoGetterSetter:
        def __getattr__(self, _key):
            return MongoDataWrapper([_key], self._collection, self._filter_query)

        def __getitem__(self, _key):
            return MongoDataWrapper([_key], self._collection, self._filter_query)

        def __setattr__(self, _key, value):
            _filter_query = self._filter_query
            self._collection.update_one(_filter_query, {"$set": {_key: value}})

        def __setitem__(self, _key, value):
            _filter_query = self._filter_query
            self._collection.update_one(_filter_query, {"$set": {_key: value}})

        def __contains__(self, _key):
            return self._collection.find_one({_key: {"$exists": True}})

        def __str__(self):
            _filter_query = self._filter_query
            doc = self._collection.find_one(_filter_query)
            return json.dumps(doc, indent=4, default=str)

        def __repr__(self):
            _filter_query = self._filter_query
            return str(self._collection.find_one(_filter_query))

        def __delattr__(self, name):
            # print(f"___delattr___ name = {name}")
            self._collection.update_one(self._filter_query, {"$unset": {name: ""}})

        def __delitem__(self, name):
            # print(f"___delattr___ name = {name}")
            self._collection.update_one(self._filter_query, {"$unset": {name: ""}})
