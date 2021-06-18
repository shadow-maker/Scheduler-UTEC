# Scheduler-UTEC
## Integrantes:
- Mauro Bobadilla - 202010114
- Carlos Andrés Montoro - 202010324
- Rodrigo Salazar - 202010387
- Eduardo Arróspide González - 202010442

## Descripción del proyecto
Una web app para crear y compartir horarios mediante un sistema de favoritos para la matricula de la universidad UTEC. Permite visualizar los alumnos, docentes, cursos y clases, aparte de poder mirar los horarios de otros usuarios para guardarlos en favoritos. Incluye sistema de autentificacion y una interfaz web amigable para la edicion de horarios.

## Objetivos:

### Objetivo General:
- Crear un sistema que le ofrezca a los alumnos una forma fácil y rapida de gestionar sus horarios

### Objetivos especificos:
- Emplear cookies para la implementacion de un sistema de autenticacion de los usuarios
- Crear una API CRUD que le permita a los alumnos gestionar sus horarios, cuenta y explorar los recursos del sistema.
- Diseñar e implementar una interfaz grafica web para la exploracion de recursos y gestion de horarios
- Implementar un sistema de seguimiento de horarios mediante su seleccion como favoritos (propios y de otros)

## Tecnologias
### Front-end
#### CSS
Esta tecnologia consiste en un lenguaje de hojas de estilo en cascada que permite la personalizacion del estilo dado a los documentos HTML.

En este proyecto se hace un uso extensivo de CSS para el styling de la interfaz web del sistema.

De esto se destaca especialmente su uso para la creacion de botones personalizados con implementación de hovering en el menú de inicio y la creacion de un estilo personalizada para las tablas empleadas para la representacion de los diversos horarios. Asimismo, mediante el CSS se ha añadido fondos a todos los documentos HTML.

#### JS y Web API's
JavaScript(JS) es un lenguaje de scripting de lado del cliente que permite la actualizacion de contenidos de una pagina de forma dinamica. Para este fin, cuenta con multiples Web API's que ofrecen funciones diversas de utilidad.

Durante el desarollo de este proyecto se ha realizado un amplio uso de JavaScript para la interfaz web del sistema.

Esta tecnologia se ha usado para poder hacer requests a la API CRUD del sistema y actualizar el docuemnto HTML actual al recibir la response, permitiendo una ejecuccion asincrona que hace mas comoda la experiencia del usuario y previene la necesidad de recargar la pagina.

Para el manejo de las Request y Response se ha usado especificamente la Fetch API, especialmente su metodo fetch(). Adicionalmente, para el manejo de algunas requests tambien se ha complementaod con la API URLSearchParams para la construccion de las urls requeridas.

### Back-end

