import inspect


class JAnyType:
    name = None

    def __init__(self, name=None):
        self.name = name

    def validate(self, value):
        pass


class JsonMapMetaclass(type):
    def __init__(cls, name, bases, dct):
        super(JsonMapMetaclass, cls).__init__(name, bases, dct)
        cls._members = inspect.getmembers(cls,
                                          predicate=lambda (field): isinstance(field, JAnyType) or (inspect.isclass(field) and issubclass(field, JAnyType)))


class JsonMap:
    __metaclass__ = JsonMapMetaclass
    _members = None

    def __init__(self, _dict=None):
        if _dict:
            self._populate(_dict)
            self._validate()

    def _populate(self, _dict):
        for item in self.__class__._members:
            setattr(self, item[0], _dict.get(item[1].name or item[0], None))

    def _validate(self):
        for item in self.__class__._members:
            item[1].validate.im_func(item[1], getattr(self, item[0]))


class JNumber(JAnyType):
    def validate(self, value):
        if not isinstance(value, (int, long)):
            raise TypeError()


class JString(JAnyType):
    def validate(self, value):
        if not isinstance(value, (str, unicode)):
            raise TypeError()


class JArray(JAnyType):
    def __init__(self, of=JAnyType, *args, **kwargs):
        JAnyType.__init__(self, *args, **kwargs)
        self.of = of

    def validate(self, value):
        if not isinstance(value, list):
            raise TypeError()
        for item in value:
            self.of.validate.im_func(self.of, item)
