from app import Alumno, Docente, Curso, Clase, Sesion, Horario, Lista, Favorito, db, TipoClaseEnum

# INSERTAR FILAS
# Alumno
alumnos = [
    Alumno(
        codigo      =202010387,
        correo      ='rodrigo.salazar@utec.edu.pe',
        password    ='sample',
        nombre      ='Rodrigo Gabriel',
        apellido    ='Salazar Alva'
    ),
    Alumno(
        codigo      =201810312,
        correo      ='cesar.martinez@utec.edu.pe',
        password    ='csr',
        nombre      ='César Alejandro',
        apellido    ='Ortiz Martinez'
    ),
    Alumno(
        codigo      =202010434,
        correo      ='leonardo.yupanqui@utec.edu.pe',
        password    ='leopass',
        nombre      ='Leonardo Fabricio',
        apellido    ='Yupanqui Mera'
    ),
    Alumno(
        codigo      =201710620,
        correo      ='alberto.pelaez@utec.edu.pe',
        password    ='albertopass',
        nombre      ='Alberto Alejandro',
        apellido    ='Pelaez Sagastegui'
    ),
    Alumno(
        codigo      =201910240,
        correo      ='nayelli.cibelly@utec.edu.pe',
        password    ='nacontra',
        nombre      ='Nayeli Cibelly',
        apellido    ='Navarro Pizarro'
    ),
    Alumno(
        codigo      =202010114,
        correo      ='mauro.bobadilla@utec.edu.pe',
        password    ='nacontra',
        nombre      ='Mauro',
        apellido    ='Bobadilla Castillo'
    ),
] 
# Docentes
docentes = [
    Docente(
        codigo      =10726,
        correo      ='tchambilla@utec.edu.pe',
        nombre      ='Teófilo',
        apellido    ='Chambilla Aquino'
    ),
    Docente(
        codigo      =65323,
        correo      ='mabisrror@utec.edu.pe',
        nombre      ='Marvin',
        apellido    ='Abisrror Zarate'
    ),
    Docente(
        codigo      =10071,
        correo      ='hpantoja@utec.edu.pe',
        nombre      ='Hermes Yesser',
        apellido    ='Pantoja Carhuavilca'
    ),
    Docente(
        codigo      =10952,
        correo      ='bmolina@utec.edu.pe',
        nombre      ='Brigida Coromoto',
        apellido    ='Molina Carabaño'
    ),
    Docente(
        codigo      =10764,
        correo      ='rperezc@utec.edu.pe',
        nombre      ='Rosulo',
        apellido    ='Perez Cupe'
    ),
]
# Cursos
cursos = [
    Curso(
        codigo = 'CS2B01',
        curso = 'Desarrollo basado en plataformas',
        lab=True,
        teoria=True,
        teoria_virutal=False
    ),
    Curso(
        codigo = 'CS2701',
        curso = 'Base de datos I',
        lab=True,
        teoria=True,
        teoria_virutal=False
    ),
    Curso(
        codigo = 'EG0006',
        curso = 'Matemáticas III',
        lab=True,
        teoria=True,
        teoria_virutal=False
    ),
]
# Commit actuales
db.session.add_all(alumnos)
db.session.add_all(docentes)
db.session.add_all(cursos)
db.session.commit()
# Clase
clases = [
    Clase(
        curso='CS2701',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='00',
        vacantes=45,
        docente=10726,
    ),
    Clase(
        curso='CS2701',
        tipo=TipoClaseEnum.lab,
        seccion='01',
        numero='01',
        vacantes=45,
        docente=10726,
    ),
    Clase(
        curso='CS2B01',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='00',
        vacantes=30,
        docente=65323,
    ),
    Clase(
        curso='CS2B01',
        tipo=TipoClaseEnum.lab,
        seccion='01',
        numero='01',
        vacantes=30,
        docente=65323,
    ),
    Clase(
        curso='CS2B01',
        tipo=TipoClaseEnum.teoria,
        seccion='02',
        numero='00',
        vacantes=30,
        docente=65323,
    ),
    Clase(
        curso='CS2B01',
        tipo=TipoClaseEnum.lab,
        seccion='02',
        numero='01',
        vacantes=30,
        docente=65323,
    ),
    Clase(
        curso='EG0006',
        tipo=TipoClaseEnum.lab,
        seccion='01',
        numero='00',
        vacantes=270,
        docente=10071,
    ),
    Clase(
        curso='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='01',
        vacantes=45,
        docente=10952,
    ),
    Clase(
        curso='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='02',
        vacantes=45,
        docente=10071,
    ),
    Clase(
        curso='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='03',
        vacantes=45,
        docente=10071,
    ),
    Clase(
        curso='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='04',
        vacantes=45,
        docente=10764,
    ),
    Clase(
        curso='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='05',
        vacantes=45,
        docente=10764,
    ),
    Clase(
        curso='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='06',
        vacantes=45,
        docente=10952,
    ),
]
# Comit
db.session.add_all(clases)
db.session.commit()
# Sesiones
sesiones = [
    Sesion(
        id=1,
        curso='CS2701',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='00',
        dia=1,
        hora_inicio=20,
        hora_fin=22
    ),
    Sesion(
        id=1,
        curso='CS2701',
        clase_tipo=TipoClaseEnum.lab,
        clase_seccion='01',
        clase_numero='01',
        dia=3,
        hora_inicio=20,
        hora_fin=22
    ),
    Sesion(
        id=2,
        curso='CS2701',
        clase_tipo=TipoClaseEnum.lab,
        clase_seccion='01',
        clase_numero='01',
        dia=5,
        hora_inicio=20,
        hora_fin=22
    ),
    Sesion(
        id=1,
        curso='CS2B01',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='00',
        dia=1,
        hora_inicio=18,
        hora_fin=19
    ),
    Sesion(
        id=1,
        curso='CS2B01',
        clase_tipo=TipoClaseEnum.lab,
        clase_seccion='01',
        clase_numero='01',
        dia=4,
        hora_inicio=18,
        hora_fin=20
    ),
    Sesion(
        id=1,
        curso='CS2B01',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='02',
        clase_numero='00',
        dia=2,
        hora_inicio=20,
        hora_fin=21
    ),
    Sesion(
        id=1,
        curso='CS2B01',
        clase_tipo=TipoClaseEnum.lab,
        clase_seccion='02',
        clase_numero='01',
        dia=5,
        hora_inicio=20,
        hora_fin=22
    ),
    Sesion(
        id=1,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.lab,
        clase_seccion='01',
        clase_numero='00',
        dia=1,
        hora_inicio=8,
        hora_fin=9
    ),
    Sesion(
        id=1,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='01',
        dia=2,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=2,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='01',
        dia=4,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=1,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='02',
        dia=3,
        hora_inicio=7,
        hora_fin=9
    ),
    Sesion(
        id=2,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='02',
        dia=4,
        hora_inicio=7,
        hora_fin=9
    ),
    Sesion(
        id=1,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='03',
        dia=3,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=2,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='03',
        dia=4,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=1,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='04',
        dia=3,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=2,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='04',
        dia=4,
        hora_inicio=7,
        hora_fin=9
    ),
    Sesion(
        id=1,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='05',
        dia=3,
        hora_inicio=11,
        hora_fin=13
    ),
    Sesion(
        id=2,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='05',
        dia=4,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=1,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='06',
        dia=3,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=2,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='06',
        dia=4,
        hora_inicio=7,
        hora_fin=9
    ),
]
# Comit
db.session.add_all(sesiones)
db.session.commit()

