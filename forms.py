from wtforms import StringField, PasswordField, EmailField, validators
from wtforms.form import Form


class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=6, max=20)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=20)])


class RegisterForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=6, max=20)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=20)])
    repeat_password = PasswordField('Repeat_password',
                                    validators=[validators.DataRequired(), validators.Length(min=6, max=20)])
    # email = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
