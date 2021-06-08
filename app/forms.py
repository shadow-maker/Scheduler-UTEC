from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.simple import SubmitField
from wtforms.validators import EqualTo, InputRequired, Email, Length
from wtforms.widgets.core import Input

class loginform(FlaskForm):
    id_utec = StringField('id_utec', validators=[InputRequired(),Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=4, max=20)])
    submit = SubmitField('Submit')

class registerform(FlaskForm):
    name = StringField('name', validators=[InputRequired(),Length(min=4, max=20)])
    last_name = StringField('last_name', validators=[InputRequired(),Length(min=4, max=20)])
    correo = StringField('correo', validators=[InputRequired(),Length(min=4, max=40)])
    id_utec = StringField('id_utec', validators=[InputRequired(),Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=4, max=20)])
    repeat_password = PasswordField('repeat_password', validators=[InputRequired(),EqualTo('password')])
    submit = SubmitField('Submit')