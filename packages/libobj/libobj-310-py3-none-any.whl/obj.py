# This file is placed in the Public Domain.


"a clean namespace"


## imports


import datetime
import json
import os
import pathlib
import sys
import uuid
import _thread


from functools import wraps
from json import JSONDecoder, JSONEncoder


## defines

def __dir__():
    return (
            'Object',
            'items',
            'keys',
            'kind',
            'update',
            'values',
            'ObjectEncoder',
            'load',
            'loads',
            'ObjectDecoder',
            'dump',
            'dumps',
            'read',
            'write'
           )


__all__ = __dir__()


lock = _thread.allocate_lock()


def locked(thislock):

    "locking decorator"

    def lockeddec(func, *args, **kwargs):

        ""

        if args or kwargs:
            locked.noargs = True

        @wraps(func)
        def lockedfunc(*args, **kwargs):
            ""
            thislock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                thislock.release()
            return res

        return lockedfunc

    return lockeddec


## object


class Object:

    "a clean namespace"

    def __init__(self, *args, **kwargs):
        ""
        if args:
            val = args[0]
            if isinstance(val, list):
                update(self, dict(val))
            elif isinstance(val, zip):
                update(self, dict(val))
            elif isinstance(val, dict):
                update(self, val)
            elif isinstance(val, Object):
                update(self, vars(val))
        if kwargs:
            self.__dict__.update(kwargs)

    def __iter__(self):
        ""
        return iter(self.__dict__)

    def __len__(self):
        ""
        return len(self.__dict__)

    def __str__(self):
        ""
        return str(self.__dict__)


def ident(obj):
    return os.path.join(
                        kind(obj),
                        str(uuid.uuid4().hex),
                        os.sep.join(str(datetime.datetime.now()).split()),
                       )

def items(obj) -> []:
    "list of (key, value) pairs"
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> []:
    "list of keys"
    return obj.__dict__.keys()


def kind(obj) -> str:
    "object's type"
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def update(obj, data) -> None:
    "update object with data"
    for key, value in items(data):
        setattr(obj, key, value)


def values(obj) -> []:
    "list of values"
    return obj.__dict__.values()


## ENCODER


class ObjectEncoder(JSONEncoder):

    "convert object to string"

    def __init__(self, *args, **kw):
        ""
        JSONEncoder.__init__(self, *args, **kw)

    def default(self, o) -> str:
        "convert object ot string"
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o,
                      (type(str), type(True), type(False),
                       type(int), type(float))
                     ):
            return str(o)
        try:
            return JSONEncoder.default(self, o)
        except TypeError:
            return str(o)

    def encode(self, o) -> str:
        "convert object to string"
        return JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False) -> str:
        "convert object to string"
        return JSONEncoder.iterencode(self, o, _one_shot)


@locked(lock)
def dump(obj, fpt, *args, **kw) -> None:
    "write object to file"
    return json.dump(obj, fpt, *args, cls=ObjectEncoder, **kw)

@locked(lock)
def dumps(*args, **kw) -> str:
    "convert object to string"
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


## DECODER


class ObjectDecoder(JSONDecoder):

    "convert string to object."

    def __init__(self):
        ""
        JSONDecoder.__init__(self)

    def decode(self, s, _w=None) -> Object:
        "decode string into object"
        val = None
        try:
            val = JSONDecoder.decode(self, s)
        except json.decoder.JSONDecodeError as ex:
            print(ex, s)
            sys.exit()
        if not val:
            val = {}
        return Object(val)

    def raw_decode(self, s, idx=0) -> (int, Object):
        "return object with index into jsonstring (upto)"
        return JSONDecoder.raw_decode(self, s, idx)


def load(fpt, *args, **kw) -> Object:
    "load json from disk and convert into object"
    return json.load(fpt, *args, cls=ObjectDecoder, **kw)


def loads(string, *args, **kw) -> Object:
    "convert object from string"
    return json.loads(string, *args, cls=ObjectDecoder, **kw)


## DISK


def read(obj, path):
    with open(path, 'r', encoding='utf-8') as ofile:
        data = load(ofile)
        update(obj, data)


def write(obj, opath=None):
    if not opath:
        opath = os.path.join("store", ident(obj))
    cdir(opath)
    with open(opath, 'w', encoding='utf-8') as ofile:
        dump(obj, ofile)
    return os.path.abspath(opath)


## UTILITY


def cdir(path):
    pth = pathlib.Path(path)
    if path.split('/')[-1].count(':') == 2:
        pth = pth.parent
    os.makedirs(pth, exist_ok=True)

