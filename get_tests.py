from app import app
from models import Assignment

with app.app_context():
    assignment = Assignment.query.get(1)
    if assignment:
        print(f"Tests for assignment '{assignment.title}':")
        print(assignment.tests)
    else:
        print("No assignment found with ID 1")