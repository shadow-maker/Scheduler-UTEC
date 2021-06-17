import json
import sys
from flask.globals import session

from sqlalchemy.orm import backref
from enum import unique
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import Length

from . import config
from . import forms

from .utils import is_safe_url, TipoClaseEnum
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
    titulo          = db.Column(db.String(64)  , nullable=False)
    alumno_codigo   = db.Column(db.String(9)    , db.ForeignKey('alumno.codigo')    , nullable=False)
    #Agregar talvez tmb fecha de creacion?
    clases          = db.relationship('Clase', secondary=lista_clases, lazy='subquery', backref=db.backref('horarios', lazy=True) )
    
    def __repr__(self):
        return f'<Clase: {self.id}>'

    def get_status(self):
        horario_dict = {}
        horario_table = [
            #L ,M ,M ,J ,V ,S ,D
            ['','','','','','',''], #7-8
            ['','','','','','',''], #8-8
            ['','','','','','',''], #9-9
            ['','','','','','',''], #10-10
            ['','','','','','',''], #11-12
            ['','','','','','',''], #12-13
            ['','','','','','',''], #13-14
            ['','','','','','',''], #14-15
            ['','','','','','',''], #15-16
            ['','','','','','',''], #16-17
            ['','','','','','',''], #17-18
            ['','','','','','',''], #18-19
            ['','','','','','',''], #19-20
            ['','','','','','',''], #20-21
            ['','','','','','',''], #21-22
        ] 
        for c in self.clases:
            for s in c.sesiones:
                for hora in range(s.hora_inicio, s.hora_fin):
                    horario_table[hora-7][s.dia-1] = c.curso.codigo

            if c.curso.codigo in horario_dict:
                horario_dict[c.curso.codigo][0] += 2**c.tipo.value
            else:
                horario_dict[c.curso.codigo] = [2**c.tipo.value, c.curso.lab * 2**TipoClaseEnum.lab.value + c.curso.teoria * 2**TipoClaseEnum.teoria.value + c.curso.teoria_virtual * 2**TipoClaseEnum.teoria_virtual.value]
        status = "Complete"
        cursos_pendientes = []
        for c in horario_dict:
            if horario_dict[c][0] != horario_dict[c][1]:
                status = "Pending"
                cursos_pendientes.append(c)
        return status, horario_table, ",".join(cursos_pendientes)

    def clase_colission(self, clase):
        if clase in self.clases:
            return "El curso ya se enceuntra en el horario"
        for c in self.clases:
                if c.curso.curso == clase.curso.curso:
                    if c.tipo == clase.tipo:
                        return f'Ya existe otra clase de {c.tipo.name} del mismo curso con otra clase: {c.curso.curso} - {c.tipo.name} - {c.seccion}.{c.numero}'
                    elif c.seccion != clase.seccion:
                        return f'Ya esta suscrito a otra seccion en el curso {c.curso}: {c.curso.curso} - {c.tipo.name} - {c.seccion}.{c.numero}'
                for s in c.sesiones:
                    for sesion in clase.sesiones:
                        if s.dia == sesion.dia:
                            if (s.hora_inicio<=sesion.hora_inicio and s.hora_fin>sesion.hora_fin) or (sesion.hora_inicio<=s.hora_inicio and sesion.hora_fin>s.hora_fin):
                                return f'Colision con otra clase: {c.curso.curso} - {c.tipo.name} - {c.seccion}.{c.numero}'
        return False


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
        return 'Error de backend' #MRE

    if not alumno:
        return 'El alumno que busca no existe' #MRE
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
        return 'No tiene permisos para modificar este perfil' #MRE
    try:
        alumno = Alumno.query.get(id)
    except:
        return 'Error de backend' #MRE

    if not alumno:
        return 'El alumno que busca no existe' #MRE
    
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

@app.route('/alumnos/<id>/delete', methods=['GET'])
@login_required
def alumnos_delete(id):
    if current_user.codigo!=id:
        return 'No tiene permisos para modificar este perfil' #MRE
    try:
        alumno = Alumno.query.get(id)
    except:
        return 'Error de backend' #MRE

    if not alumno:
        return 'El alumno que busca no existe' #MRE

    return render_template('alumnos/delete.html', alumno=alumno)


# --- Home & Explore ---

@app.route('/')
def menu_inicio():
    return render_template('home/menu.html')

@app.route('/explore')
def explore():
    return render_template('home/explore.html')

