import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models.models import Base  # Ajusta la ruta según tu proyecto

# Carga las variables de entorno
load_dotenv()

# Construye la cadena de conexión
DB_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Verifica si DB_URI está correctamente construido
if not all([os.getenv('DB_USER'), os.getenv('DB_PASS'), os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME')]):
    raise ValueError("Error: Falta alguna variable de entorno en el archivo .env")

# Crea el engine
engine = create_engine(DB_URI, echo=False)  # echo=True para ver las consultas SQL

# Crea el "SessionLocal" para manejar sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Crea las tablas en la base de datos (si no existen)
    basándose en los modelos declarados en 'Base'.
    """
    Base.metadata.create_all(bind=engine)