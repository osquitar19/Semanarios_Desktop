"""
Módulo para generar el contenido XTG del formato 'Estudie su Polla'.
Implementa un enfoque procedimental con iteraciones jerárquicas.
"""
import datetime
import pymysql
from sqlalchemy.sql import text
from sqlalchemy import and_
from db import SessionLocal
from models.models import (
    Caballos, Jinetes, ReunionCarreras, ReunionCaballos, Preparadores, Studs,
    Separaciones, CondicionesNuevas, Padrillos, Madres, Abuelos, Paises, Criadores, Colores,
    Contratiempos, ReunionContratiempos, Clasicos
)
import traceback

from sqlalchemy.dialects import mysql

# Funciones de utilidad para el formateo

from PySide6.QtGui import QFont, QFontMetrics

def condensar_texto_qxp(texto, nombre_fuente, tamano_fuente, ancho_maximo):
    fuente = QFont(nombre_fuente, tamano_fuente)
    metrics = QFontMetrics(fuente)
    ancho_texto = metrics.horizontalAdvance(texto)

    if ancho_texto <= ancho_maximo:
        return texto  # No necesita condensación

    porcentaje = int(ancho_maximo / ancho_texto * 100)
    porcentaje = max(10, min(porcentaje, 100))  # Evita valores extremos
    return f"<h{porcentaje}>{texto}<@$h>"

def fecha_formato(fecha_mysql):
    """
    Convierte una fecha de MySQL a formato 'dd MMM'
    
    Args:
        fecha_mysql: Fecha en formato MySQL ('YYYY-MM-DD') o un objeto datetime.date
        
    Returns:
        str: Fecha formateada como 'dd MMM' (ej: '01 ENE')
    """
    # Diccionario de nombres de meses abreviados en español
    meses = {
        1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR', 5: 'MAY', 6: 'JUN',
        7: 'JUL', 8: 'AGO', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DIC'
    }
    
    # Manejar tanto strings como objetos datetime.date
    if isinstance(fecha_mysql, str):
        fecha = datetime.datetime.strptime(fecha_mysql, '%Y-%m-%d')
    else:
        # Ya es un objeto datetime.date
        fecha = fecha_mysql
    
    # Formatear la fecha como "dd MMM"
    dia = fecha.day
    mes = meses[fecha.month]
    
    return f"{dia:02d} {mes}"

def modalidad_caballo(modalidad, sexo, debutante):
    """Devuelve la modalidad del caballo para Estudie su Polla"""
    if debutante != 0:
        return "(Debuta)"
    if modalidad == "M":
        return "(M. Lote)"
    elif modalidad == "L" and sexo == "M":
        return "(Ligero)"
    elif modalidad == "L" and sexo == "H":
        return "(Ligera)"
    return ""

def formato_kilos(k1, m1, k2, m2, quintos):
    """Formatea los kilos del caballo para Estudie su Polla"""
    m1_neto = f".{m1}" if m1 != 0 else ""
    m2_neto = f".{m2}" if m2 != 0 else ""
    quintos_neto = f" {quintos}/5" if quintos != 0 else ""
    descargo = f"/{k2}" if k2 != 0 else ""
    return f"{k1}{m1_neto}{descargo}{m2_neto}{quintos_neto} k.-"

def kilos_historial(kilos, tipo=1):
    """Formatea los kilos para el historial"""
    kilos = str(kilos)
    if len(kilos) == 2:
        return kilos
    if tipo == 1 and len(kilos) == 4:   
        return kilos[2:4]
    if tipo != 1 and len(kilos) == 4:
        return kilos[0:2] + "/"+ kilos[2:4]
    return "error"

def jinete_historia(session, id_jinete, id_jinete_actual=None):
    """Formatea el nombre del jinete, con etiqueta de estilo si es el mismo que el actual"""
    jinete = session.query(Jinetes).filter(Jinetes.idJinete == id_jinete).first()
    if jinete:
        # Si el jinete de la carrera anterior es el mismo que el actual, agregar etiqueta de estilo
        if id_jinete_actual is not None and id_jinete == id_jinete_actual:
            return f"<@HJinete>{jinete.estudie}<@$p>"
        return jinete.estudie
    return "---"

def distancia_historia(distancia_anterior, pista_anterior, distancia_actual, pista_actual):
    """Formatea la distancia, con etiqueta de estilo si coincide con la actual"""
    distancia_str = f"{distancia_anterior}"
    
    # Verificar si coinciden distancia y pista
    if (distancia_anterior == distancia_actual and 
        pista_anterior == pista_actual):
        distancia_str = f"<@HDistancia>{distancia_str}<@$p>"
        
    return distancia_str

def pista_historia(pista, pista_actual=None):
    """Devuelve la pista formateada para el historial, con etiquetas de estilo si coincide con la actual"""
    if pista and (pista.upper() == "C" or pista.upper() == "CÉSPED" or pista.upper() == "CESPED"):
        # Si es césped y coincide con la pista actual, añadir etiqueta de estilo
        if pista_actual and (pista_actual.upper() == "C" or pista_actual.upper() == "CÉSPED" or pista_actual.upper() == "CESPED"):
            return "<@HCesped>-C-<@$p>"
        return "-C-"
    return ""

def contar_caballos_corrieron(session, fecha, referencia):
    """Cuenta cuántos caballos corrieron en una carrera"""
    count = session.query(ReunionCaballos).filter(
        ReunionCaballos.fecha == fecha,
        ReunionCaballos.referencia == referencia,
        ReunionCaballos.corrio == 1
    ).count()
    
    return count

def cajon_neto(session, fecha, referencia, id_caballo):
    """Calcula el cajón real excluyendo los caballos retirados"""
    caballos = session.query(ReunionCaballos).filter(
        ReunionCaballos.fecha == fecha,
        ReunionCaballos.referencia == referencia,
        ReunionCaballos.corrio == 1
    ).order_by(ReunionCaballos.realCajon).all()
    
    cajon_real = 1
    for caballo in caballos:
        if caballo.idCaballo == id_caballo:
            return cajon_real
        cajon_real += 1
        
    return 0

def total_boletos(session, fecha, referencia):
    """Calcula el total de boletos jugados en una carrera"""
    caballos = session.query(ReunionCaballos).filter(
        ReunionCaballos.fecha == fecha,
        ReunionCaballos.referencia == referencia
    ).all()
    
    total = 0.0
    for caballo in caballos:
        if hasattr(caballo, 'boletosGanador') and caballo.boletosGanador is not None:
            total += float(caballo.boletosGanador)
            
    return total

def dividendo_ganador(session, fecha, referencia, id_caballo, precio_boleto=3.00, detraccion=0.74):
    """Calcula el dividendo del caballo ganador"""
    # Obtener el total de boletos jugados en la carrera
    boletos_total = total_boletos(session, fecha, referencia)
    
    # Obtener los boletos reales jugados al caballo
    caballo = session.query(ReunionCaballos).filter(
        ReunionCaballos.fecha == fecha,
        ReunionCaballos.referencia == referencia,
        ReunionCaballos.idCaballo == id_caballo
    ).first()
    
    # Si no hay datos o no tiene boletos reales, devolver "0.00"
    if not caballo or not hasattr(caballo, 'boletosReales') or caballo.boletosReales is None or float(caballo.boletosReales) == 0:
        return "0.00"
    
    # Calcular el dividendo
    dividendo = (boletos_total * detraccion * precio_boleto) / float(caballo.boletosReales)
    
    # Formatear el resultado con dos decimales
    return f"{dividendo:.2f}"

def tiempo_formato(tiempo_valor, unidad='centesimos'):
    """Convierte un tiempo en centésimos o quintos de segundo al formato adecuado"""
    # Si es None o vacío, devolver cadena vacía
    if tiempo_valor is None or tiempo_valor == '':
        return ''
        
    # Convertir a entero si es string
    if isinstance(tiempo_valor, str):
        try:
            tiempo_valor = int(tiempo_valor)
        except ValueError:
            return 'error'
            
    # Validar que es un número positivo
    if tiempo_valor < 0:
        return 'error'
    
    if unidad == 'centesimos':
        # Calcular minutos, segundos y centésimos
        minutos = tiempo_valor // 6000
        segundos = (tiempo_valor % 6000) // 100
        centesimos = tiempo_valor % 100
        
        # Formatear el resultado para centésimos
        return f"{minutos}'{segundos:02d}\"{centesimos:02d}"
    else:  # unidad == 'quintos'
        # Calcular minutos, segundos y quintos
        # 300 quintos = 60 segundos = 1 minuto
        minutos = tiempo_valor // 300
        segundos = (tiempo_valor % 300) // 5
        quintos = tiempo_valor % 5
        
        # Formatear el resultado para quintos
        return f"{minutos}'{segundos:02d}\"{quintos}"

def obtener_historia_2(session, reunion_caballo):
    """
    Obtiene información sobre los primeros 4 lugares de las carreras anteriores
    y verifica si están inscritos en la carrera actual.
    """
    from db import analizar_primeros_lugares_vs_actual
    
    # Usar la función ya existente en db.py
    return analizar_primeros_lugares_vs_actual(
        reunion_caballo.idCaballo, 
        reunion_caballo.fecha, 
        reunion_caballo.referencia
    )

def calcular_edad_caballo(fecha_nacimiento, fecha_carrera):
    """
    Calcula la edad del caballo en años en la fecha de la carrera.
    Adaptado de la función edad_años de VB6 que usa el 1 de julio como fecha de referencia.
    
    Args:
        fecha_nacimiento (datetime.date): Fecha de nacimiento del caballo
        fecha_carrera (datetime.date): Fecha de la carrera
        
    Returns:
        int: Edad del caballo en años
    """
    import datetime
    
    # Calcular diferencia básica de años
    edad = fecha_carrera.year - fecha_nacimiento.year
    
    # Crear fechas clave (1 de julio) para ambos años
    fecha_clave_nacimiento = datetime.date(fecha_nacimiento.year, 7, 1)
    fecha_clave_carrera = datetime.date(fecha_carrera.year, 7, 1)
    
    # Ajustar edad según las fechas clave
    if fecha_nacimiento < fecha_clave_nacimiento:
        # Si nació antes del 1 de julio, es un año mayor
        edad += 1
        
    if fecha_carrera < fecha_clave_carrera:
        # Si la carrera es antes del 1 de julio, es un año menor
        edad -= 1
        
    return edad

def verificar_referencia_coincide(session, carrera_referencia, fecha_actual, referencia_actual):
    """
    Verifica si la referencia de una carrera anterior coincide con la de algún caballo en la carrera actual
    
    Args:
        session: Sesión de la base de datos
        carrera_referencia: Referencia de la carrera a verificar
        fecha_actual: Fecha de la carrera actual
        referencia_actual: Referencia de la carrera actual
        
    Returns:
        bool: True si coincide, False en caso contrario
    """
    # Obtener todos los caballos inscritos en la carrera actual
    caballos_carrera_actual = session.query(ReunionCaballos).filter(
        ReunionCaballos.fecha == fecha_actual,
        ReunionCaballos.referencia == referencia_actual
    ).all()
    
    # Obtener las referencias de sus carreras anteriores
    for caballo in caballos_carrera_actual:
        carreras_anteriores = session.query(ReunionCaballos).filter(
            ReunionCaballos.idCaballo == caballo.idCaballo,
            ReunionCaballos.fecha < fecha_actual,
            ReunionCaballos.referencia == carrera_referencia,
            ReunionCaballos.corrio == 1
        ).first()
        
        if carreras_anteriores:
            return True
    
    return False

