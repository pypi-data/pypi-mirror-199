from __future__ import annotations
from typing import Any, TypeVar, Type, get_args, get_origin, Optional, Union, Iterable
import re

# Self's key and value types
K = TypeVar("K")
V = TypeVar("V")
# Incoming key and value types from arguments
K2 = TypeVar("K2")
V2 = TypeVar("V2")

# Non-variable-name-friendly chars in a type hint
CLS_NAME_CHAR_MAP = {
    "[": "0",
    "]": "00",
    "(": "1",
    ")": "11",
    ",": "2",
    "|": "3",
    "...": "4",
    '"': "5",
    "*": "6",
    "~": "7",
}
CLS_NAME_CHAR_DELIM = "_"
CLS_NAME_TYPE_DELIM = "___"


class THDictMeta(type):
    """
    NOTE: Can we make this a singleton?
    """

    def __new__(cls, name, bases, attrs):
        if bases and (bad_bases := [base for base in bases if type(base) is cls]):
            raise TypeError(f"{bad_bases[0]} cannot be subclassed. Sorry!")
        if "_" in name.lstrip("_"):
            raise ValueError(
                f"Class name, '{name}' can only contain underscores at the beginning"
            )
        return super().__new__(cls, name, bases, attrs)

    def __getitem__(cls, item: tuple[Type[K], Type[V]]) -> Type:
        """
        Types assigned to instances can be any type variable, and the created class
        will be unique
        """
        if not isinstance(item, tuple) or len(item) != 2:
            raise TypeError("Expecting a tuple of length 2 with key and value types")
        key_type, value_type = item

        key_type_name = cls.make_typed_cls_name(key_type)
        value_type_name = cls.make_typed_cls_name(value_type)

        new_cls_name = CLS_NAME_TYPE_DELIM.join(
            [
                cls.__name__,
                key_type_name,
                value_type_name,
            ]
        )

        # Don't re-construct an existing identical class
        if issubclass((existing := globals().get(new_cls_name, type)), cls):
            return existing

        new_class = type(new_cls_name, (cls,), {})  # type:ignore
        setattr(new_class, '_is_typed', True)
        globals()[new_cls_name] = new_class

        setattr(new_class, "key_type", key_type)
        setattr(new_class, "value_type", value_type)
        return new_class

    @staticmethod
    def make_typed_cls_name(tp: Type) -> str:
        def strip_module_paths(tp) -> str:
            if isinstance(tp, type):
                tp = tp.__name__
            return re.sub(
                r"([A-Za-z0-9_\.]+)\.([A-Za-z0-9_]+)([^A-Za-z0-9_])", r"\2\3", str(tp)
            )

        tp = strip_module_paths(tp)
        tp = tp.replace(" ", "").replace("'", '"')
        for k, v in CLS_NAME_CHAR_MAP.items():
            tp = tp.replace(k, CLS_NAME_CHAR_DELIM + v + CLS_NAME_CHAR_DELIM)

        assert re.fullmatch(r"^[A-Za-z0-9_]+$", tp), (
            f"Can't make valid class name for " + tp
        )
        return tp

    def type_hint(cls) -> str:
        s = cls.__name__
        for k, v in CLS_NAME_CHAR_MAP.items():
            s = s.replace(CLS_NAME_CHAR_DELIM + v + CLS_NAME_CHAR_DELIM, k)

        s = s.replace(",", ", ")
        s = s.replace("|", " | ")
        return s


class THDict(dict[K, V], metaclass=THDictMeta):
    """
    A statically-typed dictionary.

    The syntax used in type hints, `arg: THDict[str, str]`, can also be used
    to create a new instance with the specified types:

    Create a dict that must have string keys and int values
    >>> THDict[str, int](key1=5, key2=6)
    {'key1': 5, 'key2': 6}

    Pass invalid type
    >>> THDict[str, int](key1="5")
    Traceback (most recent call last):
        ...
    TypeError: Value must be of type <class 'int'>, got '<class 'str'>'

    """

    key_type = Any
    value_type = Any
    _is_typed: bool

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._validate_items()

    def __setitem__(self, key: K, val: V) -> None:
        self._validate_key_val_types(key, val)
        super().__setitem__(key, val)

    def _validate_items(self) -> None:
        for key, val in self.items():
            self._validate_key_val_types(key, val)

    def _validate_key_val_types(self, key, val) -> None:
        if not self._check_instance(key, self.key_type):
            raise TypeError(f"Key must be of type {self.key_type}, got '{type(key)}'")
        if not self._check_instance(val, self.value_type):
            # print("-----")
            # print(val)
            # print(f" '{type(val)}'")
            # print("-----")
            raise TypeError(
                f"Value must be of type {self.value_type}, got '{type(val)}'"
            )

    @staticmethod
    def _check_instance(obj: Any, tp: Type) -> bool:
        if hasattr(tp, "__args__"):
            args = get_args(tp)
            if len(args) > 0:
                origin = get_origin(tp)
                # print(f"{obj=}")  # obj=5
                # print(f"{tp=}")  # tp=int | str
                # print(f"{args=}")  # args=(<class 'int'>, <class 'str'>)
                # print(f"{origin=}")  # origin=<class 'types.UnionType'>

                # Handle unions
                if origin is Union:
                    res = any(THDict._check_instance(obj, arg) for arg in args)
                    # print("obj not instance of any arg", res)
                    return res

                # Handle generic types with parameters
                if origin is not None and origin not in (Union, Optional):
                    res = isinstance(obj, origin) and all(
                        THDict._check_instance(inner_obj, arg)
                        for inner_obj in obj
                        for arg in args
                    )
                    # print(
                    #     "isinstance obj origin and all instances in inner obj, returning",
                    #     res,
                    # )
                    return res

        return isinstance(obj, tp)
