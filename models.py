
from flask_login import UserMixin
from werkzeug.security import generate_password_hash ,check_password_hash

from extensions import db 


    
class user_table(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    student = db.relationship('Student', backref=db.backref('user_table', uselist=False)) 
    is_student = db.Column(db.Boolean , default = True)
    is_admin = db.Column(db.Boolean, default=False ) 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
        return self.id
    def is_active(self):
        return True
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(), nullable=False)
    Date_of_birth = db.Column(db.Date, nullable=False)
    Gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer , nullable = False)
    Nationality = db.Column(db.String, nullable=False)
    Address = db.Column(db.String, nullable=False)
    Phone_number = db.Column(db.String, nullable=False)
    Email = db.Column(db.String)
    Class = db.Column(db.String, nullable=False)
    student_activity = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))