[Diagrama modelo entidad-relación de la base de datos](https://drive.google.com/file/d/11JkNTHSAbAOZf8_7-TSd_0hAK1-1RmMO/view?usp=sharing)

#### Flask
Flask es un framework de backend que provee una estructura basica para implementar servidores con la estructura MVC. Este framework utiliza la libreria Jinja para la creacion de templates y SQLAlchemy para la comunicacion con la base de datos.

Esta es la tecnologia principal usada para la implementacion del backend del sistema.

#### Flask-Login
Es una extesnsion del framework Flask que permite la autenticacion de usuarios mediante Cookies.

Esta es la tecnologia empleada para la autenticacion de los Alumnos utilizando los campos codigo y password para este fin. Para la restriccion de vistas para unicamente usuarios que tiene una sesion activa se emplea el decorador @login_required en la funcion controlador associada.

#### WTForms
Es una extension del framework Flask que permite la abstraccion y automatizacion de creacion de forms mediante su abstraccion en clases y objetos.

Esta tecnologia se emplea especialmente en los forms de Login y Register para validar sus inputs y extraer la informacion en el back-end con facilidad.

### Base de datos

#### PostgreSQL
El gestor de base de datos utilizado en este proyecto es PostgreSQL. Para la comunicacion entre la base de datos y el backend se usa el modulo de psycopg2 abstraido mediante SQLAlchemy.


## Script de inicializacion de base de datos
La informacion para la conexion con la base de datos se encuentra especificada en el archivo config.py. Por defecto, este sistema trabaja en la base de datos postgres local 'utecscheduler' con el usuario postgres.

Para poblar la base de datos se debe ejecutar la script sample.py que la inicializa y rellena con los datos de ejemplo

## API
### Aplicacion Web
#### Home & Explore
- '/': GET => Landing page
- '/explore': GET => Pagina con redirecciones a vistas de listas de recursos
#### Autentificacion:
- '/auth/register/': GET=> Interfaz con form de registro; POST=> Creacion de Alumno
- '/auth/login/': GET=> Interfaz con form de login; POST=> Login con el Alumno indicado
- '/auth/logout/': GET=> Logout de alumno actual
#### Alumnos:
- '/alumnos/\<id>': GET=> Vista de alumno con alumno.codigo=id
- '/alumnos/list': GET=> Interfaz de listado y filtrado de alumnos
- '/alumnos/\<id>/update': GET=> Interfaz con forms de update; POST => Actualizacion de alumno en base al form
- '/alumnos/\<id>/delete': GET=> Interfaz de eliminacion de cuenta
#### Horarios:
- '/horarios/\<id>': GET=> Vista de horario con horario.id=id
- '/horarios/list': GET=> Interfaz de listado y filtrado de alumnos
- '/horarios/\<id>/update': GET=> Interfaz de edicion de horario
- '/alumnos/\<id>/delete': GET=> Interfaz de eliminacion de horario
#### Cursos:
- '/cursos/\<id>': GET=> Vista de curso con curso.codigo=id
- '/cursos/list': GET=> Interfaz de listado y filtrado de cursos
#### Clases:
- '/clases/\<id>': GET=> Vista de clase con clase.id=id
- '/clases/list': GET=> Interfaz de listado y filtrado de clases
#### Docentes:
- '/docentes/\<id>': GET=> Vista de docente con docente.codigo=id
- '/docentes/list': GET=> Interfaz de listado y filtrado de docentes

### API CRUD
- '/api/cursos/read': GET con Args{curso_curso(default="")} => JSON con listado de cursos cuyo nombre empieza con curso_curso
- '/api/docentes/read': GET con Args{docente_nombre(default=""), docente_apellido(default="")} => JSON con listado de docentes cuyo nombre empieza con docente_nombre y apellido empieza con docente_apellido
- '/api/alumnos/read': GET con Args{alumno_nombre(default=""), alumno_apellido(default="")} => JSON con listado de alumnos cuyo nombre empieza con alumno_nombre y apellido empieza con alumno_apellido
- '/api/horarios/read': GET con Args{horario_titulo(default="")} => JSON con listado de horarios cuyo titulo empieza con horario_titulo y
- '/api/horarios/create' : POST con {horario_titulo} => JSON del horario creado con horario.titulo=horario_titulo para el alumno actual 
- '/api/horarios/delete/\<id>' : DELETE => JSON con confirmacion del borrado del horario con horaio.id=id
- '/api/horarios/update/\<id>/rename' : PUT con {new_titulo} => JSON con confirmacion del cambio de nombre del horario con horario.id=id
- '/api/horarios/update/\<id>/add-clase' : PUT con {clase_id} => JSON con confirmacion de la adicion de la clase con clase.id=clase_id al horario con horario.id=id
- '/api/horarios/update/\<id>/delete-clase' : PUT con {clase_id} => JSON con confirmacion de la delicion de la clase con clase.id=clase_id del horario con horario.id=id
- '/api/favoritos/add/\<id>' : POST => JSON con confirmacion de la adicion del horario con horario.id=id a los favoritos del alumno actual
- '/api/favoritos/delete/\<id>' : DELETE => JSON con confirmacion de la eliminacion del horario con horario.id=id de los favoritos del alumno actual

## Hosts
El host y configuracion de deployment se encuentra definida al inicio del archivo run.py. Por defecto, la aplicacion se correa en el host local en el puerto 8888 pero es posible modificar esto editando las variables de acuerdo a la necesidad

## Forma de Auteticacion
En esta aplicacion web los usuarios son definidos por el modelo Alumno con su contraseña siendo la columna password y su identificador la columna codigo. 

El metodo de autenticacion empleado es basado en cookies. Esto se ha implementado mediante la extension Flask-Login que maneja las sesiones con el objeto LoginManager() guardando las ID de los usuarios activos en la sesión, da restricciones para algunas paginas (útil para los que no se han loggeado) mediante el decorador @login_required, facilita el uso del “Remember me” que se utiliza mucho en sitios web y proteje las sesiones de los usuarios a ser robados por “cookie thieves”. Asimismo, facilita la identificacion del usuario actual en el backend mediante la variable current_user y prove funciones varias para la gestion de sesion (login, logout, etc.).

Para poder autenticarse el cuenta con las vistas: Login, Register y Logout.

## Manejo de errores
### Aplicacion Web
- 200: SUCESS => Estado cuando la respuesta es exitosa
- 400: BAD REQUEST => Usada para abortar cuando la request realizada no es segura (ej.: redireccionamiento inseguro en parametro next)
- 401 UNAUTHORIZED => No tiene permisos para editar/eliminar ese elemento
- 404 NOT FOUND => Recurso no encontrado
- 500 INTERNAL SERVER ERROR => Error inesperado del servidor

### API CRUD
Para las llamadas CRUD las respuestas son siempre de codigo 200. Sin embargo, esto no garantiza que estas se halla realizado la modificacion deseada, sino que el error handeling se hace mediante el  elemento 'success' dentro del JSON response.

En caso de haber un error los detalles se pueden encontrar en 'error-message', el cual se mostrara en la interfaz web mediante funciones de javascript.

## Ejecuccion del sistema
La deployment script del sistema es run.py
