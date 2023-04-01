import urllib.parse
import sys
import os
import logging
import importlib.util
import importlib.machinery
import threading
import functools
import time
import numbers
import datetime
import enum
import types
import json
from pathlib import Path
from typing import TypeVar, Type, Union, Tuple, Iterable, Any, Dict, List


url_quote = urllib.parse.quote

# TODO move unrelated stuff out of core-folder


# #### make_storage ##############

class StorageMixin:
    __slots__ = ()

    def __init__(self, **kw):
        dct = {**self.__slots_defaults__, **kw}
        [setattr(self, k, v) for k, v in dct.items()]

    def keys(self) -> List[str]:
        return [*self.__class__.__slots__]

    def update(self, dct: dict):
        [setattr(self, k, v) for k, v in dct.items()]

    def __getitem__(self, k):
        try:
            return getattr(self, k)
        except AttributeError:
            raise KeyError(k)

    def as_dict(self) -> Dict[str, Any]:
        return {k: getattr(self, k) for k in self.__class__.__slots__}

    def items(self) -> Iterable[Tuple[str, Any]]:
        return ((k, getattr(self, k)) for k in self.__class__.__slots__)

    def get_defaults(self):
        return {**self.__slots_defaults__}


T = TypeVar('T')


def make_storage(cls: Type[T]) -> Union[Type[T], Type[StorageMixin]]:
    """
    Example:

    ```python
    @make_slotted
    class Config:
        host = '127.0.0.1'
        port = 8000

    cfg = Config(port=22)
    cfg = Config(foo=22)  # Attribute error

    cfg.host = '1.2.3.4'
    cfg.foo = 0  # Attribute error
    ```

    If some methods required - use mixin:

    ```python
    @make_slotted
    class Config(SomeMixin):
        ...
    ```
    """
    '''
    if cls is None:
        return lambda cls: make_storage(cls, **opt)
    '''

    defaults = {k: v for k, v in cls.__dict__.items() if not k.startswith('__')}

    dct = {
        '__slots__': [*defaults],
        '__slots_defaults__': defaults,
    }

    if cls.__bases__ == (object,):
        bases = (StorageMixin,)
    else:
        if any('__slots__' not in c.__dict__ for c in cls.__bases__):
            raise RuntimeError('Bases should have __slots__ attr.')
        bases = tuple([StorageMixin, *cls.__bases__])

    return type(cls.__name__, bases, dct)


# #### MetaPathRouter ##############

class MetaPathRouter:
    """
    Instances of this class makes alias for a package name,
    in other words instruct the import system to route request
    for a package alias, i.e.:

        MetaPathRouter("pkg", "pkg_alias")
        import pkg_alias.sub

    works as

        import pkg.sub

    author: Paolo Pastori
    """

    def __init__(self, pkg, pkg_alias="apps"):
        assert pkg_alias
        assert pkg
        if pkg != pkg_alias:
            self.pkg_alias = pkg_alias
            self.pkg = pkg
            # register as path finder
            sys.meta_path.append(self)

    def find_spec(self, fullname, path=None, target=None):
        if fullname == self.pkg_alias and path is None:
            spec = importlib.util.find_spec(self.pkg)
            if spec:
                spec.name = fullname
                spec.loader = importlib.machinery.SourceFileLoader(
                    fullname, spec.origin
                )
                return spec


def safely(func, exceptions=(Exception,), log=False, default=None):
    """
    runs the funnction and returns True on success,
    False if one of the exceptions is raised
    """
    try:
        return func()
    except exceptions as err:
        if log:
            # TODO getlogger
            logging.warn(str(err))
        return default() if callable(default) else default


def module2filename(module_name, base_path: Path = None):
    fp = Path(sys.modules[module_name].__file__)
    if base_path:
        fp = fp.relative_to(base_path)
    return str(fp)


########################################################################################
# Implement a O(1) LRU cache and memoize with expiration and monitoring (using linked list)
#########################################################################################


class Node:
    def __init__(self, key=None, value=None, t=None, m=None, prev=None, next=None):
        self.key, self.value, self.t, self.m, self.prev, self.next = (
            key,
            value,
            t,
            m,
            prev,
            next,
        )


class Cache:
    """
    O(1) caching object that remembers the 'size' most recent values
    Example:

        cache = Cache(size=1000)
        h = cache.get(filename, lambda: hash(
            open(filename).read()), 60, lambda: os.path.getmtime())

    (computes and cashes the hash of file filename but only reads the file if mtime changes and
     does not check the mtime more oftern than every 60. caches the 1000 most recent hashes)
    """

    def __init__(self, size=1000):
        self.free = size
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.mapping = {}
        self.lock = threading.Lock()

    def get(self, key, callback, expiration=3600, monitor=None):
        """If key not stored or key has expired and monitor == None or monitor() value has changed, returns value = callback()"""
        node, t0 = self.mapping.get(key), time.time()
        with self.lock:
            if node:
                # if a node was found remove it from storage
                value, t, node.next.prev, node.prev.next = (
                    node.value,
                    node.t,
                    node.prev,
                    node.next,
                )
            else:
                self.free -= 1
        # check if something may invalidate cache
        m = monitor() if monitor else None
        # check if cache expired
        if node and node.t + expiration < t0:
            # if cache should always be invalidated or m changed
            if m is None or node.m != m:
                # ignore the value found
                node = None
        if node is None:
            value, t = callback(), t0
        # add the new node back into storage
        with self.lock:
            new_node = Node(key, value, t, m, prev=self.head, next=self.head.next)
            self.mapping[key] = self.head.next = new_node.next.prev = new_node
            if self.free < 0:
                last_node = self.tail.prev
                self.tail.prev, last_node.prev.next = last_node.prev, self.tail
                del self.mapping[last_node.key]
                self.free += 1
        return value

    def memoize(self, expiration=3600):
        def decorator(func):
            @functools.wraps(func)
            def memoized_func(*args, **kwargs):
                key = "%s:%s:%s:%s" % (func.__module__, func.__name__, args, kwargs)
                return self.get(
                    key,
                    lambda args=args, kwargs=kwargs: func(*args, **kwargs),
                    expiration=expiration,
                )

            return memoized_func

        return decorator


#########################################################################################
# A Better JSON Serializer
#########################################################################################


def objectify(obj):
    """converts the obj(ect) into a json serializable object"""
    if isinstance(obj, numbers.Integral):
        return int(obj)
    elif isinstance(obj, (numbers.Rational, numbers.Real)):
        return float(obj)
    elif isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
        return obj.isoformat().replace("T", " ")
    elif isinstance(obj, (str, dict)):
        return obj
    elif isinstance(obj, enum.Enum):  # Enum class handled specially to address self reference in __dict__
        return dict(name=obj.name, value=obj.value, __class__=obj.__class__.__name__)
    else:
        jsonable_meth = (
            getattr(obj, "as_list", None) or  # noqa
            getattr(obj, "as_dict", None) or  # noqa
            getattr(obj, "xml", None)
        )
        if jsonable_meth:
            return jsonable_meth()
        elif hasattr(obj, "__iter__") or isinstance(obj, types.GeneratorType):
            return list(obj)
        elif hasattr(obj, "__dict__") and hasattr(obj, "__class__"):
            d = dict(obj.__dict__)
            d["__class__"] = obj.__class__.__name__
            return d
    return str(obj)


def dumps(obj, sort_keys=True, indent=2, ensure_ascii=False):
    return json.dumps(obj, default=objectify, sort_keys=sort_keys, indent=indent, ensure_ascii=ensure_ascii)
