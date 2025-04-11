import os
import pymysql
from sqlalchemy import create_engine
from configparser import ConfigParser
from pathlib import Path
import time
import subprocess
import platform
import sys

def is_mysql_running():
    """Verifica si MySQL está ejecutándose en el sistema"""
    system = platform.system()
    
    try:
        if system == "Windows":
            # Para Windows
            output = subprocess.check_output("sc query MySQL", shell=True)
            return b"RUNNING" in output
        elif system == "Darwin":  # macOS
            output = subprocess.check_output("ps aux | grep mysql | grep -v grep", shell=True)
            return len(output) > 0
        elif system == "Linux":
            output = subprocess.check_output("systemctl is-active mysql || systemctl is-active mysqld", shell=True, stderr=subprocess.DEVNULL)
            return b"active" in output
        return False
    except subprocess.CalledProcessError:
        return False

def start_mysql_service():
    """Intenta iniciar el servicio MySQL si no está corriendo"""
    system = platform.system()
    
    try:
        if system == "Windows":
            subprocess.run("net start MySQL", shell=True, check=True)
            return True
        elif system == "Darwin":  # macOS
            subprocess.run("brew services start mysql", shell=True, check=True)
            return True
        elif system == "Linux":
            subprocess.run("sudo systemctl start mysql || sudo systemctl start mysqld", shell=True, check=True)
            return True
    except subprocess.SubprocessError:
        return False

def get_db_connection():
    """
    📌 Devuelve un Engine de SQLAlchemy en lugar de una conexión de PyMySQL.
    Las credenciales se obtienen desde variables de entorno o desde config.ini.
    Ahora verifica si MySQL está corriendo y trata de iniciarlo si es necesario.
    """
    config = ConfigParser()
    config_path = Path(__file__).parent / 'config.ini'
    config.read(config_path)

    # 📌 Obtener configuración desde variables de entorno o config.ini
    db_config = {
        'host': os.getenv("DB_HOST", config.get('database', 'host', fallback='localhost')),
        'port': int(os.getenv("DB_PORT", config.get('database', 'port', fallback=3306))),
        'user': os.getenv("DB_USER", config.get('database', 'user', fallback='root')),
        'password': os.getenv("DB_PASS", config.get('database', 'password', fallback='')),
        'database': os.getenv("DB_NAME", config.get('database', 'database', fallback='Semanarios')),
        'charset': os.getenv("DB_CHARSET", config.get('database', 'charset', fallback='utf8mb4'))
    }

    # 📌 Verificar si MySQL está corriendo
    if not is_mysql_running():
        print("⚠️ MySQL no está ejecutándose. Intentando iniciar el servicio...")
        if not start_mysql_service():
            print("❌ No se pudo iniciar el servicio MySQL automáticamente.")
            print("Por favor inicie el servicio MySQL manualmente e intente nuevamente.")
            sys.exit(1)
        # Esperar a que MySQL esté completamente iniciado
        time.sleep(5)

    # 📌 Crear la URL de conexión para SQLAlchemy
    db_url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset={db_config['charset']}"

    max_retries = 3
    retries = 0
    
    while retries < max_retries:
        try:
            # ✅ Devuelve un Engine de SQLAlchemy
            engine = create_engine(db_url, echo=False, pool_recycle=1800, pool_pre_ping=True)
            # Verificar conexión
            with engine.connect() as conn:
                pass
            return engine
        except Exception as e:
            retries += 1
            if retries >= max_retries:
                print(f"❌ Error al conectar a la base de datos después de {max_retries} intentos: {e}")
                print("Verifique que MySQL esté instalado y que la base de datos exista.")
                sys.exit(1)
            print(f"⚠️ Intento {retries}/{max_retries}: Error de conexión, reintentando en 2 segundos...")
            time.sleep(2)