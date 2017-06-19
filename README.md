# jmap
Python library to map dictionaries, be it a json payload, to a predefined class. With typed attributes for validation. 

## Usage

```python
class UserServicePayload(jmap.JsonMap):
    first_name = jmap.JString(name="firstName")
    last_name = jmap.JString(name="lastName")
    age = jmap.JNumber # works with or without constructor
    interest_tags = jmap.JArray(name="interestTags", of=jmap.JString)

# ...

data = json.loads(request.body)

# or

data = {
    "firstName": "Miguel",
    "lastName": "Leon",
    "age": 29,
    "interestTags": ["studying", "games", "music", "sports"]
}

# ...

user = UserServicePayload(data)
print user.__dict__
```

`user` will be an instance of `UserServicePayload` with the defined attributes.
If types in the data do not match those defined in the class or fields are missing, `TypeError` will be raised.


### TODO:
- Support `optional=True` as argument to allow missing or null fields.
- Support for recursive object types.
- Support for boolean types.
- Additional validators for extensive validation. 
