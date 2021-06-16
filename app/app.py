import json
import sys

from sqlalchemy.orm import backref
from enum import unique, Enum
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from . import config
from . import forms

from .utils import is_safe_url
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




# ----------------
# Modelos & Tablas
# ----------------

class TipoClaseEnum(Enum):
    lab = 0
    teoria = 1
    teoria_virtual = 2

lista_clases = db.Table('lista',
    db.Column('horario_id', db.Integer, db.ForeignKey('horario.id'), primary_key=True),
    db.Column('clase_id', db.Integer, db.ForeignKey('clase.id'),primary_key=True)
)

lista_favoritos = db.Table('favorito',
    db.Column('horario_id', db.Integer , db.ForeignKey('horario.id')    , primary_key=True),
    db.Column('alumno_codigo', db.String(9), db.ForeignKey('alumno.codigo'), primary_key=True)
)

class Alumno(UserMixin,db.Model):
    __tablename__ = 'alumno'
    codigo      = db.Column(db.String(9)  , primary_key=True)
    correo      = db.Column(db.String(255), nullable=False, unique=True)
    password    = db.Column(db.String(64) , nullable=False)
    nombre      = db.Column(db.String(64) , nullable=False)
    apellido    = db.Column(db.String(64) , nullable=False)
    horarios    = db.relationship('Horario', backref='alumno', lazy=True)
    favoritos   = db.relationship('Horario', secondary=lista_favoritos, lazy=True, backref=db.backref('alumnos', lazy=True) )

    def __repr__(self):
        return f'<Alumno: {self.codigo} - {self.apellido}, {self.nombre}>'

    # Auth
    def get_id(self):
        return self.codigo

class Docente(db.Model):
    __tablename__ = 'docente'
    codigo          = db.Column(db.String(6)  , primary_key=True)
    correo          = db.Column(db.String(255), nullable=False, unique=True)
    nombre          = db.Column(db.String(64) , nullable=False)
    apellido        = db.Column(db.String(64) , nullable=False)
    clases          = db.relationship('Clase', backref='docente', lazy=True)

    def __repr__(self):
        return f'<Docente: {self.codigo} - {self.apellido}, {self.nombre}>'

class Curso(db.Model):
    __tablename__ = 'curso'
    codigo          = db.Column(db.String(6)  , primary_key=True)
    curso           = db.Column(db.String(255), nullable=False)
    lab             = db.Column(db.Boolean    , nullable=False)
    teoria          = db.Column(db.Boolean    , nullable=False)
    teoria_virutal  = db.Column(db.Boolean    , nullable=False)
    clases          = db.relationship('Clase', backref='curso', lazy=True)

    def __repr__(self):
        return f'<Docente: {self.codigo} - {self.curso}>'

class Clase(db.Model):
    __tablename__ = 'clase'
    id              = db.Column(db.Integer  , primary_key=True)
    curso_codigo    = db.Column(db.String(6), db.ForeignKey('curso.codigo'))
    tipo            = db.Column(db.Enum(TipoClaseEnum), nullable=False)
    seccion         = db.Column(db.String(2), nullable=False)
    numero          = db.Column(db.String(2), nullable=False)
    vacantes        = db.Column(db.Integer  , nullable=False)
    docente_codigo  = db.Column(db.String(6), db.ForeignKey('docente.codigo'), nullable=True) # Null para cuando aun no se sabe el docente
    sesiones        = db.relationship('Sesion', backref='clase', lazy=True)
    __table_args__ = (
        db.UniqueConstraint('curso_codigo','tipo','seccion','numero', name='unique_clase_por_curso'),
    )

    def __repr__(self):
        return f'<Clase: {self.id} de Curso {self.curso_codigo}>'