def verificar_caballo_gano_siguiente(session, id_caballo, fecha_carrera, referencia_carrera):
    """
    Verifica si el caballo ganó en su siguiente carrera después de la indicada
    
    Args:
        session: Sesión de la base de datos
        id_caballo: ID del caballo
        fecha_carrera: Fecha de la carrera de referencia
        referencia_carrera: Referencia de la carrera de referencia
        
    Returns:
        bool: True si el caballo ganó su siguiente carrera, False en caso contrario
    """
    # Buscar la siguiente carrera del caballo después de la fecha y referencia dadas
    siguiente_carrera = session.query(ReunionCaballos).filter(
        ReunionCaballos.idCaballo == id_caballo,
        ReunionCaballos.corrio == 1,
        # La carrera debe ser después de la de referencia o en la misma fecha pero con referencia mayor
        ((ReunionCaballos.fecha > fecha_carrera) | 
         ((ReunionCaballos.fecha == fecha_carrera) & (ReunionCaballos.referencia > referencia_carrera)))
    ).order_by(
        ReunionCaballos.fecha.asc(),
        ReunionCaballos.referencia.asc()
    ).first()
    
    # Verificar si ganó
    if siguiente_carrera and siguiente_carrera.puesto == 1:
        return True
    
    return False

def obtener_primeros_lugares(session, fecha, referencia):
    """
    Obtiene los 4 primeros lugares de una carrera con sus detalles
    
    Args:
        session: Sesión de la base de datos
        fecha (datetime.date): Fecha de la carrera
        referencia (int): Referencia de la carrera
        
    Returns:
        list: Lista con los caballos que ocuparon los 4 primeros lugares
    """
    from models.models import Caballos, ReunionCaballos, Separaciones
    
    # Obtener los caballos que corrieron en esta carrera y quedaron en los primeros 4 lugares
    primeros = session.query(
        ReunionCaballos, Caballos, Separaciones
    ).join(
        Caballos, ReunionCaballos.idCaballo == Caballos.idCaballo
    ).outerjoin(
        Separaciones, ReunionCaballos.idSeparacion == Separaciones.idSeparacion
    ).filter(
        ReunionCaballos.fecha == fecha,
        ReunionCaballos.referencia == referencia,
        ReunionCaballos.puesto <= 4,
        ReunionCaballos.corrio == 1
    ).order_by(
        ReunionCaballos.puesto.asc()
    ).all()
    
    return primeros

def generar_bloque_info_basica(session, reunion_caballo):
    """
    Genera el primer bloque: información básica del caballo
    
    Args:
        session: Sesión de la base de datos
        reunion_caballo: Objeto ReunionCaballos con los datos del caballo en la carrera
        
    Returns:
        str: Texto formateado con la información básica del caballo
    """
    from models.models import Jinetes, Preparadores, Studs
    import datetime
    
    # Obtener estadísticas del jinete y preparador
    estadistica_jinete = round(reunion_caballo.jinete.ganadas / max(1, reunion_caballo.jinete.corridas), 2)
    estadistica_preparador = round(reunion_caballo.preparador.ganadas / max(1, reunion_caballo.preparador.corridas), 2)
    
    # Obtener carreras/ganadas del caballo con este jinete
    jinete_caballo = session.query(ReunionCaballos).filter(
        ReunionCaballos.idCaballo == reunion_caballo.idCaballo,
        ReunionCaballos.idJinete == reunion_caballo.idJinete,
        ReunionCaballos.corrio == 1
    ).all()
    
    corridas_jinete = len(jinete_caballo)
    ganadas_jinete = sum(1 for rc in jinete_caballo if rc.puesto == 1)
    
    # Obtener el año de la primera carrera no corrida
    primera_carrera = session.query(ReunionCarreras).filter(
        ReunionCarreras.corrida == 0
    ).order_by(ReunionCarreras.fecha.asc()).first()
    
    if primera_carrera:
        # Establecer fecha de inicio para estadísticas: 1 de enero del año de la primera carrera no corrida
        fecha_inicio = datetime.date(primera_carrera.fecha.year, 1, 1)
    else:
        # Si no hay carreras no corridas, usar el año actual
        hoy = datetime.date.today()
        fecha_inicio = datetime.date(hoy.year, 1, 1)
    
    # Obtener carreras/ganadas del jinete con este preparador desde fecha_inicio
    jinete_preparador = session.query(ReunionCaballos).filter(
        ReunionCaballos.idJinete == reunion_caballo.idJinete,
        ReunionCaballos.idPreparador == reunion_caballo.idPreparador,
        ReunionCaballos.corrio == 1,
        ReunionCaballos.fecha >= fecha_inicio
    ).all()
    
    corridas_jinete_prep = len(jinete_preparador)
    ganadas_jinete_prep = sum(1 for rc in jinete_preparador if rc.puesto == 1)
    
    # Formatear información
    modalidad = modalidad_caballo(
        reunion_caballo.caballo.modalidad, 
        reunion_caballo.caballo.sexo, 
        reunion_caballo.debutante
    )
    
    kilos = formato_kilos(
        reunion_caballo.k1, 
        reunion_caballo.m1, 
        reunion_caballo.k2, 
        reunion_caballo.m2, 
        reunion_caballo.quintos
    )
    
    # Formatear estadísticas jinete/caballo
    info_jinete_caballo = f"{corridas_jinete}/{ganadas_jinete}" if corridas_jinete > 0 else ""
    
    # Formatear estadísticas de jinete y preparador como porcentajes
    estadistica_jinete_str = f".{int(estadistica_jinete * 100)}"
    estadistica_preparador_str = f".{int(estadistica_preparador * 100)}"
    
    # Verificar si hubo cambio de preparador
    cambio_preparador, prep_anterior, prep_actual = verificar_cambio_preparador(session, reunion_caballo.idCaballo, reunion_caballo.fecha, reunion_caballo.referencia)
    
    # Agregar asterisco al nombre del preparador si cambió
    nombre_preparador = reunion_caballo.preparador.estudie
    if cambio_preparador:
        nombre_preparador += "*"
    
    # Texto con formateo similar al ejemplo dado
    return f"\t<@P_Cajon>{reunion_caballo.cajon}\t<@P_Nombre>{reunion_caballo.caballo.nombre}<@P_Modalidad> {modalidad}\t<@$p>{info_jinete_caballo}\t<@P_Kilos>{kilos}\t<@P_Jinete>{reunion_caballo.jinete.estudie}<@P_EstadisticaPunto> {estadistica_jinete_str}\t<@$p>{corridas_jinete_prep}/{ganadas_jinete_prep}\t<@P_Preparador>{nombre_preparador}<@P_EstadisticaPunto> {estadistica_preparador_str}.-<@P_Stud>{reunion_caballo.stud.breve}"

def verificar_contratiempos(session, fecha, referencia, id_caballo, cache=None):
    """
    Verifica si un caballo tiene contratiempos registrados en una carrera específica
    
    Args:
        session: Sesión de la base de datos
        fecha: Fecha de la carrera
        referencia: Referencia de la carrera
        id_caballo: ID del caballo
        cache: Diccionario opcional para cachear resultados (clave: (fecha, referencia, idCaballo))
        
    Returns:
        bool: True si tiene contratiempos, False en caso contrario
    """
    # Usar el caché si está disponible
    if cache is not None:
        cache_key = (fecha, referencia, id_caballo)
        if cache_key in cache:
            return cache[cache_key]
    
    contratiempos = session.query(ReunionContratiempos).filter(
        ReunionContratiempos.fecha == fecha,
        ReunionContratiempos.referencia == referencia,
        ReunionContratiempos.idCaballo == id_caballo
    ).first()
    
    result = contratiempos is not None
    
    # Actualizar el caché si está disponible
    if cache is not None:
        cache_key = (fecha, referencia, id_caballo)
        cache[cache_key] = result
    
    return result

def verificar_cambio_preparador(session, id_caballo, fecha_carrera, referencia_carrera):
    """
    Verifica si hubo un cambio de preparador en esta carrera con respecto a la anterior
    
    Args:
        session: Sesión de la base de datos
        id_caballo: ID del caballo
        fecha_carrera: Fecha de la carrera a verificar
        referencia_carrera: Referencia de la carrera a verificar
        
    Returns:
        tuple: (bool, objeto_preparador_anterior, objeto_preparador_actual)
    """
    # Obtener la carrera actual
    carrera_actual = session.query(ReunionCaballos).filter(
        ReunionCaballos.idCaballo == id_caballo,
        ReunionCaballos.fecha == fecha_carrera,
        ReunionCaballos.referencia == referencia_carrera
    ).first()
    
    if not carrera_actual:
        return False, None, None
    
    # Obtener la carrera anterior
    carrera_anterior = session.query(ReunionCaballos).filter(
        ReunionCaballos.idCaballo == id_caballo,
        ReunionCaballos.corrio == 1,
        # La carrera debe ser antes de la actual
        ((ReunionCaballos.fecha < fecha_carrera) | 
         ((ReunionCaballos.fecha == fecha_carrera) & (ReunionCaballos.referencia < referencia_carrera)))
    ).order_by(
        ReunionCaballos.fecha.desc(),
        ReunionCaballos.referencia.desc()
    ).first()
    
    if not carrera_anterior:
        return False, None, None  # No hay carrera anterior para comparar
    
    # Obtener el preparador de la carrera actual
    prep_actual = session.query(Preparadores).filter(Preparadores.idPreparador == carrera_actual.idPreparador).first()
    id_prep_actual = prep_actual.idPreparador if prep_actual else None

    # Verificar si hubo cambio de preparador
    if carrera_actual.idPreparador != carrera_anterior.idPreparador:
        # Obtener objetos de los preparadores
        prep_anterior = session.query(Preparadores).filter(Preparadores.idPreparador == carrera_anterior.idPreparador).first()
        # prep_actual = session.query(Preparadores).filter(Preparadores.idPreparador == carrera_actual.idPreparador).first()
        return True, prep_anterior, prep_actual
    

    return False, None, prep_actual

