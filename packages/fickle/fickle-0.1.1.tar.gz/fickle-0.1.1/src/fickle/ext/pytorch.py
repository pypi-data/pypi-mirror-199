"""
PyTorch seems to store checkpoints in a weird zipfile that contains
a pickle file and a bunch of raw arrays. The pickle makes it a big security
risk to load other people's model weights, and unfortunately a lot of the
ML community uses such unsafe formats.

This is a module implementing loading for a decent subset of the format.
"""

import dataclasses
import warnings
import zipfile
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Tuple

import numpy as np
from marshmallow import fields

from .. import DefaultFirewall, Handler, Unpickler
from .marshmallow import BaseMarshmallowHandler, OrderedSchema, XListAsPyTuple

firewall = DefaultFirewall(unknown=True)


zip_file_var = ContextVar("zip_file")


@contextmanager
def setting(contextvar: ContextVar, value: object):
    token = contextvar.set(value)
    try:
        yield
    finally:
        contextvar.reset(token)


class InvalidDTypeWarning(UserWarning):
    pass


@dataclasses.dataclass
class StoredTensor:
    storage: object
    storage_offset: object
    size: int
    stride: Tuple[int]
    requires_grad: bool
    backward_hooks: object
    array = None

    # do not add "object" to the list below, because then it will try to load
    # python objects using pickle
    ALLOWED_DTYPES = {
        "float16",
        "float32",
        "int8",
        "int16",
        "int32",
        "int64",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
    }

    @property
    def dtype(self):
        dtype = self.storage[1]
        if dtype not in self.ALLOWED_DTYPES:
            warnings.warn(f"not loading dtype {dtype!r}", InvalidDTypeWarning)
            return None

        return np.dtype(dtype).newbyteorder("<")

    @property
    def obj_key(self):
        return self.storage[2]

    def __post_init__(self):
        zf = zip_file_var.get(None)
        if zf is not None:
            self.load_from_zipfile(zf)

        if self.array is None and self.dtype is not None:
            self.array = np.zeros(self.size, self.dtype)

    def load_from_zipfile(self, zipfile):
        with zipfile.open(f"archive/data/{self.obj_key}") as f:
            buf = f.read()
        self.load_from_buffer(buf)

    def load_from_buffer(self, buffer):
        dt = self.dtype
        if dt is None:
            return

        self.array = np.frombuffer(buffer, self.dtype).reshape(self.size)


def check_dtype_is_str(x):
    return type(x[1]) is str


class StoredTensorHandler(BaseMarshmallowHandler):
    AUTOREGISTER_INSTANCE = StoredTensor
    AUTOREGISTER_OBJECT_PATHS = ("torch._utils:_rebuild_tensor_v2",)

    class Schema(OrderedSchema):
        storage = XListAsPyTuple(fields.Raw(), validate=check_dtype_is_str)
        storage_offset = fields.Integer()
        size = XListAsPyTuple(fields.Integer())
        stride = XListAsPyTuple(fields.Integer())
        requires_grad = fields.Boolean()
        backward_hooks = fields.Raw()


class RebuildParameterHandler(BaseMarshmallowHandler):
    AUTOREGISTER_INSTANCE = ...
    AUTOREGISTER_OBJECT_PATHS = ("torch._utils:_rebuild_parameter",)


class HalfStorageHandler(Handler):
    AUTOREGISTER_OBJECT_PATHS = ("torch:HalfStorage",)
    AUTOREGISTER_INSTANCE = "float16"


class FloatStorageHandler(Handler):
    AUTOREGISTER_OBJECT_PATHS = ("torch:FloatStorage",)
    AUTOREGISTER_INSTANCE = "float32"


class LongStorageHandler(Handler):
    AUTOREGISTER_OBJECT_PATHS = ("torch:LongStorage",)
    AUTOREGISTER_INSTANCE = "int64"


class IntStorageHandler(Handler):
    AUTOREGISTER_OBJECT_PATHS = ("torch:IntStorage",)
    AUTOREGISTER_INSTANCE = "int32"


for handler in (
    StoredTensorHandler,
    HalfStorageHandler,
    FloatStorageHandler,
    LongStorageHandler,
    IntStorageHandler,
):
    handler.autoregister(firewall)


class MyUnpickler(Unpickler):
    def persistent_load(self, value):
        return value


def fake_torch_load_zipped(
    fileobj, load_weights=True, firewall=firewall, Unpickler=MyUnpickler
):
    with zipfile.ZipFile(fileobj) as zf, setting(
        zip_file_var, zf if load_weights else None
    ), zf.open("archive/data.pkl") as pf:
        return MyUnpickler(file=pf, firewall=firewall).load()
