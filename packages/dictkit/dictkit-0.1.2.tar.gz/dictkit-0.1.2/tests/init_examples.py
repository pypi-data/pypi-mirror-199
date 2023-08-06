from typing import *
from types import *
import typing
import types
import collections
import abc

from typing import (
    _GenericAlias,
    _SpecialGenericAlias,
    _CallableGenericAlias,
    _DeprecatedType,
    _AnnotatedAlias,
)

from types import (
    _GeneratorWrapper,
)

set_no_args = {
    None,
    typing.ByteString,
    typing.Hashable,
    typing.Sized,
    str,
    int,
    float,
    complex,
    range,
    bool,
    bytes,
    bytearray,
    memoryview,
    NoneType,
    Any,
    types.GenericAlias,
    MethodDescriptorType,
    MethodWrapperType,
    WrapperDescriptorType,
    BuiltinFunctionType,
    BuiltinMethodType,
    CellType,
    ClassMethodDescriptorType,
    CodeType,
    CoroutineType,
    types.DynamicClassAttribute,
    EllipsisType,
    FrameType,
    FunctionType,
    GeneratorType,
    GetSetDescriptorType,
    LambdaType,
    MemberDescriptorType,
    MethodType,
    ModuleType,
    NotImplementedType,
    types.SimpleNamespace,
    TracebackType,
    types.UnionType,
    types._GeneratorWrapper, #type:ignore
    abc.ABCMeta,
    typing.BinaryIO,
    typing.ForwardRef,
    typing.Generic,
    typing.NamedTupleMeta, #type:ignore
    typing.NewType,
    typing.ParamSpec,
    typing.ParamSpecArgs,
    typing.ParamSpecKwargs,
    typing.Protocol,
    typing.SupportsBytes,
    typing.SupportsComplex,
    typing.SupportsFloat,
    typing.SupportsIndex,
    typing.SupportsInt,
    str,
    typing.TextIO,
    typing.TypeVar,
    typing.TypeVarTuple,
    typing._AnnotatedAlias,  # type:ignore
    typing._AnyMeta,  # type:ignore
    typing._BaseGenericAlias,  # type:ignore
    typing._BoundVarianceMixin,  # type:ignore
    typing._CallableGenericAlias,  # type:ignore
    typing._CallableType,  # type:ignore
    typing._ConcatenateGenericAlias,  # type:ignore
    typing._DeprecatedType,  # type:ignore
    typing._Final,  # type:ignore
    typing._GenericAlias,  # type:ignore
    typing._Immutable,  # type:ignore
    typing._LiteralGenericAlias,  # type:ignore
    typing._LiteralSpecialForm,  # type:ignore
    typing.NamedTuple,
    typing._NotIterable,  # type:ignore
    typing._PickleUsingNameMixin,  # type:ignore
    typing._ProtocolMeta,  # type:ignore
    typing._SpecialForm,  # type:ignore
    typing._SpecialGenericAlias,  # type:ignore
    typing._TupleType,  # type:ignore
    typing.TypedDict,
    typing._TypedDictMeta,  # type:ignore
    typing._TypingEllipsis,  # type:ignore
    typing._UnionGenericAlias,  # type:ignore
    typing._UnpackGenericAlias,  # type:ignore
    typing._SpecialGenericAlias,  # type:ignore
}

set_one_arg = {
    typing.AbstractSet,
    typing.AsyncContextManager,
    typing.AsyncIterable,
    typing.AsyncIterator,
    typing.Awaitable,
    typing.Collection,
    typing.Container,
    typing.ContextManager,
    typing.Counter,
    typing.Deque,
    typing.FrozenSet,
    typing.Iterable,
    typing.Iterator,
    typing.KeysView,
    typing.List,
    typing.MappingView,
    typing.Match,
    typing.MutableSequence,
    typing.MutableSet,
    typing.Pattern,
    typing.Reversible,
    typing.Sequence,
    typing.Set,
    typing.Type,
    typing.ValuesView,
    typing.IO,
    typing.SupportsAbs,
    typing.SupportsRound,
}