def generar_bloque_historial(session, reunion_caballo, carrera_actual, mostrar_encabezado=False, cache_contratiempos=None):
    """
    Genera el segundo bloque: historial de carreras anteriores
    
    Args:
        session: Sesión de la base de datos
        reunion_caballo: Objeto ReunionCaballos con los datos del caballo en la carrera
        carrera_actual: Objeto ReunionCarreras con los datos de la carrera actual
        mostrar_encabezado: Indica si se debe mostrar el encabezado de columnas
        cache_contratiempos: Diccionario para cachear resultados de verificar_contratiempos
        
    Returns:
        str: Texto formateado con el historial de carreras anteriores
    """
    
    # Obtener historial de carreras anteriores (aumentamos a 7 para detectar cambios de preparador)
    carreras_anteriores = session.query(ReunionCaballos, ReunionCarreras).join(
        ReunionCarreras, 
        (ReunionCaballos.fecha == ReunionCarreras.fecha) & 
        (ReunionCaballos.referencia == ReunionCarreras.referencia)
    ).filter(
        ReunionCaballos.fecha < reunion_caballo.fecha, 
        ReunionCaballos.idCaballo == reunion_caballo.idCaballo,
        ReunionCaballos.corrio == 1
    ).order_by(ReunionCaballos.fecha.desc()).limit(7).all()
    
    if not carreras_anteriores:
        return ""  # Debutante, no mostramos nada
    
    contenido = ""
    
    # Si hay que mostrar el encabezado, lo agregamos
    if mostrar_encabezado:
        contenido = "    Ref.    Fecha    Kilos    Jinete    Cajón        Dist.        Tmpo.    Corr.        Pto.        Div.    Separación al ganador    TH    PF\n"
    
    # Guardamos la séptima carrera solo para verificar cambio de preparador
    carrera_previa = None
    if len(carreras_anteriores) > 6:
        carrera_previa = carreras_anteriores[6]
        carreras_anteriores = carreras_anteriores[:6]
    
    # Invertir el orden para mostrar más antiguas primero
    carreras_anteriores = list(reversed(carreras_anteriores))
    
    for i, carrera_tuple in enumerate(carreras_anteriores):
        carrera_anterior = carrera_tuple[0]  # ReunionCaballos
        info_carrera = carrera_tuple[1]      # ReunionCarreras
        
        # Verificar cambio de preparador
        # En el primer elemento, comparamos con la carrera previa (si existe)
        if i == 0 and carrera_previa:
            hubo_cambio = carrera_anterior.idPreparador != carrera_previa[0].idPreparador
        elif i > 0:
            # Comparar con la carrera anterior en la lista
            carrera_previa = carreras_anteriores[i-1][0]
            hubo_cambio = carrera_anterior.idPreparador != carrera_previa.idPreparador
        else:
            hubo_cambio = False
        
        # Formatear fecha
        fecha = fecha_formato(carrera_anterior.fecha)
        
        # Formatear jinete
        jinete_info = jinete_historia(session, carrera_anterior.idJinete, reunion_caballo.idJinete)
        
        # Formatear tiempo
        if hasattr(info_carrera, 'tipoTiempo') and info_carrera.tipoTiempo == 0:
            tiempo_info = tiempo_formato(info_carrera.tiempo, 'quintos')
        else:
            if hasattr(info_carrera, 'tiempoCentesimos') and info_carrera.tiempoCentesimos:
                tiempo_info = tiempo_formato(info_carrera.tiempoCentesimos, 'centesimos')
            else:
                tiempo_info = '--'
        
        # Obtener posición real del cajón (excluyendo retirados)
        cajon_real = cajon_neto(session, carrera_anterior.fecha, carrera_anterior.referencia, carrera_anterior.idCaballo)
        
        # Formatear información de pista
        pista_info = pista_historia(info_carrera.pista, carrera_actual.pista)
        
        # Formatear información de baranda
        baranda_info = ""
        if hasattr(info_carrera, 'baranda') and info_carrera.baranda != 0:
            baranda_info = f"B{info_carrera.baranda}"
        
        # Obtener cantidad de caballos que corrieron
        caballos_corrieron = contar_caballos_corrieron(session, carrera_anterior.fecha, carrera_anterior.referencia)
        
        # Obtener dividendo
        dividendo_info = dividendo_ganador(
            session,
            carrera_anterior.fecha, 
            carrera_anterior.referencia, 
            carrera_anterior.idCaballo
        )
        
        # Verificar si la referencia coincide con alguna carrera de otro caballo en la carrera actual
        # Excluimos al mismo caballo en la verificación
        otros_caballos = session.query(ReunionCaballos).filter(
            ReunionCaballos.fecha == reunion_caballo.fecha,
            ReunionCaballos.referencia == reunion_caballo.referencia,
            ReunionCaballos.idCaballo != reunion_caballo.idCaballo
        ).all()
        
        coincide_referencia = False
        for otro_caballo in otros_caballos:
            # Verificar si este caballo corrió en la misma referencia
            corrida_anterior = session.query(ReunionCaballos).filter(
                ReunionCaballos.idCaballo == otro_caballo.idCaballo,
                ReunionCaballos.fecha < reunion_caballo.fecha,
                ReunionCaballos.referencia == carrera_anterior.referencia,
                ReunionCaballos.corrio == 1
            ).first()
            
            if corrida_anterior:
                coincide_referencia = True
                break
                
        # Formatear referencia con estilo si coincide
        if coincide_referencia:
            ref_formateada = f"<@HReferencia>{carrera_anterior.referencia}<@$p>"
        else:
            ref_formateada = f"{carrera_anterior.referencia}"
            
        # En el bloque de historial, también verificamos si ganó su siguiente carrera
        # pero esta parte ya no necesita agregar el marcador * porque ahora se maneja mediante el estilo
        ganador_siguiente = ""
        
        # Información de separación al ganador
        if carrera_anterior.puesto == 1:
            # Si es el ganador, mostrar el segundo lugar
            segundos = session.query(ReunionCaballos, Caballos, Separaciones).join(
                Caballos, ReunionCaballos.idCaballo == Caballos.idCaballo
            ).join(
                Separaciones, ReunionCaballos.idSeparacion == Separaciones.idSeparacion
            ).filter(
                ReunionCaballos.fecha == carrera_anterior.fecha,
                ReunionCaballos.referencia == carrera_anterior.referencia,
                ReunionCaballos.puesto == 2
            ).first()
            
            if segundos:
                separacion_info = f"(2º {segundos[1].breve} {kilos_historial(segundos[0].kilos, 1)} a {segundos[2].sepEstudieFinal})"
            else:
                separacion_info = "(Ganó sin placé)"
        else:
            # Si no es ganador, obtener separación al ganador
            separacion_info = carrera_anterior.separacion.sepEstudieFinal if hasattr(carrera_anterior, 'separacion') else "--"
            
            # Obtener el ganador
            ganador = session.query(ReunionCaballos, Caballos).join(
                Caballos, ReunionCaballos.idCaballo == Caballos.idCaballo
            ).filter(
                ReunionCaballos.fecha == carrera_anterior.fecha,
                ReunionCaballos.referencia == carrera_anterior.referencia,
                ReunionCaballos.puesto == 1
            ).first()
            
            if ganador:
                separacion_info = f"{separacion_info}    {ganador[1].breve} {kilos_historial(ganador[0].kilos, 1)}"
        
        # Agregar TH (handicap) y PF (peso físico)
        th_info = f"({carrera_anterior.handicap})" if carrera_anterior.handicap else "--"
        pf_info = f"{carrera_anterior.pesoFisico}" if carrera_anterior.pesoFisico else "--"
        
        # Verificar si hay contratiempos para esta carrera (con caché)
        tiene_contratiempos = verificar_contratiempos(session, carrera_anterior.fecha, carrera_anterior.referencia, carrera_anterior.idCaballo, cache_contratiempos)
        
        # Formatear el puesto con asterisco para cambio de preparador y/o (x) para contratiempos
        puesto_info = ""
        if hubo_cambio:
            puesto_info += "*"
        if tiene_contratiempos:
            puesto_info += "(x)"
        puesto_info += f"{carrera_anterior.puesto}º"
        
        # Agregar línea formateada al contenido
        contenido += f"    {ref_formateada}    {fecha}    {kilos_historial(carrera_anterior.kilos, 2)}    {jinete_info}    {cajon_real}    {pista_info}    {distancia_historia(info_carrera.distancia, info_carrera.pista, carrera_actual.distancia, carrera_actual.pista)}    {baranda_info}    {tiempo_info}    {caballos_corrieron}        {puesto_info}{ganador_siguiente}        {dividendo_info}    {separacion_info}    {th_info}    {pf_info}\n"
    
    return contenido

def generar_bloque_resultados(session, reunion_caballo):
    """
    Genera el tercer bloque: resultado de carreras con los primeros 4 lugares
    
    Args:
        session: Sesión de la base de datos
        reunion_caballo: Objeto ReunionCaballos con los datos del caballo en la carrera
        
    Returns:
        str: Texto formateado con los resultados detallados de las carreras anteriores
    """
    from models.models import Clasicos
    
    contenido = ""
    
    # Obtener las carreras anteriores del caballo
    carreras_anteriores = session.query(ReunionCaballos, ReunionCarreras, CondicionesNuevas).join(
        ReunionCarreras, 
        (ReunionCaballos.fecha == ReunionCarreras.fecha) & 
        (ReunionCaballos.referencia == ReunionCarreras.referencia)
    ).outerjoin(
        CondicionesNuevas,
        ReunionCarreras.idCondicionEstudie == CondicionesNuevas.idCondicion
    ).filter(
        ReunionCaballos.fecha < reunion_caballo.fecha, 
        ReunionCaballos.idCaballo == reunion_caballo.idCaballo,
        ReunionCaballos.corrio == 1
    ).order_by(ReunionCaballos.fecha.desc()).limit(6).all()
    
    if not carreras_anteriores:
        return ""  # Debutante, no mostramos nada
    
    # Invertir el orden para mostrar más antiguas primero
    carreras_anteriores = list(reversed(carreras_anteriores))
    
    for carrera_tuple in carreras_anteriores:
        carrera_anterior = carrera_tuple[0]  # ReunionCaballos
        info_carrera = carrera_tuple[1]      # ReunionCarreras
        condicion = carrera_tuple[2]         # CondicionesNuevas (puede ser None)
        
        # Condiciones de la carrera - 3 casos posibles: Clásico, Handicap, o condición normal
        
        # 1. Si es un clásico, mostrar "Cl. " + marcador + (grupo)
        if info_carrera.idClasico:
            clasico = session.query(Clasicos).filter(Clasicos.idClasico == info_carrera.idClasico).first()
            if clasico:
                condicion_str = f"Cl. {clasico.marcador}"
                # Agregar grupo entre paréntesis si es un valor válido
                if clasico.grupo in ["1", "2", "3", "L", "R"]:
                    condicion_str += f" ({clasico.grupo})"
        
        # 2. Si es un handicap, mostrar "Hánd. [min, max] Hx"
        elif condicion and condicion.startRef == "H":
            min_handicap, max_handicap, categoria = obtener_rango_handicap(session, carrera_anterior.fecha, carrera_anterior.referencia)
            if min_handicap is not None and max_handicap is not None:
                condicion_str = f"Hánd. [{min_handicap}, {max_handicap}] {categoria}"
        
        # 3. En caso contrario, mostrar la condición normal
        else:
            condicion_str = condicion.estudieRef if condicion else "Cond. n/d"
        
        # Obtener el desarrollo (posición en cada parcial)
        desarrollo = formatear_desarrollo(carrera_anterior.desarrollo, " ")
        
        # Agregar el puesto final
        puesto_final = carrera_anterior.puesto
        
        # Obtener los 4 primeros lugares
        primeros_lugares = obtener_primeros_lugares(session, carrera_anterior.fecha, carrera_anterior.referencia)
        
        # Formatear resultados de la carrera
        resultado_carrera = ""
        for i, (rc, cab, sep) in enumerate(primeros_lugares):
            # Verificar si el caballo ganó su siguiente carrera
            gano_siguiente = verificar_caballo_gano_siguiente(
                session, 
                rc.idCaballo, 
                rc.fecha, 
                rc.referencia
            )
            
            # Determinar el estilo adecuado según las condiciones
            es_caballo_estudio = (rc.idCaballo == reunion_caballo.idCaballo)
            es_rival = session.query(ReunionCaballos).filter(
                ReunionCaballos.fecha == reunion_caballo.fecha,
                ReunionCaballos.referencia == reunion_caballo.referencia,
                ReunionCaballos.idCaballo == rc.idCaballo
            ).first() is not None
            
            # Aplicar el estilo correspondiente (con prioridad a combinaciones)
            if es_caballo_estudio and gano_siguiente:
                # Caballo en estudio que ganó su siguiente carrera
                nombre = f"<@HEstudioGano>{cab.breve}<@$p>"
            elif es_rival and gano_siguiente:
                # Rival actual que ganó su siguiente carrera
                nombre = f"<@HRivalGano>{cab.breve}<@$p>"
            elif es_caballo_estudio:
                # Solo caballo en estudio
                nombre = f"<@HCaballoEstudio>{cab.breve}<@$p>"
            elif es_rival:
                # Solo rival actual
                nombre = f"<@HRival>{cab.breve}<@$p>"
            elif gano_siguiente:
                # Solo ganador siguiente (ni el caballo en estudio ni rival actual)
                nombre = f"<@HGanadorSiguiente>{cab.breve}<@$p>"
            else:
                # Caso base - ninguna condición especial
                nombre = cab.breve
            
            puesto = i + 1  # Posición (1º, 2º, etc.)
            
            # Agregar separación al ganador (excepto para el ganador)
            separacion_txt = ""
            if puesto > 1 and sep:
                separacion_txt = f" [{sep.sepEstudieFinal}]"
            
            # Agregar información del caballo al resultado (usando kilos_historial)
            if puesto == 1:
                resultado_carrera += f"1º {nombre} {kilos_historial(rc.kilos, 1)}"
            else:
                resultado_carrera += f" - {puesto}º {nombre} {kilos_historial(rc.kilos, 1)}{separacion_txt}"
        
        # Agregar línea formateada
        contenido += f"    {carrera_anterior.referencia}    {condicion_str}    {desarrollo}   {puesto_final}º    {resultado_carrera}\n"
    
    return contenido

