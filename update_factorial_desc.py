from app import app, db
from models import Assignment

with app.app_context():
    assignment = Assignment.query.get(3)
    if assignment:
        old_description = assignment.description
        new_description = old_description + "\n\nВАЖНО: Функция должна ВОЗВРАЩАТЬ результат с помощью оператора return, а не печатать его с помощью print. При проверке будет вызвана функция factorial(n) и проверено возвращаемое значение."
        
        print("Старое описание:")
        print(old_description)
        print("\nНовое описание:")
        print(new_description)
        
        # Обновляем описание
        assignment.description = new_description
        db.session.commit()
        print("\nОписание задания успешно обновлено!")