import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from configparser import ConfigParser
from pathlib import Path

# Leer configuración desde config.ini como respaldo
config_path = Path(__file__).resolve().parent.parent / 'config.ini'
config = ConfigParser()
config.read(config_path)

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER', config.get('database', 'user'))}:"
    f"{os.getenv('DB_PASSWORD', config.get('database', 'password'))}@"
    f"{os.getenv('DB_HOST', config.get('database', 'host'))}:"
    f"{os.getenv('DB_PORT', config.get('database', 'port'))}/"
    f"{os.getenv('DB_NAME', config.get('database', 'database'))}"
)

# Configuración de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()