# --- Horarios ---
@app.route('/horarios/<id>')
def horarios_view(id):
    error =False
    try:
        horario = Horario.query.get(id)
    except:
        error = True

    if error:
        return 'Url no valida' #MRE
    elif horario==None:
        return 'El horario que se busca no existe' #MRE
    else:
        status, table_horario, pending_cursos = horario.get_status()
        if current_user.is_authenticated:
            in_favoritos = horario in current_user.favoritos
        else:
            in_favoritos = False

        return render_template('horarios/view.html', horario=horario, status = status, table_horario=table_horario, pending_cursos=pending_cursos, in_favoritos=in_favoritos)

@app.route('/horarios/list')
def horarios_list():
    horarios = Horario.query.all()
    return render_template('horarios/list.html',horarios=horarios)

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
        return 'Url no valida' #MRE
    elif horario==None:
        return 'El horario que se busca no existe' #MRE
    elif horario.alumno_codigo != alumno_codigo:
        return 'No tiene permisos para eliminar este horario'
    else:
        status, table_horario, pending_cursos = horario.get_status()
        return render_template('horarios/update.html', data=info, horario=horario, status = status, table_horario=table_horario, pending_cursos=pending_cursos)

@app.route('/horarios/<id>/delete')
@login_required
def horarios_delete(id):
    try:
        horario = Horario.query.get(id)
    except:
        return 'Error inesperado de backend (H)' #MRE

    if  not horario:
        return 'El horario que se busca no existe' #MRE

    if current_user!=horario.alumno:
        return 'No tiene permisos para modificar este horario' #MRE

    return render_template('horarios/delete.html', horario=horario)

# --- Curso ---
@app.route('/cursos/<id>', methods=['GET'])
def cursos_view(id):
    try:
        curso = Curso.query.get(id)
    except:
        return 'Error de backend' #MRE

    if not curso:
        return 'El curso que busca no existe' #MRE
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
        return 'Error de backend' #MRE

    if not clase:
        return 'El curso que busca no existe' #MRE
    else:
        return render_template('clases/view.html', clase=clase)

# --- Docentes ---
@app.route('/docentes/<id>', methods=['GET'])
def docentes_view(id):
    try:
        docente = Docente.query.get(id)
    except:
        return 'Error de backend' #MRE

    if not docente:
        return 'El curso que busca no existe' #MRE
    else:
        return render_template('docentes/view.html', docente=docente)

@app.route('/docentes/list', methods=['GET'])
def docentes_list():
    docentes = Docente.query.all()
    return render_template('docentes/list.html', docentes=docentes)

#### ---CRUD api ----
@app.route('/api/cursos/read', methods=['GET'])
def api_cursos_read_filter():
    error = False
    response = {}

    # Data de parametros
    curso_curso = request.args.get(key='curso_curso', default="")

    # Query
    if not error:
        cursos = Curso.query.filter(Curso.curso.startswith(curso_curso)).all()
        response["cursos"] = [
            {
                "curso_codigo":c.codigo,
                "curso_curso":c.curso,
                "curso_url":url_for('cursos_view',id=c.codigo)
            } for c in cursos]
        response["empty"] = False if cursos else True

    # Return
    response["success"] = not error
    return jsonify(response)

@app.route('/api/docentes/read', methods=['GET'])
def api_docentes_read_filter():
    error = False
    response = {}

    # Data de parametros
    docente_nombre = request.args.get(key='docente_nombre', default="")
    docente_apellido = request.args.get(key='docente_apellido', default="")

    # Query
    if not error:
        docentes = Docente.query.filter(Docente.nombre.startswith(docente_nombre)).filter(Docente.apellido.startswith(docente_apellido)).all()
        response["docentes"] = [
            {
                "docente_codigo":d.codigo,
                "docente_nombre":d.nombre,
                "docente_apellido":d.apellido,
                "docente_url":url_for('docentes_view',id=d.codigo)
            } for d in docentes]
        response["empty"] = False if docentes else True

    # Return
    response["success"] = not error
    return jsonify(response)

@app.route('/api/alumnos/read', methods=['GET'])
def api_alumnos_read_filter():
    error = False
    response = {}

    # Data de parametros
    alumno_nombre = request.args.get(key='alumno_nombre', default="")
    alumno_apellido = request.args.get(key='alumno_apellido', default="")

    # Query
    if not error:
        alumnos = Alumno.query.filter(Alumno.nombre.startswith(alumno_nombre)).filter(Alumno.apellido.startswith(alumno_apellido)).all()
        response["alumnos"] = [
            {
                "alumno_codigo":a.codigo,
                "alumno_nombre":a.nombre,
                "alumno_apellido":a.apellido,
                "alumno_url":url_for('alumnos_view',id=a.codigo)
            } for a in alumnos]
        response["empty"] = False if alumnos else True

    # Return
    response["success"] = not error
    return jsonify(response)

