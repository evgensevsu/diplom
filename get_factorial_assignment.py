from app import app
from models import Assignment

with app.app_context():
    assignments = Assignment.query.all()
    for assignment in assignments:
        print(f"Assignment ID: {assignment.id}, Title: {assignment.title}")
        if assignment.id == 3:  # ID задания с факториалом
            print(f"Tests for factorial assignment:")
            print(assignment.tests)
            break