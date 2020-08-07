# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm
# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


# Login Class Form
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


# Register Class Form
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