@app.route('/api/horarios/read', methods=['GET'])
def api_horarios_read_filter():
    error = False
    response = {}

    # Data de parametros
    horario_titulo = request.args.get(key='horario_titulo', default="")

    # Query
    if not error:
        horarios = Horario.query.filter(Horario.titulo.startswith(horario_titulo)).all()
        response["horarios"] = [
            {
                "horario_id":h.id,
                "horario_titulo":h.titulo,
                "horario_url":url_for('horarios_view',id=h.id),
                "horario_alumno_nombre":h.alumno.nombre,
                "horario_alumno_apellido":h.alumno.apellido
            } for h in horarios]
        response["empty"] = False if horarios else True

    # Return
    response["success"] = not error
    return jsonify(response)



@app.route('/api/horarios/create', methods=['POST'])
@login_required
def api_horarios_create():
    error = False
    alumno_codigo = current_user.codigo
    response = {}

    # Data de json
    try:
        horario_titulo = request.get_json()['horario_titulo']
    except:
        error = True
        response["error_message"] = "JSON incompleto"

    # Creacion
    if not error:
        try:
            horario = Horario(titulo=horario_titulo, alumno_codigo=alumno_codigo)
            db.session.add(horario)
            db.session.commit()
            horario_id = horario.id
            response["horario_url"] = url_for('horarios_view', id=horario_id)
            response["horario_id"] = horario_id
            response["horario_titulo"] = horario_titulo
        except:
            db.session.rollback()
            print(sys.exc_info())
            error = True
            response["error_message"] = "No se pudo crear el Horario"
        finally:
            db.session.close()

    response["success"] = not error
    return jsonify(response)

@app.route('/api/horarios/delete/<id>', methods=['DELETE'])
@login_required
def api_horarios_delete(id):
    error = False
    alumno = current_user
    response = {}

    # Get de objetos
    try:
        horario = Horario.query.get(id)
    except:
        print(sys.exc_info())
        error = True
        response["error_message"] = "Error inesperado de backend (H)"

    # Validar
    if not error:
        # Validar existencia de horario
        if not horario:
            error = True
            response["error_message"] = "No se pudo encontrar el horario que desea eliminar"
        # Validar permisos
        elif alumno != horario.alumno:
            error = True
            response["error_message"] = "No tiene los permisos necesarios para modificar este horario"
        
    # Delicion y actualizacion de datos
    if not error:
        try:
            db.session.delete(horario)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
            response["error_message"] = "No se pudo editar el titulo del horario"
            error = True
        finally:
            db.session.close()

    # Return
    response["success"] = not error
    return jsonify(response)


@app.route('/api/horarios/update/<id>/rename', methods=['PUT'])
@login_required
def api_horarios_update_rename(id):
    error = False
    response = {}
    alumno = current_user

    # Data de json
    try:
        new_titulo = request.get_json()['new_titulo']
    except:
        error = True
        response["error_message"] = "JSON incompleto"

    # Get de objetos
    if not error:
        try:
            horario = Horario.query.get(id)
        except:
            print(sys.exc_info())
            error = True
            response["error_message"] = "Error inesperado de backend (H)"

    # Validar
    if not error:
        # Validar existencia de horario
        if not horario:
            error = True
            response["error_message"] = "No se pudo encontrar el horario que desea editar"
        # Validar permisos
        elif alumno != horario.alumno:
            error = True
            response["error_message"] = "No tiene los permisos necesarios para modificar este horario"
        # Validar input
        elif not new_titulo:
            error = True
            response["error_message"] = "Titulo Invalido"
        
    # Insercion y actualizacion de datos
    if not error:
        try:
            horario.titulo = new_titulo
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
            response["error_message"] = "No se pudo editar el titulo del horario"
            error = True
        finally:
            db.session.close()

    # Return
    response["success"] = not error
    return jsonify(response)


@app.route('/api/horarios/update/<id>/add-clase', methods=['PUT'])
@login_required
def api_horarios_update_add(id):
    error = False
    response = {}
    alumno = current_user
    
    # Data de json
    try:
        clase_id = request.get_json()['clase_id']
    except:
        error = True
        response["error_message"] = "JSON incompleto"

    # Get de objetos
    if not error:
        try:
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

    # Validacion
    if not error:
        if not horario:
            error = True
            response["error_message"] = "No se pudo encontrar el horario que desea editar"
        elif not clase:
            error = True
            response["error_message"] = "No se pudo encontrar la clase que desea agregar"

    # Logica de permisos
    if not error:
        if alumno != horario.alumno:
            error = True
            response["error_message"] = "No tiene los permisos necesarios para modificar este horario"

    # Logica de validacion de cambios
    if not error:
        ret_message = horario.clase_colission(clase)
        if ret_message:
            error = True
            response["error_message"] = ret_message
        
    # Insercion y actualizacion de datos
    if not error:
        try:
            # Adicion
            horario.clases.append(clase)
            db.session.commit()
            # Status del horario
            status, table_horario, pending_cursos = horario.get_status()
            response["status_horario"] = status
            response["table_horario"]  = table_horario
            response["pending_cursos"] = pending_cursos
        except:
            # Error
            db.session.rollback()
            print(sys.exc_info())
            error = True
            response["error_message"] = "Error inesperado de backend"
        finally:
            db.session.close()

    # Return
    response["success"] = not error
    return jsonify(response)


