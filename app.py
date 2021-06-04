import json
from enum import unique, Enum
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

class TipoClaseEnum(Enum):
    lab = 0
    teoria = 1
    teoria_virtual = 2

# Configuracion de conexion a Base de Datos
db_type     = 'postgresql'
db_host     = 'localhost'
db_port     = '5432'
db_name     = 'utecscheduler'
db_user     = 'postgres'
db_password = input('Password: ')

# Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tablas
class Alumno(db.Model):
    __tablename__ = 'alumno'
    codigo      = db.Column(db.Integer      , primary_key=True)
    correo      = db.Column(db.String(255)  , nullable=False, unique=True)
    password    = db.Column(db.String(64)   , nullable=False)
    nombre      = db.Column(db.String(64)   , nullable=False)
    apellido    = db.Column(db.String(64)   , nullable=False)

    def __repr__(self):
        return f'<Alumno: {self.codigo} - {self.apellido}, {self.nombre}>'

class Docente(db.Model):
    __tablename__ = 'docente'
    codigo          = db.Column(db.Integer      , primary_key=True)
    correo          = db.Column(db.String(255)  , nullable=False, unique=True)
    nombre          = db.Column(db.String(64)   , nullable=False)
    apellido        = db.Column(db.String(64)   , nullable=False)

    def __repr__(self):
        return f'<Docente: {self.codigo} - {self.apellido}, {self.nombre}>'

class Curso(db.Model):
    __tablename__ = 'curso'
    codigo          = db.Column(db.String(6)    , primary_key=True) #CheckConstraint("codigo REGEX_LIKE '[A-Z]{2}\d{4}'")?
    curso           = db.Column(db.String(255)  , nullable=False)
    lab             = db.Column(db.Boolean      , nullable=False)
    teoria          = db.Column(db.Boolean      , nullable=False)
    teoria_virutal  = db.Column(db.Boolean      , nullable=False)

    def __repr__(self):
        return f'<Docente: {self.codigo} - {self.curso}>'

class Clase(db.Model):
    __tablename__ = 'clase'
    curso           = db.Column(db.String(6)    , db.ForeignKey('curso.codigo')     , primary_key=True)
    tipo            = db.Column(db.Enum(TipoClaseEnum)                              , primary_key=True)
    seccion         = db.Column(db.String(2)    , primary_key=True)
    numero          = db.Column(db.String(2)    , primary_key=True)
    vacantes        = db.Column(db.Integer      , nullable=False)
    docente         = db.Column(db.Integer      , db.ForeignKey('docente.codigo')   , nullable=True) # Null cuando aun no se sabe el docente

    def __repr__(self):
        return f'<Clase: {self.curso}, {self.tipo}, {self.seccion}, {self.numero}>'

class Sesion(db.Model):
    __tablename__ = 'sesion'
    curso           = db.Column(db.String(6)    , primary_key=True)
    clase_tipo      = db.Column(db.Enum(TipoClaseEnum)                              , primary_key=True) 
    clase_seccion   = db.Column(db.String(2)    , primary_key=True)
    clase_numero    = db.Column(db.String(2)    , primary_key=True)
    id              = db.Column(db.Integer, primary_key=True)
    dia             = db.Column(db.Integer, nullable=False) #Cambiar formato?
    hora_inicio     = db.Column(db.Integer, nullable=False) #Cambiar formato?
    hora_fin        = db.Column(db.Integer, nullable=False) #Cambiar formato?
    # Implementar frecuencia tambien
    # Llave foranea compuesta a Clase
    __table_args__  = (db.ForeignKeyConstraint(
                            [curso, clase_tipo, clase_seccion, clase_numero],
                            ['clase.curso', 'clase.tipo', 'clase.seccion', 'clase.numero']
                        ),
                        {},
                      )

    def __repr__(self):
        return f'<Clase: {self.curso}, {self.clase_tipo}, {self.clase_seccion}, {self.clase_numero}, {self.id}>'

class Horario(db.Model):
    __tablaname__ = 'horario'
    id              = db.Column(db.Integer      , primary_key=True)
    alumno          = db.Column(db.Integer      , db.ForeignKey('alumno.codigo')    , nullable=False)
    def __repr__(self):
        return f'<Clase: {self.id}>'


class Lista(db.Model):
    __tablename__ = 'lista'
    horario         = db.Column(db.Integer      , db.ForeignKey('horario.id')       , primary_key=True)
    curso           = db.Column(db.String(6)    , primary_key=True)
    clase_tipo      = db.Column(db.Enum(TipoClaseEnum)                              , primary_key=True) 
    clase_seccion   = db.Column(db.String(2)    , primary_key=True)
    clase_numero    = db.Column(db.String(2)    , primary_key=True)
    # Llave foranea compuesta a Clase
    __table_args__  = (db.ForeignKeyConstraint(
                            [curso, clase_tipo, clase_seccion, clase_numero],
                            ['clase.curso', 'clase.tipo', 'clase.seccion', 'clase.numero']
                        ),
                        {},
                      )
                      
    def __repr__(self):
        return f'<Lista: {self.horario} - {self.curso}, {self.clase_tipo}, {self.clase_seccion}, {self.clase_numero}>'

class Favorito(db.Model):
    __tablename__ = 'favoritos'
    horario         = db.Column(db.Integer      , db.ForeignKey('horario.id')       , primary_key=True)
    alumno          = db.Column(db.Integer      , db.ForeignKey('alumno.codigo')    , primary_key=True)
    def __repr__(self):
        return f'<Lista: {self.horario}, {self.alumno}>'

db.create_all()

@app.route('/')
def index():
    return 'Algo temporal'

if __name__ == '__main__':
    app.run() #(port=5002, debug=True)
#else:
#    print('using global variables from FLASK')
