from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from datetime import datetime

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher')])

class AdminRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class TeacherProfileForm(FlaskForm):
    department = StringField('Department', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])

class TeacherUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    department = StringField('Department', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    submit = SubmitField('Update Teacher')

class AppointmentForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    purpose = TextAreaField('Purpose', validators=[DataRequired()])

class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired()])

class TeacherSearchForm(FlaskForm):
    department = StringField('Department')
    subject = StringField('Subject')
    submit = SubmitField('Search')

class ScheduleForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Add Schedule')