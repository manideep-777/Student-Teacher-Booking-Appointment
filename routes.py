import logging
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Appointment, Message, Schedule
from forms import (LoginForm, RegistrationForm, TeacherProfileForm, 
                  AppointmentForm, MessageForm, TeacherSearchForm, 
                  ScheduleForm, AdminRegistrationForm, TeacherUpdateForm)

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.role == 'student' and not user.is_approved:
                flash('Your account is pending approval.', 'warning')
                return redirect(url_for('login'))
            login_user(user)
            logger.info(f"User {user.username} logged in successfully")
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        logger.info(f"New user registered: {user.username}")
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        teachers = User.query.filter_by(role='teacher').all()
        students = User.query.filter_by(role='student').all()
        return render_template('admin/dashboard.html', teachers=teachers, students=students)

    elif current_user.role == 'teacher':
        appointments = Appointment.query.filter_by(teacher_id=current_user.id).all()
        messages = Message.query.filter_by(receiver_id=current_user.id).all()
        return render_template('teacher/dashboard.html', appointments=appointments, messages=messages)

    else:  # student
        search_form = TeacherSearchForm()
        teachers_query = User.query.filter_by(role='teacher')

        if search_form.department.data:
            teachers_query = teachers_query.filter(
                User.department.ilike(f"%{search_form.department.data}%")
            )
        if search_form.subject.data:
            teachers_query = teachers_query.filter(
                User.subject.ilike(f"%{search_form.subject.data}%")
            )

        teachers = teachers_query.all()
        appointments = Appointment.query.filter_by(student_id=current_user.id).all()
        return render_template('student/dashboard.html', 
                             teachers=teachers, 
                             appointments=appointments,
                             search_form=search_form)

@app.route('/book_appointment/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(teacher_id):
    if current_user.role != 'student':
        flash('Only students can book appointments', 'danger')
        return redirect(url_for('dashboard'))

    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            student_id=current_user.id,
            teacher_id=teacher_id,
            date=form.date.data,
            time=form.time.data,
            purpose=form.purpose.data
        )
        db.session.add(appointment)
        db.session.commit()
        logger.info(f"New appointment booked by {current_user.username}")
        flash('Appointment request sent!', 'success')
        return redirect(url_for('dashboard'))

    teacher = User.query.get_or_404(teacher_id)
    return render_template('student/book_appointment.html', form=form, teacher=teacher)

@app.route('/approve_appointment/<int:appointment_id>')
@login_required
def approve_appointment(appointment_id):
    if current_user.role != 'teacher':
        flash('Unauthorized action', 'danger')
        return redirect(url_for('dashboard'))

    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'approved'
    db.session.commit()
    logger.info(f"Appointment {appointment_id} approved by {current_user.username}")
    flash('Appointment approved!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/send_message/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def send_message(receiver_id):
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            content=form.content.data
        )
        db.session.add(message)
        db.session.commit()
        logger.info(f"Message sent from {current_user.username}")
        flash('Message sent!', 'success')
        return redirect(url_for('dashboard'))

    receiver = User.query.get_or_404(receiver_id)
    return render_template('send_message.html', form=form, receiver=receiver)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'teacher':
        flash('Access denied. Only teachers can update their profiles.', 'danger')
        return redirect(url_for('dashboard'))

    form = TeacherProfileForm()
    if form.validate_on_submit():
        current_user.department = form.department.data
        current_user.subject = form.subject.data
        db.session.commit()
        logger.info(f"Teacher {current_user.username} updated their profile")
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    # Pre-populate form with current data
    if request.method == 'GET':
        form.department.data = current_user.department
        form.subject.data = current_user.subject

    return render_template('teacher/profile.html', form=form)

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def manage_schedule():
    if current_user.role != 'teacher':
        flash('Only teachers can manage schedules', 'danger')
        return redirect(url_for('dashboard'))

    form = ScheduleForm()
    if form.validate_on_submit():
        schedule = Schedule(
            teacher_id=current_user.id,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(schedule)
        db.session.commit()
        logger.info(f"Teacher {current_user.username} added new schedule")
        flash('Schedule added successfully!', 'success')
        return redirect(url_for('manage_schedule'))

    schedules = Schedule.query.filter_by(teacher_id=current_user.id).order_by(Schedule.date).all()
    return render_template('teacher/schedule.html', form=form, schedules=schedules)

@app.route('/schedule/delete/<int:schedule_id>')
@login_required
def delete_schedule(schedule_id):
    if current_user.role != 'teacher':
        flash('Unauthorized action', 'danger')
        return redirect(url_for('dashboard'))

    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.teacher_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(schedule)
    db.session.commit()
    flash('Schedule deleted successfully!', 'success')
    return redirect(url_for('manage_schedule'))

@app.route('/admin/add_teacher', methods=['POST'])
@login_required
def add_teacher():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    username = request.form.get('username')
    email = request.form.get('email')
    department = request.form.get('department')
    subject = request.form.get('subject')
    password = request.form.get('password')

    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'danger')
        return redirect(url_for('dashboard'))

    teacher = User(
        username=username,
        email=email,
        role='teacher',
        department=department,
        subject=subject,
        is_approved=True
    )
    teacher.set_password(password)

    db.session.add(teacher)
    db.session.commit()
    logger.info(f"Admin {current_user.username} added new teacher: {username}")
    flash('Teacher added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/delete_teacher/<int:teacher_id>')
