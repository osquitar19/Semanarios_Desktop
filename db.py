import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from configparser import ConfigParser
from pathlib import Path
from typing import List, Optional

from models.models import Base, ReunionCaballos
from database import get_db_connection

# Carga las variables de entorno
load_dotenv()

# Obtiene la conexión desde database.py (que ahora verifica si MySQL está corriendo)
engine = get_db_connection()

# Crea el "SessionLocal" para manejar sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Crea las tablas en la base de datos (si no existen)
    basándose en los modelos declarados en 'Base'.
    """
    Base.metadata.create_all(bind=engine)

def caballo_puesto(fecha, referencia, puesto=1) -> List[int]:
    """
    Devuelve el ID o IDs de los caballos que quedaron en el puesto especificado
    en una carrera determinada por fecha y referencia.
    
    Args:
        fecha (Date): Fecha de la carrera
        referencia (int): Referencia/número de la carrera
        puesto (int, optional): Posición final deseada. Defaults to 1 (primer puesto).
        
    Returns:
        List[int]: Lista de IDs de caballos en el puesto especificado. 
                 Si no hay empate, la lista tendrá un solo elemento.
                 Si hay empate, la lista contendrá múltiples IDs.
                 Si no se encuentra ningún caballo, retorna una lista vacía.
    """
    with SessionLocal() as session:
        resultados = session.query(ReunionCaballos.idCaballo).filter(
            ReunionCaballos.fecha == fecha,
            ReunionCaballos.referencia == referencia,
            ReunionCaballos.puesto == puesto
        ).all()
        
        # Extrae los IDs de los caballos de los resultados
        # Si hay más de uno, significa que hubo un empate
        return [resultado[0] for resultado in resultados]

def analizar_primeros_lugares_vs_actual(id_caballo, fecha_actual, referencia_actual) -> dict:
    """
    Analiza las carreras anteriores de un caballo para determinar si los caballos
    que quedaron en los 4 primeros lugares están inscritos en la carrera actual.
    
    Args:
        id_caballo (int): ID del caballo a analizar
        fecha_actual (Date): Fecha de la carrera actual
        referencia_actual (int): Referencia de la carrera actual
        
    Returns:
        dict: Diccionario con la siguiente estructura:
        {
            'carreras_anteriores': [
                {
                    'fecha': fecha_carrera,
                    'referencia': referencia_carrera,
                    'primeros_lugares': [
                        {
                            'puesto': 1,
                            'caballos': [id1, id2, ...],  # Lista en caso de empate
                            'en_carrera_actual': True/False,  # Si alguno está en carrera actual
                            'es_caballo_analizado': True/False  # Si el caballo analizado está en este puesto
                        },
                        {...}, # Puesto 2
                        {...}, # Puesto 3
                        {...}  # Puesto 4
                    ]
                },
                {...} # Otra carrera anterior
            ],
            'resumen': {
                'total_enfrentados_anteriormente': n,  # Total de caballos diferentes enfrentados anteriormente que están en carrera actual
                'ganado_a': [id1, id2, ...],  # IDs de caballos a los que ha ganado y están en carrera actual
                'perdido_contra': [id1, id2, ...],  # IDs de caballos que le han ganado y están en carrera actual
                'empatado_con': [id1, id2, ...]  # IDs de caballos con los que ha empatado y están en carrera actual
            }
        }
    """
    with SessionLocal() as session:
        # 1. Obtenemos las carreras anteriores del caballo
        carreras_anteriores = session.query(
            ReunionCaballos.fecha,
            ReunionCaballos.referencia
        ).filter(
            ReunionCaballos.idCaballo == id_caballo,
            ReunionCaballos.corrio == 1  # Solo carreras que ya se corrieron
        ).order_by(
            ReunionCaballos.fecha.desc()  # Ordenamos por fecha descendente (más recientes primero)
        ).all()
        
        # 2. Obtenemos los caballos inscritos en la carrera actual
        caballos_carrera_actual = session.query(
            ReunionCaballos.idCaballo
        ).filter(
            ReunionCaballos.fecha == fecha_actual,
            ReunionCaballos.referencia == referencia_actual,
            ReunionCaballos.corrio == 0  # Solo los que no han corrido
        ).all()
        
        # Convertimos a un conjunto para búsquedas rápidas
        caballos_actuales = {caballo[0] for caballo in caballos_carrera_actual}
        
        # Inicializamos el resultado
        resultado = {
            'carreras_anteriores': [],
            'resumen': {
                'total_enfrentados_anteriormente': 0,
                'ganado_a': [],
                'perdido_contra': [],
                'empatado_con': []
            }
        }
        
        # Conjuntos para seguimiento de caballos únicos en el resumen
        ganado_a = set()
        perdido_contra = set()
        empatado_con = set()
        
        # 3. Para cada carrera anterior, analizamos los 4 primeros lugares
        for fecha, referencia in carreras_anteriores:
            carrera_info = {
                'fecha': fecha,
                'referencia': referencia,
                'primeros_lugares': []
            }
            
            # Posición del caballo analizado en esta carrera
            puesto_caballo_analizado = session.query(
                ReunionCaballos.puesto
            ).filter(
                ReunionCaballos.fecha == fecha,
                ReunionCaballos.referencia == referencia,
                ReunionCaballos.idCaballo == id_caballo
            ).scalar()
            
            # Analizamos los primeros 4 puestos
            for puesto in range(1, 5):
                caballos_en_puesto = caballo_puesto(fecha, referencia, puesto)
                
                # Si no hay caballos en este puesto (puede pasar si hubo empate en puesto anterior)
                if not caballos_en_puesto:
                    continue
                
                # Verificamos si alguno está en la carrera actual
                en_carrera_actual = any(cab_id in caballos_actuales for cab_id in caballos_en_puesto)
                
                # Verificamos si el caballo analizado está en este puesto
                es_caballo_analizado = id_caballo in caballos_en_puesto
                
                # Actualizamos los resúmenes
                for cab_id in caballos_en_puesto:
                    if cab_id in caballos_actuales and cab_id != id_caballo:
                        # Si el caballo analizado está en un puesto mejor
                        if puesto_caballo_analizado < puesto:
                            ganado_a.add(cab_id)
                        # Si el caballo analizado está en un puesto peor
                        elif puesto_caballo_analizado > puesto:
                            perdido_contra.add(cab_id)
                        # Si están en el mismo puesto (empate)
                        elif puesto_caballo_analizado == puesto and cab_id != id_caballo:
                            empatado_con.add(cab_id)
                
                # Agregamos la información de este puesto
                carrera_info['primeros_lugares'].append({
                    'puesto': puesto,
                    'caballos': caballos_en_puesto,
                    'en_carrera_actual': en_carrera_actual,
                    'es_caballo_analizado': es_caballo_analizado
                })
            
            # Agregamos la información de esta carrera
            resultado['carreras_anteriores'].append(carrera_info)
        
        # Actualizamos el resumen final
        resultado['resumen']['ganado_a'] = list(ganado_a)
        resultado['resumen']['perdido_contra'] = list(perdido_contra)
        resultado['resumen']['empatado_con'] = list(empatado_con)
        resultado['resumen']['total_enfrentados_anteriormente'] = len(ganado_a) + len(perdido_contra) + len(empatado_con)
        
        return resultado