def obtener_estadisticas_pista(session, id_caballo, pista_actual, distancia_actual, cache=None):
    """
    Obtiene estadísticas del caballo por tipo de pista y distancia
    
    Args:
        session: Sesión de la base de datos
        id_caballo: ID del caballo
        pista_actual: Tipo de pista de la carrera actual ('A' para arena, 'C' para césped)
        distancia_actual: Distancia de la carrera actual
        cache: Diccionario opcional para cachear resultados (clave: (id_caballo, pista_actual, distancia_actual))
        
    Returns:
        dict: Diccionario con estadísticas
    """
    # Usar el caché si está disponible
    if cache is not None:
        cache_key = (id_caballo, pista_actual, distancia_actual)
        if cache_key in cache:
            return cache[cache_key]
    # Inicializar resultados
    resultados = {
        'arena_corridas': 0,
        'arena_ganadas': 0,
        'arena_premios': 0,
        'cesped_corridas': 0,
        'cesped_ganadas': 0,
        'cesped_premios': 0,
        'distancia_corridas': 0,
        'distancia_ganadas': 0,
        'distancia_premios': 0,
        'total_corridas': 0,
        'total_ganadas': 0,
        'total_premios': 0
    }
    
    # Obtener todas las carreras anteriores del caballo
    carreras = session.query(ReunionCaballos, ReunionCarreras).join(
        ReunionCarreras,
        (ReunionCaballos.fecha == ReunionCarreras.fecha) &
        (ReunionCaballos.referencia == ReunionCarreras.referencia)
    ).filter(
        ReunionCaballos.idCaballo == id_caballo,
        ReunionCaballos.corrio == 1
    ).all()
    
    # Procesar cada carrera
    for rc, carrera in carreras:
        # Actualizar totales
        resultados['total_corridas'] += 1
        if rc.puesto == 1:
            resultados['total_ganadas'] += 1
        if rc.premioGanado:
            resultados['total_premios'] += float(rc.premioGanado)
        
        # Estadísticas por tipo de pista
        if carrera.pista == 'A':  # Arena
            resultados['arena_corridas'] += 1
            if rc.puesto == 1:
                resultados['arena_ganadas'] += 1
            if rc.premioGanado:
                resultados['arena_premios'] += float(rc.premioGanado)
        elif carrera.pista == 'C':  # Césped
            resultados['cesped_corridas'] += 1
            if rc.puesto == 1:
                resultados['cesped_ganadas'] += 1
            if rc.premioGanado:
                resultados['cesped_premios'] += float(rc.premioGanado)
        
        # Estadísticas por distancia y misma pista
        if carrera.distancia == distancia_actual and carrera.pista == pista_actual:
            resultados['distancia_corridas'] += 1
            if rc.puesto == 1:
                resultados['distancia_ganadas'] += 1
            if rc.premioGanado:
                resultados['distancia_premios'] += float(rc.premioGanado)
    
    # Actualizar el caché si está disponible
    if cache is not None:
        cache_key = (id_caballo, pista_actual, distancia_actual)
        cache[cache_key] = resultados
    
    return resultados

def obtener_hermanos(session, id_caballo, id_padre, id_madre, fecha_nacimiento):
    """
    Obtiene los hermanos enteros y maternos mayores que el caballo
    
    Args:
        session: Sesión de la base de datos
        id_caballo: ID del caballo actual (para excluirlo)
        id_padre: ID del padre del caballo
        id_madre: ID de la madre del caballo
        fecha_nacimiento: Fecha de nacimiento del caballo
        
    Returns:
        tuple: (hermanos_enteros, hermanos_maternos, es_primer_producto, info_no_disponible)
    """
    # Verificar si tiene padres por defecto (en cuyo caso la info no está disponible)
    info_no_disponible = False
    if id_padre == 3689 and id_madre == 3932:
        info_no_disponible = True
        return [], [], False, info_no_disponible
    
    # Obtener hermanos enteros (mismo padre y madre) mayores que el caballo
    hermanos_enteros = session.query(Caballos).filter(
        Caballos.idCaballo != id_caballo,
        Caballos.idPadre == id_padre,
        Caballos.idMadre == id_madre,
        Caballos.fechaNac < fecha_nacimiento
    ).order_by(Caballos.fechaNac).all()
    
    # Obtener hermanos maternos (solo misma madre) mayores que el caballo
    hermanos_maternos = session.query(Caballos).filter(
        Caballos.idCaballo != id_caballo,
        Caballos.idMadre == id_madre,
        Caballos.idPadre != id_padre,
        Caballos.fechaNac < fecha_nacimiento
    ).order_by(Caballos.fechaNac).all()
    
    # Verificar si hay algún hermano mayor (entero o materno)
    es_primer_producto = len(hermanos_enteros) == 0 and len(hermanos_maternos) == 0
    
    return hermanos_enteros, hermanos_maternos, es_primer_producto, info_no_disponible

def formatear_lista_nombres(nombres_lista, sexo="M"):
    """
    Formatea una lista de nombres con la conjunción adecuada antes del último elemento
    
    Args:
        nombres_lista: Lista de nombres a formatear
        sexo: Sexo del caballo para determinar la conjunción adecuada
        
    Returns:
        str: Lista formateada con conjunciones
    """
    if not nombres_lista:
        return ""
    
    if len(nombres_lista) == 1:
        return nombres_lista[0]
    
    # Para el último nombre, verificar si empieza con 'I' o 'Hi' para usar "e" en lugar de "y"
    ultimo = nombres_lista[-1]
    if ultimo.startswith(('I', 'i', 'Hi', 'hi')):
        conjuncion = " e "
    else:
        conjuncion = " y "
    
    return ", ".join(nombres_lista[:-1]) + conjuncion + ultimo

def generar_bloque_pedigree(session, reunion_caballo):
    """
    Genera el cuarto bloque: pedigree y detalles del caballo
    
    Args:
        session: Sesión de la base de datos
        reunion_caballo: Objeto ReunionCaballos con los datos del caballo en la carrera
        
    Returns:
        str: Texto formateado con la información de pedigree del caballo
    """
    from datetime import datetime
    
    caballo = reunion_caballo.caballo
    
    # Obtener información detallada
    sexo_txt = ""
    if caballo.sexo == "M":
        sexo_txt = "Macho"
    elif caballo.sexo == "H":
        sexo_txt = "Hembra"
    elif caballo.sexo == "C":
        sexo_txt = "Castrado"
    
    # Obtener color
    color = session.query(Colores).filter(Colores.idColor == caballo.idColor).first()
    color_txt = ""
    if color:
        if caballo.sexo == "H":
            color_txt = color.colorHembra.lower() if color.colorHembra else ""
        else:
            color_txt = color.color.lower() if color.color else ""
    
    # Calcular edad
    edad = calcular_edad_caballo(caballo.fechaNac, reunion_caballo.fecha)
    
    # Obtener información del padrillo (padre)
    padre = session.query(Padrillos).filter(Padrillos.idPadre == caballo.idPadre).first()
    padre_nombre = padre.padre if padre else "N/D"
    
    # Obtener información de la madre
    madre = session.query(Madres).filter(Madres.idMadre == caballo.idMadre).first()
    madre_nombre = madre.madre if madre else "N/D"
    
    # Obtener información del abuelo materno
    abuelo_id = madre.idAbuelo if madre else None
    abuelo = session.query(Abuelos).filter(Abuelos.idAbuelo == abuelo_id).first() if abuelo_id else None
    abuelo_nombre = abuelo.abuelo if abuelo else "N/D"
    
    # Obtener país de nacimiento
    pais = session.query(Paises).filter(Paises.idPais == caballo.idPais).first()
    pais_txt = pais.inicialesPais if pais else ""
    
    # Obtener criador
    criador = session.query(Criadores).filter(Criadores.idCriador == caballo.idCriador).first()
    criador_txt = criador.criador if criador else "N/D"
    
    # Morning line y votos (pronosticador)
    ml_str = ""
    if hasattr(reunion_caballo, 'morningLine1') and reunion_caballo.morningLine1:
        ml_str = f"ML: {reunion_caballo.morningLine1}/1"
        if hasattr(reunion_caballo, 'votos') and reunion_caballo.votos:
            ml_str += f" - {reunion_caballo.votos} "
            ml_str += "voto" if reunion_caballo.votos == 1 else "votos"
    
    # Obtener información de colores del stud
    stud = reunion_caballo.stud
    colores_stud = stud.colores if hasattr(stud, 'colores') and stud.colores else ""
    
    # Formatear bloque de pedigree
    pedigree = f"{sexo_txt}, {color_txt}, {edad} a., {padre_nombre} y {madre_nombre} por {abuelo_nombre}.- {pais_txt}.- {criador_txt}.    {ml_str}\n"
    
    # Agregar fecha de nacimiento y hermanos
    if caballo.fechaNac:
        fecha_nac = caballo.fechaNac.strftime("%d.%m.%Y")
        pedigree += f"N. {fecha_nac}.-"
        
        # Obtener información de hermanos
        hermanos_enteros, hermanos_maternos, es_primer_producto, info_no_disponible = obtener_hermanos(
            session, 
            caballo.idCaballo, 
            caballo.idPadre, 
            caballo.idMadre, 
            caballo.fechaNac
        )
        
        # Si la información no está disponible
        if info_no_disponible:
            pedigree += " No disponible"
        # Formatear texto de hermanos
        elif es_primer_producto:
            pedigree += " Primer producto"
        else:
            # Determinar género para la palabra "entero/a" según el sexo
            if caballo.sexo == "H":
                hermano_txt = "Hermana"
                entero_txt = "entera"
                materno_txt = "materna"
            else:
                hermano_txt = "Hermano"
                entero_txt = "entero"
                materno_txt = "materno"
            
            # Formatear hermanos enteros
            hermanos_enteros_txt = ""
            if hermanos_enteros:
                # Usar el campo minusculas en lugar de nombre
                nombres_enteros = [h.minusculas for h in hermanos_enteros]
                nombres_enteros_formateados = formatear_lista_nombres(nombres_enteros, caballo.sexo)
                hermanos_enteros_txt = f"{hermano_txt} {entero_txt} de {nombres_enteros_formateados}"
            
            # Formatear hermanos maternos
            hermanos_maternos_txt = ""
            if hermanos_maternos:
                # Usar el campo minusculas en lugar de nombre
                nombres_maternos = [h.minusculas for h in hermanos_maternos]
                nombres_maternos_formateados = formatear_lista_nombres(nombres_maternos, caballo.sexo)
                
                if hermanos_enteros_txt:
                    hermanos_maternos_txt = f" y {materno_txt} de {nombres_maternos_formateados}"
                else:
                    hermanos_maternos_txt = f"{hermano_txt} {materno_txt} de {nombres_maternos_formateados}"
            
            # Combinar información de hermanos
            if hermanos_enteros_txt or hermanos_maternos_txt:
                pedigree += f" {hermanos_enteros_txt}{hermanos_maternos_txt}"
    
    # Agregar colores del stud en una nueva línea
    if colores_stud:
        pedigree += f"\nColores.- {colores_stud}"
    
    return pedigree

