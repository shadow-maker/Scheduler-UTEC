# Configuracion de conexion a Base de Datos
db_type     = 'postgresql'
db_host     = 'localhost'
db_port     = '5432'
db_name     = 'utecscheduler'
db_user     = 'postgres'
db_password = input('Password: ')
 
# Config de SQLAlchemy
SQLALCHEMY_DATABASE_URI = f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

