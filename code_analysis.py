import requests
import json
import time
import random

# Deepseek API URL и ключ
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/analyze_code"
DEEPSEEK_API_KEY = "055d7503d5e9e355c40d52bb99427f05"  # Ваш API ключ для Deepseek

# Добавляем переменные для отслеживания запросов
RATE_LIMIT_WINDOW = 60  # 60 секунд (1 минута)
MAX_REQUESTS_PER_WINDOW = 5  # Максимальное количество запросов в окне
MIN_RETRY_DELAY = 2  # Минимальная задержка между повторными попытками в секундах
MAX_RETRY_DELAY = 10  # Максимальная задержка между повторными попытками в секундах

# Последнее время запроса и счетчик запросов
last_request_time = 0
request_count = 0


def make_api_request(func, *args, **kwargs):
    """
    Вспомогательная функция для выполнения запросов к API с учетом ограничений скорости.

    Args:
        func: Функция для вызова
        *args: Аргументы для передачи функции
        **kwargs: Именованные аргументы для передачи функции

    Returns:
        Результат выполнения функции
    """
    global last_request_time, request_count

    # Проверка частоты запросов
    current_time = time.time()
    time_passed = current_time - last_request_time

    if time_passed < RATE_LIMIT_WINDOW:
        # Мы все еще в текущем окне
        if request_count >= MAX_REQUESTS_PER_WINDOW:
            # Достигнут лимит запросов, ожидаем до конца окна
            sleep_time = RATE_LIMIT_WINDOW - time_passed + random.uniform(0.5, 2.0)
            print(f"Достигнут лимит запросов. Ожидание {sleep_time:.2f} секунд...")
            time.sleep(sleep_time)
            # Сбрасываем счетчик и обновляем время последнего запроса
            last_request_time = time.time()
            request_count = 0
    else:
        # Прошло достаточно времени, начинаем новое окно
        last_request_time = current_time
        request_count = 0

    # Повторные попытки с экспоненциальной задержкой
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            request_count += 1
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e).lower()

            # Проверяем сообщение об ошибке для определения типа ошибки
            if "429" in error_msg or "too many requests" in error_msg or "rate limit" in error_msg:
                # Это ошибка превышения лимита запросов
                retry_count += 1
                if retry_count >= max_retries:
                    raise e

                # Экспоненциальная задержка с джиттером
                delay = min(MAX_RETRY_DELAY, MIN_RETRY_DELAY * (2 ** retry_count)) + random.uniform(0.1, 1.0)
                print(f"Превышен лимит запросов (429). Повторная попытка через {delay:.2f} секунд...")
                time.sleep(delay)

                # Сбрасываем счетчик для нового окна
                last_request_time = time.time()
                request_count = 0
            elif "500" in error_msg or "503" in error_msg or "service unavailable" in error_msg:
                # Это ошибка сервера
                retry_count += 1
                if retry_count >= max_retries:
                    raise e

                # Задержка перед повторной попыткой
                delay = min(MAX_RETRY_DELAY, MIN_RETRY_DELAY * retry_count) + random.uniform(0.1, 1.0)
                print(f"Ошибка API: {str(e)}. Повторная попытка через {delay:.2f} секунд...")
                time.sleep(delay)
            else:
                # Другие ошибки просто проксируем выше
                raise e


def analyze_code(code, assignment_description=None, test_cases=None, language="python"):
    """
    Анализирует код студента с использованием Deepsek API.

    Args:
        code (str): Код студента для анализа
        assignment_description (str, optional): Описание задания
        test_cases (str, optional): Тестовые случаи для проверки кода
        language (str, optional): Язык программирования

    Returns:
        dict: Анализ кода и рекомендации
    """
    payload = {
        "code": code,
        "language": language,
        "assignment_description": assignment_description or '',
        "test_cases": test_cases or []
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Отправляем запрос к Deepsek API для анализа кода
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            # Преобразуем JSON-ответ в словарь
            analysis = response.json()
            return analysis
        else:
            print(f"Ошибка при анализе кода: {response.text}")
            return {
                "issues": ["Не удалось проанализировать код с помощью Deepsek."],
                "suggestions": ["Попробуйте позже."],
                "explanation": f"Произошла ошибка: {response.text}",
                "improved_code": "",
                "learning_concepts": []
            }

    except Exception as e:
        print(f"Ошибка при отправке запроса: {str(e)}")
        return {
            "issues": ["Не удалось проанализировать код с помощью Deepsek."],
            "suggestions": ["Попробуйте позже."],
            "explanation": f"Произошла ошибка при запросе: {str(e)}",
            "improved_code": "",
            "learning_concepts": []
        }


def get_learning_resources(concepts, language="python"):
    """
    Получает учебные ресурсы по заданным концепциям через Deepsek API.

    Args:
        concepts (list): Список концепций для изучения
        language (str, optional): Язык программирования

    Returns:
        dict: Учебные ресурсы по каждой концепции
    """
    if not concepts:
        return {}

    concepts_str = ", ".join(concepts)
    payload = {
        "concepts": concepts_str,
        "language": language
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Отправляем запрос к Deepsek API для получения учебных ресурсов
        response = requests.post(f"{DEEPSEEK_API_URL}/get_learning_resources", json=payload, headers=headers)

        if response.status_code == 200:
            resources = response.json()
            return resources
        else:
            print(f"Ошибка при получении ресурсов: {response.text}")
            return {concept: {"description": "Информация временно недоступна", "examples": [], "practice": ""} for
                    concept in concepts}

    except Exception as e:
        print(f"Ошибка при отправке запроса: {str(e)}")
        return {concept: {"description": "Информация временно недоступна", "examples": [], "practice": ""} for concept
                in concepts}
