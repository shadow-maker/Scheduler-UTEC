import json
from sqlalchemy.orm import backref
import config
from enum import unique, Enum
from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

# -------------------
# Configuracion Flask
# -------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)

# ------
# Tablas
# ------

class TipoClaseEnum(Enum):
    lab = 0
    teoria = 1
    teoria_virtual = 2

class Alumno(db.Model):
    __tablename__ = 'alumno'
    codigo      = db.Column(db.Integer      , primary_key=True)
    correo      = db.Column(db.String(255)  , nullable=False, unique=True)
    password    = db.Column(db.String(64)   , nullable=False)
    nombre      = db.Column(db.String(64)   , nullable=False)
    apellido    = db.Column(db.String(64)   , nullable=False)
    horarios    = db.relationship('Horario', backref='alumno', lazy=True)

    def __repr__(self):
        return f'<Alumno: {self.codigo} - {self.apellido}, {self.nombre}>'

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

# Horarios
@app.route('/horarios/list')
def horarios_list():
    horarios = Horario.query.all()
    return render_template('horarios/list.html',data=horarios)

@app.route('/horarios/create')
def horarios_create():
    info = Curso.query.all()
    return render_template('tables.html',data=info)

@app.route('/horarios/update/<id>')
def horarios_update(id):
    return render_template('update.html', id = id)

@app.route('/horarios/delete/<id>')
def horarios_delete(id):
    return 'temp'

@app.route('/horarios/view/<id>')
def horarios_view(id):
    return 'temp'

# Authetificacion
@app.route('/auth/login/')
def login():
    return render_template('login.html')

@app.route('/auth/register/')
def register():
    return render_template('register.html')

# Alumno
@app.route('/alumnos/list')
def horarios_update(id):
    alumnos = Alumno.query.all()
    return 'temp'

@app.route('/alumnos/view/<id>')
def horarios_update(id):
    alumno = Alumno.query.get(id)
    return 'temp'

@app.route('/alumnos/update/<id>')
def horarios_update(id):
    return 'temp'

@app.route('/alumnos/delete/<id>')
def horarios_delete(id):
    return 'temp'


#
# APP EXECUTION
#

if __name__ == '__main__':
    app.run() #(port=5002, debug=True)
#else:
#    print('using global variables from FLASK')