def obtener_calificacion_estudie(session, reunion_caballo, cache=None):
    """
    Obtiene la calificación del caballo en el campo estudiePata de Comentarios
    
    Args:
        session: Sesión de la base de datos
        reunion_caballo: Objeto ReunionCaballos con los datos del caballo en la carrera
        cache: Diccionario opcional para cachear resultados (clave: (fecha, referencia, idCaballo))
        
    Returns:
        str: Texto con la calificación del caballo
    """
    from models.models import Comentarios
    
    # Usar el caché si está disponible
    if cache is not None:
        cache_key = (reunion_caballo.fecha, reunion_caballo.referencia, reunion_caballo.idCaballo)
        if cache_key in cache:
            return cache[cache_key]
    
    try:
        # Buscar en la tabla Comentarios
        comentario = session.query(Comentarios).filter(
            Comentarios.fecha == reunion_caballo.fecha,
            Comentarios.referencia == reunion_caballo.referencia,
            Comentarios.idCaballo == reunion_caballo.idCaballo
        ).first()
        
        # Verificar si encontramos un comentario
        if not comentario:
            result = "SIN Comentario"
        elif not isinstance(comentario, Comentarios):
            result = "error de atributo"
        else:
            # Tratar de acceder al atributo de forma segura
            try:
                estudiePata = comentario.EstudiePata
                if estudiePata is None:
                    result = ""
                else:
                    estudiePata = estudiePata.strip()
                    # Mapear el valor a un texto
                    if estudiePata == "1":
                        result = "MUY BUENA"
                    elif estudiePata == "2":
                        result = "BUENA"
                    elif estudiePata == "3":
                        result = "ARRIESGADA"
                    elif estudiePata.upper() == "S":
                        result = "SUPLENTE"
                    else:
                        result = ""
            except (AttributeError, TypeError):
                result = "error 2 de atributo"
            
    except Exception as e:
        # Capturar cualquier error y devolver un valor predeterminado
        print(f"Error al obtener calificación: {e}")
        result = "SIN CALIFICAR"
    
    # Actualizar el caché si está disponible
    if cache is not None:
        cache_key = (reunion_caballo.fecha, reunion_caballo.referencia, reunion_caballo.idCaballo)
        cache[cache_key] = result
        
    return result

def generar_bloque_estadisticas(session, reunion_caballo, carrera_actual):
    """
    Genera el sexto bloque: estadísticas del caballo por tipo de pista y distancia
    
    Args:
        session: Sesión de la base de datos
        reunion_caballo: Objeto ReunionCaballos con los datos del caballo en la carrera
        carrera_actual: Objeto ReunionCarreras con los datos de la carrera actual
        
    Returns:
        str: Texto formateado con las estadísticas del caballo
    """
    # Obtener calificación del EstudiePata
    
    calificacion = obtener_calificacion_estudie(session, reunion_caballo)
    
    calificacion = ""
    
    # Verificar si es debutante
    es_debutante = session.query(ReunionCaballos).filter(
        ReunionCaballos.fecha < reunion_caballo.fecha,
        ReunionCaballos.idCaballo == reunion_caballo.idCaballo,
        ReunionCaballos.corrio == 1
    ).first() is None
    
    # Si es debutante, mostrar información especial
    if es_debutante:
        peso_fisico = reunion_caballo.pesoFisico if hasattr(reunion_caballo, 'pesoFisico') and reunion_caballo.pesoFisico else "---"
        return f"{calificacion}\t\tPeso físico (aprox.) {peso_fisico} k.- Es información del preparador DEBUTA"
    
    # Para caballos no debutantes, mostrar estadísticas normales
    pista_actual = carrera_actual.pista
    distancia_actual = carrera_actual.distancia
    
    stats = obtener_estadisticas_pista(session, 
                                       reunion_caballo.idCaballo, 
                                       pista_actual, 
                                       distancia_actual)
    
    # Formatear sumas ganadas a enteros
    arena_premios = int(stats['arena_premios'])
    cesped_premios = int(stats['cesped_premios'])
    distancia_premios = int(stats['distancia_premios'])
    total_premios = int(stats['total_premios'])
    
    # Formatear estadísticas según la pista actual
    if pista_actual == 'A':  # Arena
        estadisticas = f"| Arena: {stats['arena_corridas']}/{stats['arena_ganadas']} - S/. {arena_premios:,} | "
        estadisticas += f"Distancia: {stats['distancia_corridas']}/{stats['distancia_ganadas']} - S/. {distancia_premios:,} | "
        estadisticas += f"Césped: {stats['cesped_corridas']}/{stats['cesped_ganadas']} | "
    else:  # Césped
        estadisticas = f"| Césped: {stats['cesped_corridas']}/{stats['cesped_ganadas']} - S/. {cesped_premios:,} | "
        estadisticas += f"Distancia: {stats['distancia_corridas']}/{stats['distancia_ganadas']} - S/. {distancia_premios:,} | "
        estadisticas += f"Arena: {stats['arena_corridas']}/{stats['arena_ganadas']} | "
    
    # Agregar resumen
    cc = stats['total_corridas']  # Carreras corridas
    cg = stats['total_ganadas']   # Carreras ganadas
    estadisticas += f"CC: {cc} CG: {cg} | S/. {total_premios:,}"
    
    # Combinar calificación con estadísticas
    return f"{calificacion}\t\t{estadisticas}"

def formatear_desarrollo(desarrollo_carrera, separador='\t'):
    uno = int(desarrollo_carrera[0:2])
    dos = int(desarrollo_carrera[2:4])
    tre = int(desarrollo_carrera[4:6])
    return f"{uno}º{separador}{dos}º{separador}{tre}º"

def obtener_rango_handicap(session, fecha, referencia):
    """
    Obtiene el rango (mínimo y máximo) del handicap para una carrera
    
    Args:
        session: Sesión de la base de datos
        fecha: Fecha de la carrera
        referencia: Referencia de la carrera
        
    Returns:
        tuple: (min_handicap, max_handicap, categoria) o (None, None, None) si no hay datos
        categoria: Clasificación del handicap (H5, H4, H3, H2, H1, HS)
    """
    from models.models import ReunionCaballos
    
    # Obtener todos los caballos de la carrera que corrieron y tienen handicap
    caballos_handicap = session.query(ReunionCaballos).filter(
        ReunionCaballos.fecha == fecha,
        ReunionCaballos.referencia == referencia,
        ReunionCaballos.corrio != 0,           # Solo incluir los que corrieron
        ReunionCaballos.handicap.isnot(None),  # Excluir valores NULL
        ReunionCaballos.handicap != ''         # Excluir valores vacíos
    ).all()
    
    # Si no hay caballos con handicap, retornar None, None, None
    if not caballos_handicap:
        return None, None, None
    
    # Convertir los handicaps a enteros (para manejar negativos correctamente)
    handicaps = []
    for caballo in caballos_handicap:
        try:
            # Manejar valores con signo negativo al inicio
            handicap_str = caballo.handicap.strip()
            if handicap_str.startswith('-'):
                handicap_valor = -int(handicap_str[1:])
            else:
                handicap_valor = int(handicap_str)
            handicaps.append(handicap_valor)
        except (ValueError, TypeError, AttributeError):
            # Ignorar valores que no se pueden convertir a entero
            continue
    
    # Si no hay handicaps válidos, retornar None, None, None
    if not handicaps:
        return None, None, None
    
    # Encontrar el mínimo y máximo
    min_handicap = min(handicaps)
    max_handicap = max(handicaps)
    
    # Determinar la categoría del handicap
    if max_handicap <= 5:
        categoria = "H5"
    elif max_handicap <= 10:
        categoria = "H4"
    elif max_handicap <= 20:
        categoria = "H3"
    elif max_handicap <= 30:
        categoria = "H2"
    elif max_handicap <= 40:
        categoria = "H1"
    else:
        categoria = "HS"
    
    return min_handicap, max_handicap, categoria

def formatear_fecha_apronte(fecha):
    """
    Formatea una fecha al formato [dd-Mmm]
    
    Args:
        fecha: Fecha en formato datetime.date
        
    Returns:
        str: Fecha formateada como [dd-Mmm]
    """
    meses = {
        1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
    }
    return f"[{fecha.day}-{meses[fecha.month]}]"

def formatear_tiempo_quintos(tiempo):
    """
    Formatea un tiempo en quintos de segundo
    
    Args:
        tiempo: Tiempo en quintos de segundo
        
    Returns:
        str: Tiempo formateado como m'ss"q
    """
    # 300 quintos = 60 segundos = 1 minuto
    minutos = tiempo // 300
    segundos = f"{((tiempo % 300) // 5):02d}"
    quintos = f"{tiempo % 5}"
    if minutos != 0:
        return f"{minutos}'{segundos}\"{quintos}"
    else:
        return f"{segundos}\"{quintos}"

