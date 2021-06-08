from app import Alumno, Docente, Curso, Clase, Sesion, Horario, \
                TipoClaseEnum,\
                db

# INSERTAR FILAS
# Alumno
alumnos = [
    Alumno(
        codigo      ='202010387',
        correo      ='rodrigo.salazar@utec.edu.pe',
        password    ='sample',
        nombre      ='Rodrigo Gabriel',
        apellido    ='Salazar Alva'
    ),
    Alumno(
        codigo      ='201810312',
        correo      ='cesar.martinez@utec.edu.pe',
        password    ='csr',
        nombre      ='César Alejandro',
        apellido    ='Ortiz Martinez'
    ),
    Alumno(
        codigo      ='202010434',
        correo      ='leonardo.yupanqui@utec.edu.pe',
        password    ='leopass',
        nombre      ='Leonardo Fabricio',
        apellido    ='Yupanqui Mera'
    ),
    Alumno(
        codigo      ='201710620',
        correo      ='alberto.pelaez@utec.edu.pe',
        password    ='albertopass',
        nombre      ='Alberto Alejandro',
        apellido    ='Pelaez Sagastegui'
    ),
    Alumno(
        codigo      ='201910240',
        correo      ='nayelli.cibelly@utec.edu.pe',
        password    ='nacontra',
        nombre      ='Nayeli Cibelly',
        apellido    ='Navarro Pizarro'
    ),
    Alumno(
        codigo      ='202010114',
        correo      ='mauro.bobadilla@utec.edu.pe',
        password    ='nacontra',
        nombre      ='Mauro',
        apellido    ='Bobadilla Castillo'
    ),
] 
# Docentes
docentes = [
    Docente(
        codigo      ='10726',
        correo      ='tchambilla@utec.edu.pe',
        nombre      ='Teófilo',
        apellido    ='Chambilla Aquino'
    ),
    Docente(
        codigo      ='65323',
        correo      ='mabisrror@utec.edu.pe',
        nombre      ='Marvin',
        apellido    ='Abisrror Zarate'
    ),
    Docente(
        codigo      ='10071',
        correo      ='hpantoja@utec.edu.pe',
        nombre      ='Hermes Yesser',
        apellido    ='Pantoja Carhuavilca'
    ),
    Docente(
        codigo      ='10952',
        correo      ='bmolina@utec.edu.pe',
        nombre      ='Brigida Coromoto',
        apellido    ='Molina Carabaño'
    ),
    Docente(
        codigo      ='10764',
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
        id = 1,
        curso_codigo='CS2701',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='00',
        vacantes=45,
        docente_codigo=10726,
    ),
    Clase(
        id = 2,
        curso_codigo='CS2701',
        tipo=TipoClaseEnum.lab,
        seccion='01',
        numero='01',
        vacantes=45,
        docente_codigo=10726,
    ),
    Clase(
        id = 3,
        curso_codigo='CS2B01',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='00',
        vacantes=30,
        docente_codigo=65323,
    ),
    Clase(
        id = 4,
        curso_codigo='CS2B01',
        tipo=TipoClaseEnum.lab,
        seccion='01',
        numero='01',
        vacantes=30,
        docente_codigo=65323,
    ),
    Clase(
        id = 5,
        curso_codigo='CS2B01',
        tipo=TipoClaseEnum.teoria,
        seccion='02',
        numero='00',
        vacantes=30,
        docente_codigo=65323,
    ),
    Clase(
        id = 6,
        curso_codigo='CS2B01',
        tipo=TipoClaseEnum.lab,
        seccion='02',
        numero='01',
        vacantes=30,
        docente_codigo=65323,
    ),
    Clase(
        id = 7,
        curso_codigo='EG0006',
        tipo=TipoClaseEnum.lab,
        seccion='01',
        numero='00',
        vacantes=270,
        docente_codigo=10071,
    ),
    Clase(
        id = 8,
        curso_codigo='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='01',
        vacantes=45,
        docente_codigo=10952,
    ),
    Clase(
        id = 9,
        curso_codigo='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='02',
        vacantes=45,
        docente_codigo=10071,
    ),
    Clase(
        id = 10,
        curso_codigo='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='03',
        vacantes=45,
        docente_codigo=10071,
    ),
    Clase(
        id = 11,
        curso_codigo='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='04',
        vacantes=45,
        docente_codigo=10764,
    ),
    Clase(
        id = 12,
        curso_codigo='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='05',
        vacantes=45,
        docente_codigo=10764,
    ),
    Clase(
        id = 13,
        curso_codigo='EG0006',
        tipo=TipoClaseEnum.teoria,
        seccion='01',
        numero='06',
        vacantes=45,
        docente_codigo=10952,
    ),
]
# Comit
db.session.add_all(clases)
db.session.commit()
# Sesiones
sesiones = [
    Sesion(
        id=1,
        clase_id=1,
        dia=1,
        hora_inicio=20,
        hora_fin=22
    ),
    Sesion(
        id=2,
        clase_id=2,
        dia=3,
        hora_inicio=20,
        hora_fin=22
    ),
    Sesion(
        id = 3,
        clase_id=2,
        dia=5,
        hora_inicio=20,
        hora_fin=22
    ),
    Sesion(
        id=4,
        clase_id=3,
        dia=1,
        hora_inicio=18,
        hora_fin=19
    ),
    Sesion(
        id=5,
        clase_id=4,
        dia=4,
        hora_inicio=18,
        hora_fin=20
    ),
    Sesion(
        id=6,
        clase_id=5,
        dia=2,
        hora_inicio=20,
        hora_fin=21
    ),
    Sesion(
        id=7,
        clase_id=6,
        dia=5,
        hora_inicio=20,
        hora_fin=22
    ),
    Sesion(
        id=8,
        clase_id=7,
        dia=1,
        hora_inicio=8,
        hora_fin=9
    ),
    Sesion(
        id=9,
        clase_id=8,
        dia=2,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=10,
        clase_id=8,
        dia=4,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=11,
        clase_id=9,
        dia=3,
        hora_inicio=7,
        hora_fin=9
    ),
    Sesion(
        id=12,
        clase_id=9,
        dia=4,
        hora_inicio=7,
        hora_fin=9
    ),
    Sesion(
        id=13,
        clase_id=10,
        dia=3,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=14,
        clase_id=10,
        dia=4,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=15,
        clase_id=11,
        dia=3,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=16,
        clase_id=11,
        dia=4,
        hora_inicio=7,
        hora_fin=9
    ),
    Sesion(
        id=17,
        clase_id=12,
        dia=3,
        hora_inicio=11,
        hora_fin=13
    ),
    Sesion(
        id=18,
        clase_id=12,
        dia=4,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=19,
        clase_id=13,
        dia=3,
        hora_inicio=9,
        hora_fin=11
    ),
    Sesion(
        id=20,
        clase_id=13,
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
        alumno_codigo = '202010387'
)
# Comit
db.session.add_all([h1])
db.session.commit()

# Lista
h1.clases.append(Clase.query.get(1))
h1.clases.append(Clase.query.get(2))
h1.clases.append(Clase.query.get(3))
h1.clases.append(Clase.query.get(4))
h1.clases.append(Clase.query.get(7))
h1.clases.append(Clase.query.get(12))
db.session.add(h1)
db.session.commit()


# FAVORITOS
a1 = Alumno.query.get('201810312')
a2 = Alumno.query.get('202010114')
a1.favoritos.append(h1)
a2.favoritos.append(h1)
db.session.add(a1)
db.session.add(a2)
db.session.commit()
