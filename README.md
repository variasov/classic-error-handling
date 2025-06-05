# Classic Error Handling

Этот пакет предоставляет примитивы для обработки ошибок на уровне приложения.
Часть проекта "Classic".

## Установка

```bash
pip install classic-error-handling
```

## Использование

Примеры оформления ошибок:

```python
from classic.error_handling import Error, ErrorsList


# Ошибка с пространством имен
class Namespaced(Error):
    namespace = 'some_namespace'


# Наследование пространства имен
class InheritingNamespace(Namespaced):
    pass


# Ошибка с пространством имен и явным кодом
class NamespacedWithCode(Error):
    namespace = 'some_namespace'
    code = 'some_error'


# Ошибка с явным кодом без пространства имен
class WithCode(Error):
    code = 'some_error'


# Ошибка с литеральным сообщением
class WithLiteralMessage(Error):
    message_template = 'some_message'


# Ошибка с шаблоном сообщения
class WithMessageTemplate(Error):
    message_template = 'some_template: {arg}'
```

Пример использования:

```python
from classic.error_handling import Error, ErrorsList


# Определяем ошибки приложения
class IncorrectState(Error):
    namespace = 'app'
    message_template = 'Некорректное состояние приложения - "{text}"'


class ServiceNotReady(Error):
    namespace = 'app'
    message_template = 'Сервис еще не готов'


# В сервисах:
class SomeService:
    
    def __init__(self):
        self.ready_to_serve = False

    def is_ready(self):
        """Демонстрирует простое использование"""
        if not self.ready_to_serve:
            raise ServiceNotReady()

    def mark_as_ready(self):
        """Демонстрирует использование шаблонов сообщений"""
        if self.ready_to_serve:
            raise IncorrectState(text='Сервис уже готов')
        self.ready_to_serve = True

    def just_give_errors(self):
        """Демонстрирует метод, который может вернуть несколько ошибок"""
        errors = [IncorrectState(text='ошибка 1'), 
                  IncorrectState(text='ошибка 2')]
        raise ErrorsList(*errors)


# Где-то в адаптерах:

service = SomeService()

try:
    service.is_ready()
except Error as error:
    print(f'Приложение ответило с кодом ошибки "{error.code_representation}", '
          f'сообщение: "{error.message}"')

try:
    service.mark_as_ready()
    service.mark_as_ready()
except Error as error:
    print(f'Приложение ответило с кодом ошибки "{error.code_representation}", '
          f'сообщение: "{error.message}"')
    
try:
    service.just_give_errors()
except ErrorsList as errors_list:
    for error in errors_list.errors:
        print(f'Приложение ответило с кодом ошибки "{error.code_representation}", '
              f'сообщение: "{error.message}"')
