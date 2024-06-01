from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    surname = db.Column(db.String(150), nullable=False)
    otherNames = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150))
    department = db.Column(db.String(150), nullable=False)
    is_instructor = db.Column(db.Boolean, default=False)
