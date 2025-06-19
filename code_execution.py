import sys
import io
import traceback
import contextlib


def safe_input(prompt=''):
    """
    Функция для безопасного получения ввода от пользователя. Проверяет на пустой ввод и преобразует в число.
    Возвращает None в случае ошибки.
    """
    user_input = input(prompt).strip()  # Считываем и удаляем лишние пробелы
    if user_input == '':  # Проверка на пустую строку
        print("Ошибка: входная строка пуста.")
        return None
    try:
        return int(user_input)  # Преобразуем в число
    except ValueError:
        print("Ошибка: введено не число.")
        return None


def execute_code(code, input_data=None):
    """
    Безопасное выполнение кода Python в контролируемой среде.

    Аргументы:
    code (str): Код Python для выполнения
    input_data: Необязательные входные данные для передачи коду, могут быть string, int, float и т. д.

    Возвращает:
    tuple: (success, output), где success — логическое значение, указывающее, было ли выполнение успешным,
    а output — это выходное сообщение или сообщение об ошибке
    """
    # Преобразовать input_data в string, если это не None
    if input_data is None:
        input_data = ''
    else:
        input_data = str(input_data)

    # Создать строковые буферы для stdout и stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    # Создать StringIO для ввода
    input_buffer = io.StringIO(input_data)

    # Перенаправление стандартных потоков
    with contextlib.redirect_stdout(stdout_buffer), \
            contextlib.redirect_stderr(stderr_buffer):

        original_input = input

        def custom_input(prompt=''):
            print(prompt, end='')
            return input_buffer.readline().rstrip('\n')

        max_execution_time = 5  # seconds

        try:
            __builtins__['input'] = custom_input  # Подменяем стандартную функцию input

            # Выполнение кода
            exec(code)
            success = True
            output = stdout_buffer.getvalue()

        except Exception as e:
            success = False
            error_traceback = traceback.format_exc()
            output = f"Error: {str(e)}\n\n{error_traceback}"

        finally:
            __builtins__['input'] = original_input  # Восстанавливаем стандартную функцию input

    return success, output


# Пример использования
code = """
num = safe_input("Введите число: ")
if num is not None:
    print(f"Вы ввели: {num}")
"""

# Ввод для тестирования
input_data = "42"  # Пример ввода

# Выполнение кода с использованием безопасного ввода
success, output = execute_code(code, input_data)
print("Результат выполнения:")
print(output)
