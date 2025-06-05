from classic.error_handling import Error, ErrorsList


class Namespaced(Error):
    namespace = 'some_namespace'


class InheritingNamespace(Namespaced):
    pass


class NamespacedWithCode(Error):
    namespace = 'some_namespace'
    code = 'some_error'


class WithCode(Error):
    code = 'some_error'


class WithLiteralMessage(Error):
    message_template = 'some_message'


class WithMessageTemplate(Error):
    message_template = 'some_template: {arg}'


class TestError:

    def test_namespaced(self):
        error = Namespaced()

        assert error.namespace == 'some_namespace'
        assert error.code == 'namespaced'
        assert error.representation == {
            'code': 'some_namespace.namespaced',
            'context': {},
        }
        assert str(error) == 'Namespaced()'

    def test_namespaced_inheriting(self):
        error = InheritingNamespace()

        assert error.namespace == 'some_namespace'
        assert error.code == 'inheriting_namespace'
        assert error.representation == {
            'code': 'some_namespace.inheriting_namespace',
            'context': {},
        }
        assert str(error) == 'InheritingNamespace()'

    def test_code(self):
        error = WithCode()

        assert error.namespace is None
        assert error.code == 'some_error'
        assert error.representation == {'code': 'some_error', 'context': {}}
        assert str(error) == 'WithCode()'

    def test_literal_message(self):
        error = WithLiteralMessage()

        assert error.namespace is None
        assert error.code == 'with_literal_message'
        assert error.representation == {
            'code': 'with_literal_message',
            'message': 'some_message',
            'context': {},
        }
        assert str(error) == 'WithLiteralMessage("some_message")'

    def test_message_template(self):
        error = WithMessageTemplate(arg=1)

        assert error.namespace is None
        assert error.code == 'with_message_template'
        assert error.representation == {
            'code': 'with_message_template',
            'message': 'some_template: 1',
            'context': {
                'arg': 1
            },
        }
        assert str(error) == 'WithMessageTemplate("some_template: 1")'

    def test_context(self):
        error = WithCode(arg=1)

        assert error.namespace is None
        assert error.code == 'some_error'
        assert error.representation == {
            'code': 'some_error',
            'context': {
                'arg': 1
            },
        }
        assert str(error) == "WithCode(arg=1)"


class TestErrorsList:

    def test_(self):
        errors_list = ErrorsList(WithCode(), WithCode())

        assert errors_list.code == 'errors_list'
        assert errors_list.representation == [
            {'code': 'some_error', 'context': {}},
            {'code': 'some_error', 'context': {}},
        ]
