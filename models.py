from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    date_of_registration = db.Column(db.DateTime, nullable=False, default=datetime.now())

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    date_added = db.Column(db.DateTime, default=datetime.now())
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)
