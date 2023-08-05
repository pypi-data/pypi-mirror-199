# MongoGetterSetter Documentation

`MongoGetterSetter` is a metaclass that provides a convenient getter and setter API for instances of the classes that use it, allowing natural operations in Python objects to easily reflect in MongoDB documents.

The idea is to convert MongoDB Document into Python Object in High Level, and all other document's sub documents are treated as dictionaties.

This project is under active development.

Usage:
```
from mongogettersetter import MongoGetterSetter
```

### Methods

- `__getattr__(self, key)`: Returns a `MongoDataWrapper` instance for the given `key`. See below for the capabalities of `MongoDataWrapper`

    Example:

    Here, we initialize MyClass with `collection` and `filter_query` as mandatory attributes for MongoGetterSetter to function properly. These 3 arrtibutes are used internally to do further manipulations to MongoDB

    ```
    class MyClass(metaclass=MongoGetterSetter):
        def init(self, _id):
        self._filter_query = {"id": _id} # or the ObjectID, at your convinence
        self._collection = collection # Should be a pymongo.MongoClient[database].collection

        # if the document doesn't exist, we could create it here
        try:
            self._id # if the document doesn't exist, self._id will raise Attribute Error
        except AttributeError:
            self._collection.insert_one({
                "id": _id
            })


    obj = MyClass(_id)
    result = obj.some_key
    ```
- `__getitem__(self, key, value)`: Gets the value of the specified `key` from the MongoDB document.

    Example:

    ```
    print(obj['some_key'])
    ```
- `__setattr__(self, key, value)`: Sets the value of the specified `key` in the MongoDB document.

    Example:

    ```
    obj.some_key = "new_value"
    ```

- `__setitem__(self, key, value)`: Sets the value of the specified `key` in the MongoDB document.

    Example:

    ```
    obj['some_key'] = "new_value"
    ```

- `__contains__(self, key)`: Checks if the MongoDB document contains the specified `key`.

    Example:

    ```
    if "some_key" in obj:
        print("Key exists")
    ```

- `__str__(self)`: Returns a string representation of the MongoDB document.

    Example:

    ```
    print(obj)
    ```
- `__delitem__(self, key)`: Removes the specified key from the MongoDB document.

    Example:
    ```
    del obj['some_key']
    ```
- `__delattr__(self, key)`: Removes the specified key from the MongoDB document.

    Example:
    ```
    del obj.some_key
    ```

## MongoDataWrapper

`MongoDataWrapper` is a subscriptable class, which wraps MongoDB document datatypes to provide MongoDB Array/List Operations over a simple, straightforward API to perform various operations on the MongoDB collection. Check the list of methods for the allowed operations.

### Methods

- `__init__(self, _id, key, collection)`: Initialize the instance with the given `_id`, `key`, and `collection`.

- `get(self)`: Returns the value of the key in the MongoDB document.

- `inArray(self, value)`: Checks if the given `value` is present in the array of the document's key.

- `push(self, *values, maximum=-1)`: Pushes one or more `values` into the array of the document's key. If `maximum` is specified, it will limit the array size to the `maximum` value.

- `addToSet(self, value)`: Adds a `value` to the array of the document's key only if it doesn't exist in the array.

- `pop(self, direction=1)`: Removes the first (`direction=-1`) or the last (`direction=1`) element from the array of the document's key.

- `pull(self, value)`: Removes the specified `value` from the array of the document's key.

- `pullAll(self, *values)`: Removes all occurrences of the specified `values` from the array of the document's key.

- `matchSize(self, value)`: Checks if the size of the array of the document's key is equal to the given `value`.

- `elemMatch(self, **kvalues)`: Checks if the array of the document's key contains at least one element that matches the specified key-value pairs in `kvalues`.

- `matchAll(self, *values)`: Checks if the array of the document's key contains all the specified `values`.

- `update(self, field, match, **kvalues)`: Updates the nested field `field` of the document's key where the `field` value matches `match`, with the key-value pairs provided in `kvalues`.

- `__getitem__(self, index)`: Returns the value of the array of the document's key at the specified `index`.

