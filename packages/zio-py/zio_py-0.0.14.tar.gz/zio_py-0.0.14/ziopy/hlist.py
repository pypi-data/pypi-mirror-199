import functools
from abc import ABCMeta
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, overload

from typing_extensions import TypeAlias

A = TypeVar("A")
R = TypeVar("R")
H = TypeVar("H", covariant=True)

T = TypeVar("T", covariant=True, bound="HList")


class HList(metaclass=ABCMeta):
    def prepend(self: T, head: A) -> "HCons[A, T]":
        return HCons(head, self)

    def __rpow__(self: T, head: A) -> "HCons[A, T]":
        return self.prepend(head)


@dataclass(frozen=True)
class HNil(HList):
    def apply(self, f: Callable[[], R]) -> R:
        return f()

    def apply_0(self, f: Callable[[], R]) -> R:
        return f()


@dataclass(frozen=True)
class HCons(Generic[H, T], HList):
    head: H
    tail: T


T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
T8 = TypeVar("T8")
T9 = TypeVar("T9")
T10 = TypeVar("T10")
T11 = TypeVar("T11")
T12 = TypeVar("T12")
T13 = TypeVar("T13")
T14 = TypeVar("T14")
T15 = TypeVar("T15")


# TODO: If mypy's ParamSpec actually worked as expected, lots of this boilerplate
# would go away. In the meantime, behold the horror.
HList1: TypeAlias = HCons[T1, HNil]
HList2: TypeAlias = HCons[T1, HList1[T2]]
HList3: TypeAlias = HCons[T1, HList2[T2, T3]]
HList4: TypeAlias = HCons[T1, HList3[T2, T3, T4]]
HList5: TypeAlias = HCons[T1, HList4[T2, T3, T4, T5]]
HList6: TypeAlias = HCons[T1, HList5[T2, T3, T4, T5, T6]]
HList7: TypeAlias = HCons[T1, HList6[T2, T3, T4, T5, T6, T7]]
HList8: TypeAlias = HCons[T1, HList7[T2, T3, T4, T5, T6, T7, T8]]
HList9: TypeAlias = HCons[T1, HList8[T2, T3, T4, T5, T6, T7, T8, T9]]
HList10: TypeAlias = HCons[T1, HList9[T2, T3, T4, T5, T6, T7, T8, T9, T10]]
HList11: TypeAlias = HCons[T1, HList10[T2, T3, T4, T5, T6, T7, T8, T9, T10, T11]]


@overload
def hlisted(f: Callable[[], R]) -> Callable[[HNil], R]: ...
@overload
def hlisted(f: Callable[[T1], R]) -> Callable[[HList1[T1]], R]: ...
@overload
def hlisted(f: Callable[[T1, T2], R]) -> Callable[[HList2[T1, T2]], R]: ...
@overload
def hlisted(f: Callable[[T1, T2, T3], R]) -> Callable[[HList3[T1, T2, T3]], R]: ...
@overload
def hlisted(f: Callable[[T1, T2, T3, T4], R]) -> Callable[[HList4[T1, T2, T3, T4]], R]: ...
@overload
def hlisted(f: Callable[[T1, T2, T3, T4, T5], R]) -> Callable[[HList5[T1, T2, T3, T4, T5]], R]: ...
@overload
def hlisted(f: Callable[[T1, T2, T3, T4, T5, T6], R]) -> Callable[[HList6[T1, T2, T3, T4, T5, T6]], R]: ...
@overload
def hlisted(f: Callable[[T1, T2, T3, T4, T5, T6, T7], R]) -> Callable[[HList7[T1, T2, T3, T4, T5, T6, T7]], R]: ...
@overload
def hlisted(f: Callable[[T1, T2, T3, T4, T5, T6, T7, T8], R]) -> Callable[[HList8[T1, T2, T3, T4, T5, T6, T7, T8]], R]: ...
@overload
def hlisted(f: Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9], R]) -> Callable[[HList9[T1, T2, T3, T4, T5, T6, T7, T8, T9]], R]: ...
@overload
def hlisted(f: Callable[[T1, T2, T3, T4, T5, T6, T7, T8, T9, T10], R]) -> Callable[[HList10[T1, T2, T3, T4, T5, T6, T7, T8, T9, T10]], R]: ...


def hlisted(f: Callable[..., R]) -> Callable[..., R]:
    def g(hlist: HList) -> R:
        if isinstance(hlist, HNil):
            return f()
        elif isinstance(hlist, HCons):
            # Partially apply f with Head=T1 to get a function
            # `T2, T3, T4, ... -> R`
            f_partial = functools.partial(f, hlist.head)

            # now hlist the partially applied function
            f_partial_hlisted = hlisted(f_partial)

            # Apply it to the tail
            return f_partial_hlisted(hlist.tail)
        else:
            raise TypeError

    return g