def generar_bloque_linea_final(session, reunion_caballo):
    """
    Genera la línea final del quinto bloque con información adicional
    
    Args:
        session: Sesión de la base de datos
        reunion_caballo: Objeto ReunionCaballos con los datos del caballo en la carrera
        
    Returns:
        str: Texto formateado con la línea final de información
    """
    from datetime import datetime, timedelta
    from models.models import Aprontes, ReunionCaballos
    import time
    
    componentes = []
    
    # 1. T.H. (handicap)
    if reunion_caballo.handicap:
        componentes.append(f"T.H.: {reunion_caballo.handicap}")
    
    # 2. Días de descanso (si son más de 30)
    # Obtener la carrera anterior más reciente
    carrera_anterior = session.query(ReunionCaballos).filter(
        ReunionCaballos.idCaballo == reunion_caballo.idCaballo,
        ReunionCaballos.corrio == 1,
        ((ReunionCaballos.fecha < reunion_caballo.fecha) | 
         ((ReunionCaballos.fecha == reunion_caballo.fecha) & 
          (ReunionCaballos.referencia < reunion_caballo.referencia)))
    ).order_by(
        ReunionCaballos.fecha.desc(),
        ReunionCaballos.referencia.desc()
    ).first()
    
    if carrera_anterior:
        # Calcular días de descanso
        dias_descanso = (reunion_caballo.fecha - carrera_anterior.fecha).days
        
        if dias_descanso >= 30:
            componentes.append(f"Descansó {dias_descanso} días")
    
    # 3. Carreras sin ganar
    # Obtener todas las carreras corridas
    carreras_corridas = session.query(ReunionCaballos).filter(
        ReunionCaballos.idCaballo == reunion_caballo.idCaballo,
        ReunionCaballos.corrio == 1,
        ((ReunionCaballos.fecha < reunion_caballo.fecha) | 
         ((ReunionCaballos.fecha == reunion_caballo.fecha) & 
          (ReunionCaballos.referencia < reunion_caballo.referencia)))
    ).order_by(
        ReunionCaballos.fecha.desc(),
        ReunionCaballos.referencia.desc()
    ).all()
    
    # Verificar si ha ganado alguna carrera
    if not carreras_corridas:
        componentes.append("No ha corrido")
    else:
        # Contar carreras desde la última victoria
        ultima_victoria = None
        carreras_sin_ganar = 0
        
        for carrera in carreras_corridas:
            if carrera.puesto == 1:
                ultima_victoria = carrera
                break
            carreras_sin_ganar += 1
        
        if ultima_victoria is None:
            if len(carreras_corridas) > 0:
                componentes.append("No ha ganado")
        elif carreras_sin_ganar == 0:
            componentes.append("Ganó en su anterior")
        else:
            componentes.append(f"No gana hace {carreras_sin_ganar} carreras")
    
    # 4. Información de trabajos (T)
    info_trabajos = "T.: "
    
    # 4.1 Verificar si corrió la última semana
    if carrera_anterior and (reunion_caballo.fecha - carrera_anterior.fecha).days <= 7:
        info_trabajos += "corrió la última semana"
    else:
        # 4.2 Buscar aprontes posteriores a su carrera más reciente
        fecha_ultima_carrera = carrera_anterior.fecha if carrera_anterior else datetime.date(1900, 1, 1)
        
        aprontes = session.query(Aprontes).filter(
            Aprontes.idCaballo == reunion_caballo.idCaballo,
            Aprontes.fecha > fecha_ultima_carrera,
            Aprontes.fecha < reunion_caballo.fecha
        ).order_by(Aprontes.fecha.asc()).all()
        
        if not aprontes:
            info_trabajos += "galopó"
        else:
            aprontes_formateados = []
            
            for apronte in aprontes:
                apronte_txt = f"con {apronte.jinete} {apronte.distancia} en {formatear_tiempo_quintos(apronte.tiempo)}"
                
                # Agregar tiempos finales si existen
                if apronte.tpoFin1 != 0:
                    apronte_txt += f" ({formatear_tiempo_quintos(apronte.tpoFin1)})"
                if apronte.tpoFin2 != 0:
                    apronte_txt += f" ({formatear_tiempo_quintos(apronte.tpoFin2)})"
                
                # Agregar pista y calificación
                apronte_txt += f" {apronte.pista}"
                if apronte.calificacion:
                    apronte_txt += f" ({apronte.calificacion})"
                
                # Agregar fecha
                apronte_txt += f" {formatear_fecha_apronte(apronte.fecha)}"
                
                aprontes_formateados.append(apronte_txt)
            
            info_trabajos += "; ".join(aprontes_formateados)
    
    componentes.append(info_trabajos)
    
    # Unir todos los componentes
    return ". ".join(componentes), dias_descanso

def generar_bloque_carreras_irregulares(session, reunion_caballo, cache_contratiempos=None):
    """
    Genera el quinto bloque: carreras irregulares (contratiempos) y cambios de preparador
    
    Args:
        session: Sesión de la base de datos
        reunion_caballo: Objeto ReunionCaballos con los datos del caballo en la carrera
        cache_contratiempos: Diccionario para cachear resultados de verificar_contratiempos
        
    Returns:
        str: Texto formateado con las carreras irregulares y cambios de preparador, o cadena vacía si no hay
    """
    # Obtener carreras anteriores con sus respectiva referencia (hasta 7 para verificar cambios de preparador)
    carreras_anteriores = session.query(ReunionCaballos).filter(
        ReunionCaballos.fecha < reunion_caballo.fecha,
        ReunionCaballos.idCaballo == reunion_caballo.idCaballo,
        ReunionCaballos.corrio == 1
    ).order_by(ReunionCaballos.fecha.desc()).limit(7).all()
    
    if not carreras_anteriores:
        return ""  # Debutante, no hay contratiempos ni cambios de preparador
    
    # Si tenemos 7 carreras, quedarnos con las 6 más recientes para mostrar (pero usar la séptima para verificar cambios)
    carrera_previa = None
    if len(carreras_anteriores) > 6:
        carrera_previa = carreras_anteriores[6]
        carreras_en_historial = carreras_anteriores[:6]
    else:
        carreras_en_historial = carreras_anteriores
    
    # Invertir el orden para mostrar las más antiguas primero (como en el historial)
    carreras_en_historial = list(reversed(carreras_en_historial))
    
    # Verificar si hay algún contratiempo o cambio de preparador en cualquiera de las carreras
    tiene_algun_contratiempo = False
    tiene_algun_cambio_prep = False
    
    # Primero verificamos contratiempos
    for carrera_anterior in carreras_en_historial:
        if verificar_contratiempos(session, carrera_anterior.fecha, carrera_anterior.referencia, carrera_anterior.idCaballo, cache_contratiempos):
            tiene_algun_contratiempo = True
            break
    
    # Luego verificamos cambios de preparador
    for i, carrera_anterior in enumerate(carreras_en_historial):
        # En el primer elemento, comparar con carrera_previa si existe
        if i == 0 and carrera_previa:
            if carrera_anterior.idPreparador != carrera_previa.idPreparador:
                tiene_algun_cambio_prep = True
                break
        elif i > 0:
            # Comparar con la carrera anterior en la lista
            if carrera_anterior.idPreparador != carreras_en_historial[i-1].idPreparador:
                tiene_algun_cambio_prep = True
                break
    
    # Si no hay contratiempos ni cambios de preparador, no mostramos este bloque
    if not tiene_algun_contratiempo and not tiene_algun_cambio_prep:
        return ""
    
    # Iniciar el contenido para cada sección
    contenido = ""
    contenido_contratiempos = ""
    contenido_cambios_prep = ""
    
    # Procesar contratiempos
    if tiene_algun_contratiempo:
        contenido_contratiempos = "CARR. IRREG.: "
        
        for carrera_anterior in carreras_en_historial:
            # Obtener los contratiempos de esta carrera
            contratiempos = session.query(ReunionContratiempos, Contratiempos).join(
                Contratiempos, 
                ReunionContratiempos.idContratiempo == Contratiempos.idContratiempo
            ).filter(
                ReunionContratiempos.fecha == carrera_anterior.fecha,
                ReunionContratiempos.referencia == carrera_anterior.referencia,
                ReunionContratiempos.idCaballo == carrera_anterior.idCaballo
            ).order_by(ReunionContratiempos.orden).all()
            
            # Si esta carrera tiene contratiempos, los agregamos al contenido
            if contratiempos:
                # Verificar cambio de preparador para añadir el asterisco
                hubo_cambio = False
                index = carreras_en_historial.index(carrera_anterior)
                if index == 0 and carrera_previa:
                    hubo_cambio = carrera_anterior.idPreparador != carrera_previa.idPreparador
                elif index > 0:
                    hubo_cambio = carrera_anterior.idPreparador != carreras_en_historial[index-1].idPreparador
                
                # Añadir asterisco antes de (x) si hubo cambio de preparador
                prefijo = "*" if hubo_cambio else ""
                
                for i, (rc, contra) in enumerate(contratiempos):
                    if i == 0:
                        # Primera entrada para esta carrera
                        contenido_contratiempos += f"{prefijo}(x){carrera_anterior.puesto}º: {contra.contratiempo}. "
                    else:
                        # Más de un contratiempo para la misma carrera
                        contenido_contratiempos += f"{contra.contratiempo}. "
        
        # Eliminar el último espacio y punto si existe
        if contenido_contratiempos.endswith(". "):
            contenido_contratiempos = contenido_contratiempos[:-2]
    
    # Procesar cambios de preparador
    if tiene_algun_cambio_prep:
        contenido_cambios_prep = "Cambio de prep.: "
        
        for i, carrera_anterior in enumerate(carreras_en_historial):
            hubo_cambio = False
            prep_anterior = None
            prep_actual = None
            
            # Determinar si hubo cambio y con qué carrera comparar
            if i == 0 and carrera_previa:
                if carrera_anterior.idPreparador != carrera_previa.idPreparador:
                    hubo_cambio = True
                    # Obtener objetos de preparadores
                    prep_anterior = session.query(Preparadores).filter(Preparadores.idPreparador == carrera_previa.idPreparador).first()
                    prep_actual = session.query(Preparadores).filter(Preparadores.idPreparador == carrera_anterior.idPreparador).first()
            elif i > 0:
                if carrera_anterior.idPreparador != carreras_en_historial[i-1].idPreparador:
                    hubo_cambio = True
                    # Obtener objetos de preparadores
                    prep_anterior = session.query(Preparadores).filter(Preparadores.idPreparador == carreras_en_historial[i-1].idPreparador).first()
                    prep_actual = session.query(Preparadores).filter(Preparadores.idPreparador == carrera_anterior.idPreparador).first()
            
            # Si hubo cambio, añadir información
            if hubo_cambio and prep_anterior and prep_actual:
                # Verificar si también tiene contratiempos (con caché)
                tiene_contratiempo = verificar_contratiempos(session, carrera_anterior.fecha, carrera_anterior.referencia, carrera_anterior.idCaballo, cache_contratiempos)
                prefijo = "(x)" if tiene_contratiempo else ""
                
                contenido_cambios_prep += f"*{prefijo}{carrera_anterior.puesto}º: de {prep_anterior.estudie} a {prep_actual.estudie}. "
        
        # Eliminar el último espacio y punto si existe
        if contenido_cambios_prep.endswith(". "):
            contenido_cambios_prep = contenido_cambios_prep[:-2]
    
    # Combinar ambos contenidos
    if contenido_contratiempos and contenido_cambios_prep:
        contenido = f"{contenido_contratiempos} {contenido_cambios_prep}"
    elif contenido_contratiempos:
        contenido = contenido_contratiempos
    else:
        contenido = contenido_cambios_prep
    
    return contenido


