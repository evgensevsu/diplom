import unittest
from app import app, db, User, Client, Note, bcrypt
from flask import url_for
from flask_login import current_user
import time

class FlaskTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создаем тестовое приложение и тестовую базу данных
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF для тестов
        cls.client = app.test_client()

        # Создаем все таблицы для теста
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Удаляем тестовую базу данных после тестов
        with app.app_context():
            db.drop_all()

    # Модульные тесты для моделей

    def test_create_user(self):
        # Проверка создания пользователя с корректными данными
        username = f"testuser_{int(time.time())}"  # Уникальное имя пользователя
        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Проверяем, что пользователь был добавлен в базу данных
        added_user = User.query.filter_by(username=username).first()
        self.assertIsNotNone(added_user)
        self.assertEqual(added_user.username, username)

    def test_create_client(self):
        # Проверка создания клиента с корректными данными
        username = f"testuser_{int(time.time())}"  # Уникальное имя пользователя
        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        client = Client(
            first_name="John", last_name="Doe", email="john.doe@example.com",
            phone="1234567890", address="Some Address", user_id=user.id
        )
        db.session.add(client)
        db.session.commit()

        # Проверяем, что клиент был добавлен в базу данных
        added_client = Client.query.filter_by(first_name="John").first()
        self.assertIsNotNone(added_client)
        self.assertEqual(added_client.first_name, "John")

    def test_create_note(self):
        # Проверка создания заметки для клиента
        username = f"testuser_{int(time.time())}"  # Уникальное имя пользователя
        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        client = Client(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", address="Some Address", user_id=user.id)
        db.session.add(client)
        db.session.commit()

        note_content = "This is a test note"
        new_note = Note(client_id=client.id, note=note_content)
        db.session.add(new_note)
        db.session.commit()

        # Проверяем, что заметка была добавлена
        added_note = Note.query.filter_by(client_id=client.id).first()
        self.assertIsNotNone(added_note)
        self.assertEqual(added_note.note, note_content)

    def test_update_client(self):
        # Проверка обновления информации о клиенте
        username = f"testuser_{int(time.time())}"  # Уникальное имя пользователя
        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        client = Client(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", address="Some Address", user_id=user.id)
        db.session.add(client)
        db.session.commit()

        client.first_name = "Jane"
        db.session.commit()

        updated_client = Client.query.get(client.id)
        self.assertEqual(updated_client.first_name, "Jane")

    def test_delete_client(self):
        # Проверка удаления клиента
        username = f"testuser_{int(time.time())}"  # Уникальное имя пользователя
        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        client = Client(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", address="Some Address", user_id=user.id)
        db.session.add(client)
        db.session.commit()

        db.session.delete(client)
        db.session.commit()

        deleted_client = Client.query.get(client.id)
        self.assertIsNone(deleted_client)

    # Интеграционные тесты для работы с формами и редиректами

    def test_register_user(self):
        # Проверка регистрации нового пользователя
        username = f"newuser_{int(time.time())}"  # Уникальное имя пользователя
        response = self.client.post('/register', data=dict(
            username=username,
            password='newpassword'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Вход', response.data.decode('utf-8'))  # После регистрации пользователь должен быть перенаправлен на страницу входа

    def test_login_valid_user(self):
        # Проверка успешного входа с корректными данными
        username = f"testuser_{int(time.time())}"  # Уникальное имя пользователя
        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', data=dict(
            username=username,
            password='testpassword'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Планировщик питания', response.data.decode('utf-8'))  # Проверка наличия текста "Планировщик питания"

    def test_add_note_to_client(self):
        # Тест на добавление заметки клиенту
        with app.app_context():
            username = f"testuser_{int(time.time())}"  # Уникальное имя пользователя
            hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            client = Client(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", address="Some Address", user_id=user.id)
            db.session.add(client)
            db.session.commit()

            # Добавление заметки
            note_content = "This is a test note"
            new_note = Note(client_id=client.id, note=note_content)
            db.session.add(new_note)
            db.session.commit()

            # Проверка наличия заметки
            note = Note.query.filter_by(client_id=client.id).first()
            self.assertIsNotNone(note)
            self.assertEqual(note.note, note_content)

    def test_view_client_details(self):
        # Тест на отображение подробностей клиента
        with app.app_context():
            username = f"testuser_{int(time.time())}"  # Уникальное имя пользователя
            hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            client = Client(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", address="Some Address", user_id=user.id)
            db.session.add(client)
            db.session.commit()

            response = self.client.get(url_for('client_details', client_id=client.id))
            self.assertEqual(response.status_code, 200)
            self.assertIn('John Doe', response.data.decode('utf-8'))  # Проверка отображения имени клиента

if __name__ == '__main__':
    unittest.main()
