from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Lesson, Assignment, Submission
from forms import LessonForm, AssignmentForm, SubmissionForm
from datetime import datetime
import json
from code_execution import execute_code
from code_analysis import analyze_code, get_learning_resources
from analytics import generate_performance_chart, generate_difficulty_distribution, generate_topic_performance
from flask import jsonify
# Инициализация объектов
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diplom.db'
db.init_app(app)  # Инициализация базы данных
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Функция загрузки пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Основные маршруты для входа и регистрации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))  # Перенаправление на dashboard
        else:
            flash('Неверный логин или пароль', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрированы! Пожалуйста, войдите в систему.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # Выход пользователя
    flash('Вы успешно вышли из системы.', 'info')
    return redirect(url_for('login'))  # Перенаправление на страницу входа

# Стартовая страница (перенаправление на dashboard)
@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))  # Перенаправление на страницу dashboard

# Маршрут для Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Получаем количество уроков, заданий и решений
    lesson_count = Lesson.query.count()  # Количество уроков
    assignment_count = Assignment.query.count()  # Количество заданий
    submission_count = Submission.query.count()  # Количество решений

    # Получаем завершенные уроки
    completed_lessons = Lesson.query.filter_by(is_completed=True).count()  # Количество завершенных уроков

    # Вычисляем прогресс
    progress_percentage = (completed_lessons / lesson_count) * 100 if lesson_count > 0 else 0

    # Получаем последние 5 уроков и заданий
    lessons = Lesson.query.order_by(Lesson.date_created.desc()).limit(5).all()
    assignments = Assignment.query.order_by(Assignment.date_created.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        lesson_count=lesson_count,
        assignment_count=assignment_count,
        submission_count=submission_count,
        lessons=lessons,
        assignments=assignments,
        completed_lessons=completed_lessons,
        progress_percentage=progress_percentage
    )

@app.route('/lessons')
@login_required
def lessons():
    lessons = Lesson.query.all()  # Получаем все уроки из базы данных
    return render_template('lessons.html', lessons=lessons)

@app.route('/assignments')
@login_required
def assignments():
    assignments = Assignment.query.all()  # Получаем все задания из базы данных
    return render_template('assignments.html', assignments=assignments)



@app.route('/admin_panel')
@login_required
def admin_panel():
    return render_template('admin_panel.html')  # шаблон для панели администратора


@app.route('/analytics')
def analytics_dashboard():
    assignments = Assignment.query.all()
    submissions = Submission.query.all()

    # Генерация графиков успеваемости
    performance_chart = generate_performance_chart(submissions, 'line')
    performance_bar = generate_performance_chart(submissions, 'bar')
    performance_pie = generate_performance_chart(submissions, 'pie')

    # Генерация распределения по сложности
    difficulty_chart = generate_difficulty_distribution(assignments, submissions)

    # Генерация тепловой карты по темам
    topics_chart = generate_topic_performance(assignments, submissions)

    return render_template(
        'analytics.html',
        title='Аналитика обучения',
        performance_chart=performance_chart,
        performance_bar=performance_bar,
        performance_pie=performance_pie,
        difficulty_chart=difficulty_chart,
        topics_chart=topics_chart,
        submission_count=len(submissions)
    )


@app.route('/lessons/new', methods=['GET', 'POST'])
def new_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            content=form.content.data,
            order=int(form.order.data),
            is_published=form.is_published.data
        )
        db.session.add(lesson)
        db.session.commit()
        flash('Урок успешно создан!', 'success')
        return redirect(url_for('lessons'))

    # Добавляем пустой параметр lesson=None для поддержки шаблона
    return render_template('lesson_detail.html', title='Новый урок', form=form, legend='Новый урок', lesson=None)


