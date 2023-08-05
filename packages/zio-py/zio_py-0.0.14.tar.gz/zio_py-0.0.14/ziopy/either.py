import functools
from abc import ABCMeta
from dataclasses import dataclass
from typing import (Any, Callable, Generic, NoReturn, Optional, Type, TypeVar,
                    Union)

from typing_extensions import Concatenate, Final, ParamSpec, Protocol

from ziopy.util import RaiseLeft, raise_exception

A = TypeVar('A', covariant=True)
A1 = TypeVar('A1')
A2 = TypeVar('A2')
AA = TypeVar('AA')
A_con = TypeVar("A_con", contravariant=True)

B = TypeVar('B', covariant=True)
B1 = TypeVar('B1')
B2 = TypeVar('B2')
BB = TypeVar('BB')

C = TypeVar('C')
C1 = TypeVar('C1')
C2 = TypeVar('C2')

E = TypeVar('E', covariant=True)
E1 = TypeVar('E1')
E2 = TypeVar('E2')
E_con = TypeVar('E_con', contravariant=True)

X = TypeVar('X', bound=BaseException)
P = ParamSpec("P")
PP = ParamSpec("PP")


@dataclass(frozen=True)
class EitherException(Generic[A], Exception):
    value: A


@dataclass(frozen=True)
class TypeMatchException(Generic[AA], Exception):
    value: Optional[AA]


class GetItem(Protocol[A_con, B]):
    def __getitem__(self, item: A_con) -> B:
        pass


class Either(Generic[A, B], metaclass=ABCMeta):
    """Right-biased disjunction"""

    @staticmethod
    def left(a: AA) -> "Either[AA, NoReturn]":
        return Left(a)

    @staticmethod
    def right(b: BB) -> "Either[NoReturn, BB]":
        return Right(b)

    @staticmethod
    def from_union(
        value: Union[A, B],
        left_type: Type[A],
        right_type: Type[B]
    ) -> "Either[A, B]":
        if isinstance(value, left_type):
            return Either.left(value)
        elif isinstance(value, right_type):
            return Either.right(value)
        else:
            raise TypeError()

    @staticmethod
    def from_optional(value: Optional[B]) -> "Either[None, B]":
        if value is None:
            return Either.left(value)
        return Either.right(value)

    def to_left(self: "Either[AA, NoReturn]") -> "Left[AA]":
        if not isinstance(self, Left):
            raise TypeError("to_left can only be called on an instance of Left.")
        return self

    def to_right(self: "Either[NoReturn, BB]") -> "Right[BB]":
        if not isinstance(self, Right):
            raise TypeError("to_right can only be called on an instance of Right.")
        return self

    def match(
        self,
        case_left: "Callable[[Left[A]], C1]",
        case_right: "Callable[[Right[B]], C2]"
    ) -> Union[C1, C2]:
        if isinstance(self, Left):
            return case_left(self)
        elif isinstance(self, Right):
            return case_right(self)
        else:
            raise TypeError()

    def fold(
        self,
        case_left: "Callable[[A], C1]",
        case_right: "Callable[[B], C2]"
    ) -> Union[C1, C2]:
        return self.match(
            lambda x: case_left(x.value),
            lambda y: case_right(y.value)
        )

    def swap(self) -> "Either[B, A]":
        return self.match(
            lambda left: Either.right(left.value),
            lambda right: Either.left(right.value)
        )

    def map(self, f: Callable[[B], C]) -> "Either[A, C]":
        return self.match(
            lambda left: left,
            lambda right: Either.right(f(right.value))
        )

    def map_left(self, f: Callable[[A], C]) -> "Either[C, B]":
        return self.match(
            lambda left: Either.left(f(left.value)),
            lambda right: right
        )

    def flat_map(self, f: "Callable[[B], Either[AA, C]]") -> "Either[Union[A, AA], C]":
        return self.match(
            lambda left: left,
            lambda right: f(right.value)
        )

    def __lshift__(self, f: "Callable[[B], Either[AA, C]]") -> "Either[Union[A, AA], C]":
        return self.flat_map(f)

    def flatten(self: "Either[A1, Either[AA, BB]]") -> "Either[Union[A1, AA], BB]":
        return self.flat_map(lambda x: x)

    def require(
        self,
        predicate: Callable[[B], bool],
        to_error: Callable[[B], AA]
    ) -> "Either[Union[A, AA], B]":
        def _case_right(right: Right[B]) -> "Either[Union[A, AA], B]":
            if predicate(right.value):
                return right
            return Either.left(to_error(right.value))

        return self.match(
            lambda left: left,
            _case_right
        )

    def asserting(
        self,
        predicate: Callable[[B], bool],
        to_error: Callable[[B], X]
    ) -> "Either[A, B]":
        def _case_right(right: Right[B]) -> "Either[A, B]":
            if not predicate(right.value):
                raise to_error(right.value)
            return right

        return self.match(
            lambda left: left,
            _case_right
        )

    def raise_errors(self: "Either[AA, BB]") -> "Either[NoReturn, BB]":
        def _case_left(error: AA) -> NoReturn:
            if isinstance(error, Exception):
                raise error from error
            else:
                raise EitherException(value=error)

        return self.fold(_case_left, lambda x: Either.right(x))

    def tap(self, op: "Callable[[Either[A, B]], Any]") -> "Either[A, B]":
        op(self)
        return self

    def display(self, description: Optional[str] = None) -> "Either[A, B]":
        if description is not None:
            print(f"{description}:")
        return self.tap(print)

    def to_union(self) -> Union[A, B]:
        return self.match(lambda x: x.value, lambda y: y.value)

    def cast(self: "Either[AA, BB]", t: Type[C]) -> "Either[Union[AA, TypeError], C]":
        return self.flat_map(
            lambda b: Either.right(b) if isinstance(b, t)
            else Either.left(
                TypeError(f"Unable to cast value {b} (of type {type(b).__name__}) as type {t.__name__}.")
            )
        )


