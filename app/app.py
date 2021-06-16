import json
import sys
from flask.globals import session

from sqlalchemy.orm import backref
from enum import unique
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from . import config
from . import forms

from .utils import is_safe_url, status_horario, TipoClaseEnum
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
    curso           = db.Column(db.String(255), nullable=False, unique=True)
    lab             = db.Column(db.Boolean    , nullable=False)
    teoria          = db.Column(db.Boolean    , nullable=False)
    teoria_virtual  = db.Column(db.Boolean    , nullable=False)
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

@app.route("/auth/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(  url_for('login')  )

# --- Alumno ---
@app.route('/alumnos/<id>', methods=['GET'])
def alumnos_view(id):
    try:
        alumno = Alumno.query.get(id)
    except:
        return 'Error de backend' # MEJORAR RESPUESTA DE ERROR

    if not alumno:
        return 'El alumno que busca no existe' # MEJORAR RESPUESTA DE ERROR
    else:
        return render_template('alumnos/view.html', alumno=alumno)

@app.route('/alumnos/list', methods=['GET'])
def alumnos_list():
    alumnos = Alumno.query.all()
    return render_template('alumnos/list.html', alumnos=alumnos)

@login_required
@app.route('/alumnos/<id>/update', methods=['GET','POST'])
def alumnos_update(id):
    if current_user.codigo!=id:
        return 'No tiene permisos para modificar este perfil' # MEJORAR RESPUESTA DE ERROR
    try:
        alumno = Alumno.query.get(id)
    except:
        return 'Error de backend' # MEJORAR RESPUESTA DE ERROR

    if not alumno:
        return 'El alumno que busca no existe' # MEJORAR RESPUESTA DE ERROR
    
    form=forms.updatealumnoform()
    error=False
    if form.validate_on_submit():
        same_email = Alumno.query.filter_by(correo=form.correo.data).first()
        if not same_email or same_email==alumno:
            form.populate_alumno(alumno)
            db.session.add(alumno)
            db.session.commit()
            return redirect( url_for('alumnos_view', id=alumno.codigo) )
        else:
            error ="Ya existe otro usuario con este correo"
    else:
        form.from_alumno(alumno)
    
    return render_template('alumnos/update.html', alumno=alumno, form=form, error=error)

# CORREGIR PARA QUE FUNCIONE CON METODO DELETE
@app.route('/alumnos/<id>/delete', methods=['GET', 'POST'])
def alumnos_delete(id):
    if current_user.codigo!=id:
        return 'No tiene permisos para modificar este perfil' # MEJORAR RESPUESTA DE ERROR
    try:
        alumno = Alumno.query.get(id)
    except:
        return 'Error de backend' # MEJORAR RESPUESTA DE ERROR

    if not alumno:
        return 'El alumno que busca no existe' # MEJORAR RESPUESTA DE ERROR

    if request.method == 'POST':
        error = False
        try:
            alumno_id = alumno.codigo
            db.session.delete(alumno)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
            error = True
        finally:
            db.session.close()
        

        if error:
            return 'No se pudo eliminar el alumno' # MEJORAR RESPUESTA DE ERROR
        else:
            return redirect( url_for('menu_inicio') )
            #return f'Se elimino correctamente el alumno {alumno_id}' # MEJORAR RESPUESTA DE EXITO
    else:
        return render_template('alumnos/delete.html', alumno=alumno)


# --- Home & Explore ---

@app.route('/')
def menu_inicio():
    return render_template('home/menu.html')

@app.route('/explore')
def explore():
    return render_template('home/explore.html')

# --- Horarios ---
@app.route('/horarios/list')
def horarios_list():
    horarios = Horario.query.all()
    return render_template('horarios/list.html',horarios=horarios)
    
# --- Curso ---
@app.route('/cursos/<id>', methods=['GET'])
def cursos_view(id):
    try:
        curso = Curso.query.get(id)
    except:
        return 'Error de backend' # MEJORAR RESPUESTA DE ERROR

    if not curso:
        return 'El curso que busca no existe' # MEJORAR RESPUESTA DE ERROR
    else:
        return render_template('cursos/view.html', curso=curso)

@app.route('/cursos/list', methods=['GET'])
def cursos_list():
    cursos = Curso.query.all()
    return render_template('cursos/list.html', cursos=cursos)

# --- Clases ---
@app.route('/clases/<id>', methods=['GET'])
def clases_view(id):
    try:
        clase = Clase.query.get(id)
    except:
        return 'Error de backend' # MEJORAR RESPUESTA DE ERROR

    if not clase:
        return 'El curso que busca no existe' # MEJORAR RESPUESTA DE ERROR
    else:
        return render_template('clases/view.html', clase=clase)

# --- Docentes ---
@app.route('/docentes/<id>', methods=['GET'])
def docentes_view(id):
    try:
        docente = Docente.query.get(id)
    except:
        return 'Error de backend' # MEJORAR RESPUESTA DE ERROR

    if not docente:
        return 'El curso que busca no existe' # MEJORAR RESPUESTA DE ERROR
    else:
        return render_template('docentes/view.html', docente=docente)

@app.route('/docentes/list', methods=['GET'])
def docentes_list():
    docentes = Docente.query.all()
    return render_template('docentes/list.html', docentes=docentes)











@app.route('/horarios/create')
@login_required
def horarios_create():
    error = False
    alumno_codigo = current_user.codigo
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

@app.route('/horarios/<id>/update')
@login_required
def horarios_update(id):
    error =False
    alumno_codigo = current_user.codigo
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
        status = status_horario(horario)
        return render_template('horarios/update.html', data=info, horario=horario, status = status)

@app.route('/horarios/<id>/delete')
@login_required
def horarios_delete(id):
    error =False
    alumno_codigo = current_user.codigo

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

@app.route('/horarios/<id>')
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
















####

@app.route('/horarios/update/<id>/add', methods=['UPDATE'])
def horarios_update_add(id):
    error = False
    response = {}
    alumno_codigo = str(202010387) # TEMPORAL: El codigo de alumno debe salir del auth actual
    
    # Get de objetos
    try:
        clase_id = request.get_json()['clase_id']
        clase = Clase.query.get(int(clase_id))
    except:
        print(sys.exc_info())
        error = True
        response["error_message"] = "Error inesperado de backend (C)"
    try:
        horario = Horario.query.get(id)
    except:
        print(sys.exc_info())
        error = True
        response["error_message"] = "Error inesperado de backend (H)"

    if not error:
        # Logica de validacion
        if clase in horario.clases:
            error=True
            response["error_message"] = "El curso ya se enceuntra en el horario"
        else:
            for c in horario.clases:
                if c.curso.curso == clase.curso.curso:
                    if c.tipo == clase.tipo:
                        error = True
                        response["error_message"] = f'Ya existe otra clase de {c.tipo.name} del mismo curso con otra clase: {c.curso.curso} - {c.tipo.name} - {c.seccion}.{c.numero}'
                        break
                    elif c.seccion != clase.seccion:
                        error = True
                        response["error_message"] = f'Ya esta suscrito a otra seccion en el curso {c.curso}: {c.curso.curso} - {c.tipo.name} - {c.seccion}.{c.numero}'
                        break
                for s in c.sesiones:
                    for sesion in clase.sesiones:
                        if s.dia == sesion.dia:
                            if (s.hora_inicio<=sesion.hora_inicio and s.hora_fin>sesion.hora_fin) or (sesion.hora_inicio<=s.hora_inicio and sesion.hora_fin>s.hora_fin):
                                error = True
                                response["error_message"] = f'Colision con otra clase: {c.curso.curso} - {c.tipo.name} - {c.seccion}.{c.numero}'
                                break
                if error:
                    break
            if not error:
                try:
                    horario.clases.append(clase)
                    db.session.commit()
                    #response["success_message"] = "Se agrego correctamente la clase"
                except:
                    db.session.rollback()
                    print(sys.exc_info())
                    response["error_message"] = "Error inesperado de backend"
                    error = True

        # Status del horario
        status = status_horario(horario)
        db.session.close()
        # Return
        response["success"] = not error
        response["status_horario"] = status
    return jsonify(response)

# Indice
#@app.route('/auth')
#@login_required
#def menu_registered():
    return 'Solo los registrados entran aca'


