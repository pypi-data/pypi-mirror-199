import dataclasses
import importlib
import io
import sys
from collections import defaultdict
import collections

from .util import IdMap
from .exc import FirewallError, UnpickleTypeError, UnpickleError


@dataclasses.dataclass
class Firewall:
    """
    The firewall determines what calls are allowed and how they should be handled.
    The actual calls are handled by :class:`Handler` objects which need to have
    been registered using :meth:`register`.

    To determine the appropriate handler, the firewall does the following:

    1. The object is checked against instance-registered handlers.
    2. The object type is checked against type-registered handlers.
    3. The object's superclasses are checked against subtype-registered handlers.

    The first one to match wins. If none apply, an error is raised.

    Parameters
    ----------
    unknown: bool
        Register default handlers which produce :class:`Unknown` objects.
    """

    unknown: bool = dataclasses.field(default=False)
    instance_handlers: IdMap = dataclasses.field(default_factory=IdMap, init=False)
    type_handlers: IdMap = dataclasses.field(default_factory=IdMap, init=False)
    subtype_handlers: IdMap = dataclasses.field(default_factory=IdMap, init=False)
    import_handlers: dict = dataclasses.field(
        default_factory=lambda: defaultdict(list), init=False
    )

    def __post_init__(self):
        for h in self.get_autoregister_handlers():
            h.autoregister(self)

    def load(self, file) -> object:
        """
        Load pickled data from ``file``. Return loaded data.

        Convenience method to avoid constructing the Unpickler object explicitly.
        """
        from .unpickler import Unpickler

        return Unpickler(file=file, firewall=self).load()

    def loads(self, s: bytes) -> object:
        """
        Load pickled data from provided bytestring. Return loaded data.
        """
        return self.load(io.BytesIO(s))

    def _assert_identifier(self, s):
        if not s.isidentifier():
            raise UnpickleError(f"bad identifier {s!r}")

    def _object_path_to_tuple(self, path: str, name: str = None):
        if name is None:
            module, sep, name = path.rpartition(":")
        else:
            module = path
            sep = ":"

        key = module.split(".") if module else []

        for s in key:
            self._assert_identifier(s)

        if sep:
            key.append("")
            if name:
                if not key:
                    raise AssertionError("cannot have empty module but nonempty name")
                self._assert_identifier(name)
                key.append(name)

        return tuple(key)

    def get_autoregister_handlers(self):
        if self.unknown:
            return [UnknownHandler, UnknownTypeHandler, UnknownFactoryHandler]
        else:
            return []

    def register(self, handler: "Handler", instance=None, type=None, subtype=None):
        """
        Register a method handler.

        Parameters
        ----------
        instance: object, optional
            If the object is precisely ``instance``, then this handler applies.
        type: object, optional
            If the type (class) of the object is precisely ``type``, then this handler
            applies.
        subtype: object, optional
            If the object's type (class) is a subclass of ``subtype``, then this
            handler applies.
        """
        if type is not None:
            self.type_handlers[type] = handler

        if subtype is not None:
            self.subtype_handlers[subtype] = handler

        if instance is not None:
            self.instance_handlers[instance] = handler

    def register_importer(self, handler: "Handler", path: str):
        """
        Register a handler when a subpath of ``path`` is imported.

        If the pickle file asks for "pkg.subpkg.MyClass", then the following
        paths will be queried:
            - "pkg.subpkg:MyClass"
            - "pkg.subpkg:"
            - "pkg.subpkg"
            - "pkg"
            - ""

        If the handler is registered using one of these tuples, then it will
        be called with the requested module and name ("pkg.subpkg" and
        "MyClass"). If it raises NotImplementedError, then the next handler
        will be called if there is one.
        """
        self.import_handlers[self._object_path_to_tuple(path)].append(handler)

    def get_handler_class(self, instance: object, method: str):
        h = self.instance_handlers.get(instance)
        if h is not None:
            return h

        h = self.type_handlers.get(type(instance))
        if h is not None:
            return h

        for cls in type(instance).mro():
            h = self.subtype_handlers.get(cls)
            if h is not None:
                return h

        raise KeyError(f"cannot find handler for {instance!r}.{method:s}")

    @staticmethod
    def _assert_kwargs(d):
        if type(d) is not dict:
            raise UnpickleTypeError("invalid kwargs - not a dict")

        if not all(type(k) is str for k in d):
            raise UnpickleTypeError("invalid kwargs - keys not strings")

    @staticmethod
    def _assert_args(x):
        t = type(x)
        if t is not list and t is not tuple:
            raise UnpickleTypeError("invalid args - not a tuple or list")

    @staticmethod
    def _assert_nonempty_str(x):
        if type(x) is not str or not x:
            raise UnpickleTypeError("must be nonempty string")

    def call(self, instance, method, args, kwargs={}):
        self._assert_args(args)
        self._assert_kwargs(kwargs)
        handler_class = self.get_handler_class(instance, method)
        try:
            handler = handler_class(instance)
            return getattr(handler, method)(*args, **kwargs)
        except Exception as exc:
            raise FirewallError(
                f"handler {handler!r} failed to handle {method:s} with "
                f"args={args!r} and kwargs={kwargs!r}"
            ) from exc

    def import_object(self, module: str, name: str) -> object:
        self._assert_nonempty_str(module)
        self._assert_nonempty_str(name)

        # "pkg.subpkg.MyClass" becomes ("pkg", "subpkg", "", "MyClass")
        importers = self.import_handlers
        path = self._object_path_to_tuple(module, name)

        # look up, in this order:
        # - ("pkg", "subpkg", "", "MyClass")
        # - ("pkg", "subpkg", "")
        # - ("pkg", "subpkg")
        # - ("pkg",)
        # - ()
        for i in range(len(path), -1, -1):
            subpath = path[:i]
            for handler in reversed(importers.get(subpath, ())):
                try:
                    return handler(module, name)
                except NotImplementedError:
                    pass

        module_and_name = f"{module}:{name}"
        raise FirewallError(f"access denied to {module_and_name!r}")


