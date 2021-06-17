from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length

class loginform(FlaskForm):
    id_utec = StringField('id_utec', validators=[
        InputRequired(message="No se ha ingresado ID UTEC"),
        Length(min=9, max=9, message="Longitud de ID UTEC invalida")
        ])
    password = PasswordField('password', validators=[
        InputRequired(message="No se ha ingresado contraseña"),
        Length(min=1, max=64, message="Longitud de contraseña invalida")
        ])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')

class registerform(FlaskForm):
    name = StringField('name', validators=[
        InputRequired(message="No se ha ingresado un Nombre(s)"),
        Length(min=1, max=64, message="Longitud de nombre invaldia (<=64)")
        ])
    last_name = StringField('last_name', validators=[
        InputRequired(message="No se ha ingresado un Apellido(s)"),
        Length(min=1, max=64, message="Longitud de apellido invaldia (<=64)")
        ])
    correo = StringField('correo', validators=[
        InputRequired(message="No se ha ingresado Correo UTEC"),
        Email(message="El correo ingresado no es un correo valido"),
        Length(min=1, max=255, message="Longitud de correo invaldia (<=255)")
        ])
    id_utec = StringField('id_utec', validators=[
        InputRequired(message="No se ha ingresado ID UTEC"),
        Length(min=9, max=9, message="Longitud de ID UTEC invalida")
        ])
    password = PasswordField('password', validators=[
        InputRequired(message="No se ha ingresado contraseña"),
        Length(min=1, max=64, message="La contraseña ingresada es demasiado larga")
        ])
    repeat_password = PasswordField('repeat_password', validators=[
        InputRequired(message="No se ha ingresado la validacion de contraseña"),
        EqualTo('password', message="Las contraseñas ingresadas no son iguales")
        ])
    submit = SubmitField('Submit')


class updatealumnoform(FlaskForm):
    name = StringField('name', validators=[
        Length(min=1, max=64, message="Longitud de nombre invalida (<=64)")
        ])
    last_name = StringField('last_name', validators=[
        Length(min=1, max=64, message="Longitud de apellido invalida (<=64)")
        ])
    correo = StringField('correo', validators=[
        Email(message="El correo ingresado no es un correo valido"),
        Length(min=1, max=255, message="Longitud de correo invalida (<=255)")
        ])
    submit = SubmitField('Submit')

    def from_alumno(self, alumno):
        self.name.data = alumno.nombre
        self.last_name.data = alumno.apellido
        self.correo.data = alumno.correo

    def populate_alumno(self, alumno):
        alumno.nombre = self.name.data
        alumno.apellido = self.last_name.data
        alumno.correo = self.correo.data
