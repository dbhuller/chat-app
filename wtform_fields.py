from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    """ Registration Form """

    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=16, message="Username must be between 4 and 16 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=6, max=16, message="Password must be between 6 and 16 characters")])
    confirm_password = PasswordField('confirm_password_lable', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')
