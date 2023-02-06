from contextlib import suppress as original_suppress, ContextDecorator
from functools import wraps
from typing import Any, Callable, Union, get_origin, get_args

from .errors import BaseError


def is_error(obj: Any) -> bool:
    return isinstance(obj, BaseError)


def return_errors(fn: Callable[[...], Any]):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except BaseError as error:
            return error

    returns = wrapper.__annotations__.get('return')
    if not returns:
        wrapper.__annotations__['return'] = Union[Any, BaseError]
    elif get_origin(returns) == Union:
        return_args = get_args(returns)
        if BaseError not in return_args:
            wrapper.__annotations__['return'] = Union[return_args, BaseError]
    else:
        wrapper.__annotations__['return'] = Union[returns, BaseError]

    return wrapper


class suppress(original_suppress, ContextDecorator):
    pass
