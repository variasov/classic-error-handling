import inspect
from typing import Union

from classic.error_handling import BaseError, Error, return_errors, is_error


class SomeError(Error):
    code = 'test_error'


@return_errors
def some_func(arg: int = None) -> int:
    if arg:
        return arg

    raise SomeError


class TestReturnError:

    def test_return_arg(self):
        assert some_func(1) == 1

    def test_returning_error(self):
        result = some_func()

        assert isinstance(result, SomeError)
        assert result.code == 'test_error'

    def test_annotation(self):
        signature = inspect.signature(some_func)

        assert len(signature.parameters) == 1
        assert signature.parameters['arg'].annotation is int
        assert signature.return_annotation == Union[int, BaseError]


class TestIsError:

    def test_with_error(self):
        assert is_error(SomeError())

    def test_with_another_exceptions(self):
        assert not is_error(ValueError())
