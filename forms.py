from wtforms import StringField, PasswordField, EmailField, validators
from wtforms.form import Form


class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=6, max=20)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=20)])


class RegisterForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=6, max=20)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=20)])
    repeat_password = PasswordField('New Password', [validators.InputRequired(), validators.EqualTo('password', message='Passwords must match')])