# Horario
h1=Horario(
        alumno = 202010387
)
# Comit
db.session.add_all([h1])
db.session.commit()

# Lista
listas = [
    Lista(
        horario=h1.id,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='05'
    ),
    Lista(
        horario=h1.id,
        curso='EG0006',
        clase_tipo=TipoClaseEnum.lab,
        clase_seccion='01',
        clase_numero='00'
    ),
    Lista(
        horario=h1.id,
        curso='CS2B01',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='00',
    ),
    Lista(
        horario=h1.id,
        curso='CS2B01',
        clase_tipo=TipoClaseEnum.lab,
        clase_seccion='01',
        clase_numero='01',
    ),
    Lista(
        horario=h1.id,
        curso='CS2701',
        clase_tipo=TipoClaseEnum.teoria,
        clase_seccion='01',
        clase_numero='00',
    ),
    Lista(
        horario=h1.id,
        curso='CS2701',
        clase_tipo=TipoClaseEnum.lab,
        clase_seccion='01',
        clase_numero='01',
    ),
]
# Comit
db.session.add_all(listas)
db.session.commit()

# FAVORITOS
favoritos = [
    Favorito(
        horario=h1.id,
        alumno=201810312
    ),
    Favorito(
        horario=h1.id,
        alumno=202010114
    ),
]
db.session.add_all(favoritos)
db.session.commit()