def deteccion_estadistica_especial(session, id_caballo, fecha, referencia):
    print(id_caballo, fecha, referencia)
    
    # Recorrido por las carreras de la semana actual
    query = (
        session.query(
            ReunionCarreras,
            ReunionCaballos,
            Caballos,
            Preparadores,
            CondicionesNuevas,
            Clasicos
        )
            .join(ReunionCaballos, (ReunionCarreras.fecha == ReunionCaballos.fecha) &
                                 (ReunionCarreras.referencia == ReunionCaballos.referencia))
            .join(Caballos, ReunionCaballos.idCaballo == Caballos.idCaballo)
            .join(Preparadores, ReunionCaballos.idPreparador == Preparadores.idPreparador)
            .join(CondicionesNuevas, ReunionCarreras.idCondicionEstudie == CondicionesNuevas.idCondicion)
            .outerjoin(Clasicos, ReunionCarreras.idClasico == Clasicos.idClasico)
            .filter(ReunionCarreras.fecha == fecha)
            .filter(ReunionCarreras.referencia == referencia)
            .filter(ReunionCaballos.idCaballo == id_caballo)
        )
    caballo_actual = query.first()
    print (f"---> {caballo_actual.Caballos.nombre}")
    if not caballo_actual:
        print("Algo falló en el query")
        return {}
    
    preparador_actual = caballo_actual.Preparadores.estudie
    id_preparador_actual = caballo_actual.ReunionCaballos.idPreparador
    ejemplar= caballo_actual.Caballos.nombre
    
    # Número de Carreras corridas del caballo actual
    query = session.query(ReunionCaballos).filter(
        ReunionCaballos.fecha < fecha,
        ReunionCaballos.corrio == True,
        ReunionCaballos.idCaballo == id_caballo)
    corridas = query.count()
   
    # Ultima carrera del caballo actual    
    query = (
    session.query(ReunionCarreras, ReunionCaballos)
    .join(ReunionCaballos, 
        (ReunionCaballos.fecha == ReunionCarreras.fecha) & 
        (ReunionCaballos.referencia == ReunionCarreras.referencia)
    )
    .filter(
        ReunionCaballos.fecha < fecha,
        ReunionCaballos.corrio == True,
        ReunionCaballos.idCaballo == id_caballo
    )
    .order_by(ReunionCarreras.fecha.desc())
    )
    ultima_carrera = query.first()

    dist_ult, pista_ult = 0, ""  # O cualquier valor predeterminado apropiado
    corta_a_larga = False
    larga_a_corta = False
    cesped_a_arena = False
    arena_a_cesped = False
    r1, r2, r3 = 0, 0, 0
    descanso = 0
    
    columnas = ['corridasClasicos',
                'ganadasClasicos',
                'corridasCondicional',
                'ganadasCondicional',
                'corridasHandicap',
                'ganadasHandicap',
                'corridasCambioCesped',
                'ganadasCambioCesped',
                'corridasCambioArena',
                'ganadasCambioArena',
                'corridasReap1',
                'ganadasReap1',
                'corridasReap2',
                'ganadasReap2',
                'corridasReap3',
                'ganadasReap3',
                'corridasCambioCorta',
                'ganadasCambioCorta',
                'corridasCambioLarga',
                'ganadasCambioLarga',
                'corridasCambioPrep',
                'ganadasCambioPrep',
                'corridasDebutantes',
                'ganadasDebutantes',
                'corridas2doDebut',
                'ganadas2doDebut']




    camb_prep, prep_anterior, prep_actual = verificar_cambio_preparador(session, id_caballo, fecha, referencia)
    
    prepa = session.query(Preparadores).filter(Preparadores.idPreparador == id_preparador_actual).first()
    # print("----------------->",prep_anterior, prep_actual, id_preparador_actual)
    estadisticas = {col: getattr(prepa, col) for col in columnas}

    # Verificar si hay un clásico asociado
    tiene_clasico = caballo_actual.Clasicos is not None and caballo_actual.Clasicos.idClasico is not None
    id_clasico = caballo_actual.Clasicos.idClasico if tiene_clasico else 0


    if caballo_actual.ReunionCaballos.debutante == True: # Debutante
        print (f"DEBUTA ---> {caballo_actual.Caballos.nombre}")
        # Valores por defecto o manejar el caso sin carreras anteriores
        dist_ult, pista_ult = 0, ""  # O cualquier valor predeterminado apropiado
        corta_a_larga = False
        larga_a_corta = False
        cesped_a_arena = False
        arena_a_cesped = False
        r1, r2, r3 = 0, 0, 0
        descanso = 0

        detectados = {
            "debutante": True,
            "2do_debut": False,
            "handicap": caballo_actual.CondicionesNuevas.startRef.upper() == "H",
            "condicional": caballo_actual.CondicionesNuevas.startRef.lower() == "c" and id_clasico == 0,
            "cam_prep": False,
            "clasico": id_clasico != 0,
            "corta_a_larga": False,
            "larga_a_corta": False,
            "cesped_a_arena": False,
            "arena_a_cesped": False,
            "R1": False,
            "R2": False,
            "R3": False
        }
        print("DEBUTANTE ")
        
    else:
        dist_ult, pista_ult = ultima_carrera.ReunionCarreras.distancia, ultima_carrera.ReunionCarreras.pista
        dist_act, pista_act = caballo_actual.ReunionCarreras.distancia, caballo_actual.ReunionCarreras.pista
        corta = 1400
        descanso = (fecha - ultima_carrera.ReunionCarreras.fecha).days
        print("--------------------------------")
        print(descanso, fecha, ultima_carrera.ReunionCarreras.fecha)
        r1, r2, r3 = 0, 0, 0

        if dist_ult <= corta and dist_act > corta:
            corta_a_larga = True
        if dist_ult > corta and dist_act <= corta:
            larga_a_corta = True
        if pista_ult == "C" and pista_act == "A":
            cesped_a_arena = True
        if pista_ult == "A" and pista_act == "C":
            arena_a_cesped = True
        if descanso >= 31 and descanso <= 60:
            r1 = "R1"
        if descanso >= 61 and descanso <= 180:
            r2 = "R2"
        if descanso >= 181:
            r3 = "R3"
            
        # camb_prep, prep_anterior, prep_actual, id_prep_actual = verificar_cambio_preparador(session, id_caballo, fecha, referencia)

        
        


        if prep_actual is not None:
            print ("Preparador:")
            print (prep_actual.estudie)
        

        
        detectados = {
            "debutante": corridas == 0,
            "2do_debut": corridas == 1,
            "handicap": caballo_actual.CondicionesNuevas.startRef.upper() == "H",
            "condicional": caballo_actual.CondicionesNuevas.startRef.lower() == "c" and id_clasico == 0,
            "cam_prep": camb_prep,
            "clasico": id_clasico != 0,
            "corta_a_larga": corta_a_larga,
            "larga_a_corta": larga_a_corta,
            "cesped_a_arena": cesped_a_arena,
            "arena_a_cesped": arena_a_cesped,
            "R1": r1,
            "R2": r2,
            "R3": r3
        }
    
    print(f"{caballo_actual.ReunionCaballos.cajon}.- {caballo_actual.Caballos.nombre}")
    
    # clasico_info = caballo_actual.Clasicos.minusculas if tiene_clasico else "No es clásico"
    # print(f"{caballo_actual.ReunionCarreras.idClasico}: {clasico_info}")
    for key, value in detectados.items():
        print(f"   {key}: {value}")

    # print ("Salida: ", prep_anterior, preparador_actual, id_preparador_actual, detectados, estadisticas)
    
    salida = f"{preparador_actual}: "
    salida += f"Debutantes: {estadisticas['corridasDebutantes']} {estadisticas['ganadasDebutantes']}. "  if detectados['debutante'] else ""
    salida += f"Condicionales: {estadisticas['corridasCondicional']} {estadisticas['ganadasCondicional']}. "  if detectados['condicional'] else ""
    salida += f"Handicap: {estadisticas['corridasHandicap']} {estadisticas['ganadasHandicap']}. "  if detectados['handicap'] else ""
    salida += f"Clásicos: {estadisticas['corridasClasicos']} {estadisticas['ganadasClasicos']}. "  if detectados['clasico'] else ""
    salida += f"Cambio a corta: {estadisticas['corridasCambioCorta']} {estadisticas['ganadasCambioCorta']}. "  if detectados['larga_a_corta'] else ""
    salida += f"Cambio a larga: {estadisticas['corridasCambioLarga']} {estadisticas['ganadasCambioLarga']}. "  if detectados['corta_a_larga'] else ""
    salida += f"Cambio a arena: {estadisticas['corridasCambioArena']} {estadisticas['ganadasCambioArena']}. "  if detectados['cesped_a_arena'] else ""    
    salida += f"Cambio a césped: {estadisticas['corridasCambioCesped']} {estadisticas['ganadasCambioCesped']}. "  if detectados['arena_a_cesped'] else ""

    print (salida)
    return salida
    # return prep_anterior, prep_actual, detectados, estadisticas

    


