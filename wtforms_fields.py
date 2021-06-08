from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email
from wtforms.widgets.core import Input

class loginform(FlaskForm):
    username=StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])