@dataclass(frozen=True)
class Left(Generic[A], Either[A, NoReturn]):
    value: A


@dataclass(frozen=True)
class Right(Generic[B], Either[NoReturn, B]):
    value: B


class EitherMonad(Generic[E_con]):
    def __lshift__(self, arg: Either[E_con, BB]) -> BB:
        return arg.fold(
            lambda e: raise_exception(RaiseLeft(e)),
            lambda a: a
        )


def monadic_method(
    func: Callable[Concatenate[AA, EitherMonad[E], P], Either[E, A]]
) -> Callable[Concatenate[AA, P], Either[E, A]]:
    @functools.wraps(func)
    def _wrapper(self_arg: AA, *args: P.args, **kwargs: P.kwargs) -> Either[E, A]:
        try:
            return func(self_arg, EitherMonad(), *args, **kwargs)
        except RaiseLeft as raise_left:
            # NOTE: WJH (02/03/23) mypy can't prove that the generic type
            #       of the RaiseLeft instance here is `E`, so we have to
            #       use `type: ignore`.
            return Either.left(raise_left.value)  # type: ignore
    return _wrapper


def monadic(
    func: Callable[Concatenate[EitherMonad[E], P], Either[E, A]]
) -> Callable[P, Either[E, A]]:
    @functools.wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> Either[E, A]:
        try:
            return func(EitherMonad(), *args, **kwargs)
        except RaiseLeft as raise_left:
            # NOTE: WJH (02/03/23) mypy can't prove that the generic type
            #       of the RaiseLeft instance here is `E`, so we have to
            #       use `type: ignore`.
            return Either.left(raise_left.value)  # type: ignore
    return _wrapper


class WithArgs(Protocol[P, A_con, B]):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Callable[[A_con], B]:
        pass


class _Identities:
    def __getitem__(self, t: Type[AA]) -> "EitherArrow[[AA], NoReturn, AA]":
        return EitherArrow.from_callable(lambda x: x)