@dataclasses.dataclass
class Handler:
    """
    Unpickle method call handler for an object instance.

    Parameters
    ----------
    instance: object
        The object for which calls are being handled. This object is provided by the
        :class:`Firewall` object.

    Attributes
    ----------
    AUTOREGISTER_INSTANCE: object, optional
        See :meth:`Firewall.register`.
    AUTOREGISTER_TYPE: object, optional
        See :meth:`Firewall.register`.
    AUTOREGISTER_SUBTYPE: object, optional
        See :meth:`Firewall.register`.

    """

    instance: object = dataclasses.field()

    AUTOREGISTER_INSTANCE = None
    AUTOREGISTER_TYPE = None
    AUTOREGISTER_SUBTYPE = None
    AUTOREGISTER_OBJECT_PATHS = ()

    @classmethod
    def autoregister_import_object(cls, module, name):
        return cls.AUTOREGISTER_INSTANCE

    @classmethod
    def autoregister(cls, firewall: "Firewall"):
        """
        Automatically register this handler class for instance
        :attr:`AUTOREGISTER_INSTANCE`, for class :attr:`AUTOREGISTER_TYPE`, and for
        superclasses of :attr:`AUTOREGISTER_SUBTYPE`.

        Also register this handler to be consulted when importing from import paths
        given in :attr:`AUTOREGISTER_OBJECT_PATHS`.
        """
        firewall.register(
            cls,
            instance=cls.AUTOREGISTER_INSTANCE,
            type=cls.AUTOREGISTER_TYPE,
            subtype=cls.AUTOREGISTER_SUBTYPE,
        )

        for path in cls.AUTOREGISTER_OBJECT_PATHS:
            firewall.register_importer(cls.autoregister_import_object, path)

    def call_new(self, *args, **kwargs):
        """
        Called by NEWOBJ and NEWOBJ_EX opcodes.
        """
        raise NotImplementedError

    def call_unreduce(self, *args):
        """
        Called by REDUCE opcode.
        """
        raise NotImplementedError

    def call_setstate(self, state):
        """
        Called by BUILD opcode when :attr:`instance` has a ``__setstate__`` method.
        """
        raise NotImplementedError

    def call_setstate_from_dict(self, state: dict, slotstate: dict):
        """
        Called by BUILD opcode when :attr:`instance` does not have a ``__setstate__``
        method.
        """
        raise NotImplementedError

    def call_append(self, item):
        """
        Called by APPEND opcode to append to a list.
        """
        raise NotImplementedError

    def call_extend(self, sequence):
        """
        Called by EXTEND opcode to append to a list.
        """
        raise NotImplementedError

    def call_setitem(self, key, value):
        """
        Called by SETITEM and SETITEMS opcode to add to a dict.
        """
        raise NotImplementedError

    def call_additems(self, sequence):
        """
        Called by ADDITEMS opcode to add to a set.
        """
        raise NotImplementedError

    def default_new(self, *args, **kwargs):
        return self.instance.__new__(*args, **kwargs)

    def default_unreduce(self, *args, **kwargs):
        return self.instance(*args, **kwargs)

    def default_setstate(self, state):
        return self.instance.__setstate__(state)

    def default_setstate_from_dict(self, state: dict, slotstate: dict):
        inst = self.instance
        inst_dict = inst.__dict__
        intern = sys.intern
        for k, v in state.items():
            if type(k) is str:
                k = intern(k)
            inst_dict[k] = v

        for k, v in slotstate.items():
            setattr(inst, k, v)

    def default_append(self, item):
        self.instance.append(item)

    def default_extend(self, sequence):
        self.instance.extend(sequence)

    def default_setitem(self, key, value):
        self.instance[key] = value

    def default_additems(self, sequence):
        self.instance.update(sequence)