@app.route('/lessons/<int:lesson_id>')
def lesson_detail(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    # Проверяем, опубликован ли урок
    if not lesson.is_published:
        abort(404)

    return render_template(
        'lesson_detail.html',
        title=lesson.title,
        lesson=lesson
    )


@app.route('/lessons/<int:lesson_id>/edit', methods=['GET', 'POST'])
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    form = LessonForm()

    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.content = form.content.data
        lesson.order = int(form.order.data)
        lesson.is_published = form.is_published.data
        lesson.date_updated = datetime.utcnow()
        db.session.commit()
        flash('Урок успешно обновлен!', 'success')
        return redirect(url_for('lesson_detail', lesson_id=lesson.id))

    elif request.method == 'GET':
        form.title.data = lesson.title
        form.content.data = lesson.content
        form.order.data = str(lesson.order)
        form.is_published.data = lesson.is_published

    # Передаем параметр lesson для доступа в шаблоне
    return render_template('lesson_detail.html', title='Редактирование урока', form=form, legend='Редактирование урока',
                           lesson=lesson)


@app.route('/lessons/<int:lesson_id>/complete', methods=['POST'])
def complete_lesson(lesson_id):
    # Найдем урок по ID
    lesson = Lesson.query.get_or_404(lesson_id)

    # Устанавливаем статус завершения урока
    lesson.is_completed = True  # Убедитесь, что у модели Lesson есть поле is_completed
    lesson.date_completed = datetime.utcnow()  # Устанавливаем дату завершения

    # Сохраняем изменения в базе данных
    db.session.commit()

    flash('Урок успешно завершен!', 'success')

    return redirect(url_for('lesson_detail', lesson_id=lesson.id))


@app.route('/lessons/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    # Убедитесь, что у пользователя есть права на удаление урока (например, только администратор или создатель)
    db.session.delete(lesson)
    db.session.commit()

    flash('Урок успешно удален!', 'success')
    return redirect(url_for('lessons'))





@app.route('/assignments/<int:assignment_id>')
def assignment_detail(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

    # Проверяем, опубликовано ли задание
    if not assignment.is_published:
        abort(404)

    # Используем SubmissionForm для отправки решения
    submission_form = SubmissionForm()

    # Проверяем, есть ли уже отправленное решение
    submission = Submission.query.filter_by(assignment_id=assignment_id).order_by(
        Submission.date_submitted.desc()).first()

    return render_template(
        'assignment_detail.html',
        title=assignment.title,
        assignment=assignment,
        form=submission_form,
        submission=submission
    )


@app.route('/assignments/new', methods=['GET', 'POST'])
def new_assignment():
    form = AssignmentForm()
    if form.validate_on_submit():
        # Валидируем формат JSON для тестов
        try:
            json.loads(form.tests.data)
        except json.JSONDecodeError:
            flash('Тестовые случаи должны быть в формате JSON', 'danger')
            return render_template('assignment_detail.html', title='Новое задание', form=form, legend='Новое задание')

        assignment = Assignment(
            title=form.title.data,
            description=form.description.data,
            tests=form.tests.data,
            difficulty=form.difficulty.data,
            is_published=form.is_published.data
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Задание успешно создано!', 'success')
        return redirect(url_for('assignments'))

    # Явно указываем, что submission=None и assignment=None, чтобы избежать ошибок в шаблоне
    return render_template('assignment_detail.html', title='Новое задание', form=form, legend='Новое задание',
                           submission=None, assignment=None)


@app.route('/assignments/<int:assignment_id>/edit', methods=['GET', 'POST'])
def edit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    form = AssignmentForm()

    if form.validate_on_submit():
        # Валидируем формат JSON для тестов
        try:
            json.loads(form.tests.data)
        except json.JSONDecodeError:
            flash('Тестовые случаи должны быть в формате JSON', 'danger')
            return render_template('assignment_detail.html', title='Редактирование задания', form=form,
                                   legend='Редактирование задания', submission=None)

        assignment.title = form.title.data
        assignment.description = form.description.data
        assignment.tests = form.tests.data
        assignment.difficulty = form.difficulty.data
        assignment.is_published = form.is_published.data
        assignment.date_updated = datetime.utcnow()
        db.session.commit()
        flash('Задание успешно обновлено!', 'success')
        return redirect(url_for('assignment_detail', assignment_id=assignment.id))

    elif request.method == 'GET':
        form.title.data = assignment.title
        form.description.data = assignment.description
        form.tests.data = assignment.tests
        form.difficulty.data = assignment.difficulty
        form.is_published.data = assignment.is_published

    # Передаем также assignment для доступа в шаблоне и submission=None чтобы избежать ошибок
    return render_template('assignment_detail.html', title='Редактирование задания', form=form,
                           legend='Редактирование задания', assignment=assignment, submission=None)


@app.route('/assignments/<int:assignment_id>/submit', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

    # Проверяем, опубликовано ли задание
    if not assignment.is_published:
        flash('Это задание еще не доступно', 'danger')
        return redirect(url_for('assignments'))

    # Отладочная информация о запросе
    print("Метод запроса:", request.method)
    print("Данные формы:", request.form)

    if request.method == 'POST':
        try:
            # Получаем код пользователя непосредственно из формы
            code = request.form.get('code', '')

            if not code:
                flash('Пожалуйста, введите решение задания', 'danger')
                return redirect(url_for('assignment_detail', assignment_id=assignment_id))

            # Парсим тесты с проверкой на ошибки
            try:
                tests_json = assignment.tests
                print("Строка тестов:", tests_json)
                tests = json.loads(tests_json)
                print("Содержимое тестов после разбора:", tests)
            except Exception as e:
                flash(f'Ошибка при разборе тестов: {str(e)}', 'danger')
                print(f"Ошибка при разборе тестов: {str(e)}")
                return redirect(url_for('assignment_detail', assignment_id=assignment_id))

            all_passed = True
            feedback = []

            # Обрабатываем каждый тест с проверкой на ошибки
            for i, test in enumerate(tests):
                try:
                    print(f"Обработка теста {i + 1}:", test)
                    input_data = test.get('input', '')
                    expected_output = test.get('expected_output', '')

                    # Числовые входные данные должны быть преобразованы из строки в число, если в тестах хранятся строки
                    try:
                        # Пытаемся преобразовать строковые данные в числа, если возможно
                        if isinstance(input_data, str) and input_data.isdigit():
                            input_data = int(input_data)
                    except:
                        # Если не получилось преобразовать, оставляем как есть
                        pass

                    # Безопасное преобразование ожидаемого результата в строку
                    expected_output_str = str(expected_output).strip() if expected_output is not None else ""

                    # Запускаем код студента
                    result, output = execute_code(code, input_data)

                    if result:
                        # Убираем пробелы в конце для сравнения
                        output = output.strip()

                        # Обрабатываем вывод: если вывод содержит несколько строк, берем последнюю непустую
                        # (это позволяет обрабатывать случаи, когда студент оставил примеры с print)
                        output_lines = output.strip().split("\n")
                        # Удаляем пустые строки в конце
                        while output_lines and not output_lines[-1].strip():
                            output_lines.pop()

                        # Если есть строки в выводе, берем последнюю для сравнения
                        if output_lines:
                            final_output = output_lines[-1].strip()
                        else:
                            final_output = ""

                        # Нормализуем вывод для сравнения: учитываем возможные числовые сравнения
                        try:
                            # Пробуем преобразовать оба значения в числа для более точного сравнения
                            output_num = int(final_output)
                            expected_num = int(expected_output_str)
                            comparison_result = (output_num == expected_num)

                            # Добавляем информацию о том, какую часть вывода использовали для проверки
                            if len(output_lines) > 1:
                                print(f"Для сравнения использована последняя строка вывода: '{final_output}'")
                        except:
                            # Если не получается сравнить как числа, сравниваем как строки
                            comparison_result = (final_output == expected_output_str)

                        if comparison_result:
                            feedback.append(f"Тест {i + 1}: Пройден")
                        else:
                            all_passed = False
                            feedback.append(
                                f"Тест {i + 1}: Не пройден - Ожидалось '{expected_output_str}', получено '{final_output}' (из полного вывода: '{output}')")
                    else:
                        all_passed = False
                        feedback.append(f"Тест {i + 1}: Ошибка - {output}")

                except Exception as e:
                    all_passed = False
                    feedback.append(f"Тест {i + 1}: Ошибка при выполнении теста - {str(e)}")
                    print(f"Ошибка при обработке теста {i + 1}: {str(e)}")

            # Создаем новое представление
            submission = Submission(
                student_name="Ученик",  # Фиксированное имя, т.к. убрали аутентификацию
                assignment_id=assignment_id,
                code=code,
                result="Passed" if all_passed else "Failed",
                # Сохраняем в базе на английском для совместимости с шаблонами
                feedback="\n".join(feedback)
            )
            db.session.add(submission)
            db.session.commit()

            flash('Ваше задание отправлено и проверено!', 'success')

            # Перенаправляем на страницу с информацией о представлении
            return redirect(url_for('view_submission', submission_id=submission.id))

        except Exception as e:
            # Обрабатываем глобальные ошибки
            flash(f'Произошла ошибка при проверке задания: {str(e)}', 'danger')
            print(f"Глобальная ошибка в submit_assignment: {str(e)}")
            return redirect(url_for('assignment_detail', assignment_id=assignment_id))

    # Если метод GET, перенаправляем на страницу задания
    return redirect(url_for('assignment_detail', assignment_id=assignment_id))


@app.route('/submissions/<int:submission_id>')
def view_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    assignment = Assignment.query.get_or_404(submission.assignment_id)

    return render_template(
        'submission.html',
        title=f'Представление для {assignment.title}',
        submission=submission,
        assignment=assignment
    )


@app.route('/analyze_code', methods=['POST'])
def analyze_code_route():
    data = request.get_json()

    if not data or 'code' not in data:
        return jsonify({'success': False, 'error': 'Код не предоставлен'}), 400

    code = data['code']
    assignment_description = data.get('assignment_description', '')
    test_cases = data.get('test_cases', None)

    # Анализ кода
    analysis = analyze_code(code, assignment_description, test_cases)

    # Если у нас есть концепции для изучения, получаем учебные ресурсы
    learning_resources = {}
    if 'learning_concepts' in analysis and analysis['learning_concepts']:
        learning_resources = get_learning_resources(analysis['learning_concepts'])

    return jsonify({
        'success': True,
        'analysis': analysis,
        'learning_resources': learning_resources
    })


@app.route('/code_editor')
def code_editor():
    return render_template('code_editor.html', title='Интерактивный редактор кода')


@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.get_json()

    if not data or 'code' not in data:
        return jsonify({'success': False, 'output': 'Код не предоставлен'}), 400

    code = data['code']
    input_data = data.get('input', '')

    result, output = execute_code(code, input_data)

    return jsonify({'success': result, 'output': output})

# Запуск приложения
if __name__ == '__main__':
    # Создание базы данных, если она не существует
    with app.app_context():
        db.create_all()
    app.run(debug=True)
