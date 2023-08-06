# import sys
import json

# sys.(64)setrecursionlimit


class MongoDictWrapper(dict):
    """
    MongoDictWrapper is a wrapper around the dictionary object to provide the functionality of updating the database when the dictionary is updated. It is used to wrap the dictionary object in the MongoGetterSetter class. It is not meant to be used directly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prepare(self, _key, _collection, _filter_query):
        """
        Prepare the MongoDictWrapper object to be used. This method is called by the MongoGetterSetter class when the object is created.
        """

        self._filter_query = _filter_query
        self._collection = _collection
        self._key = _key[0]
        self._keys = _key
        # path = '.'.join(str(v) for v in self._keys)
        # print(f"__prepare__ you are at: {path}")

    def __setattr__(self, _key, value):
        _key = str(_key)
        """
        Set the value of the key in the dictionary and update the database.
        """
        if _key in ["_filter_query", "_collection", "_key", "_keys"]:
            self.__dict__[_key] = value
        else:
            # Call the parent __setitem__ method to actually set the value in the dictionary
            path = ".".join(str(v) for v in self._keys)
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
        """
        Get the value of the key in the dictionary.
        """
        _key = str(_key)
        if _key in self.__dict__:
            return self.__dict__[_key]
        else:
            path = ".".join(str(v) for v in self._keys)
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
        _key = str(_key)
        """
        Get the value of the key in the dictionary.
        """
        path = ".".join(str(v) for v in self._keys)
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
        _key = str(_key)
        """
        Set the value of the key in the dictionary and update the database.
        """
        # Call the parent __setitem__ method to actually set the value in the dictionary
        path = ".".join(str(v) for v in self._keys)
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
        _key = str(_key)
        """
        Delete the item from the dictionary and update the database.
        """
        super().__delitem__(_key)
        path = ".".join(str(v) for v in self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )

    def __delattr_(self, _key):
        _key = str(_key)
        """
        Delete the item from the dictionary and update the database.
        """
        super().__delitem__(_key)
        path = ".".join(str(v) for v in self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
    
    def delete(self):
        """
        Delete the nested object from the MongoDB Document
        """
        
        path = ".".join(str(v) for v in self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path: ""}}
        )

    def get(self, _key, default=None):
        """
        Get the value of the key from the dictionary. If the key is not present, return the default value.
        """

        if _key in self:
            return self[_key]
        else:
            return default

    def pop(self, _key, default=None):
        """
        Pop the value of the key from the dictionary and update the database. If the key is not present, return the default value.
        """

        value = super().pop(_key, default)
        path = ".".join(str(v) for v in self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
        return value

    def update(self, other):
        """
        Update the dictionary with the other dictionary and update the database.
        """

        super().update(other)
        d = dict(self)
        other.update(d)
        path = ".".join(str(v) for v in self._keys)
        update = {"$set": {path: other}}
        self._collection.update_one(self._filter_query, update, upsert=True)

    def clear(self):
        """
        Clear the dictionary and update the database.
        """

        # print("__clear__ ")
        path = ".".join(str(v) for v in self._keys)
        update = {"$set": {path: {}}}
        self._collection.update_one(self._filter_query, update)
        super().clear()


class MongoDataWrapper:

    """
    `MongoDataWrapper` is a subscriptable class, which wraps MongoDB document datatypes to provide MongoDB Array/List Operations over a simple, straightforward API to perform various operations on the MongoDB collection. Check the list of methods for the allowed operations.
    """

    def __init__(self, _key, _collection, _filter_query):
        self._filter_query = _filter_query
        self._collection = _collection
        self._key = _key[0]
        self._keys = _key

    def get(self, _key=None):
        """
        Get the original representation of the document as it exists without MongoGetterSetter Wrappers.
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
        """
        Check if the value exists in the array. Returns True if the value exists in the array, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return self._collection.find_one({path: {"$in": [value]}})

    def append(self, *value):
        """
        Append the value to the array. Returns True if the value is appended, else False.
        """

        return self.push(*value)

    def push(self, *values, maximum=0):
        """
        Push the value to the array. Returns True if the value is pushed, else False.
        """

        path = ".".join(str(v) for v in self._keys)
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
        """
        Add the value to the array if it does not exist. Returns True if the value is added, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return (
            self._collection.update_one(
                self._filter_query, {"$addToSet": {path: value}}
            ).modified_count
            > 0
        )

    def pop(self, direction=1):
        """
        Pop the value from the array. Returns True if the value is popped, else False. direction=1 for popping from the end, direction=-1 for popping from the beginning.
        """

        path = ".".join(str(v) for v in self._keys)
        return (
            self._collection.update_one(
                self._filter_query, {"$pop": {path: direction}}
            ).modified_count
            > 0
        )

    def remove(self, item):
        """
        Remove the value from the array. Returns True if the value is removed, else False.
        """

        return self.pull(item)

    def count(self):
        """
        Return the length of the array/string/object
        """

        return self.__len__()

    def pull(self, value):
        """
        Remove the value from the array. Returns True if the value is removed, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return (
            self._collection.update_one(
                self._filter_query, {"$pull": {path: value}}
            ).modified_count
            > 0
        )

    def insert(self, index, value):
        """
        Insert the value at the index in the array. Returns True if the value is inserted, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        insert_query = {"$push": {path: {"$each": [value], "$position": index}}}
        return (
            self._collection.update_one(self._filter_query, insert_query).modified_count
            > 0
        )

    def pullAll(self, *values):
        """
        Remove all the (given) values from the array. Returns True if the value is removed, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return (
            self._collection.update_one(
                self._filter_query, {"$pullAll": {path: values}}
            ).modified_count
            > 0
        )

    def matchSize(self, value):
        """
        Check if the array has the given size. Returns True if the array has the given size, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return bool(self._collection.find_one({path: {"$size": value}}))

    def elemMatch(self, **kvalues):
        """
        Check if the array has an element that matches the given key-value pairs. Returns True if the array has an element that matches the given key-value pairs, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return bool(self._collection.find_one({path: {"$elemMatch": kvalues}}))

    def matchAll(self, *values):
        """
        Check if the array has all the given values. Returns True if the array has all the given values, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return bool(self._collection.find_one({path: {"$all": values}}))

    def update(self, field, match, **kvalues):
        """
        Update the value of the field in the array element that matches the given value. Returns True if the value is updated, else False.
        """

        path = ".".join(str(v) for v in self._keys)
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
        """
        Return the length of the array/string/object
        """

        return len(self.get())

    def __str__(self):
        """
        Return the string representation of the array/string/object
        """

        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return json.dumps(nested_dict, indent=4, default=str)

    def __repr__(self):
        """
        Return the string representation of the array/string/object
        """

        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return str(nested_dict)

    def __int__(self):
        """
        Return the integer representation of the array/string/object
        """

        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return int(nested_dict)

    def __float__(self):
        """
        Return the float representation of the array/string/object
        """

        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return float(nested_dict)

    def __bool__(self):
        """
        Return the boolean representation of the array/string/object
        """

        nested_dict = self._collection.find_one(self._filter_query)
        for k in self._keys:
            nested_dict = nested_dict[k]
        return bool(nested_dict)

    def __getitem__(self, _key):
        """
        Return the value of the key in the array/string/object
        """

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
        """
        Return the value of the key in the array/string/object
        """

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
        """
        Set the value of the key in the array/string/object
        """
        _key = str(_key)
        if _key in ["_filter_query", "_collection", "_key", "_keys"]:
            self.__dict__[_key] = value
        else:
            path = ".".join(str(v) for v in self._keys)
            self._collection.update_one(
                self._filter_query, {"$set": {path + "." + _key: value}}
            )
            # # print("__setattr__", _key, value)

    def __setitem__(self, index, value):
        """
        Set the value of the key in the array/string/object
        """
        path = ".".join(str(v) for v in self._keys)
        update_query = {path + "." + str(index): value}
        self._collection.update_one(self._filter_query, {"$set": update_query})

    def __delitem__(self, _key):
        """
        Delete the key in the array/string/object using del keyword
        """
        path = ".".join(str(v) for v in self._keys)
        data = self.get()
        _key = str(_key)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
        if isinstance(data, list):
            self.pull(None)

    def __delattr__(self, _key):
        """
        Delete the key in the array/string/object using del keyword
        """
        path = ".".join(str(v) for v in self._keys)
        data = self.get()
        _key = str(_key)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
        if isinstance(data, list):
            self.pull(None)
    
    def delete(self):
        """
        Delete the nested object from the MongoDB Document
        """
        
        path = ".".join(str(v) for v in self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path: ""}}
        )
        