- `__setitem__(self, index, value)`: Sets the value of the array of the document's key at the specified `index` to the given `value`.

- `__delitem__(self, index)`: Removes the value of the array of the document's key at the specified `index`.

- `__len__(self)`: Returns the length of the array of the document's key.

- `__str__(self)`: Returns a string representation of the value of the document's key.

- `__repr__(self)`: Returns a string representation of the value of the document's key.


## MongoDictWrapper

`MongoDictWrapper` is a class that inherits from the `dict` class and extends its functionalities to access dictionary keys as attributes. It allows you to access, modify, and manipulate MongoDB documents using Python dictionaries. When a MongoDataWrapper returns a `dict`, it automatically is wrapped with `MongoDictWrapper`, when it returns a `list`, it automatically is wrapped with `MongoDataWrapper` to allow manipulation of MongoDB object inside a MongoDB object, like a `dict` inside a `dict`. If you wish to access the value as default datatype, consider get() method.

### Methods

- `__init__(self, *args, **kwargs)`: Constructor method that initializes the base `dict` class.

- `prepare(self, _id, key, collection, filter_query)`: This method initializes the internal data structure that stores information about the document's location in the MongoDB collection.

- `__getitem__(self, key)`: Overrides the base `dict` method to return a wrapped MongoDictWrapper when accessing a nested dictionary.

- `__setitem__(self, key, value)`: Overrides the base `dict` method to update the MongoDB document when setting a key-value pair.

- `__delitem__(self, key)`: Overrides the base `dict` method to delete a key-value pair from the MongoDB document when deleting an item.

- `get(self, key, default=None)`: Overrides the base `dict` method to return the value of the key in the MongoDB document, or the `default` value if the key is not present.

- `pop(self, key, default=None)`: Overrides the base `dict` method to remove and return the value of the key in the MongoDB document, or the `default` value if the key is not present.

- `popitem(self)`: Overrides the base `dict` method to return an arbitrary key-value pair from the MongoDB document.

- `setdefault(self, key, default=None)`: Overrides the base `dict` method to return the value of the key in the MongoDB document if it exists, or sets the key to the `default` value if it does not exist.

- `update(self, other)`: Overrides the base `dict` method to update the MongoDB document with the key-value pairs from the `other` dictionary or iterable.

- `clear(self)`: Overrides the base `dict` method to remove all key-value pairs from the MongoDB document.

- `__len__(self)`: Overrides the base `dict` method to return the number of key-value pairs in the MongoDB document.

- `__str__(self)`: Overrides the base `dict` method to return a string representation of the MongoDB document.

- `__repr__(self)`: Overrides the base `dict` method to return a string representation of the MongoDB document.
## Examples

To provide a more detailed example, let's assume you have a MongoDB collection named people with the following documents:

```
[
    {
        "_id": 1,
        "name": "Alice",
        "age": 30,
        "skills": ["Python", "Django", "JavaScript"],
        "contact": {
            "email": "alice@example.com",
            "phone": "555-1234"
        },
        "projects": [
            {
                "title": "Project A",
                "status": "completed"
            },
            {
                "title": "Project B",
                "status": "in progress"
            }
        ]
    },
    {
        "_id": 2,
        "name": "Bob",
        "age": 25,
        "skills": ["Java", "Spring", "JavaScript"],
        "contact": {
            "email": "bob@example.com",
            "phone": "555-5678"
        },
        "projects": [
            {
                "title": "Project X",
                "status": "completed"
            },
            {
                "title": "Project Y",
                "status": "in progress"
            }
        ]
    }
]
```

Now, let's create a class called `People` with `MongoGetterSetter` as its metaclass.