class ListHandler(Handler):
    AUTOREGISTER_TYPE = list

    def call_append(self, item):
        self.default_append(item)

    def call_extend(self, sequence):
        self.default_extend(sequence)


class DictHandler(Handler):
    AUTOREGISTER_TYPE = dict

    def call_setitem(self, key, value):
        self.default_setitem(key, value)


class SetHandler(Handler):
    AUTOREGISTER_TYPE = set

    def call_additems(self, sequence):
        self.default_update(sequence)


class OrderedDictHandler(Handler):
    AUTOREGISTER_INSTANCE = collections.OrderedDict
    AUTOREGISTER_OBJECT_PATHS = ("collections:OrderedDict",)

    def call_unreduce(self):
        # TODO: support initializing from a sequence or mapping
        return self.default_unreduce()


@dataclasses.dataclass
class Unknown:
    """
    This class represents an object of unrecognized type.
    """

    type: str
    args: list = dataclasses.field(default_factory=list)
    kwargs: dict = dataclasses.field(default_factory=dict)
    state: object = None

    def __setstate__(self, state):
        self.state = state

    def __repr__(self):
        lst = [repr(x) for x in self.args or ()]
        if self.kwargs:
            lst.extend(f"{k}={v!r}" for k, v in self.kwargs.items())
        args = ", ".join(lst)
        if self.state is not None:
            lst.append(f"__state__={self.state!r}")
        return f"{self.type}({args})"


@dataclasses.dataclass(eq=False)
class UnknownFactory:
    """
    This represents an imported name that is unrecognized.
    """

    type: str

    def __call__(self, args, kwargs):
        return Unknown(type=self.type, args=args, kwargs=kwargs)


class UnknownFactoryHandler(Handler):
    AUTOREGISTER_TYPE = UnknownFactory

    def call_unreduce(self, *args, **kwargs):
        obj = self.instance(args, kwargs)
        return obj


class UnknownHandler(Handler):
    AUTOREGISTER_OBJECT_PATHS = ("",)
    AUTOREGISTER_INSTANCE = Unknown

    @classmethod
    def autoregister_import_object(cls, module, name):
        return UnknownFactory(f"{module}.{name}")


class UnknownTypeHandler(Handler):
    AUTOREGISTER_TYPE = Unknown

    def call_setstate(self, state):
        self.instance.state = state


class CodecsEncodeHandler(Handler):
    AUTOREGISTER_OBJECT_PATHS = ("_codecs:encode",)
    AUTOREGISTER_INSTANCE = object()
    ALLOWED_CODECS = {"latin1"}

    def call_unreduce(self, string, codec):
        if type(string) is not str:
            raise TypeError
        if type(codec) is not str:
            raise TypeError
        if codec not in self.ALLOWED_CODECS:
            raise AssertionError(f"bad codec {codec}")

        return string.encode(codec)


class DefaultFirewall(Firewall):
    def get_autoregister_handlers(self):
        lst = super().get_autoregister_handlers()
        lst.extend(
            (
                ListHandler,
                DictHandler,
                SetHandler,
                OrderedDictHandler,
                CodecsEncodeHandler,
            )
        )
        return lst
