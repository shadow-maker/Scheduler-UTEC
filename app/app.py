import json
import sys

from sqlalchemy.orm import backref
from enum import unique, Enum
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from . import config
from . import forms
# -------------------
# Configuracion Flask
# -------------------

app = Flask(__name__)
app.config['SECRET_KEY']='projectodb'
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)
login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# ------
# Tablas
# ------

class TipoClaseEnum(Enum):
    lab = 0
    teoria = 1
    teoria_virtual = 2

class Alumno(UserMixin,db.Model):
    __tablename__ = 'alumno'
    codigo      = db.Column(db.Integer      , primary_key=True)
    correo      = db.Column(db.String(255)  , nullable=False, unique=True)
    password    = db.Column(db.String(64)   , nullable=False)
    nombre      = db.Column(db.String(64)   , nullable=False)
    apellido    = db.Column(db.String(64)   , nullable=False)
    horarios    = db.relationship('Horario', backref='alumno', lazy=True)

    def __repr__(self):
        return f'<Alumno: {self.codigo} - {self.apellido}, {self.nombre}>'

#-----
# Login Authentication
#-----

@login_manager.user_loader
def load_user(user_codigo):
    return Alumno.query.get(user_codigo)

class Docente(db.Model):
    __tablename__ = 'docente'
    codigo          = db.Column(db.Integer      , primary_key=True)
    correo          = db.Column(db.String(255)  , nullable=False, unique=True)
    nombre          = db.Column(db.String(64)   , nullable=False)
    apellido        = db.Column(db.String(64)   , nullable=False)
    clases          = db.relationship('Clase', backref='docente', lazy=True)

    def __repr__(self):
        return f'<Docente: {self.codigo} - {self.apellido}, {self.nombre}>'

class Curso(db.Model):
    __tablename__ = 'curso'
    codigo          = db.Column(db.String(6)    , primary_key=True)
    curso           = db.Column(db.String(255)  , nullable=False)
    lab             = db.Column(db.Boolean      , nullable=False)
    teoria          = db.Column(db.Boolean      , nullable=False)
    teoria_virutal  = db.Column(db.Boolean      , nullable=False)
    clases          = db.relationship('Clase', backref='curso', lazy=True)

    def __repr__(self):
        return f'<Docente: {self.codigo} - {self.curso}>'

class Clase(db.Model):
    __tablename__ = 'clase'
    curso_codigo    = db.Column(db.String(6)    , db.ForeignKey('curso.codigo')     , primary_key=True)
    tipo            = db.Column(db.Enum(TipoClaseEnum)                              , primary_key=True)
    seccion         = db.Column(db.String(2)    , primary_key=True)
    numero          = db.Column(db.String(2)    , primary_key=True)
    vacantes        = db.Column(db.Integer      , nullable=False)
    docente_codigo  = db.Column(db.Integer      , db.ForeignKey('docente.codigo')   , nullable=True)        # Null para cuando aun no se sabe el docente
    sesiones        = db.relationship('Sesion', backref='clase', lazy=True)

    def __repr__(self):
        return f'<Clase: {self.curso_codigo}, {self.tipo}, {self.seccion}, {self.numero}>'

class Sesion(db.Model):
    __tablename__ = 'sesion'
    curso_codigo    = db.Column(db.String(6)    , primary_key=True)
    clase_tipo      = db.Column(db.Enum(TipoClaseEnum)                              , primary_key=True) 
    clase_seccion   = db.Column(db.String(2)    , primary_key=True)
    clase_numero    = db.Column(db.String(2)    , primary_key=True)
    id              = db.Column(db.Integer      , primary_key=True)
    dia             = db.Column(db.Integer      , nullable=False) #Cambiar formato?
    hora_inicio     = db.Column(db.Integer      , nullable=False) #Cambiar formato?
    hora_fin        = db.Column(db.Integer      , nullable=False) #Cambiar formato?
    # Implementar frecuencia tambien
    # Llave foranea compuesta a Clase
    __table_args__  = (db.ForeignKeyConstraint(
                            [curso_codigo, clase_tipo, clase_seccion, clase_numero],
                            ['clase.curso_codigo', 'clase.tipo', 'clase.seccion', 'clase.numero']
                        ),
                        {},
                      )

    def __repr__(self):
        return f'<Clase: {self.curso_codigo}, {self.clase_tipo}, {self.clase_seccion}, {self.clase_numero}, {self.id}>'

class Horario(db.Model):
    __tablaname__ = 'horario'
    id              = db.Column(db.Integer      , primary_key=True)
    alumno_codigo   = db.Column(db.Integer      , db.ForeignKey('alumno.codigo')    , nullable=False)
    #Agregar talvez tmb fecha de creacion?
    def __repr__(self):
        return f'<Clase: {self.id}>'


