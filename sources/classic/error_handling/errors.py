from collections import defaultdict
from typing import List, ClassVar, Optional

from .utils import camel_case_to_dash


namespaces = defaultdict(list)


def represent_error(error):
    return {
        'code': error.code_representation,
        'context': error.context,
    }


def represent_error_with_message(error):
    representation = represent_error(error)
    representation['message'] = error.message
    return representation


class ErrorMeta(type):

    def __new__(mcs, name, bases, dct):
        if 'code' not in dct:
            dct['code'] = camel_case_to_dash(name)

        if 'namespace' in dct:
            assert dct['code'] not in namespaces[dct['namespace']]

            namespaces[dct['namespace']].append(dct['code'])
            namespace = dct['namespace']
        else:
            namespace = mcs.get_namescpace(mcs, bases)

        if namespace is not None:
            dct['code_representation'] = f"{namespace}.{dct['code']}"
        else:
            dct['code_representation'] = dct['code']

        if 'message_template' in dct:
            dct['representation'] = property(represent_error_with_message)
        else:
            dct['representation'] = property(represent_error)

        return super().__new__(mcs, name, bases, dct)

    def get_namescpace(mcs, classes):
        for cls in classes:
            if namespace := getattr(cls, 'namespace', None):
                return namespace


class BaseError(Exception):
    """
    Base class for application logic errors.
    """

    code: ClassVar[str] = None

    @property
    def representation(self):
        raise NotImplementedError


class Error(BaseError, metaclass=ErrorMeta):
    namespace: ClassVar[str] = None
    message_template: ClassVar[str] = None
    message: Optional[str] = None
    code_representation: str
    representation: str

    def __init__(self, **kwargs):
        self.context = kwargs
        if self.message_template:
            self.message = self.message_template.format_map(kwargs)
        elif not self.message:
            self.message = None

    def __str__(self):
        if message := self.message:
            return f'{self.__class__.__name__}("{message}")'
        elif self.context:
            attrs = ', '.join(f'{k}={v}' for k, v in self.context.items())
            return f'{self.__class__.__name__}({attrs})'
        else:
            return f'{self.__class__.__name__}()'


class ErrorsList(BaseError):
    """
    Class for situations, when application
    must send many errors in one time.
    """

    code = 'errors_list'

    def __init__(self, *args: Error):
        self.errors: List[Error] = []
        self.errors.extend(args)

    def add(self, *args):
        self.errors.extend(args)

    @property
    def representation(self):
        return [error.representation for error in self.errors]
