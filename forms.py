from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SubmitField

class LessonForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    order = IntegerField('Порядок', validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    is_published = BooleanField('Опубликовано')
    submit = SubmitField('Сохранить урок')

class AssignmentForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    tests = StringField('Тесты', validators=[DataRequired()])
    difficulty = StringField('Сложность', validators=[DataRequired()])
    is_published = BooleanField('Опубликовано', validators=[DataRequired()])
    submit = SubmitField('Сохранить задание')  # Добавлено

class SubmissionForm(FlaskForm):
    code = StringField('Код', validators=[DataRequired()])
    submit = SubmitField('Отправить решение')  # Добавлено
