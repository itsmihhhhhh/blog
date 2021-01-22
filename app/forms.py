from flask_wtf import Form
from wtforms import StringField, BooleanField,  TextAreaField, SelectMultipleField, SelectField, TextField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed


from .models import User, Blog, Category


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    username = TextField('username', validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('email', validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])

class BlogForm(Form):
    title = TextField('Title', validators=[DataRequired()])
    body = TextAreaField('Description', validators=[DataRequired(), Length(max=2000)])

class PasswordForm(Form):
    cur_password = PasswordField('password', validators=[DataRequired()])
    password = PasswordField('new password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
