from datetime import datetime
from app.utils.database import db

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class Employee(db.Model):
#     __tablename__ = 'employees'
#     id = db.Column(db.Integer, primary_key=True)
#     emp_id = db.Column(db.Integer, unique=True, nullable=False)
#     emp_name = db.Column(db.String(100), nullable=False)
#     emp_email = db.Column(db.String(100), unique=True, nullable=False)
#     emp_password = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    host_id = db.Column(db.Integer, nullable=False)
    attendees = db.Column(db.JSON)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    agenda = db.Column(db.Text)
    meeting_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)