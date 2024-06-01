from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from . import db
from datetime import datetime

views = Blueprint('views', __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    if current_user.is_instructor:
        return render_template('instructor_home.html')
    else:
        return render_template('student_home.html')
