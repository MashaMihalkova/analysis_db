from datetime import datetime, date


def decorator(name):
    def wrapper(K):
        setattr(K, name, eval(name))
        return K

    return wrapper


def get_dict(self):
    return self.__dict__


def _asdict(self):
    return self.__dict__


def json_datetime_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
