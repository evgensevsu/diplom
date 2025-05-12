from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Добавлен атрибут is_active

    def __repr__(self):
        return f"<User {self.username}>"


class Lesson(db.Model):
    __tablename__ = 'lesson'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)  # Используем "order" как имя столбца
    is_published = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)  # Новое поле для отслеживания завершенности урока
    date_completed = db.Column(db.DateTime, nullable=True)  # Дата завершения урока

    def __repr__(self):
        return f'<Lesson {self.title}>'

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tests = db.Column(db.Text, nullable=False)  # JSON string of test cases
    difficulty = db.Column(db.String(20), default="Medium")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)

    submissions = db.relationship('Submission', backref='assignment', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Assignment('{self.title}', difficulty={self.difficulty})"

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False, default="Аноним")
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(20), default="Not evaluated")
    feedback = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Submission(student_name='{self.student_name}', assignment_id={self.assignment_id}, result='{self.result}')"