```
from pymongo import MongoClient
from mongogettersetter import MongoGetterSetter

# Connect to the MongoDB database and collection
client = MongoClient("mongodb://localhost:27017/")
db = client["example_db"]
people_collection = db["people"]

class People(metaclass=MongoGetterSetter):
    def __init__(self, _id):
        self._filter_query = {"id": _id}  # or the ObjectID, at your convenience
        self._collection = people_collection  # Should be a pymongo.MongoClient[database].collection

        try:
            self._id # if the document doesn't exist, self._id will raise Attribute Error
        except AttributeError:
            self._collection.insert_one({
                "id": _id
            })



# Create a People object for Alice with _id = 1
alice = People(1)

# Access and modify Alice's name
print(alice.name)  # Output: 'Alice'
alice.name = "Alice Johnson"
print(alice.name)  # Output: 'Alice Johnson'

# Check if Alice's document has a 'contact' field
if 'contact' in alice:
    print("Contact field exists")

# Access and modify Alice's email
print(alice.contact)  # Output: {'email': 'alice@example.com', 'phone': '555-1234'}
alice.contact.email = "alice.johnson@example.com"
print(alice.contact.email)  # Output: 'alice.johnson@example.com'



# Access and modify Alice's skills
print(alice.skills)# Output: ['Python', 'Django', 'JavaScript']

print(alice.skills.get())  # Output: ['Python', 'Django', 'JavaScript']
alice.skills.push("React", maximum=4)
print(alice.skills.get())  # Output: ['Python', 'Django', 'JavaScript', 'React']
alice.skills.pop(direction=-1)
print(alice.skills.get())  # Output: ['Python', 'Django', 'JavaScript']

# Access and modify Alice's projects

print(alice.projects.get())  # Output: [{'title': 'Project A', 'status': 'completed'}, {'title': 'Project B', 'status': 'in progress'}]
alice.projects.update("title", "Project A", status="archived")
print(alice.projects.get())  # Output: [{'title': 'Project A', 'status': 'archived'}, {'title': 'Project B', 'status': 'in progress'}]
```

## More MongoDataWrapper examples

```
# Create a People object for Alice with _id = 1
alice = People(1)

# Create MongoDataWrapper instances for Alice's skills and projects
alice_skills = alice.skills
alice_projects = alice.projects

# Examples for each method of the MongoDataWrapper class

# 1. get()
print(alice_skills.get())  # Output: ['Python', 'Django', 'JavaScript']

# 2. inArray()
print(alice_skills.inArray("Python"))  # Output: True

# 3. push()
alice_skills.push("React", "Java", maximum=5)
print(alice_skills.get())  # Output: ['Python', 'Django', 'JavaScript', 'React', 'Java']

# 4. addToSet()
alice_skills.addToSet("C++")
print(alice_skills.get())  # Output: ['Python', 'Django', 'JavaScript', 'React', 'Java', 'C++']

# 5. pop()
alice_skills.pop(direction=-1)
print(alice_skills.get())  # Output: ['Python', 'Django', 'JavaScript', 'React', 'Java']

# 6. pull()
alice_skills.pull("Java")
print(alice_skills.get())  # Output: ['Python', 'Django', 'JavaScript', 'React']

# 7. pullAll()
alice_skills.pullAll("Python", "React")
print(alice_skills.get())  # Output: ['Django', 'JavaScript']

# 8. size()
print(alice_skills.size(2))  # Output: True

# 9. elemMatch()
print(alice_projects.elemMatch(title="Project A", status="completed"))  # Output: True

# 10. all()
print(alice_skills.all("Django", "JavaScript"))  # Output: True

# 11. update()
alice_projects.update("title", "Project A", status="archived")
print(alice_projects.get())  # Output: [{'title': 'Project A', 'status': 'archived'}, {'title': 'Project B', 'status': 'in progress'}]

# 12. __len__()
print(len(alice_skills))  # Output: 2

# 13. __str__() and __repr__()
print(alice_skills)  # Output: ['Django', 'JavaScript']
print(repr(alice_skills))  # Output: ['Django', 'JavaScript']
```

## More MongoDictWrapper examples