@login_required
def delete_teacher(teacher_id):
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    teacher = User.query.get_or_404(teacher_id)
    if teacher.role != 'teacher':
        flash('Invalid teacher ID', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(teacher)
    db.session.commit()
    logger.info(f"Admin {current_user.username} deleted teacher: {teacher.username}")
    flash('Teacher deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/approve_student/<int:student_id>')
@login_required
def approve_student(student_id):
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    student = User.query.get_or_404(student_id)
    if student.role != 'student':
        flash('Invalid student ID', 'danger')
        return redirect(url_for('dashboard'))

    student.is_approved = True
    db.session.commit()
    logger.info(f"Admin {current_user.username} approved student: {student.username}")
    flash('Student approved successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    # Check if admin already exists
    if User.query.filter_by(role='admin').first():
        flash('Admin already exists', 'danger')
        return redirect(url_for('login'))

    form = AdminRegistrationForm()
    if form.validate_on_submit():
        admin = User(
            username=form.username.data,
            email=form.email.data,
            role='admin',
            is_approved=True
        )
        admin.set_password(form.password.data)
        try:
            db.session.add(admin)
            db.session.commit()
            logger.info(f"Admin user created: {admin.username}")
            flash('Admin account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Error creating admin user: {str(e)}")
            db.session.rollback()
            flash('Error creating admin account. Please try again.', 'danger')

    return render_template('create_admin.html', form=form)


@app.route('/admin/update_teacher/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def update_teacher(teacher_id):
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    teacher = User.query.get_or_404(teacher_id)
    if teacher.role != 'teacher':
        flash('Invalid teacher ID', 'danger')
        return redirect(url_for('dashboard'))

    form = TeacherUpdateForm()

    if request.method == 'GET':
        form.username.data = teacher.username
        form.email.data = teacher.email
        form.department.data = teacher.department
        form.subject.data = teacher.subject

    if form.validate_on_submit():
        existing_email = User.query.filter(User.email == form.email.data, User.id != teacher_id).first()
        if existing_email:
            flash('Email already registered', 'danger')
            return redirect(url_for('update_teacher', teacher_id=teacher_id))

        teacher.username = form.username.data
        teacher.email = form.email.data
        teacher.department = form.department.data
        teacher.subject = form.subject.data

        try:
            db.session.commit()
            logger.info(f"Admin {current_user.username} updated teacher: {teacher.username}")
            flash('Teacher updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            logger.error(f"Error updating teacher: {str(e)}")
            db.session.rollback()
            flash('Error updating teacher. Please try again.', 'danger')

    return render_template('admin/update_teacher.html', form=form, teacher=teacher)