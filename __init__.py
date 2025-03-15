# __init__.py

import os
from configparser import ConfigParser
from pathlib import Path
import pymysql

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Leer configuración desde config.ini
config = ConfigParser()
config.read(BASE_DIR / 'config.ini')

# Configuración de la base de datos
DB_CONFIG = {
    'host': config.get('database', 'host'),
    'port': config.getint('database', 'port'),
    'user': config.get('database', 'user'),
    'password': config.get('database', 'password'),
    'database': config.get('database', 'database'),
    'charset': config.get('database', 'charset', fallback='utf8mb4'),
    'autocommit': True
}

def connect_to_db():
    """Crea una conexión a la base de datos."""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise