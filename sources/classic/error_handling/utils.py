import re


__camel_case_re = re.compile(r'(?<!^)(?=[A-Z])')


def camel_case_to_dash(text: str) -> str:
    return __camel_case_re.sub('_', text).lower()
