document.addEventListener('DOMContentLoaded', function() {
    // Инициализция редактора CodeMirror
    window.codeEditor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
        mode: 'python',
        theme: 'darcula',
        lineNumbers: true,
        indentUnit: 4,
        indentWithTabs: false,
        smartIndent: true,
        tabSize: 4,
        autoCloseBrackets: true,
        matchBrackets: true,
        extraKeys: {
            "Tab": function(cm) {
                cm.replaceSelection("    ", "end");
            }
        }
    });

    window.codeEditor.setSize(null, 400);
    
    // Execute code function
    const executeCode = function() {
        const code = window.codeEditor.getValue();
        const input = document.getElementById('input-data').value;
        const outputElement = document.getElementById('code-output');

        outputElement.innerHTML = '<div class="text-center"><span class="spinner-border spinner-border-sm"></span> Выполнение кода...</div>';
        
        // Вызов API
        fetch('/run_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: code,
                input: input
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                outputElement.innerHTML = `<pre class="p-3 bg-dark text-light rounded">${data.output}</pre>`;
            } else {
                outputElement.innerHTML = `<pre class="p-3 bg-danger text-white rounded">${data.output}</pre>`;
            }
        })
        .catch((error) => {
            outputElement.innerHTML = `<div class="alert alert-danger">Error executing code: ${error}</div>`;
        });
    };
    

    const runButton = document.getElementById('run-code');
    if (runButton) {
        runButton.addEventListener('click', executeCode);
    }
    
    // Ctrl+Enter для запуска кода
    window.codeEditor.setOption('extraKeys', {
        'Ctrl-Enter': executeCode
    });
    
    // Тёмный/светлый режим
    const toggleDarkMode = document.getElementById('toggle-dark-mode');
    if (toggleDarkMode) {
        toggleDarkMode.addEventListener('change', function() {
            if (this.checked) {
                window.codeEditor.setOption('theme', 'darcula');
            } else {
                window.codeEditor.setOption('theme', 'default');
            }
        });
    }
});

// Функция для загрузки примеров кода
function loadSampleCode(type) {

    const codeEditor = document.querySelector('.CodeMirror').CodeMirror;
    
    switch(type) {
        case 'hello':
            codeEditor.setValue('# Моя первая программа на Python\nprint("Привет, мир!")');
            break;
        case 'variables':
            codeEditor.setValue('# Переменные и типы данных\n\n# Целые числа\nвозраст = 17\nбаллы = 95\n\n# Числа с плавающей точкой\nрост = 1.75\nпи = 3.14159\n\n# Строки\nимя = "Алиса"\nсообщение = \'Python - это интересно!\'\n\n# Логические значения\nшкольник = True\nвыполнено = False\n\n# Вывод переменных\nprint("Имя:", имя)\nprint("Возраст:", возраст)\nprint("Рост:", рост, "метров")\nprint("Школьник?", школьник)');
            break;
        case 'conditionals':
            codeEditor.setValue('# Условные операторы\n\nвозраст = int(input("Введите ваш возраст: "))\n\nif возраст >= 18:\n    print("Вы совершеннолетний")\n    if возраст >= 65:\n        print("Вы пенсионер")\nelse:\n    print("Вы несовершеннолетний")\n    лет_до_совершеннолетия = 18 - возраст\n    print(f"Вы станете совершеннолетним через {лет_до_совершеннолетия} лет")');
            break;
        case 'loops':
            codeEditor.setValue('# Циклы\n\n# Цикл for\nprint("Цикл for с range()")\nfor i in range(5):\n    print(f"Итерация {i}")\n\nprint("\\nЦикл for для списка")\nфрукты = ["яблоко", "банан", "груша", "апельсин"]\nfor фрукт in фрукты:\n    print(f"Фрукт: {фрукт}")\n\n# Цикл while\nprint("\\nЦикл while")\nсчетчик = 0\nwhile счетчик < 5:\n    print(f"Счетчик: {счетчик}")\n    счетчик += 1');
            break;
        case 'functions':
            codeEditor.setValue('# Функции\n\n# Простая функция без параметров\ndef приветствие():\n    print("Привет, мир!")\n\n# Функция с параметрами\ndef персональное_приветствие(имя):\n    print(f"Привет, {имя}!")\n\n# Функция с параметрами по умолчанию\ndef приветствие_с_возрастом(имя, возраст=18):\n    print(f"Привет, {имя}! Тебе {возраст} лет.")\n\n# Функция с возвратом значения\ndef сложение(a, b):\n    return a + b\n\n# Вызов функций\nприветствие()\nперсональное_приветствие("Иван")\nприветствие_с_возрастом("Мария", 17)\nприветствие_с_возрастом("Алекс")\n\n# Использование возвращаемого значения\nрезультат = сложение(5, 3)\nprint(f"5 + 3 = {результат}")');
            break;
        case 'factorial':
            codeEditor.setValue('# Функция для вычисления факториала числа\ndef factorial(n):\n    """Вычисляет факториал числа n.\n    \n    Аргументы:\n        n (int): Неотрицательное целое число\n        \n    Возвращает:\n        int: Факториал числа n\n    """\n    if n == 0 or n == 1:\n        return 1\n    else:\n        result = 1\n        for i in range(2, n + 1):\n            result *= i\n        return result\n\n# ВАЖНО: функция должна ВОЗВРАЩАТЬ результат, а не печатать его!\n# При проверке задания система вызовет функцию и проверит возвращаемое значение\n\n# Тестирование функции (можно оставить для отладки):\nprint(factorial(5))  # Ожидаемый результат: 120');
            break;
    }
}
