from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Course, Enrollment
from datetime import datetime

views = Blueprint('views', __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    if current_user.is_instructor:
        courses = Course.query.filter_by(instructor_name=current_user.otherNames)
        return render_template('instructor_home.html', courses=courses)
    else:
        return render_template('student_home.html')

@views.route('/view-courses')
def view_courses():
    enrolled_courses = Enrollment.query.filter_by(user_id=current_user.id).all()
    return render_template('view_courses.html', enrolled_courses=enrolled_courses)

@views.route('/create-course', methods=['GET', 'POST'])
def create_courses():
    if request.method == 'POST':
        title = request.form.get('title')
        code = request.form.get('code')
        description = request.form.get('description')
        instructor_name = current_user.otherNames
        course = Course.query.filter_by(title=title).first()
        if course:
            flash('Course already exist', category='error')
        else:
            # add user to database
            new_course = Course(title=title, code=code, description=description, instructor_name=instructor_name)
            db.session.add(new_course)
            db.session.commit()

            flash('Course created', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_course.html')

@views.route('/manage-course/<id>', methods=['GET', 'POST'])
def manage_courses(id):
    course = Course.query.filter_by(id=id).first()
    return render_template('manage_course.html', course=course)

@views.route('/enroll-course', methods=['GET', 'POST'])
def enroll_course():
    courses = Course.query.all()
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        print(f"Selected Course ID: {course_id}")

        if course_id:
            course = Course.query.get(course_id)
            if course:
                new_enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
                db.session.add(new_enrollment)
                db.session.commit()
                flash('You have successfully enrolled in the course!', 'success')
            else:
                flash('Course not found.', 'danger')
        else:
            flash('Invalid course selection.', 'danger')
    return render_template('enroll_course.html', courses=courses)