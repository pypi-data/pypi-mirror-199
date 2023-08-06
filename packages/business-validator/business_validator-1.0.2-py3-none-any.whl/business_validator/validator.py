from __future__ import annotations
import functools
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, Generic, TypeAlias
from business_validator.types import (
    ValidationContext,
    ValidationError,
    ValidatorFunc,
    _T,
)

Self: TypeAlias = Any


def validate(name: str | None = None) -> Callable[[ValidatorFunc], ValidatorFunc]:
    def decorator(f: ValidatorFunc) -> ValidatorFunc:
        @wraps(f)
        async def wrapper(self: Validator[Any]) -> None:
            await f(self)

        wrapper.name = name  # type: ignore[attr-defined]
        wrapper.__is_validator__ = True  # type: ignore[attr-defined]

        return wrapper

    return decorator


def pre_state(
    function: Callable[[Self], bool],
    error: _T | None = None,
) -> Callable[[ValidatorFunc], ValidatorFunc]:
    def decorator(f: ValidatorFunc) -> ValidatorFunc:
        @wraps(f)
        async def wrapper(self: Validator[Any]) -> None:
            if function(self):
                await f(self)
            elif error is not None:
                self.context.add_error(error)

        return wrapper

    return decorator


class Validator(Generic[_T]):
    async def setup(self) -> None:
        ...

    async def dispose(self) -> None:
        ...

    async def validate(self) -> None:
        await self.setup()
        try:
            context = self.context
            for validator in self._get_validation_methods():
                await validator(self)
        finally:
            await self.dispose()

        if context.errors:
            raise ValidationError(context.errors)

    @functools.cached_property
    def context(self) -> ValidationContext[_T]:
        return ValidationContext()

    async def errors(self) -> list[_T]:
        try:
            await self.validate()
        except ValidationError as e:
            return e.messages
        return []

    @classmethod
    def _get_validation_methods(
        cls,
    ) -> list[Callable[["Validator[_T]"], Awaitable[None]]]:
        return [
            value
            for value in cls.__dict__.values()
            if getattr(value, "__is_validator__", False)
        ]
