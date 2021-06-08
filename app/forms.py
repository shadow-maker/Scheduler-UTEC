from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import SubmitField
from wtforms.validators import EqualTo, InputRequired, Length

class loginform(FlaskForm):
    id_utec = StringField('id_utec', validators=[InputRequired(),Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=4, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')

class registerform(FlaskForm):
    name = StringField('name', validators=[InputRequired(),Length(min=4, max=20)])
    last_name = StringField('last_name', validators=[InputRequired(),Length(min=4, max=20)])
    correo = StringField('correo', validators=[InputRequired(),Length(min=4, max=40)])
    id_utec = StringField('id_utec', validators=[InputRequired(),Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=4, max=20)])
    repeat_password = PasswordField('repeat_password', validators=[InputRequired(),EqualTo('password')])
    submit = SubmitField('Submit')