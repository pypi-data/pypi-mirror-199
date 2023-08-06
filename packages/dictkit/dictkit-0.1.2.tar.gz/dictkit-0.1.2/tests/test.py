# 3.11
from typing import *
import pandas as pd
pd.set_option('display.min_rows', 150)
pd.set_option('display.max_rows', 0)
from types import *
import typing
import types
import json
# import pandas as pd
from typing import (
    _GenericAlias,
    _SpecialGenericAlias,
    _DeprecatedType,
    _CallableGenericAlias,
    _AnnotatedAlias,
)
from dictkit import UtilDict
import re


# print(x.__parameters__)
import inspect

members = [
    (a,b, 'typing') for a,b in inspect.getmembers(typing)
] + [
    (a,b, 'types') for a,b in inspect.getmembers(types)
]
members = [
    x for x in members if (inspect.isclass(x[1]) or isinstance(x[1], (GenericAlias, _GenericAlias, _SpecialGenericAlias))) and not inspect.ismodule(x[1]) and not isinstance(x[1], _DeprecatedType)
]

members = [
    ('str', str, 'builtin'),
    ('int', int, 'builtin'),
    ('float', float, 'builtin'),
    ('complex', complex, 'builtin'),
    ('list', list, 'builtin'),
    ('tuple', tuple, 'builtin'),
    ('range', range, 'builtin'),
    ('dict', dict, 'builtin'),
    ('set', set, 'builtin'),
    ('frozenset', frozenset, 'builtin'),
    ('bool', bool, 'builtin'),
    ('bytes', bytes, 'builtin'),
    ('bytearray', bytearray, 'builtin'),
    ('memoryview', memoryview, 'builtin'),
    ('NoneType', NoneType, 'builtin'),
    ('None', None, 'builtin'),
] + members

members = UtilDict(**{
    name: UtilDict(
        cls=cls,
        cls_name=str(cls).replace("<class '", "").replace("'>", ""),
        type=type(cls),
        origin=get_origin(cls),
        has_args=hasattr(cls, '__args__'),
        cls_is_type=isinstance(cls, type),
        kind=kind,
    )
    for name, cls, kind in members
})

init_args = dict(
    int=[1],
    str=['x'],
    list=[['a','b']],
    tuple=[('a','b')],
    dict=[{'a':5}],
    no_args=[],
)
init_kwargs = dict(
    one_str={'a':'a'}
)

def x():
    pass

# a = MappingProxyType[str]
# print(isinstance(Self, GenericAlias))
# x = MappingProxyType({})
# print(a.__args__)
# print(get_origin(a))

# print(isinstance(x, MappingProxyType[str]))
# print(int(*[]))
# quit()

def try_typehint_one_arg(tp, return_valid = False, type_of_hinted=False) -> bool:
    types = [{}, [], 'a', 5, dict, int]
    for t in types:
        try:
            x = tp[int | str]
            if return_valid:
                return t.__name__ if isinstance(t, type) else str(t)
            if type_of_hinted:
                return str(type(x))
            return True
        except Exception as e:
            pass
    return False

def try_typehint_two_args(tp, return_valid = False, type_of_hinted=False) -> bool:
    types = [{}, [], 'a', 5, dict, int]
    for t1 in types:
        for t2 in types:
            try:
                x = tp[t1, t2]
                if return_valid:
                    return (
                        (t1.__name__ if isinstance(t1, type) else str(t1))
                        + (t2.__name__ if isinstance(t2, type) else str(t2))
                    )
                if type_of_hinted:
                    return str(type(x))
                return True
            except Exception as e:
                pass
    return False

def try_typehint_three_args(tp, return_valid = False, type_of_hinted=False) -> bool:
    types = [{}, [], 'a', 5, dict, int]
    for t1 in types:
        for t2 in types:
            for t3 in types:
                try:
                    x = tp[t1, t2, t3]
                    if return_valid:
                        return (
                            (t1.__name__ if isinstance(t1, type) else str(t1))
                            + (t2.__name__ if isinstance(t2, type) else str(t2))
                            + (t3.__name__ if isinstance(t3, type) else str(t3))
                        )
                    if type_of_hinted:
                        return str(type(x))
                    return True
                except Exception as e:
                    pass
    return False

for k,v in members.items():
    v['th_1_type'] = try_typehint_one_arg(v['cls'], type_of_hinted=True)
    v['th_2_type'] = try_typehint_two_args(v['cls'], type_of_hinted=True)
    v['th_3_type'] = try_typehint_three_args(v['cls'], type_of_hinted=True)


members_str = {
    k: dict(v)
    for k,v in members.items()
}
df = pd.DataFrame(members_str.values(), index=members_str.keys())
df = df.sort_values(['cls_is_type','kind','th_1_type','th_2_type', 'th_3_type'])
# df = df.drop(columns=['origin', 'type', 'cls_name',])

print("No args")
print(df[(df.th_1_type == False) & (df.th_2_type == False) & (df.th_3_type == False)])
quit()
print("One only")
print(df[(df.th_1_type != False) & (df.th_2_type == False) & (df.th_3_type == False)])
print("Two only")
print(df[(df.th_1_type == False) & (df.th_2_type != False) & (df.th_3_type == False)])
print("Three only")
print(df[(df.th_1_type == False) & (df.th_2_type == False) & (df.th_3_type != False)])
print("Any amount")
print(df[(df.th_1_type != False) & (df.th_2_type != False) & (df.th_3_type != False)])
quit()
print(df[df.th_1_arg == True])
print()
print(df[df.th_2_arg == True])
print()
print(df[(df.th_2_arg == True) & (df.th_1_arg == True)])
print()
print(df[(df.th_2_arg == False) & (df.th_1_arg == False)])
quit()

T = TypeVar("T", bound=int)

arg = AbstractSet[UtilDict[str | T, Callable[[Iterable[UtilDict[..., str]]], int]]]

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
CLS_NAME_OUTER = "__"


def make_typed_cls_name(s) -> str:
    def strip_module_paths(s) -> str:
        if isinstance(s, type):
            s = s.__name__
        return re.sub(r"([A-Za-z0-9_\.]+)\.([A-Za-z0-9_]+)([^A-Za-z0-9_])", r"\2\3", str(s))

    s = CLS_NAME_OUTER + strip_module_paths(s) + CLS_NAME_OUTER
    s = s.replace(" ", "").replace("'", '"')
    for k,v in CLS_NAME_CHAR_MAP.items():
        s = s.replace(k, CLS_NAME_CHAR_DELIM + v + CLS_NAME_CHAR_DELIM)

    assert re.fullmatch(r"^[A-Za-z0-9_]+$", s), f"Can't make valid class name for " + s
    return s

def can_make_valid_cls_name(s):
    ...

def cls_name_to_type_hint(s: str) -> str:
    for k,v in CLS_NAME_CHAR_MAP.items():
        s = s.replace(CLS_NAME_CHAR_DELIM + v + CLS_NAME_CHAR_DELIM, k)

    s = s.replace(",", ", ")
    s = s.replace("|", " | ")
    s = s.removeprefix(CLS_NAME_OUTER)
    s = s.removesuffix(CLS_NAME_OUTER)
    return s


# x = get_cls_name(arg)
# print(TypeVar("X"))

# if re.fullmatch(r"", x):
    # print('yes')

# a = Tuple[int, *List[str]]
# b = Tuple[int, List[str]]
if re.search(r"\d", "_FHDSL_"):
    print("invalid")

# print(type(a.__args__[1]))