```
>>> e = Employee(4051)
>>> e
{'_id': ObjectId('640311ab0469a9c4eaf3d2bd'), 'id': 4051, 'name': 'Manoj', 'email': 'manoj123@gmail.com', 'password': 'different password', 'about': None, 'token': '7f471974-ae46-4ac0-a882-1980c300c4d6', 'country': None, 'location': None, 'lng': 0, 'lat': 0, 'dob': None, 'gender': 0, 'userType': 1, 'userStatus': 1, 'profilePicture': 'Images/9b291404-bc2e-4806-88c5-08d29e65a5ad.png', 'coverPicture': 'Images/44af97d9-b8c9-4ec1-a099-010671db25b7.png', 'enablefollowme': False, 'sendmenotifications': False, 'sendTextmessages': False, 'enabletagging': False, 'createdAt': '2020-01-01T11:13:27.1107739', 'updatedAt': '2020-01-02T09:16:49.284864', 'livelng': 77.389849, 'livelat': 28.6282231, 'liveLocation': 'Unnamed Road, Chhijarsi, Sector 63, Noida, Uttar Pradesh 201307, India', 'creditBalance': 127, 'myCash': 0, 'data': [4, 3, 4, 5, 7], 'arr': {'name': 'shiro', 'pass': 'hello', 'score': {'subject': {'minor': 'physics', 'major': 'science'}, 'score': 95}}, 'scores': [{'subject': 'math', 'score': 95}, {'subject': 'physics', 'score': 85}, {'subject': 'chemistry', 'score': 95}], 'recent_views': [4, 4, 4, 4, 4, 4, 4, 4, 4], 'fix': 1, 'hello': 1}
>>> e.arr
{'name': 'shiro', 'pass': 'hello', 'score': {'subject': {'minor': 'physics', 'major': 'science'}, 'score': 95}}
>>> e.arr['name'] = 'sibidharan' # MongoDataWrapper is also Subscriptable
>>> e.arr
{'name': 'sibidharan', 'pass': 'hello', 'score': {'subject': {'minor': 'physics', 'major': 'science'}, 'score': 95}}
>>> e.arr.score # Queried from the MongoDB directly
{'subject': {'minor': 'physics', 'major': 'science'}, 'score': 95}
>>> e.arr.score['subject']
{'minor': 'physics', 'major': 'science'}
>>> e.arr.score.subject
{'minor': 'physics', 'major': 'science'}
>>> e.arr.score.subject.minor = 'chemistry'
{'minor': 'physics', 'major': 'science'}
# is same as the following
>>> e.arr.score['subject']['minor'] = 'chemistry' # All change are reflected in MongoDB Document
>>> e.arr
{'name': 'sibidharan', 'pass': 'hello', 'score': {'subject': {'minor': 'chemistry', 'major': 'science'}, 'score': 95}}
>>> del e.arr.score['subject'] # Can delete any key in dictionary
>>> del e.arr # Can delete a key itself from the MongoDB Document
```

# High-level Overview of the code for contributers to better understand the implementation

Any and all contributions are welcome ❤️

1. `MongoDictWrapper`: A wrapper for dictionaries that provides additional methods for interaction with MongoDB documents.

   Methods:
   - `prepare`
   - `__getitem__`
   - `__setitem__`
   - `__delitem__`
   - `get`
   - `pop`
   - `update`
   - `clear`

2. `MongoDataWrapper`: A wrapper class for the data stored in MongoDB documents.

   Methods:
   - `get`
   - `inArray`
   - `push`
   - `addToSet`
   - `pop`
   - `pull`
   - `pullAll`
   - `size`
   - `elemMatch`
   - `all`
   - `update`
   - `__len__`
   - `__str__`
   - `__repr__`
   - `__getattr__`
   - `__getitem__`
   - `__setattr__`
   - `__setitem__`
   - `__delitem__`
   - `__delattr__`

3. `MongoGetterSetter`: A metaclass that provides a way to override the default behavior of `getattr`, `setattr`, `contains`, `str`, `repr`, and `delattr` to work with MongoDB documents.

   Nested class: `PyMongoGetterSetter`
   
   Methods:
   - `__getattr__`
   - `__getitem__`
   - `__setattr__`
   - `__setitem__`
   - `__contains__`
   - `__str__`
   - `__repr__`
   - `__delattr__`
   - `__delitem__`


## Credits

Thanks to GPT-4 for helping me write this documentation. If you find any errors or somethings doesn't work as the documentation says, raise an issue in here https://git.selfmade.ninja/sibidharan/pymongogettersetter