# blueprints/main.py
from flask import Blueprint, render_template ,request , redirect , url_for ,session
from flask_login import current_user ,login_manager , LoginManager , login_user , UserMixin , logout_user , login_required
from datetime import datetime 
from email_validator import validate_email, EmailNotValidError
from extensions import db
from models import Student ,user_table
main_bp = Blueprint('main', __name__ )

@main_bp.route('/')
@login_required
def students():
    if current_user.is_admin:
        students = Student.query.all()
        return render_template('students.html', students=students)
    else:
        return redirect(url_for('check.login'))


@main_bp.route('/add', methods=['GET' ,  'POST'])

def add_student():
    
    if request.method == 'POST':
        Name = request.form['name']
        Date_of_birth = request.form['birthday']
        Date_of_birth = datetime.strptime(Date_of_birth, '%Y-%m-%d').date()
        today = datetime.now().date().year
        age = today  - Date_of_birth.year 
        Gender = request.form['Gender']
        Nationality = request.form['nationality']
        Address = request.form['address']
        Phone_number = request.form['phonenumber']
        Email = request.form['email']
        Class = request.form['Class']
        username = request.form['username']
        password = request.form['password']       
        try:
            valid_email = validate_email(Email)
            # Tạo người dùng mới
            user = user_table(username=username)
            user.set_password(password)
            db.session.add(user)

            db.session.flush()
            # Tạo học sinh mới và liên kết với người dùng
            student = Student(Name=Name, Date_of_birth=Date_of_birth, Gender=Gender,age  = age, Nationality=Nationality,
                              Address=Address, Phone_number=Phone_number, Email=valid_email.email, Class=Class, user_id=user.id)
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('main.students'))
        except EmailNotValidError:
            return 'Invalid email address!'       
    else:
        return render_template('add.html')

#--------------------------------------------
@main_bp.route('/students/<int:id>')
@login_required
def student_detail(id):
    student = Student.query.get(id)
    return render_template('student_detail.html', student=student)
#-----------------------------------------------------------------
@main_bp.route('/students/<int:id>/update' , methods = ['GET' , 'POST'])
@login_required
def update_student(id):
    student = Student.query.get(id)
    if request.method == 'POST':
        student.Name  = request.form['Name']
        student.Date_of_birth  = request.form['BirthDay']
        student.Gender  = request.form['Gender']
        student.Nationality  = request.form['Nationality']
        student.Address  = request.form['Address']
        student.Phone_number  = request.form['Phone_number']
        student.Email  = request.form['Email']
        student.Class  = request.form['Class']
        db.session.commit()
        return redirect(url_for('main.students'))
    else:
        return render_template('update.html', student=student)
#----------------------------------------------------------------------
@main_bp.route('/students/<int:id>/delete', methods=['POST' , 'GET'])
@login_required
def delete_student(id):
    student = Student.query.get(id)
    user = user_table.query.get(student.user_id)
    db.session.delete(student)
    db.session.delete(user)  # Xóa cả bản ghi người dùng
    db.session.commit()
    return redirect(url_for('main.students'))
#-------------------------------------------
@main_bp.route('/update_activity/<int:id>', methods=['POST', 'GET'])
@login_required
def update_activity(id):
    stu = Student.query.get(id)
    if request.method == 'POST':
        new_activity = request.form['activity']
        if current_user.is_admin == True: 
            if stu.student_activity:
                stu.student_activity = stu.student_activity + '\n' + "admin"  + ': ' + new_activity
            else:
                stu.student_activity = "admin" + ': ' + new_activity
        else:          
            if stu.student_activity:
                stu.student_activity = stu.student_activity + '\n' + stu.Name + ': ' + new_activity
            else:
                stu.student_activity = stu.Name + ':' + new_activity
        db.session.commit()
        return render_template('student_detail.html', student=stu)
    
    return redirect(url_for('student_detail.html'))

 