class EitherArrow(Generic[P, A, B]):
    @staticmethod
    def from_either(either: Either[E, Callable[P, A]]) -> "EitherArrow[P, E, A]":
        return EitherArrow(lambda *args, **kwargs: either.map(lambda f: f(*args, **kwargs)))

    @staticmethod
    def from_callable(f: Callable[P, A]) -> "EitherArrow[P, NoReturn, A]":
        return EitherArrow(lambda *args, **kwargs: Either.right(f(*args, **kwargs)))

    @staticmethod
    def right(x: AA) -> "EitherArrow[[], NoReturn, AA]":
        return EitherArrow(lambda: Either.right(x))

    @staticmethod
    def left(x: BB) -> "EitherArrow[[], BB, NoReturn]":
        return EitherArrow(lambda: Either.left(x))

    identity: Final = _Identities()

    def __init__(self, f: Callable[P, Either[A, B]]) -> None:
        self._f = f

    def to_callable(self) -> "Callable[P, Either[A, B]]":
        return self._f

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> "Either[A, B]":
        return self._f(*args, **kwargs)

    def catch(
        self: "EitherArrow[P, E, AA]",
        exc: Type[X]
    ) -> "EitherArrow[P, Union[E, X], AA]":
        def _g(*args: P.args, **kwargs: P.kwargs) -> Either[Union[E, X], AA]:
            try:
                return self._f(*args, **kwargs)
            except exc as e:
                return Either.left(e)
        return EitherArrow(_g)

    def to_left(self: "EitherArrow[P, AA, NoReturn]") -> Callable[P, Left[AA]]:
        return lambda *args, **kwargs: self._f(*args, **kwargs).to_left()

    def to_right(self: "EitherArrow[P, NoReturn, BB]") -> Callable[P, Right[BB]]:
        return lambda *args, **kwargs: self._f(*args, **kwargs).to_right()

    def match(
        self,
        case_left: "Callable[[Left[A]], C1]",
        case_right: "Callable[[Right[B]], C2]"
    ) -> Callable[P, Union[C1, C2]]:
        return lambda *args, **kwargs: self._f(*args, **kwargs).match(case_left, case_right)

    def fold(
        self,
        case_left: "Callable[[A], C1]",
        case_right: "Callable[[B], C2]"
    ) -> Callable[P, Union[C1, C2]]:
        return lambda *args, **kwargs: self._f(*args, **kwargs).fold(case_left, case_right)

    def swap(self) -> "EitherArrow[P, B, A]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).swap())

    def map(self, f: Callable[[B], C]) -> "EitherArrow[P, A, C]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).map(f))

    def map_left(self, f: Callable[[A], C]) -> "EitherArrow[P, C, B]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).map_left(f))

    def flat_map(self, f: "Callable[[B], Either[AA, C]]") -> "EitherArrow[P, Union[A, AA], C]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).flat_map(f))

    def __lshift__(self, f: "Callable[[B], Either[AA, C]]") -> "EitherArrow[P, Union[A, AA], C]":
        return self.flat_map(f)

    def flatten(
        self: "EitherArrow[P, A1, Either[AA, BB]]"
    ) -> "EitherArrow[P, Union[A1, AA], BB]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).flatten())

    def require(
        self,
        predicate: Callable[[B], bool],
        to_error: Callable[[B], AA]
    ) -> "EitherArrow[P, Union[A, AA], B]":
        return EitherArrow(
            lambda *args, **kwargs: self._f(*args, **kwargs).require(predicate, to_error)
        )

    def asserting(
        self,
        predicate: Callable[[B], bool],
        to_error: Callable[[B], X]
    ) -> "EitherArrow[P, A, B]":
        return EitherArrow(
            lambda *args, **kwargs: self._f(*args, **kwargs).asserting(predicate, to_error)
        )

    def or_else(self, other: "EitherArrow[P, AA, BB]") -> "EitherArrow[P, A | AA, B | BB]":
        return EitherArrow(
            lambda *args, **kwargs: self._f(*args, **kwargs).match(
                lambda _: other(*args, **kwargs),
                lambda a: a
            )
        )

    def raise_errors(self: "EitherArrow[P, AA, BB]") -> "EitherArrow[P, NoReturn, BB]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).raise_errors())

    def tap(self, op: "Callable[[Either[A, B]], Any]") -> "EitherArrow[P, A, B]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).tap(op))

    def display(self, description: Optional[str] = None) -> "EitherArrow[P, A, B]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).display(description))

    def to_union(self) -> Callable[P, Union[A, B]]:
        return lambda *args, **kwargs: self._f(*args, **kwargs).to_union()

    def cast(self: "EitherArrow[P, AA, BB]", t: Type[C]) -> "EitherArrow[P, Union[AA, TypeError], C]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).cast(t))

    def __getitem__(self: "EitherArrow[P, AA, GetItem[B1, C1]]", key: B1) -> "EitherArrow[P, AA, C1]":
        return EitherArrow(
            lambda *args, **kwargs: self._f(*args, **kwargs).map(lambda x: x[key])
        )

    def match_types(self: "EitherArrow[P, AA, BB]") -> "EitherArrow[P, AA, NoReturn]":
        def _f(arg: BB) -> NoReturn:
            raise TypeMatchException(arg)
        return self.map(_f)

    def at_type(
        self: "EitherArrow[P, AA, BB]",
        target_type: Type[B2],
        operation: "Callable[[B2], Either[A2, C]]"
    ) -> "EitherArrow[P, Union[AA, A2], Union[BB, C]]":
        def _recover(arg: Union[BB, TypeMatchException]) -> Either[A2, Union[BB, C]]:
            if not isinstance(arg, TypeMatchException):
                return Either.right(arg)
            if isinstance(arg.value, target_type):
                return operation(arg.value)
            else:
                raise arg from arg

        return (
            self.swap()
            .catch(TypeMatchException)
            .swap()
            .flat_map(_recover)
        )

    def with_args_map(
        self: "EitherArrow[P, AA, BB]",
        f: WithArgs[P, BB, C]
    ) -> "EitherArrow[P, AA, C]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).map(lambda x: f(*args, **kwargs)(x)))

    def with_args_flat_map(
        self: "EitherArrow[P, A, BB]",
        f: WithArgs[P, BB, Either[AA, C]]
    ) -> "EitherArrow[P, Union[A, AA], C]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).flat_map(lambda x: f(*args, **kwargs)(x)))

    def with_args_map_left(
        self: "EitherArrow[P, AA, B]",
        f: WithArgs[P, AA, C]
    ) -> "EitherArrow[P, C, B]":
        return EitherArrow(lambda *args, **kwargs: self._f(*args, **kwargs).map_left(lambda x: f(*args, **kwargs)(x)))
