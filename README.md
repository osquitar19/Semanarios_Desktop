# Semanarios Desktop

Una aplicación de escritorio moderna desarrollada en Python para la gestión de información hípica, reescrita desde Visual Basic 6.

## Descripción

Este proyecto es una modernización de un sistema de gestión hípica, implementado con tecnologías modernas y una arquitectura robusta. La aplicación permite manejar diversos aspectos relacionados con carreras de caballos, incluyendo:

- Gestión de pesos físicos
- Control de aprontes
- Manejo de programas
- Seguimiento de resultados

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal de desarrollo
- **PySide6**: Framework para la interfaz gráfica de usuario
- **SQLAlchemy**: ORM para la gestión de base de datos
- **MySQL**: Sistema de gestión de base de datos
- **Python-dotenv**: Gestión de variables de entorno

## Estructura del Proyecto

```
semanarios-desktop/
├── assets/              # Recursos estáticos
├── data/               # Datos y recursos
├── generated/          # Archivos UI generados
├── models/            # Modelos de base de datos
├── scripts/           # Scripts de utilidad
├── src/               # Código fuente principal
├── tests/             # Pruebas unitarias
├── ui/                # Archivos de interfaz de usuario
├── main.py            # Punto de entrada de la aplicación
├── db.py              # Configuración de base de datos
├── logica_*.py        # Módulos de lógica de negocio
└── pyproject.toml     # Configuración del proyecto
```

## Módulos Principales

### Lógica de Negocio

- **logica_pesos_fisicos.py**: Gestión de pesos físicos de caballos
- **logica_aprontes.py**: Control y registro de aprontes
- **logica_programas.py**: Manejo de programas de carreras
- **logica_resultados.py**: Registro y consulta de resultados
- **logica_main_window.py**: Ventana principal de la aplicación

### Base de Datos

El proyecto utiliza MySQL como sistema de base de datos, con SQLAlchemy como ORM. La configuración se maneja a través de variables de entorno en un archivo `.env`.

## Requisitos

Las dependencias principales incluyen:

- Python 3.x
- PySide6 6.8.2.1
- SQLAlchemy 2.0.32
- PyMySQL 1.1.0
- Pandas 2.2.2
- Python-dotenv 1.0.1

## Configuración

1. Crear un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Unix
.venv\Scripts\activate     # En Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements_uv.txt
```

3. Configurar variables de entorno:
Crear un archivo `.env` con:
```
DB_USER=usuario
DB_PASS=contraseña
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nombre_db
```

## Uso

Para ejecutar la aplicación:

```bash
python main.py
```

## Desarrollo

El proyecto utiliza varias herramientas de desarrollo:

- **convert_ui_to_py.py**: Script para convertir archivos UI de Qt a Python
- **pyproject.toml**: Gestión de dependencias y configuración del proyecto
- **.gitignore**: Control de archivos para Git

## Contribución

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear una rama para tu característica
3. Commit de tus cambios
4. Push a la rama
5. Crear un Pull Request

## Licencia

[Especificar la licencia del proyecto]

Lógica de la ventana principal: logica_main_window.py
UI de la ventana principal: generated/ui_main_window.py

La ventana principal tiene un menú con opciones y un contenedor. Cada una de estas opciones debe llevar a una ventana que será incorporada en el contenedor de la ventana principal.
Hay sólo dos opciones implementadas del menú (Edición de texto ---> Aprontes y --->Pesos físicos). La ventanas implementadas son: logica_aprontes.py, generated/ui_aprontes.py, logica_pesos_fisicos.py, generated/ui_pesos_fisicos.py


