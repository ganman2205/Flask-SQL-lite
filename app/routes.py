
from flask import Blueprint, jsonify, request
from app.models import Student, db

students_bp = Blueprint('students', __name__)

# Route to show the list of students
@students_bp.route("/show", methods=['GET'])
def show_student_list():
    students = Student.query.all()
    student_list = [{'roll_number': student.roll_number, 'name': student.name} for student in students]
    response_data = {
        "message": f"{len(student_list)} students found.",
        "student list": student_list,
    }
    return jsonify(response_data), 200

# Route to add a student
@students_bp.route("/add/<string:roll_number>", methods=['POST'])
def add_student(roll_number):
    data = request.get_json()

    # Check if required fields are present in the request
    if 'name' not in data:
        return jsonify({"error": "Name is a required field."}), 400

    new_student = Student(roll_number=roll_number, name=data['name'])

    # Add the new student to the database
    db.session.add(new_student)
    db.session.commit()

    response_data = {
        'message': 'Student added successfully!',
        'student': {'roll_number': new_student.roll_number, 'name': new_student.name},
    }
    return jsonify(response_data), 201

# Route to delete a student
@students_bp.route("/delete/<string:roll_number>", methods=['DELETE'])
def delete_student(roll_number):
    student = Student.query.filter_by(roll_number=roll_number).first()

    if student:
        # Delete the student from the database
        db.session.delete(student)
        db.session.commit()

        response_data = {
            'message': f'Student with roll number {roll_number} deleted successfully!',
        }
        return jsonify(response_data), 200
    else:
        response_data = {
            'message': f'No student found with roll number {roll_number}',
        }
        return jsonify(response_data), 404