class Lista(db.Model):
    __tablename__ = 'lista'
    horario_id      = db.Column(db.Integer      , db.ForeignKey('horario.id')       , primary_key=True)
    curso_codigo    = db.Column(db.String(6)    , primary_key=True)
    clase_tipo      = db.Column(db.Enum(TipoClaseEnum)                              , primary_key=True) 
    clase_seccion   = db.Column(db.String(2)    , primary_key=True)
    clase_numero    = db.Column(db.String(2)    , primary_key=True)
    # Llave foranea compuesta a Clase
    __table_args__  = (db.ForeignKeyConstraint(
                            [curso_codigo, clase_tipo, clase_seccion, clase_numero],
                            ['clase.curso_codigo', 'clase.tipo', 'clase.seccion', 'clase.numero']
                        ),
                        {},
                      )
                      
    def __repr__(self):
        return f'<Lista: {self.horario_id} - {self.curso_codigo}, {self.clase_tipo}, {self.clase_seccion}, {self.clase_numero}>'

class Favorito(db.Model):
    __tablename__ = 'favorito'
    horario_id      = db.Column(db.Integer      , db.ForeignKey('horario.id')       , primary_key=True)
    alumno_codigo   = db.Column(db.Integer      , db.ForeignKey('alumno.codigo')    , primary_key=True)
    def __repr__(self):
        return f'<Lista: {self.horario_id}, {self.alumno_codigo}>'

db.create_all() # Crear tablas en bd

# ------
# ROUTES
# ------

# --- Horarios ---
@app.route('/horarios/list')
def horarios_list():
    horarios = Horario.query.all()
    return render_template('horarios/list.html',data=horarios)
    
@app.route('/horarios/create')
def horarios_create():
    error = False
    alumno_codigo = 202010387 # TEMPORAL: El codigo de alumno debe salir del auth actual
    try:
        horario = Horario(alumno_codigo=alumno_codigo)
        db.session.add(horario)
        db.session.commit()
        horario_id = horario.id
    except:
        db.session.rollback()
        print(sys.exc_info())
        error = True
    finally:
        db.session.close()

    if error:
        return 'No se pudo crear el horario' # MEJORAR RESPUESTA DE ERROR
    else:
        return redirect(  url_for('horarios_update', id=horario_id) )

@app.route('/horarios/update/<id>')
def horarios_update(id):
    error =False
    alumno_codigo = 202010387 # TEMPORAL: El codigo de alumno debe salir del auth actual
    info = Curso.query.all()

    try:
        horario = Horario.query.get(id)
    except:
        error = True

    if error:
        return 'Url no valida' # MEJORAR RESPUESTA DE ERROR
    elif horario==None:
        return 'El horario que se busca no existe' # MEJORAR RESPUESTA DE ERROR
    else:
        return render_template('horarios/update.html', data=info, horario=horario)

@app.route('/horarios/delete/<id>')
def horarios_delete(id):
    error =False
    alumno_codigo = 202010387 # TEMPORAL: El codigo de alumno debe salir del auth actual

    try:
        horario = Horario.query.get(id)
    except:
        return 'Url no valida' # MEJORAR RESPUESTA DE ERROR

    if horario == None:
        return 'El horario que se busca no existe' # MEJORAR RESPUESTA DE ERROR
    
    if horario.alumno_codigo != alumno_codigo:
        return 'No tiene permisos para eliminar este horario'

    try:
        horario_id = horario.id
        db.session.delete(horario)
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
        error = True
    finally:
        db.session.close()

    if error:
        return 'No se pudo eliminar el horario' # MEJORAR RESPUESTA DE ERROR
    else:
        return f'Se elimino correctamente el horario {horario_id}' # MEJORAR RESPUESTA DE EXITO

@app.route('/horarios/view/<id>')
def horarios_view(id):
    error =False
    try:
        horario = Horario.query.get(id)
    except:
        error = True

    if error:
        return 'Url no valida' # MEJORAR RESPUESTA DE ERROR
    elif horario==None:
        return 'El horario que se busca no existe' # MEJORAR RESPUESTA DE ERROR
    else:
        return render_template('horarios/view.html', horario=horario)

# --- Authetificacion ---
@app.route('/auth/login/', methods=['GET','POST'])
def login():
    form=forms.loginform()
    if form.validate_on_submit():
        user = Alumno.query.filter_by(codigo=form.id_utec.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user,remember=form.remember.data)
                return "Coneccion Exitosa"
        return "CUENTA INCORRECTA"
    return render_template('auth/login.html',form=form)

@app.route('/auth/register/', methods=['GET','POST'])
def register():
    form=forms.registerform()
    if form.validate_on_submit():
        new_user = Alumno(codigo=form.id_utec.data, correo=form.correo.data, password=form.password.data,
        nombre=form.name.data, apellido=form.last_name.data )
        db.session.add(new_user)
        db.session.commit()
        return "HOLA"
    return render_template('auth/register.html', form=form)

# Alumno
@app.route('/')
@login_required
def menu_inicio(id):
    return 'Solo los registrados entran aca'

@app.route('/alumnos/list')
def alumnos_list(id):
    alumnos = Alumno.query.all()
    return 'temp'

@app.route('/alumnos/view/<id>')
def alumnos_view(id):
    alumno = Alumno.query.get(id)
    return 'temp'

@app.route('/alumnos/update/<id>')
def alumnos_update(id):
    return 'temp'

@app.route('/alumnos/delete/<id>')
def alumnos_delete(id):
    return 'temp'


