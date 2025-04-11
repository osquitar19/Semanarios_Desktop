"""
Módulo para generar el contenido XTG del formato 'Estudie su Polla'.
Implementa un enfoque procedimental con iteraciones jerárquicas.
"""
import datetime
import pymysql
from sqlalchemy.sql import text
from db import SessionLocal
from models.models import (
    Caballos, Jinetes, ReunionCarreras, ReunionCaballos, Preparadores, Studs,
    Separaciones, CondicionesNuevas, Padrillos, Madres, Abuelos, Paises, Criadores, Colores
)

# Funciones de utilidad para el formateo
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
    
    Args:
        fecha_nacimiento (datetime.date): Fecha de nacimiento del caballo
        fecha_carrera (datetime.date): Fecha de la carrera
        
    Returns:
        int: Edad del caballo en años
    """
    # Calcular diferencia de años
    edad = fecha_carrera.year - fecha_nacimiento.year
    
    # Ajustar si aún no ha cumplido años en el año de la carrera
    if fecha_carrera.month < fecha_nacimiento.month or (
        fecha_carrera.month == fecha_nacimiento.month and 
        fecha_carrera.day < fecha_nacimiento.day
    ):
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
    
    # Texto con formateo similar al ejemplo dado
    return f"{reunion_caballo.cajon}    {reunion_caballo.caballo.nombre} {modalidad}    {info_jinete_caballo}    {kilos} {reunion_caballo.jinete.estudie} {estadistica_jinete_str}    {corridas_jinete_prep}/{ganadas_jinete_prep}    {reunion_caballo.preparador.estudie} {estadistica_preparador_str}.-{reunion_caballo.stud.breve}"

def generar_bloque_historial(session, reunion_caballo, carrera_actual):
    """
    Genera el segundo bloque: historial de carreras anteriores
    
    Args:
        session: Sesión de la base de datos
        reunion_caballo: Objeto ReunionCaballos con los datos del caballo en la carrera
        carrera_actual: Objeto ReunionCarreras con los datos de la carrera actual
        
    Returns:
        str: Texto formateado con el historial de carreras anteriores
    """
    
    contenido = "    Ref.    Fecha    Kilos    Jinete    Cajón        Dist.        Tmpo.    Corr.        Pto.        Div.    Separación al ganador    TH    PF\n"
    
    # Obtener historial de carreras anteriores
    carreras_anteriores = session.query(ReunionCaballos, ReunionCarreras).join(
        ReunionCarreras, 
        (ReunionCaballos.fecha == ReunionCarreras.fecha) & 
        (ReunionCaballos.referencia == ReunionCarreras.referencia)
    ).filter(
        ReunionCaballos.fecha < reunion_caballo.fecha, 
        ReunionCaballos.idCaballo == reunion_caballo.idCaballo,
        ReunionCaballos.corrio == 1
    ).order_by(ReunionCaballos.fecha.desc()).limit(6).all()
    
    if not carreras_anteriores:
        return contenido + "    Debutante\n"
    
    # Invertir el orden para mostrar más antiguas primero
    carreras_anteriores = list(reversed(carreras_anteriores))
    
    for carrera_tuple in carreras_anteriores:
        carrera_anterior = carrera_tuple[0]  # ReunionCaballos
        info_carrera = carrera_tuple[1]      # ReunionCarreras
        
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
            
        # Verificar si el caballo ganó su siguiente carrera
        if verificar_caballo_gano_siguiente(session, carrera_anterior.idCaballo, carrera_anterior.fecha, carrera_anterior.referencia):
            # Aplicar estilo especial si ganó
            ganador_siguiente = "<@HGanadorSiguiente>*<@$p>"
        else:
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
        
        # Agregar línea formateada al contenido
        contenido += f"    {ref_formateada}    {fecha}    {kilos_historial(carrera_anterior.kilos, 2)}    {jinete_info}    {cajon_real}    {pista_info}    {distancia_historia(info_carrera.distancia, info_carrera.pista, carrera_actual.distancia, carrera_actual.pista)}    {baranda_info}    {tiempo_info}    {caballos_corrieron}        {carrera_anterior.puesto}º{ganador_siguiente}        {dividendo_info}    {separacion_info}    {th_info}    {pf_info}\n"
    
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
        return contenido + "    Debutante\n"
    
    # Invertir el orden para mostrar más antiguas primero
    carreras_anteriores = list(reversed(carreras_anteriores))
    
    for carrera_tuple in carreras_anteriores:
        carrera_anterior = carrera_tuple[0]  # ReunionCaballos
        info_carrera = carrera_tuple[1]      # ReunionCarreras
        condicion = carrera_tuple[2]         # CondicionesNuevas (puede ser None)
        
        # Condiciones de la carrera
        condicion_str = condicion.estudieRef if condicion else "Cond. n/d"
        
        # Obtener el desarrollo (posición en cada parcial)
        # desarrollo = carrera_anterior.desarrollo.split('-') if carrera_anterior.desarrollo else ['--', '--', '--']
        desarrollo = formatear_desarrollo(carrera_anterior.desarrollo, " ")
        # while len(desarrollo) != 6:
            # desarrollo.append('--')
        
        # Agregar el puesto final
        puesto_final = carrera_anterior.puesto
        
        # Obtener los 4 primeros lugares
        primeros_lugares = obtener_primeros_lugares(session, carrera_anterior.fecha, carrera_anterior.referencia)
        
        # Formatear resultados de la carrera
        resultado_carrera = ""
        for i, (rc, cab, sep) in enumerate(primeros_lugares):
            # Aplicar estilo al caballo en estudio o si coincide con un caballo de la carrera actual
            if rc.idCaballo == reunion_caballo.idCaballo:
                # El caballo de la historia es el mismo que estamos estudiando
                nombre = f"<@HCaballoEstudio>{cab.breve}<@$p>"
            elif session.query(ReunionCaballos).filter(
                ReunionCaballos.fecha == reunion_caballo.fecha,
                ReunionCaballos.referencia == reunion_caballo.referencia,
                ReunionCaballos.idCaballo == rc.idCaballo
            ).first():
                # Este caballo también está en la carrera actual
                nombre = f"<@HRival>{cab.breve}<@$p>"
            else:
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
        # contenido += f"    {carrera_anterior.referencia}    {condicion_str}    {desarrollo[0]}    {desarrollo[1]}    {desarrollo[2]}    {puesto_final}º    {resultado_carrera}\n"
        contenido += f"    {carrera_anterior.referencia}    {condicion_str}    {desarrollo}   {puesto_final}º    {resultado_carrera}\n"
    
    return contenido

def obtener_estadisticas_pista(session, id_caballo, pista_actual, distancia_actual):
    """
    Obtiene estadísticas del caballo por tipo de pista y distancia
    
    Args:
        session: Sesión de la base de datos
        id_caballo: ID del caballo
        pista_actual: Tipo de pista de la carrera actual ('A' para arena, 'C' para césped)
        distancia_actual: Distancia de la carrera actual
        
    Returns:
        dict: Diccionario con estadísticas
    """
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
    
    return resultados

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
    
    # Agregar fecha de nacimiento si está disponible
    if caballo.fechaNac:
        fecha_nac = caballo.fechaNac.strftime("%d.%m.%Y")
        pedigree += f"N. {fecha_nac}.-"
        
        # Agregar información de hermanos maternos si existe
        # Esta información requeriría una consulta adicional que no implementamos aquí
    
    # Agregar colores del stud
    if colores_stud:
        pedigree += f" Colores.- {colores_stud}\n"
    
    return pedigree

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
    # Obtener estadísticas del caballo
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
    
    # Comenzar con el formato correspondiente según la pista actual
    if pista_actual == 'A':  # Arena
        resultado = f"| Arena: {stats['arena_corridas']}/{stats['arena_ganadas']} - S/. {arena_premios:,} | "
        resultado += f"Distancia: {stats['distancia_corridas']}/{stats['distancia_ganadas']} - S/. {distancia_premios:,} | "
        resultado += f"Césped: {stats['cesped_corridas']}/{stats['cesped_ganadas']} | "
    else:  # Césped
        resultado = f"| Césped: {stats['cesped_corridas']}/{stats['cesped_ganadas']} - S/. {cesped_premios:,} | "
        resultado += f"Distancia: {stats['distancia_corridas']}/{stats['distancia_ganadas']} - S/. {distancia_premios:,} | "
        resultado += f"Arena: {stats['arena_corridas']}/{stats['arena_ganadas']} | "
    
    # Agregar resumen
    cc = stats['total_corridas']  # Carreras corridas
    cg = stats['total_ganadas']   # Carreras ganadas
    resultado += f"CC: {cc} CG: {cg} | S/. {total_premios:,}"
    
    return resultado

def formatear_desarrollo(desarrollo_carrera, separador='\t'):
    uno = int(desarrollo_carrera[0:2])
    dos = int(desarrollo_carrera[2:4])
    tre = int(desarrollo_carrera[4:6])
    return f"{uno}º{separador}{dos}º{separador}{tre}º"

def generar_contenido_estudie():
    """Genera el contenido para 'Estudie su Polla' usando bloques estructurados"""
    from models.models import ReunionCarreras, ReunionCaballos, Caballos, Jinetes, Preparadores, Studs
    
    with SessionLocal() as session:
        contenido = ""
        
        # 1. Iteración por Fechas
        fechas = session.query(ReunionCarreras.fecha).filter(
            ReunionCarreras.corrida == 0
        ).distinct().order_by(ReunionCarreras.fecha).all()
        
        for fecha_tuple in fechas:
            fecha = fecha_tuple[0]
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
                
                for reunion_caballo in caballos:
                    # BLOQUE 1: Información básica del caballo
                    contenido += generar_bloque_info_basica(session, reunion_caballo) + "\n"
                    
                    # BLOQUE 2: Historial de carreras anteriores
                    contenido += generar_bloque_historial(session, reunion_caballo, carrera) + "\n"
                    
                    # BLOQUE 3: Resultados detallados
                    contenido += generar_bloque_resultados(session, reunion_caballo) + "\n"
                    
                    # BLOQUE 4: Pedigree y detalles
                    contenido += generar_bloque_pedigree(session, reunion_caballo) + "\n"
                    
                    # BLOQUE 6: Estadísticas del caballo por pista y distancia
                    contenido += generar_bloque_estadisticas(session, reunion_caballo, carrera) + "\n"
                    
                    # Espacio entre caballos
                    contenido += "\n"
                
                # Separación entre carreras
                contenido += "\n"
        
        return contenido