def generar_contenido_estudie():
    """Genera el contenido para 'Estudie su Polla' usando bloques estructurados"""
    import time
    from models.models import ReunionCarreras, ReunionCaballos, Caballos, Jinetes, Preparadores, Studs
    
    # Registrar tiempo de inicio
    tiempo_inicio = time.time()
    print("Iniciando generación de contenido XTG Estudie...")
    
    # Crear cachés para optimizar consultas
    cache_contratiempos = {}
    cache_comentarios = {}
    cache_estadisticas = {}

    # XPressTags
    initXtg = "<v20.14><e9>" # Inicio para versión Quark 2024

    
    with SessionLocal() as session:
        contenido = initXtg
        
        # 1. Iteración por Fechas
        fechas = session.query(ReunionCarreras.fecha).filter(
            ReunionCarreras.corrida == 0
        ).distinct().order_by(ReunionCarreras.fecha).all()
        
        
            

        for fecha_tuple in fechas:
            fecha = fecha_tuple[0]
            # ETIQUETA: Título de fecha
            ### contenido += f"<@TituloFecha>\nFecha: {fecha}\n<@$p>"
            contenido += f"@TituloFecha:Fecha: {fecha}\n<@$p>"
            contenido += "<@Separador>------------------\n<@$p>"

            
            # # 2. Iteración por Carreras
            # carreras = session.query(ReunionCarreras).filter(
            #     ReunionCarreras.fecha == fecha
            # ).order_by(ReunionCarreras.referencia).all()

            # 2. Iteración por Carreras
            carreras = session.query(ReunionCarreras, CondicionesNuevas,Clasicos).outerjoin(
                CondicionesNuevas,
                ReunionCarreras.idCondicionEstudie == CondicionesNuevas.idCondicion).outerjoin(
                Clasicos,
                ReunionCarreras.idClasico == Clasicos.idClasico
            ).filter(
                ReunionCarreras.fecha == fecha
            ).order_by(ReunionCarreras.referencia).all()


            
            # Cachear debutantes por carrera
            debutantes_por_carrera = {}
            
            for carrera, condicion, classico in carreras:
                # ETIQUETA: Título de carrera
                contenido += f"<@TituloCarrera>{carrera.ordenDeCarrera}ª Carrera. {carrera.referencia}.  {carrera.distancia} mts. {carrera.pista}\n<@$p>"
                
                # 3. Iteración por Caballos
                caballos = session.query(ReunionCaballos).join(
                    Caballos, ReunionCaballos.idCaballo == Caballos.idCaballo
                ).join(
                    Jinetes, ReunionCaballos.idJinete == Jinetes.idJinete
                ).join(
                    Preparadores, ReunionCaballos.idPreparador == Preparadores.idPreparador
                ).join(
                    Studs, ReunionCaballos.idStud == Studs.idStud
                ).filter(
                    ReunionCaballos.fecha == fecha, 
                    ReunionCaballos.referencia == carrera.referencia
                ).order_by(ReunionCaballos.realCajon).all()
                
                # Pre-cargar datos para todos los caballos en esta carrera
                
                # 1. Primero identificar todos los debutantes
                id_caballos = [rc.idCaballo for rc in caballos]
                for rc in caballos:
                    if rc.idCaballo not in debutantes_por_carrera:
                        es_debutante = session.query(ReunionCaballos).filter(
                            ReunionCaballos.fecha < rc.fecha,
                            ReunionCaballos.idCaballo == rc.idCaballo,
                            ReunionCaballos.corrio == 1
                        ).first() is None
                        debutantes_por_carrera[rc.idCaballo] = es_debutante
                
                # 2. Precargar todos los comentarios de esta carrera de una sola vez
                from models.models import Comentarios
                comentarios_carrera = session.query(Comentarios).filter(
                    Comentarios.fecha == fecha,
                    Comentarios.referencia == carrera.referencia,
                    Comentarios.idCaballo.in_(id_caballos)
                ).all()
                
                # Cargar en el caché
                for comentario in comentarios_carrera:
                    cache_key = (comentario.fecha, comentario.referencia, comentario.idCaballo)
                    if cache_key not in cache_comentarios:
                        try:
                            estudiePata = comentario.EstudiePata
                            if estudiePata is None:
                                result = ""
                            else:
                                estudiePata = estudiePata.strip()
                                # Mapear el valor a un texto
                                if estudiePata == "1":
                                    result = "MUY BUENA"
                                elif estudiePata == "2":
                                    result = "BUENA"
                                elif estudiePata == "3":
                                    result = "ARRIESGADA"
                                elif estudiePata.upper() == "S":
                                    result = "SUPLENTE"
                                else:
                                    result = ""
                            cache_comentarios[cache_key] = result
                        except (AttributeError, TypeError):
                            cache_comentarios[cache_key] = "error de atributo"
                
                # 3. Para los no debutantes, precargar sus carreras anteriores para detectar contratiempos
                no_debutantes = [rc for rc in caballos if not debutantes_por_carrera[rc.idCaballo]]
                
                for rc in no_debutantes:
                    # Obtener carreras anteriores
                    carreras_anteriores = session.query(ReunionCaballos).filter(
                        ReunionCaballos.fecha < rc.fecha,
                        ReunionCaballos.idCaballo == rc.idCaballo,
                        ReunionCaballos.corrio == 1
                    ).order_by(ReunionCaballos.fecha.desc()).limit(7).all()
                    
                    # Para cada carrera anterior, precargar contratiempos
                    for ca in carreras_anteriores:
                        # Usar chequeo rápido para llenar el caché de contratiempos
                        if (ca.fecha, ca.referencia, ca.idCaballo) not in cache_contratiempos:
                            verificar_contratiempos(session, ca.fecha, ca.referencia, ca.idCaballo, cache_contratiempos)
                    
                    # También precargar estadísticas
                    cache_key = (rc.idCaballo, carrera.pista, carrera.distancia)
                    if cache_key not in cache_estadisticas:
                        obtener_estadisticas_pista(session, rc.idCaballo, carrera.pista, carrera.distancia, cache_estadisticas)
                
                # Determinar si es el primer caballo de la carrera
                for i, reunion_caballo in enumerate(caballos):
                    # Obtener si es debutante del caché
                    es_debutante = debutantes_por_carrera[reunion_caballo.idCaballo]
                    
                    # Determinar si mostrar encabezado (solo en el primer caballo no debutante)
                    mostrar_encabezado = (i == 0) and not es_debutante
                    
                    # BLOQUE 1: Información básica del caballo
                    info_basica = generar_bloque_info_basica(session, reunion_caballo)
                    contenido += f"<@InfoBasica>{info_basica}\n<@$p>"
                    
                    # Para debutantes, omitir bloques 2 y 3
                    if not es_debutante:
                        # BLOQUE 2: Historial de carreras anteriores
                        historial = generar_bloque_historial(session, reunion_caballo, carrera, mostrar_encabezado, cache_contratiempos)
                        if historial:
                            contenido += f"<@Historial>{historial}\n<@$p>"
                        
                        # BLOQUE 3: Resultados detallados
                        resultados = generar_bloque_resultados(session, reunion_caballo)
                        if resultados:
                            contenido += f"<@Resultados>{resultados}\n<@$p>"
                    
                    # BLOQUE 4: Pedigree y detalles
                    pedigree = generar_bloque_pedigree(session, reunion_caballo)
                    if pedigree:
                        contenido += f"<@Pedigree>{pedigree}\n<@$p>"
                    
                    # BLOQUE 5: Carreras irregulares (contratiempos) y línea final
                    # Para todos los caballos (debutantes y no debutantes)
                    
                    # Para caballos no debutantes - incluir contratiempos y línea final
                    if not es_debutante:
                        # Parte 1: Carreras irregulares
                        carreras_irregulares = generar_bloque_carreras_irregulares(session, reunion_caballo, cache_contratiempos)
                        
                        # Parte 2: Línea final con T.H., descanso, carreras sin ganar y aprontes
                        linea_final, descanso = generar_bloque_linea_final(session, reunion_caballo)
                        
                        # Combinar ambas partes
                        bloque5_completo = ""
                        if carreras_irregulares:
                            bloque5_completo += f"<@CarrerasIrregulares>{carreras_irregulares}\n<@$p>"
                        
                        bloque5_completo += f"<@LineaFinal>{linea_final}<@$p>"
                        
                        contenido += bloque5_completo + "\n\n"
                    # Para debutantes - incluir sólo línea final con aprontes
                    else:
                        # Versión simplificada para debutantes
                        from models.models import Aprontes
                        import time
                        
                        # Buscar todos los aprontes del caballo
                        aprontes = session.query(Aprontes).filter(
                            Aprontes.idCaballo == reunion_caballo.idCaballo,
                            Aprontes.fecha < reunion_caballo.fecha
                        ).order_by(Aprontes.fecha.asc()).all()
                        
                        if aprontes:
                            aprontes_txt = "T.: "
                            aprontes_formateados = []
                            
                            for apronte in aprontes:
                                apronte_txt = f"con {apronte.jinete} {apronte.distancia} en {formatear_tiempo_quintos(apronte.tiempo)}"
                                
                                # Agregar tiempos finales si existen
                                if apronte.tpoFin1 != 0:
                                    apronte_txt += f" ({formatear_tiempo_quintos(apronte.tpoFin1)})"
                                if apronte.tpoFin2 != 0:
                                    apronte_txt += f" ({formatear_tiempo_quintos(apronte.tpoFin2)})"
                                
                                # Agregar pista y calificación
                                apronte_txt += f" {apronte.pista}"
                                if apronte.calificacion:
                                    apronte_txt += f" ({apronte.calificacion})"
                                
                                # Agregar fecha
                                apronte_txt += f" {formatear_fecha_apronte(apronte.fecha)}"
                                
                                aprontes_formateados.append(apronte_txt)
                            
                            aprontes_txt += "; ".join(aprontes_formateados)
                            ### contenido += f"<@AprontinDebutante>{aprontes_txt}\n\n<@$p>"
                            contenido += f"<@AprontinDebutante>{aprontes_txt}<@$p>"
                        else:
                            contenido += f"<@AprontinDebutante>T.: galopó<@$p>"

                    contenido = contenido.rstrip()
                    salida = deteccion_estadistica_especial(session, reunion_caballo.idCaballo, fecha, carrera.referencia)
                    contenido += salida + "\n<@$p>"


                    # BLOQUE 6: Estadísticas del caballo por pista y distancia
                    calificacion = obtener_calificacion_estudie(session, reunion_caballo, cache_comentarios)

                    
                    # LLAMADA A ESTADISTICAS ESPECIALES DE PREPARADORES

                    # prep_anterior, prep_actual, indicadores, estadistica = deteccion_estadistica_especial(session, reunion_caballo.idCaballo, fecha, carrera.referencia)



                    if es_debutante:
                        peso_fisico = reunion_caballo.pesoFisico if hasattr(reunion_caballo, 'pesoFisico') and reunion_caballo.pesoFisico else "---"
                        estadisticas_txt = f"{calificacion}\t\tPeso físico (aprox.) {peso_fisico} k.- Es información del preparador DEBUTA"
                        contenido += f"<@EstadisticasDebutante>{estadisticas_txt}\n<@$p>"
                    else:
                        # if indicadores['debutante']:
                        #     contenido += f"Debuta"
                        # if indicadores['condicional']:
                        #     contenido += f"Condicional"                        
                        
                        
                        stats = obtener_estadisticas_pista(session, reunion_caballo.idCaballo, carrera.pista, carrera.distancia, cache_estadisticas)
                        
                        
                        
                        # Formatear sumas ganadas a enteros
                        arena_premios = int(stats['arena_premios'])
                        cesped_premios = int(stats['cesped_premios'])
                        distancia_premios = int(stats['distancia_premios'])
                        total_premios = int(stats['total_premios'])
                        
                        # Formatear estadísticas según la pista actual
                        if carrera.pista == 'A':  # Arena
                            estadisticas = f"| Arena: {stats['arena_corridas']}/{stats['arena_ganadas']} - S/. {arena_premios:,} | "
                            estadisticas += f"Distancia: {stats['distancia_corridas']}/{stats['distancia_ganadas']} - S/. {distancia_premios:,} | "
                            estadisticas += f"Césped: {stats['cesped_corridas']}/{stats['cesped_ganadas']} | "
                        else:  # Césped
                            estadisticas = f"| Césped: {stats['cesped_corridas']}/{stats['cesped_ganadas']} - S/. {cesped_premios:,} | "
                            estadisticas += f"Distancia: {stats['distancia_corridas']}/{stats['distancia_ganadas']} - S/. {distancia_premios:,} | "
                            estadisticas += f"Arena: {stats['arena_corridas']}/{stats['arena_ganadas']} | "
                        
                        # Agregar resumen
                        cc = stats['total_corridas']
                        cg = stats['total_ganadas']
                        estadisticas += f"CC: {cc} CG: {cg} | S/. {total_premios:,}"
                        
                        estadisticas_txt = f"{calificacion}\t\t{estadisticas}"
                        contenido += f"<@Estadisticas>{estadisticas_txt}\n<@$p>"
                    
                    # Espacio entre caballos
                    contenido += "\n"
                
                # Separación entre carreras
                contenido += "<@SeparacionCarreras>\n\n<@$p>"
    
    # Calcular tiempo transcurrido
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    minutos = int(tiempo_total // 60)
    segundos = int(tiempo_total % 60)
    
    # Imprimir estadísticas del caché
    print(f"Comentarios cacheados: {len(cache_comentarios)}")
    print(f"Contratiempos cacheados: {len(cache_contratiempos)}")
    print(f"Estadísticas cacheadas: {len(cache_estadisticas)}")
    
    # Imprimir el tiempo en la consola
    mensaje = f"TIEMPO DE EJECUCIÓN: {minutos} minutos y {segundos} segundos"
    print("=" * len(mensaje))
    print(mensaje)
    print("=" * len(mensaje))
    
    # Información sobre las etiquetas agregadas
    print("\nEtiquetas de formateo XTG agregadas:")
    print("- <@TituloFecha>: Encabezados de fecha")
    print("- <@Separador>: Líneas separadoras")
    print("- <@TituloCarrera>: Encabezados de carrera")
    print("- <@InfoBasica>: Información básica del caballo")
    print("- <@Historial>: Historial de carreras anteriores")
    print("- <@Resultados>: Resultados detallados")
    print("- <@Pedigree>: Pedigree y detalles del caballo")
    print("- <@CarrerasIrregulares>: Información sobre carreras irregulares")
    print("- <@LineaFinal>: Línea final con trabajos")
    print("- <@AprontinDebutante>: Información de trabajos para debutantes")
    print("- <@EstadisticasDebutante>: Estadísticas para caballos debutantes")
    print("- <@Estadisticas>: Estadísticas generales")
    print("- <@SeparacionCarreras>: Separación entre carreras")
    
    # Devolver 
    return contenido
    
