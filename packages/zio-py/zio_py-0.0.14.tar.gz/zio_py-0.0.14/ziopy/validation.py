from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, NoReturn, TypeVar

from ziopy.either import Either
from ziopy.hlist import HCons, HList, HNil

A = TypeVar("A")
E = TypeVar("E")
H = TypeVar("H")
T = TypeVar("T", bound=HList)
U = TypeVar("U", bound="Validation")


class Validation(Generic[E, T], metaclass=ABCMeta):
    @abstractmethod
    def validate(self) -> Either[List[E], T]:
        pass


@dataclass(frozen=True)
class VNil(Validation[NoReturn, HNil]):
    def prepend(self, h: Either[E, H]) -> "VCons[E, H, VNil, HCons[H, HNil]]":
        return VCons(h, self)

    def __rpow__(self, h: Either[E, H]) -> "VCons[E, H, VNil, HCons[H, HNil]]":
        return self.prepend(h)

    def validate(self) -> Either[List[E], HNil]:
        return Either.right(HNil())


@dataclass(frozen=True)
class VCons(Generic[E, H, U, T], Validation[E, T]):
    head: Either[E, H]
    tail: U

    def prepend(self, h: Either[E, A]) -> "VCons[E, A, VCons[E, H, U, T], HCons[A, T]]":
        return VCons(h, self)

    def __rpow__(self, h: Either[E, A]) -> "VCons[E, A, VCons[E, H, U, T], HCons[A, T]]":
        return self.prepend(h)

    def validate(self) -> Either[List[E], T]:
        tail_v = self.tail.validate()

        return (
            self.head
            .map_left(
                lambda e: tail_v.fold(lambda errs: [e] + errs, lambda _: [e])
            )
            .flat_map(lambda t1: tail_v.map(lambda rs: (t1 ** rs)))
        )
