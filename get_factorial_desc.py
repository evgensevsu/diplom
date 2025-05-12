from app import app
from models import Assignment

with app.app_context():
    assignment = Assignment.query.get(3)
    print('Описание задания:')
    print(assignment.description)