class Sesion(db.Model):
    __tablename__ = 'sesion'
    id              = db.Column(db.Integer      , primary_key=True)
    clase_id        = db.Column(db.Integer , db.ForeignKey('clase.id'), nullable=False)
    # Numeracion de sesion? #REVISAR
    dia             = db.Column(db.Integer      , nullable=False) #Cambiar formato?
    hora_inicio     = db.Column(db.Integer      , nullable=False) #Cambiar formato?
    hora_fin        = db.Column(db.Integer      , nullable=False) #Cambiar formato?
    # Implementar frecuencia tambien?

    def __repr__(self):
        return f'<Clase: {self.id} de Clase {self.clase_id}>'

class Horario(db.Model):
    __tablaname__ = 'horario'
    id              = db.Column(db.Integer      , primary_key=True)
    alumno_codigo   = db.Column(db.String(9)    , db.ForeignKey('alumno.codigo')    , nullable=False)
    #Agregar talvez tmb fecha de creacion?
    clases          = db.relationship('Clase', secondary=lista_clases, lazy='subquery', backref=db.backref('horarios', lazy=True) )
    
    def __repr__(self):
        return f'<Clase: {self.id}>'


db.create_all() # Crear tablas en bd


#-----
# Login Authentication
#-----

@login_manager.user_loader
def load_user(user_codigo):
    return Alumno.query.get(user_codigo)


# ------
# ROUTES
# ------

# --- Authetificacion ---
@app.route('/auth/register/', methods=['GET','POST'])
def register():
    form=forms.registerform()
    error=False
    if form.validate_on_submit():
        same_id = Alumno.query.get(form.id_utec.data)
        if not same_id:
            same_email = Alumno.query.filter_by(correo=form.correo.data).first()
            if not same_email:
                new_user = Alumno(codigo=form.id_utec.data, correo=form.correo.data, password=form.password.data,
                nombre=form.name.data, apellido=form.last_name.data )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                error = "Ya existe un usuario con este correo"
        else:
            error = "Ya existe un usuario con esta ID UTEC"
    return render_template('auth/register.html', form=form, error=error)

@app.route('/auth/login/', methods=['GET','POST'])
def login():
    form=forms.loginform()
    error=False 
    if form.validate_on_submit():
        # Get user
        user = Alumno.query.get(form.id_utec.data)
        next = request.args.get('next')
        if not is_safe_url(next):
            # Por fines de seguridad cancela si el redirect no es seguro
            return abort(400)
        # Si existe
        if user:
            # Si es valido
            if user.password == form.password.data:
                login_user(user,remember=form.remember.data)
                return redirect(next or url_for('menu_inicio'))
            else:
                error = "Credenciales no validas"
        else:
            error = "Credenciales no validas"
    return render_template('auth/login.html',form=form, error=error)

@app.route("/auth/logout")
@login_required
def logout():
    logout_user()
    return redirect(  url_for('login')  )

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
@login_required
def horarios_update(id):
    error =False
    alumno_codigo = str(202010387) # TEMPORAL: El codigo de alumno debe salir del auth actual
    info = Curso.query.all()

    try:
        horario = Horario.query.get(id)
    except:
        error = True

    if error:
        return 'Url no valida' # MEJORAR RESPUESTA DE ERROR
    elif horario==None:
        return 'El horario que se busca no existe' # MEJORAR RESPUESTA DE ERROR
    elif horario.alumno_codigo != alumno_codigo:
        return 'No tiene permisos para eliminar este horario'
    else:
        return render_template('horarios/update.html', data=info, horario=horario)

@app.route('/horarios/delete/<id>')
def horarios_delete(id):
    error =False
    alumno_codigo = str(202010387) # TEMPORAL: El codigo de alumno debe salir del auth actual

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
        print(horario.clases)
        return render_template('horarios/view.html', horario=horario)

# Alumno
@app.route('/alumnos/list')
def alumnos_list():
    alumnos = Alumno.query.all()
    return 'Alumnos List'

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

# Indice
@app.route('/auth')
@login_required
def menu_registered():
    return 'Solo los registrados entran aca'

@app.route('/')
def menu_inicio():
    return render_template('menu.html')