set_two_args = {
    typing.Callable,
    typing.AsyncGenerator,
    typing.ChainMap,
    typing.DefaultDict,
    typing.Dict,
    typing.ItemsView,
    typing.Mapping,
    typing.MutableMapping,
    typing.OrderedDict,
}

set_three_args = {
    typing.Coroutine,
    typing.Generator,
}

set_any_num_args = {
    typing.Tuple,
    list,
    tuple,
    dict,
    set,
    frozenset,
    AsyncGeneratorType,
    MappingProxyType,
    collections.defaultdict,
}

TypeInfo = collections.namedtuple("TypeInfo", ["cls", "param_cls", "type", "origin"])

one_arg = {
    'AbstractSet': (typing.AbstractSet, typing._GenericAlias),  # type:ignore
    'AsyncContextManager': (typing.AsyncContextManager, typing._GenericAlias),  # type:ignore
    'AsyncIterable': (typing.AsyncIterable, typing._GenericAlias),  # type:ignore
    'AsyncIterator': (typing.AsyncIterator, typing._GenericAlias),  # type:ignore
    'Awaitable': (typing.Awaitable, typing._GenericAlias),  # type:ignore
    'Collection': (typing.Collection, typing._GenericAlias),  # type:ignore
    'Container': (typing.Container, typing._GenericAlias),  # type:ignore
    'ContextManager': (typing.ContextManager, typing._GenericAlias),  # type:ignore
    'Counter': (typing.Counter, typing._GenericAlias),  # type:ignore
    'Deque': (typing.Deque, typing._GenericAlias),  # type:ignore
    'FrozenSet': (typing.FrozenSet, typing._GenericAlias),  # type:ignore
    'Iterable': (typing.Iterable, typing._GenericAlias),  # type:ignore
    'Iterator': (typing.Iterator, typing._GenericAlias),  # type:ignore
    'KeysView': (typing.KeysView, typing._GenericAlias),  # type:ignore
    'List': (typing.List, typing._GenericAlias),  # type:ignore
    'MappingView': (typing.MappingView, typing._GenericAlias),  # type:ignore
    'Match': (typing.Match, typing._GenericAlias),  # type:ignore
    'MutableSequence': (typing.MutableSequence, typing._GenericAlias),  # type:ignore
    'MutableSet': (typing.MutableSet, typing._GenericAlias),  # type:ignore
    'Pattern': (typing.Pattern, typing._GenericAlias),  # type:ignore
    'Reversible': (typing.Reversible, typing._GenericAlias),  # type:ignore
    'Sequence': (typing.Sequence, typing._GenericAlias),  # type:ignore
    'Set': (typing.Set, typing._GenericAlias),  # type:ignore
    'Type': (typing.Type, typing._GenericAlias),  # type:ignore
    'ValuesView': (typing.ValuesView, typing._GenericAlias),  # type:ignore
    'IO': (typing.IO, typing._GenericAlias),  # type:ignore
    'SupportsAbs': (typing.SupportsAbs, typing._GenericAlias),  # type:ignore
    'SupportsRound': (typing.SupportsRound, typing._GenericAlias),  # type:ignore
}

two_args = {
    'Callable': (typing.Callable, typing._CallableGenericAlias), # type:ignore
    'AsyncGenerator': (typing.AsyncGenerator, typing._GenericAlias), # type:ignore
    'ChainMap': (typing.ChainMap, typing._GenericAlias), # type:ignore
    'DefaultDict': (typing.DefaultDict, typing._GenericAlias), # type:ignore
    'Dict': (typing.Dict, typing._GenericAlias), # type:ignore
    'ItemsView': (typing.ItemsView, typing._GenericAlias), # type:ignore
    'Mapping': (typing.Mapping, typing._GenericAlias), # type:ignore
    'MutableMapping': (typing.MutableMapping, typing._GenericAlias), # type:ignore
    'OrderedDict': (typing.OrderedDict, typing._GenericAlias), # type:ignore
}