@app.route('/api/horarios/update/<id>/delete-clase', methods=['PUT'])
@login_required
def api_horarios_update_delete(id):
    error = False
    response = {}
    alumno = current_user
    
    # Data de json
    try:
        clase_id = request.get_json()['clase_id']
    except:
        error = True
        response["error_message"] = "JSON incompleto"


    # Get de objetos
    if not error:
        try:
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

    # Logica de permisos
    if not error:
        if alumno != horario.alumno:
            error = True
            response["error_message"] = "No tiene los permisos necesarios para modificar este horario"

    # Logica de validacion de cambios
    if not error:
        if clase not in horario.clases:
            error = True
            response["error_message"] = "El curso que intenta eliminar no forma parte de este horario"

    # Insercion y actualizacion de datos
    if not error:
        try:
            horario.clases.remove(clase)
            db.session.commit()
            # Status del horario
            status, table_horario, pending_cursos = horario.get_status()
            response["status_horario"] = status
            response["table_horario"] = table_horario
            response["pending_cursos"] = pending_cursos
        except:
            db.session.rollback()
            print(sys.exc_info())
            response["error_message"] = "Error inesperado de backend"
            error = True
        finally:
            db.session.close()

    # Return
    response["success"] = not error
    return jsonify(response)

@app.route('/api/favoritos/add/<id>', methods=['POST'])
@login_required
def api_favoritos_add(id):
    error = False
    response = {}
    alumno = current_user

    # Get de objetos
    try:
        horario = Horario.query.get(id)
    except:
        print(sys.exc_info())
        error = True
        response["error_message"] = "Error inesperado de backend (H)"

    # Validar
    if not error:
        # Validar existencia de horario
        if not horario:
            error = True
            response["error_message"] = "No se pudo encontrar el horario que desea agregar"
        # Validar si ya existe relacion
        elif horario in alumno.favoritos:
            error = True
            response["error_message"] = "Horario ya esta en tus favoritos"
        
    # Insercion y actualizacion de datos
    if not error:
        try:
            alumno.favoritos.append(horario)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
            response["error_message"] = "No se pudo agregar a favoritos el horario"
            error = True
        finally:
            db.session.close()

    # Return
    response["success"] = not error
    return jsonify(response)

@app.route('/api/favoritos/delete/<id>', methods=['DELETE'])
@login_required
def api_favoritos_delete(id):
    error = False
    response = {}
    alumno = current_user

    # Get de objetos
    try:
        horario = Horario.query.get(id)
    except:
        print(sys.exc_info())
        error = True
        response["error_message"] = "Error inesperado de backend (H)"

    # Validar
    if not error:
        # Validar existencia de horario
        if not horario:
            error = True
            response["error_message"] = "No se pudo encontrar el horario que desea quitar"
        # Validar si ya existe relacion
        elif horario not in alumno.favoritos:
            error = True
            response["error_message"] = "Horario no esta en tus favoritos"
        
    # Delicion y actualizacion de datos
    if not error:
        try:
            alumno.favoritos.remove(horario)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
            response["error_message"] = "No se pudo eliminar de tus favoritos el horario"
            error = True
        finally:
            db.session.close()

    # Return
    response["success"] = not error
    return jsonify(response)

@app.route('/api/alumnos/delete/<id>', methods=['DELETE'])
@login_required
def api_alumnos_delete(id):
    error = False
    response = {}
    alumno = current_user

    if current_user.codigo!=id:
        error = True
        response["error_message"] = 'No tiene permisos para modificar este perfil'
    
    if not error:
        try:
            alumno = Alumno.query.get(id)
        except:
            error = True
            response["error_message"] ='Error de backend'

    if not error:
        if not alumno:
            error = True
            response["error_message"] = 'El alumno no existe'

    if not error:
        try:
            db.session.delete(alumno)
            db.session.commit()
            response["redirect"] = url_for('menu_inicio')
        except:
            db.session.rollback()
            print(sys.exc_info())
            error = True
            response["error_message"] = 'No se pudo eliminar el alumno'
        finally:
            db.session.close()
        

    # Return
    response["success"] = not error
    return jsonify(response)

