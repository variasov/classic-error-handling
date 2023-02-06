from classic.error_handling.utils import camel_case_to_dash


def test_camel_case_to_dash():
    assert camel_case_to_dash('SomeName') == 'some_name'
    assert camel_case_to_dash('some_name') == 'some_name'