three_args = {
    'Coroutine': (typing.Coroutine, typing._GenericAlias), # type:ignore
    'Generator': (typing.Generator, typing._GenericAlias), # type:ignore
}

any_num_args = {
    'Tuple': (typing.Tuple, typing._GenericAlias), # type:ignore
    'list': (list, types.GenericAlias),
    'tuple': (tuple, types.GenericAlias),
    'dict': (dict, types.GenericAlias),
    'set': (set, types.GenericAlias),
    'frozenset': (frozenset, types.GenericAlias),
    'AsyncGeneratorType': (AsyncGeneratorType, types.GenericAlias),
    'MappingProxyType': (MappingProxyType, types.GenericAlias),
    'defaultdict': (collections.defaultdict, types.GenericAlias),
}

# one_arg_origins = {
#     collections.abc.Set,
#     contextlib.AbstractAsyncContextManager,
#     collections.abc.AsyncIterable,
#     collections.abc.AsyncIterator,
#     collections.abc.Awaitable,
#     collections.abc.Collection,
#     collections.abc.Container,
#     contextlib.AbstractContextManager,
#     collections.Counter,
#     collections.deque,
#     frozenset,
#     collections.abc.Iterable,
#     collections.abc.Iterator,
#     collections.abc.KeysView,
#     list,
#     collections.abc.MappingView,
#     re.Match,
#     collections.abc.MutableSequence,
#     collections.abc.MutableSet,
#     re.Pattern,
#     collections.abc.Reversible,
#     collections.abc.Sequence,
#     set,
#     type,
#     collections.abc.ValuesView,
#     None,
#     None,
#     None,
# }
#
# two_arg_origins = {
#     collections.abc.Callable,
#     collections.abc.AsyncGenerator,
#     collections.ChainMap,
#     collections.defaultdict,
#     dict,
#     collections.abc.ItemsView,
#     collections.abc.Mapping,
#     collections.abc.MutableMapping,
#     collections.OrderedDict,
# }
#
# three_arg_origins = {
#     collections.abc.Coroutine,
#     collections.abc.Generator,
# }
#
# any_arg_origins = {
#     tuple,
# }

