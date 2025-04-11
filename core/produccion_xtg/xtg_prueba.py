"""
Módulo para generar el contenido XTG del formato 'Prueba'.
Implementa un enfoque procedimental con iteraciones jerárquicas.
"""
from sqlalchemy import desc
from db import SessionLocal
from models.models import (
    Caballos, ReunionCarreras, ReunionCaballos
)

def generar_contenido_prueba():
    """Genera el contenido de prueba para el XTG usando iteraciones jerárquicas"""
    with SessionLocal() as session:
        contenido = ""
        
        # 1. Iteración por Fechas
        fechas = session.query(ReunionCarreras.fecha).filter(
            ReunionCarreras.corrida == 0
        ).distinct().order_by(ReunionCarreras.fecha).all()
        
        fechas = [fecha[0] for fecha in fechas]  # Extraer solo las fechas
        
        for fecha in fechas:
            contenido += f"\nFecha: {fecha}\n"
            contenido += "------------------\n"
            
            # 2. Iteración por Carreras
            carreras = session.query(ReunionCarreras).filter(
                ReunionCarreras.fecha == fecha
            ).order_by(ReunionCarreras.referencia).all()
            
            for carrera in carreras:
                contenido += f"{carrera.ordenDeCarrera}ª Carrera. {carrera.referencia}.  {carrera.distancia} mts. {carrera.pista}\n"
                
                # 3. Iteración por Caballos
                caballos = session.query(ReunionCaballos).join(
                    Caballos, ReunionCaballos.idCaballo == Caballos.idCaballo
                ).filter(
                    ReunionCaballos.fecha == fecha, 
                    ReunionCaballos.referencia == carrera.referencia
                ).order_by(ReunionCaballos.realCajon).all()
                
                for caballo in caballos:
                    # Información básica del caballo
                    contenido += f"  {caballo.cajon}\t{caballo.caballo.nombre}\t{caballo.kilos}\n"
                    
                    # Carreras anteriores
                    carreras_anteriores = session.query(ReunionCaballos).join(
                        Caballos, ReunionCaballos.idCaballo == Caballos.idCaballo
                    ).filter(
                        ReunionCaballos.fecha < fecha, 
                        ReunionCaballos.idCaballo == caballo.idCaballo
                    ).order_by(desc(ReunionCaballos.fecha)).limit(6).all()
                    
                    for carrera_anterior in carreras_anteriores:
                        contenido += f"    {carrera_anterior.referencia}\t{carrera_anterior.fecha}\t{carrera_anterior.puesto}º\t{carrera_anterior.kilos}\n"
        
        return contenido