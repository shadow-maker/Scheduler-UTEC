# COSAS POR HACER

## Backend
* Agregar filtros para horarios
  * En base a tiempo
  * En base a profesores
  * En base a likes
* Sortear horarios
* Validacion al momento de hacer commit a un horario
* Se pasa variable de lista de cursos y secciones

## Frontend
* Representacion de horarios en forma de tabla (bonito)
  * Dado una lista de secciones y sus sesiones
* Pagina de perfil - publico
  * Lista de likes (de otros usuarios)
  * Lista de horarios (tuyos)
    * Si es tuyo mostrar opcion de EDIT -> Redirecciona a pagina de update
  * Información personal
    * Nombre
    * Apellido
    * Codigo
    * Email
  * Pagina de edicion de informacion personal
* Vista por cursos / secciones
* Opcion / Pagina de crear horario [✓]
* Feed de horarios
  * Opciones de sorting
* Pagina de UPDATE
  * Implementación de botones fetch para actualizar el horario actual
    * Agregar (visualmente) secciones
      * Validar si hay colisiones (antes de mandar al back)
    * Quitar (visualmente) secciones
    * Commit (post) -> Los cambios a nivel local se almacenan y validan en el backend

## Extra
* Sacar todas las combinaciones posibles segun cursos
* Vista por favoritos
* Agregar tabla de cursos likes para los alumnos
* Posibilitar que el usuario cambie su contraseña



# Estructura general
* Flujo de register/login/logout [✓]
* Flujo de busqueda y vista de usuarios [✓] *(Falta filtros)
* Flujo de creacion de horarios
* Flujo de busqueda y vista de horarios