"""
ONE ARG ONLY
                                                cls                    cls_name                                   type                                            origin  has_args  cls_is_type    kind                       th_1_type
AbstractSet                      typing.AbstractSet          typing.AbstractSet  <class 'typing._SpecialGenericAlias'>                     <class 'collections.abc.Set'>     False        False  typing  <class 'typing._GenericAlias'>
AsyncContextManager      typing.AsyncContextManager  typing.AsyncContextManager  <class 'typing._SpecialGenericAlias'>  <class 'contextlib.AbstractAsyncContextManager'>     False        False  typing  <class 'typing._GenericAlias'>
AsyncIterable                  typing.AsyncIterable        typing.AsyncIterable  <class 'typing._SpecialGenericAlias'>           <class 'collections.abc.AsyncIterable'>     False        False  typing  <class 'typing._GenericAlias'>
AsyncIterator                  typing.AsyncIterator        typing.AsyncIterator  <class 'typing._SpecialGenericAlias'>           <class 'collections.abc.AsyncIterator'>     False        False  typing  <class 'typing._GenericAlias'>
Awaitable                          typing.Awaitable            typing.Awaitable  <class 'typing._SpecialGenericAlias'>               <class 'collections.abc.Awaitable'>     False        False  typing  <class 'typing._GenericAlias'>
Collection                        typing.Collection           typing.Collection  <class 'typing._SpecialGenericAlias'>              <class 'collections.abc.Collection'>     False        False  typing  <class 'typing._GenericAlias'>
Container                          typing.Container            typing.Container  <class 'typing._SpecialGenericAlias'>               <class 'collections.abc.Container'>     False        False  typing  <class 'typing._GenericAlias'>
ContextManager                typing.ContextManager       typing.ContextManager  <class 'typing._SpecialGenericAlias'>       <class 'contextlib.AbstractContextManager'>     False        False  typing  <class 'typing._GenericAlias'>
Counter                              typing.Counter              typing.Counter  <class 'typing._SpecialGenericAlias'>                     <class 'collections.Counter'>     False        False  typing  <class 'typing._GenericAlias'>
Deque                                  typing.Deque                typing.Deque  <class 'typing._SpecialGenericAlias'>                       <class 'collections.deque'>     False        False  typing  <class 'typing._GenericAlias'>
FrozenSet                          typing.FrozenSet            typing.FrozenSet  <class 'typing._SpecialGenericAlias'>                               <class 'frozenset'>     False        False  typing  <class 'typing._GenericAlias'>
Iterable                            typing.Iterable             typing.Iterable  <class 'typing._SpecialGenericAlias'>                <class 'collections.abc.Iterable'>     False        False  typing  <class 'typing._GenericAlias'>
Iterator                            typing.Iterator             typing.Iterator  <class 'typing._SpecialGenericAlias'>                <class 'collections.abc.Iterator'>     False        False  typing  <class 'typing._GenericAlias'>
KeysView                            typing.KeysView             typing.KeysView  <class 'typing._SpecialGenericAlias'>                <class 'collections.abc.KeysView'>     False        False  typing  <class 'typing._GenericAlias'>
List                                    typing.List                 typing.List  <class 'typing._SpecialGenericAlias'>                                    <class 'list'>     False        False  typing  <class 'typing._GenericAlias'>
MappingView                      typing.MappingView          typing.MappingView  <class 'typing._SpecialGenericAlias'>             <class 'collections.abc.MappingView'>     False        False  typing  <class 'typing._GenericAlias'>
Match                                  typing.Match                typing.Match  <class 'typing._SpecialGenericAlias'>                                <class 're.Match'>     False        False  typing  <class 'typing._GenericAlias'>
MutableSequence              typing.MutableSequence      typing.MutableSequence  <class 'typing._SpecialGenericAlias'>         <class 'collections.abc.MutableSequence'>     False        False  typing  <class 'typing._GenericAlias'>
MutableSet                        typing.MutableSet           typing.MutableSet  <class 'typing._SpecialGenericAlias'>              <class 'collections.abc.MutableSet'>     False        False  typing  <class 'typing._GenericAlias'>
Pattern                              typing.Pattern              typing.Pattern  <class 'typing._SpecialGenericAlias'>                              <class 're.Pattern'>     False        False  typing  <class 'typing._GenericAlias'>
Reversible                        typing.Reversible           typing.Reversible  <class 'typing._SpecialGenericAlias'>              <class 'collections.abc.Reversible'>     False        False  typing  <class 'typing._GenericAlias'>
Sequence                            typing.Sequence             typing.Sequence  <class 'typing._SpecialGenericAlias'>                <class 'collections.abc.Sequence'>     False        False  typing  <class 'typing._GenericAlias'>
Set                                      typing.Set                  typing.Set  <class 'typing._SpecialGenericAlias'>                                     <class 'set'>     False        False  typing  <class 'typing._GenericAlias'>
Type                                    typing.Type                 typing.Type  <class 'typing._SpecialGenericAlias'>                                    <class 'type'>     False        False  typing  <class 'typing._GenericAlias'>
ValuesView                        typing.ValuesView           typing.ValuesView  <class 'typing._SpecialGenericAlias'>              <class 'collections.abc.ValuesView'>     False        False  typing  <class 'typing._GenericAlias'>
IO                              <class 'typing.IO'>                   typing.IO                         <class 'type'>                                              None     False         True  typing  <class 'typing._GenericAlias'>
SupportsAbs            <class 'typing.SupportsAbs'>          typing.SupportsAbs         <class 'typing._ProtocolMeta'>                                              None     False         True  typing  <class 'typing._GenericAlias'>
SupportsRound        <class 'typing.SupportsRound'>        typing.SupportsRound         <class 'typing._ProtocolMeta'>                                              None     False         True  typing  <class 'typing._GenericAlias'>

TWO ARGS ONLY
                                  cls               cls_name                                   type                                    origin  has_args  cls_is_type    kind                               th_2_type
Callable              typing.Callable        typing.Callable         <class 'typing._CallableType'>        <class 'collections.abc.Callable'>     False        False  typing  <class 'typing._CallableGenericAlias'>
AsyncGenerator  typing.AsyncGenerator  typing.AsyncGenerator  <class 'typing._SpecialGenericAlias'>  <class 'collections.abc.AsyncGenerator'>     False        False  typing          <class 'typing._GenericAlias'>
ChainMap              typing.ChainMap        typing.ChainMap  <class 'typing._SpecialGenericAlias'>            <class 'collections.ChainMap'>     False        False  typing          <class 'typing._GenericAlias'>
DefaultDict        typing.DefaultDict     typing.DefaultDict  <class 'typing._SpecialGenericAlias'>         <class 'collections.defaultdict'>     False        False  typing          <class 'typing._GenericAlias'>
Dict                      typing.Dict            typing.Dict  <class 'typing._SpecialGenericAlias'>                            <class 'dict'>     False        False  typing          <class 'typing._GenericAlias'>
ItemsView            typing.ItemsView       typing.ItemsView  <class 'typing._SpecialGenericAlias'>       <class 'collections.abc.ItemsView'>     False        False  typing          <class 'typing._GenericAlias'>
Mapping                typing.Mapping         typing.Mapping  <class 'typing._SpecialGenericAlias'>         <class 'collections.abc.Mapping'>     False        False  typing          <class 'typing._GenericAlias'>
MutableMapping  typing.MutableMapping  typing.MutableMapping  <class 'typing._SpecialGenericAlias'>  <class 'collections.abc.MutableMapping'>     False        False  typing          <class 'typing._GenericAlias'>
OrderedDict        typing.OrderedDict     typing.OrderedDict  <class 'typing._SpecialGenericAlias'>         <class 'collections.OrderedDict'>     False        False  typing          <class 'typing._GenericAlias'>


THREE ARGS ONLY
                        cls          cls_name                                   type                               origin  has_args  cls_is_type    kind                       th_3_type
Coroutine  typing.Coroutine  typing.Coroutine  <class 'typing._SpecialGenericAlias'>  <class 'collections.abc.Coroutine'>     False        False  typing  <class 'typing._GenericAlias'>
Generator  typing.Generator  typing.Generator  <class 'typing._SpecialGenericAlias'>  <class 'collections.abc.Generator'>     False        False  typing  <class 'typing._GenericAlias'>


ANY NUMBER OF ARGS
                                                  cls                 cls_name                         type           origin  has_args  cls_is_type     kind                       th_1_type
Tuple                                    typing.Tuple             typing.Tuple  <class 'typing._TupleType'>  <class 'tuple'>     False        False   typing  <class 'typing._GenericAlias'>
list                                   <class 'list'>                     list               <class 'type'>             None     False         True  builtin    <class 'types.GenericAlias'>
tuple                                 <class 'tuple'>                    tuple               <class 'type'>             None     False         True  builtin    <class 'types.GenericAlias'>
dict                                   <class 'dict'>                     dict               <class 'type'>             None     False         True  builtin    <class 'types.GenericAlias'>
set                                     <class 'set'>                      set               <class 'type'>             None     False         True  builtin    <class 'types.GenericAlias'>
frozenset                         <class 'frozenset'>                frozenset               <class 'type'>             None     False         True  builtin    <class 'types.GenericAlias'>
AsyncGeneratorType          <class 'async_generator'>          async_generator               <class 'type'>             None     False         True    types    <class 'types.GenericAlias'>
MappingProxyType               <class 'mappingproxy'>             mappingproxy               <class 'type'>             None     False         True    types    <class 'types.GenericAlias'>
defaultdict         <class 'collections.defaultdict'>  collections.defaultdict               <class 'type'>             None     False         True   typing    <class 'types.GenericAlias'>

NO ARGS
                                                                 cls                         cls_name                                   type                                origin  has_args  cls_is_type     kind
None                                                            None                             None                     <class 'NoneType'>                                  None     False        False  builtin
ByteString                                         typing.ByteString                typing.ByteString  <class 'typing._SpecialGenericAlias'>  <class 'collections.abc.ByteString'>     False        False   typing
Hashable                                             typing.Hashable                  typing.Hashable  <class 'typing._SpecialGenericAlias'>    <class 'collections.abc.Hashable'>     False        False   typing
Sized                                                   typing.Sized                     typing.Sized  <class 'typing._SpecialGenericAlias'>       <class 'collections.abc.Sized'>     False        False   typing
str                                                    <class 'str'>                              str                         <class 'type'>                                  None     False         True  builtin
int                                                    <class 'int'>                              int                         <class 'type'>                                  None     False         True  builtin
float                                                <class 'float'>                            float                         <class 'type'>                                  None     False         True  builtin
complex                                            <class 'complex'>                          complex                         <class 'type'>                                  None     False         True  builtin
range                                                <class 'range'>                            range                         <class 'type'>                                  None     False         True  builtin
bool                                                  <class 'bool'>                             bool                         <class 'type'>                                  None     False         True  builtin
bytes                                                <class 'bytes'>                            bytes                         <class 'type'>                                  None     False         True  builtin
bytearray                                        <class 'bytearray'>                        bytearray                         <class 'type'>                                  None     False         True  builtin
memoryview                                      <class 'memoryview'>                       memoryview                         <class 'type'>                                  None     False         True  builtin
NoneType                                          <class 'NoneType'>                         NoneType                         <class 'type'>                                  None     False         True    types
GenericAlias                            <class 'types.GenericAlias'>               types.GenericAlias                         <class 'type'>                                  None      True         True    types
MethodDescriptorType                     <class 'method_descriptor'>                method_descriptor                         <class 'type'>                                  None     False         True    types
MethodWrapperType                           <class 'method-wrapper'>                   method-wrapper                         <class 'type'>                                  None     False         True    types
WrapperDescriptorType                   <class 'wrapper_descriptor'>               wrapper_descriptor                         <class 'type'>                                  None     False         True    types
BuiltinFunctionType             <class 'builtin_function_or_method'>       builtin_function_or_method                         <class 'type'>                                  None     False         True    types
BuiltinMethodType               <class 'builtin_function_or_method'>       builtin_function_or_method                         <class 'type'>                                  None     False         True    types
CellType                                              <class 'cell'>                             cell                         <class 'type'>                                  None     False         True    types
ClassMethodDescriptorType           <class 'classmethod_descriptor'>           classmethod_descriptor                         <class 'type'>                                  None     False         True    types
CodeType                                              <class 'code'>                             code                         <class 'type'>                                  None     False         True    types
CoroutineType                                    <class 'coroutine'>                        coroutine                         <class 'type'>                                  None     False         True    types
DynamicClassAttribute          <class 'types.DynamicClassAttribute'>      types.DynamicClassAttribute                         <class 'type'>                                  None     False         True    types
EllipsisType                                      <class 'ellipsis'>                         ellipsis                         <class 'type'>                                  None     False         True    types
FrameType                                            <class 'frame'>                            frame                         <class 'type'>                                  None     False         True    types
FunctionType                                      <class 'function'>                         function                         <class 'type'>                                  None     False         True    types
GeneratorType                                    <class 'generator'>                        generator                         <class 'type'>                                  None     False         True    types
GetSetDescriptorType                     <class 'getset_descriptor'>                getset_descriptor                         <class 'type'>                                  None     False         True    types
LambdaType                                        <class 'function'>                         function                         <class 'type'>                                  None     False         True    types
MemberDescriptorType                     <class 'member_descriptor'>                member_descriptor                         <class 'type'>                                  None     False         True    types
MethodType                                          <class 'method'>                           method                         <class 'type'>                                  None     False         True    types
ModuleType                                          <class 'module'>                           module                         <class 'type'>                                  None     False         True    types
NotImplementedType                      <class 'NotImplementedType'>               NotImplementedType                         <class 'type'>                                  None     False         True    types
SimpleNamespace                      <class 'types.SimpleNamespace'>            types.SimpleNamespace                         <class 'type'>                                  None     False         True    types
TracebackType                                    <class 'traceback'>                        traceback                         <class 'type'>                                  None     False         True    types
UnionType                                  <class 'types.UnionType'>                  types.UnionType                         <class 'type'>                                  None      True         True    types
_GeneratorWrapper                  <class 'types._GeneratorWrapper'>          types._GeneratorWrapper                         <class 'type'>                                  None     False         True    types
ABCMeta                                        <class 'abc.ABCMeta'>                      abc.ABCMeta                         <class 'type'>                                  None     False         True   typing
Any                                                       typing.Any                       typing.Any              <class 'typing._AnyMeta'>                                  None     False         True   typing
BinaryIO                                   <class 'typing.BinaryIO'>                  typing.BinaryIO                         <class 'type'>                                  None     False         True   typing
ForwardRef                               <class 'typing.ForwardRef'>                typing.ForwardRef                         <class 'type'>                                  None     False         True   typing
Generic                                     <class 'typing.Generic'>                   typing.Generic                         <class 'type'>              <class 'typing.Generic'>     False         True   typing
NamedTupleMeta                       <class 'typing.NamedTupleMeta'>            typing.NamedTupleMeta                         <class 'type'>                                  None     False         True   typing
NewType                                     <class 'typing.NewType'>                   typing.NewType                         <class 'type'>                                  None     False         True   typing
ParamSpec                                 <class 'typing.ParamSpec'>                 typing.ParamSpec                         <class 'type'>                                  None     False         True   typing
ParamSpecArgs                         <class 'typing.ParamSpecArgs'>             typing.ParamSpecArgs                         <class 'type'>                                  None     False         True   typing
ParamSpecKwargs                     <class 'typing.ParamSpecKwargs'>           typing.ParamSpecKwargs                         <class 'type'>                                  None     False         True   typing
Protocol                                   <class 'typing.Protocol'>                  typing.Protocol         <class 'typing._ProtocolMeta'>                                  None     False         True   typing
SupportsBytes                         <class 'typing.SupportsBytes'>             typing.SupportsBytes         <class 'typing._ProtocolMeta'>                                  None     False         True   typing
SupportsComplex                     <class 'typing.SupportsComplex'>           typing.SupportsComplex         <class 'typing._ProtocolMeta'>                                  None     False         True   typing
SupportsFloat                         <class 'typing.SupportsFloat'>             typing.SupportsFloat         <class 'typing._ProtocolMeta'>                                  None     False         True   typing
SupportsIndex                         <class 'typing.SupportsIndex'>             typing.SupportsIndex         <class 'typing._ProtocolMeta'>                                  None     False         True   typing
SupportsInt                             <class 'typing.SupportsInt'>               typing.SupportsInt         <class 'typing._ProtocolMeta'>                                  None     False         True   typing
Text                                                   <class 'str'>                              str                         <class 'type'>                                  None     False         True   typing
TextIO                                       <class 'typing.TextIO'>                    typing.TextIO                         <class 'type'>                                  None     False         True   typing
TypeVar                                     <class 'typing.TypeVar'>                   typing.TypeVar                         <class 'type'>                                  None     False         True   typing
TypeVarTuple                           <class 'typing.TypeVarTuple'>              typing.TypeVarTuple                         <class 'type'>                                  None     False         True   typing
_AnnotatedAlias                     <class 'typing._AnnotatedAlias'>           typing._AnnotatedAlias                         <class 'type'>                                  None     False         True   typing
_AnyMeta                                   <class 'typing._AnyMeta'>                  typing._AnyMeta                         <class 'type'>                                  None     False         True   typing
_BaseGenericAlias                 <class 'typing._BaseGenericAlias'>         typing._BaseGenericAlias                         <class 'type'>                                  None     False         True   typing
_BoundVarianceMixin             <class 'typing._BoundVarianceMixin'>       typing._BoundVarianceMixin                         <class 'type'>                                  None     False         True   typing
_CallableGenericAlias         <class 'typing._CallableGenericAlias'>     typing._CallableGenericAlias                         <class 'type'>                                  None     False         True   typing
_CallableType                         <class 'typing._CallableType'>             typing._CallableType                         <class 'type'>                                  None     False         True   typing
_ConcatenateGenericAlias   <class 'typing._ConcatenateGenericAlias'>  typing._ConcatenateGenericAlias                         <class 'type'>                                  None     False         True   typing
_DeprecatedType                     <class 'typing._DeprecatedType'>           typing._DeprecatedType                         <class 'type'>                                  None     False         True   typing
_Final                                       <class 'typing._Final'>                    typing._Final                         <class 'type'>                                  None     False         True   typing
_GenericAlias                         <class 'typing._GenericAlias'>             typing._GenericAlias                         <class 'type'>                                  None     False         True   typing
_Immutable                               <class 'typing._Immutable'>                typing._Immutable                         <class 'type'>                                  None     False         True   typing
_LiteralGenericAlias           <class 'typing._LiteralGenericAlias'>      typing._LiteralGenericAlias                         <class 'type'>                                  None     False         True   typing
_LiteralSpecialForm             <class 'typing._LiteralSpecialForm'>       typing._LiteralSpecialForm                         <class 'type'>                                  None     False         True   typing
_NamedTuple                              <class 'typing.NamedTuple'>                typing.NamedTuple        <class 'typing.NamedTupleMeta'>                                  None     False         True   typing
_NotIterable                           <class 'typing._NotIterable'>              typing._NotIterable                         <class 'type'>                                  None     False         True   typing
_PickleUsingNameMixin         <class 'typing._PickleUsingNameMixin'>     typing._PickleUsingNameMixin                         <class 'type'>                                  None     False         True   typing
_ProtocolMeta                         <class 'typing._ProtocolMeta'>             typing._ProtocolMeta                         <class 'type'>                                  None     False         True   typing
_SpecialForm                           <class 'typing._SpecialForm'>              typing._SpecialForm                         <class 'type'>                                  None     False         True   typing
_SpecialGenericAlias           <class 'typing._SpecialGenericAlias'>      typing._SpecialGenericAlias                         <class 'type'>                                  None     False         True   typing
_TupleType                               <class 'typing._TupleType'>                typing._TupleType                         <class 'type'>                                  None     False         True   typing
_TypedDict                                <class 'typing.TypedDict'>                 typing.TypedDict        <class 'typing._TypedDictMeta'>                                  None     False         True   typing
_TypedDictMeta                       <class 'typing._TypedDictMeta'>            typing._TypedDictMeta                         <class 'type'>                                  None     False         True   typing
_TypingEllipsis                     <class 'typing._TypingEllipsis'>           typing._TypingEllipsis                         <class 'type'>                                  None     False         True   typing
_UnionGenericAlias               <class 'typing._UnionGenericAlias'>        typing._UnionGenericAlias                         <class 'type'>                                  None     False         True   typing
_UnpackGenericAlias             <class 'typing._UnpackGenericAlias'>       typing._UnpackGenericAlias                         <class 'type'>                                  None     False         True   typing
_alias                         <class 'typing._SpecialGenericAlias'>      typing._SpecialGenericAlias                         <class 'type'>                                  None     False         True   typing

"""

