import dataclasses
from enum import Enum
from collections.abc import Callable, Coroutine
from typing import Any, Generic, TypeAlias, TypeVar

from pydantic.generics import GenericModel


_T = TypeVar("_T")
_S = TypeVar("_S")

ValidatorFunc: TypeAlias = Callable[[Any], Coroutine[Any, Any, None]]


class ErrorCodeEnum(str, Enum):
    unique_constraint = "UNIQUE CONSTRAINT"
    not_found = "NOT FOUND"
    permission_denied = "PERMISSION DENIED"


class ErrorSchema(GenericModel, Generic[_S]):
    code: str
    message: str
    detail: str | None = None
    source: _S | None = None


class ValidationError(Generic[_T], Exception):
    messages: list[_T]

    def __init__(self, messages: list[_T], *args: object) -> None:
        super().__init__(*args)
        self.messages = messages


@dataclasses.dataclass()
class ValidationContext(Generic[_T]):
    _errors: list[_T] = dataclasses.field(default_factory=list)

    def add_error(self, error: _T) -> None:
        self._errors.append(error)

    def extend_nested_error(self, errors: list[_T]) -> None:
        self._errors.extend(errors)

    @property
    def errors(self) -> list[_T]:
        return self._errors