class MongoGetterSetter(type):

    """
    `MongoGetterSetter` is a metaclass that provides a convenient getter and setter API for instances of the classes that use it, allowing natural operations in Python objects to easily reflect in MongoDB documents.
    """

    def __call__(cls, *args, **kwargs):
        """
        Return a new instance of the class
        """

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
                "delete": cls.PyMongoGetterSetter.delete,
            },
        )
        return instance

    class PyMongoGetterSetter:

        """
        `PyMongoGetterSetter` is a class that provides a convenient getter and setter API for instances of the classes that use it, allowing natural operations in Python objects to easily reflect in MongoDB documents.
        """

        def __getattr__(self, _key):
            """
            Return the value of the key in the array/string/object
            """
            return MongoDataWrapper([_key], self._collection, self._filter_query)

        def __getitem__(self, _key):
            """
            Return the value of the key in the array/string/object
            """
            return MongoDataWrapper([_key], self._collection, self._filter_query)

        def __setattr__(self, _key, value):
            """
            Set the value of the key in the array/string/object
            """
            _filter_query = self._filter_query
            self._collection.update_one(_filter_query, {"$set": {_key: value}})

        def __setitem__(self, _key, value):
            """
            Set the value of the key in the array/string/object
            """
            _filter_query = self._filter_query
            self._collection.update_one(_filter_query, {"$set": {_key: value}})

        def __contains__(self, _key):
            """
            Return the value of the key in the array/string/object
            """
            return self._collection.find_one({_key: {"$exists": True}})

        def __str__(self):
            """
            Return the string representation of the array/string/object
            """
            _filter_query = self._filter_query
            doc = self._collection.find_one(_filter_query)
            return json.dumps(doc, indent=4, default=str)

        def __repr__(self):
            """
            Return the string representation of the array/string/object
            """
            _filter_query = self._filter_query
            return str(self._collection.find_one(_filter_query))

        def __delattr__(self, name):
            """
            Delete the key in the array/string/object using del keyword
            """
            # print(f"___delattr___ name = {name}")
            self._collection.update_one(self._filter_query, {"$unset": {name: ""}})

        def __delitem__(self, name):
            """
            Delete the key in the array/string/object using del keyword
            """
            # print(f"___delattr___ name = {name}")
            self._collection.update_one(self._filter_query, {"$unset": {name: ""}})
            
        def delete(self):
            """
            Delete the object from the MongoDB collection
            """
            # print(f"deleting {self._id}")
            self._collection.delete_one(self._filter_query)
