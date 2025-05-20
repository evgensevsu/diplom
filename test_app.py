import pytest
from app import app, db, User, Lesson, Assignment
from flask import url_for

@pytest.fixture(scope='module')
def test_client():
    # Создание тестового клиента Flask
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = 'mysecret'

    with app.test_client() as client:
        with app.app_context():
            # Создание таблиц в тестовой базе данных
            db.create_all()
        yield client
        with app.app_context():
            # Удаление таблиц после выполнения тестов
            db.drop_all()

@pytest.fixture
def new_user():
    # Создание нового пользователя для теста
    user = User(username='testuser', password='password')
    db.session.add(user)
    db.session.commit()
    return user

def test_register(test_client):
    # Тест регистрации нового пользователя
    response = test_client.post('/register', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Зарегистрируйтесь здесь' in response.data.decode('utf-8')  # Проверка строки на странице регистрации

def test_login(test_client, new_user):
    # Тест логина пользователя
    response = test_client.post('/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Привет, testuser' in response.data.decode('utf-8')  # Проверка приветственного сообщения на dashboard

def test_dashboard_access(test_client, new_user):
    # Тест доступности защищённой страницы Dashboard
    test_client.post('/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)

    response = test_client.get('/dashboard')
    assert response.status_code == 200
    assert 'Панель управления' in response.data.decode('utf-8')  # Проверка наличия панели управления

def test_logout(test_client, new_user):
    # Тест выхода пользователя
    test_client.post('/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)

    response = test_client.post('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'Выход' in response.data.decode('utf-8')  # Проверка сообщения о выходе из системы

def test_create_lesson(test_client, new_user):
    # Тест создания нового урока
    test_client.post('/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)

    response = test_client.post('/lessons/new', data={
        'title': 'New Lesson',
        'content': 'Lesson content here',
        'order': '1',
        'is_published': 'True'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Новый урок' in response.data.decode('utf-8')  # Проверка страницы создания нового урока

def test_lesson_in_db(test_client, new_user):
    # Проверка, что урок был добавлен в базу данных
    test_client.post('/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)

    test_client.post('/lessons/new', data={
        'title': 'New Lesson',
        'content': 'Lesson content here',
        'order': '1',
        'is_published': 'True'
    }, follow_redirects=True)

    lesson = Lesson.query.filter_by(title='New Lesson').first()
    assert lesson is not None
    assert lesson.title == 'New Lesson'  # Проверка, что урок был добавлен

def test_create_assignment(test_client, new_user):
    # Тест создания нового задания
    test_client.post('/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)

    response = test_client.post('/assignments/new', data={
        'title': 'New Assignment',
        'description': 'Assignment description here',
        'tests': '{"input": "1", "expected_output": "2"}',
        'difficulty': 'Easy',
        'is_published': 'True'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Новое задание' in response.data.decode('utf-8')  # Проверка страницы создания нового задания

def test_assignment_in_db(test_client, new_user):
    # Проверка, что задание было добавлено в базу данных
    test_client.post('/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)

    test_client.post('/assignments/new', data={
        'title': 'New Assignment',
        'description': 'Assignment description here',
        'tests': '{"input": "1", "expected_output": "2"}',
        'difficulty': 'Easy',
        'is_published': 'True'
    }, follow_redirects=True)

    assignment = Assignment.query.filter_by(title='New Assignment').first()
    assert assignment is not None
    assert assignment.title == 'New Assignment'  # Проверка, что задание было добавлено

# Запуск тестов
if __name__ == '__main__':
    pytest.main()
