from flask import Blueprint , render_template ,redirect ,request, session  , url_for ,flash
from flask_login import login_manager , login_user , LoginManager ,logout_user ,login_required
from models import user_table  , Student
check_bp = Blueprint('check' ,__name__  , url_prefix="/check")
from extensions import db

@check_bp.route('/')
def checkbl():
    return render_template('login.html')


@check_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Kiểm tra người dùng là admin_user hay User
        user = user_table.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if user.is_admin:
                login_user(user)
                session['user'] = user.id
                current_user = user
                return redirect(url_for('main.students'))
            elif( user.is_admin == False) and (user.is_student == True):
                login_user(user)
                session['user'] = user.id
                current_user = user
                user_id = user.id
                print(user.id)
                student = Student.query.filter_by(user_id=user.id).first()
                print(type(student))
                return redirect(url_for('main.student_detail', id = student.id))
        else:
            flash('Invalid username or password')  # Thêm thông báo lỗi
    return render_template('login.html')

@check_bp.route('/signup' , methods  = ['GET' , 'POST'])
def signup():
    existing_user = user_table.query.all()
    if not  existing_user:
        if request.method == 'POST':
            username = request.form['username'] 
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password == confirm_password:
                new_user = user_table(username = username,is_admin = True ,is_student = False)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                return   redirect(url_for('check.login'))
            else:
                return flash('something wrong')
        else:
            return render_template('signup.html')
    else:
       return render_template('login.html')
@check_bp.route('/logout' , methods = ['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('check.login'))   