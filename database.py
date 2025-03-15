import os
import pymysql
from sqlalchemy import create_engine
from configparser import ConfigParser
from pathlib import Path

def get_db_connection():
    """
    📌 Devuelve un Engine de SQLAlchemy en lugar de una conexión de PyMySQL.
    Las credenciales se obtienen desde variables de entorno o desde config.ini.
    """
    config = ConfigParser()
    config_path = Path(__file__).parent / 'config.ini'
    config.read(config_path)

    # 📌 Obtener configuración desde variables de entorno o config.ini
    db_config = {
        'host': os.getenv("DB_HOST", config.get('database', 'host', fallback='localhost')),
        'port': int(os.getenv("DB_PORT", config.get('database', 'port', fallback=3306))),
        'user': os.getenv("DB_USER", config.get('database', 'user', fallback='root')),
        'password': os.getenv("DB_PASSWORD", config.get('database', 'password', fallback='')),
        'database': os.getenv("DB_NAME", config.get('database', 'database', fallback='Semanarios')),
        'charset': os.getenv("DB_CHARSET", config.get('database', 'charset', fallback='utf8mb4'))
    }

    # 📌 Crear la URL de conexión para SQLAlchemy
    db_url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset={db_config['charset']}"

    try:
        # ✅ Devuelve un Engine de SQLAlchemy
        engine = create_engine(db_url, echo=False, pool_recycle=1800)
        return engine
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None  # Devuelve None si hay error