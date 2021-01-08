from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User
from passlib.hash import pbkdf2_sha256

# validate if username and password match existing username and password in DB for login
def invalid_credentials(form, field):
    """ Username and password validation """
    username_entered = form.username.data 
    password_entered = field.data

    # check username is valid
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or Password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or Password is incorrect")

# Registration form fields
class RegistrationForm(FlaskForm):
    """ Registration Form """

    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=16, message="Username must be between 4 and 16 characters")])

    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=6, max=16, message="Password must be between 6 and 16 characters")])

    confirm_password = PasswordField('confirm_password_lable', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])

    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists, please select another username")

# Login form fields
class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField('username_label', validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')

