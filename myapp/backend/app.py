from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Using SQLAlchemy
db = SQLAlchemy(app)

# Enabling CORS for the app instance
CORS(app)


# Import models after db is defined
from models import Student, Instructor, Course, Enrollment


# All Routes
"""
    Routes for Student Class
"""
@app.route('/api/students', methods=['GET'])
def get_students():
    print("Fetching students...")
    students = Student.query.all()
    student_list = [{'id': student.id, 'name': student.name, 'credits_earned': student.credits_earned} for student in students]
    return jsonify(student_list)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    student = Student(name=data['name'], credits_earned=data['credits_earned'])
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student added'}), 201

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json
    student = Student.query.get(id)
    student.name = data['name']
    student.credits_earned = data['credits_earned']
    db.session.commit()
    return jsonify({'message': 'Student updated'})

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'})

"""
    Routes for Instructor Class
"""
@app.route('/api/instructors', methods=['GET'])
def get_instructors():
    instructors = Instructor.query.all()
    instructor_list = [{'id': instructor.id, 'name': instructor.name, 'department': instructor.department} for instructor in instructors]
    return jsonify(instructor_list)

@app.route('/api/instructors', methods=['POST'])
def add_instructor():
    data = request.json
    instructor = Instructor(name=data['name'], department=data['department'])
    db.session.add(instructor)
    db.session.commit()
    return jsonify({'message': 'Instructor added'}), 201

@app.route('/api/instructors/<int:id>', methods=['PUT'])
def update_instructor(id):
    data = request.json
    instructor = Instructor.query.get(id)
    if instructor is None:
        return jsonify({'message': 'Instructor not found'}), 404
    instructor.name = data['name']
    instructor.department = data['department']
    db.session.commit()
    return jsonify({'message': 'Instructor updated'})

@app.route('/api/instructors/<int:id>', methods=['DELETE'])
def delete_instructor(id):
    instructor = Instructor.query.get(id)
    if instructor is None:
        return jsonify({'message': 'Instructor not found'}), 404
    db.session.delete(instructor)
    db.session.commit()
    return jsonify({'message': 'Instructor deleted'})

 
"""
    Routes for Course class CRUD
"""
@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    course_list = [{'id': course.id, 'title': course.title, 'instructor_id': course.instructor_id} for course in courses]
    return jsonify(course_list)

@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.json
    course = Course(title=data['title'], instructor_id=data['instructor_id'])
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Course added'}), 201

@app.route('/api/courses/<int:id>', methods=['PUT'])
def update_course(id):
    data = request.json
    course = Course.query.get(id)
    if course is None:
        return jsonify({'message': 'Course not found'}), 404
    course.title = data['title']
    course.instructor_id = data['instructor_id']
    db.session.commit()
    return jsonify({'message': 'Course updated'})

@app.route('/api/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if course is None:
        return jsonify({'message': 'Course not found'}), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted'})

"""
    Routes for Enrollment CRUD
"""
@app.route('/api/enrollments', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.query.all()
    enrollment_list = [
        {
            'id': enrollment.id, 
            'student_id': enrollment.student_id, 
            'course_id': enrollment.course_id,
            'grade': enrollment.grade
        } 
        for enrollment in enrollments
    ]
    return jsonify(enrollment_list)

@app.route('/api/enrollments', methods=['POST'])
def add_enrollment():
    data = request.json
    enrollment = Enrollment(student_id=data['student_id'], course_id=data['course_id'], grade=data['grade'])
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrollment added'}), 201

@app.route('/api/enrollments/<int:id>', methods=['PUT'])
def update_enrollment(id):
    data = request.json
    enrollment = Enrollment.query.get(id)
    if enrollment is None:
        return jsonify({'message': 'Enrollment not found'}), 404
    enrollment.student_id = data['student_id']
    enrollment.course_id = data['course_id']
    enrollment.grade = data['grade']
    db.session.commit()
    return jsonify({'message': 'Enrollment updated'})

@app.route('/api/enrollments/<int:id>', methods=['DELETE'])
def delete_enrollment(id):
    enrollment = Enrollment.query.get(id)
    if enrollment is None:
        return jsonify({'message': 'Enrollment not found'}), 404
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrollment deleted'})

"""
    Populating Database with data
"""
@app.route('/api/populate_db', methods=['GET'])
def populate_db():
    # Adding Students
    students = [
        Student(id=387, name='John Walker', credits_earned=93),
        Student(id=209, name='David Jameson', credits_earned=87),
        Student(id=101, name='Emma Wells', credits_earned=57),
        Student(id=190, name='Nisha Singh', credits_earned=92),
        Student(id=978, name='Jack Thompson', credits_earned=100),
        Student(id=350, name='Ben Joseph', credits_earned=79),
        Student(id=270, name='Kate Jimpson', credits_earned=68)
    ]
    db.session.add_all(students)

    # Adding Instructors
    instructors = [
        Instructor(id=456, name='Jim George', department='Statistics'),
        Instructor(id=589, name='Kevin Mathews', department='Information Systems'),
        Instructor(id=821, name='John Sullins', department='Health Sciences'),
        Instructor(id=954, name='William Robertson', department='Physics'),
        Instructor(id=673, name='Sandra Wilson', department='Biology'),
        Instructor(id=535, name='Donna Joseph', department='Computer Science'),
        Instructor(id=990, name='Natalia Smith', department='Chemistry')
    ]
    db.session.add_all(instructors)

    # Adding Courses
    courses = [
        Course(id=9076, title='Software Engineering', instructor_id=535),
        Course(id=1028, title='Organic Chemistry I', instructor_id=990),
        Course(id=7654, title='Health Informatics', instructor_id=821),
        Course(id=8721, title='Database Systems', instructor_id=589)
    ]
    db.session.add_all(courses)

    # Committing the changes
    db.session.commit()

    return jsonify({'message': 'Database populated'})



if __name__ == "__main__":
    db.create_all()  # creates database and the table
    app.run(debug=True)
