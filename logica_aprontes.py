import os
import re
import datetime

from PySide6.QtWidgets import (
    QWidget, QMessageBox, QListWidgetItem, QMenu, QInputDialog
)
from PySide6.QtGui import QCursor, QAction, QKeySequence, QFont, QShortcut
from PySide6 import QtCore, QtWidgets

from generated.ui_aprontes import Ui_Aprontes
from db import SessionLocal  # Para crear sesiones
from models.models import Caballos, Jinetes, Aprontes as AprontesModel  # Modelos necesitados

class Aprontes(QWidget):
    """Ventana para gestionar y procesar archivos de aprontes."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_Aprontes()
        self.ui.setupUi(self)

        # Conexiones de interfaz
        self.cargar_lista_archivos()
        self.ui.listArchivos.itemClicked.connect(self.cargar_archivo)
        self.ui.btnGuardar.clicked.connect(self.guardar_archivo)
        # Ya no usamos el botón de validación, pues se valida al cargar
        self.ui.btnValidar.setVisible(False)  # Ocultamos el botón de validación

        self.ui.listArchivos.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.listArchivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)

        # Aquí podrías inyectar tu sesión de SQLAlchemy
        self.session = SessionLocal()  # Placeholder para tu Session

    # -------------------------------------------------------------------------
    # 1. CARGA Y CONVERSIÓN (transformaciones)
    # -------------------------------------------------------------------------
    def cargar_archivo(self, item):
        ruta_archivo = os.path.join("/Users/oscarorellana/Proyectos/colaboradores/originales", item.text())
        try:
            with open(ruta_archivo, "r", encoding=self.obtener_codificacion()) as f:
                lineas = f.readlines()

            # Eliminar líneas vacías
            lineas = [ln.strip() for ln in lineas if ln.strip()]

            # Eliminar encabezados fijos
            encabezados_a_eliminar = [
                "JOCKEY CLUB DEL PERU",
                "DEPARTAMENTO HIPICO",
                "COMISION DE PROGRAMA"
            ]
            lineas = [ln for ln in lineas if ln not in encabezados_a_eliminar]

            # Fecha derivada del nombre de archivo
            nombre_archivo = item.text()
            fecha_larga = None
            if len(nombre_archivo) >= 8 and nombre_archivo[0] == "A":
                # Ej: A20231231.txt => A + año(4) + semana(2) + dia(1)
                anio = int(nombre_archivo[1:5])
                semana = int(nombre_archivo[5:7])
                dia_semana = int(nombre_archivo[7:8])
                fecha_larga = self.obtener_fecha_larga(anio, semana, dia_semana)

            # Reemplazar la línea "APRONTES REALIZADOS EL DIA ..." con la fecha nueva (si existe)
            if fecha_larga:
                for i, ln in enumerate(lineas):
                    if ln.startswith("APRONTES REALIZADOS EL DIA"):
                        lineas[i] = f"APRONTES REALIZADOS EL DIA {fecha_larga}"

            # Unir en un texto único y aplicar transformaciones
            texto = "\n".join(lineas)
            texto = self.transformar_contenido(texto)
            
            # Validar todas las líneas durante la carga
            texto = self.validar_contenido_completo(texto)

            self.ui.txtTexto.setPlainText(texto)

            # Generar y mostrar nombre nuevo en el label
            nuevo_nombre = self.generar_nombre_nuevo(nombre_archivo)
            self.ui.lblNombreNuevo.setText(nuevo_nombre)

        except UnicodeDecodeError:
            QMessageBox.critical(
                self, "Error de Codificación",
                "No se pudo leer el archivo debido a un error de codificación."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo leer el archivo:\n{str(e)}")

    def transformar_contenido(self, texto):
        """
        Aplica las conversiones que tuvieras antes:
         - abreviaciones
         - eliminación paréntesis con " con "
         - procesar paréntesis (fechas)
         - eliminar paréntesis sin fechas
         - validar y corregir jinetes
        """
        texto = self.aplicar_abreviaciones(texto)
        texto = self.eliminar_parentesis_antes_de_con(texto)
        texto = self.procesar_parentesis(texto)
        texto = self.eliminar_parentesis_sin_fechas(texto)
        texto = self.normalizar_jinetes(texto)
        return texto

    def aplicar_abreviaciones(self, texto):
        ABREVIACIONES = {
            "rematando de subida": "rem. de sub.",
            "rematando": "rem.",
            "muy fácil": "muy fác.",
            "fácil": "fác.",
            "de subida": "de sub.",
            "en pelo": "pelo",
            "del partidor": "pe.",
            "partidor": "pe.",
            "/5": "",
            ",": " , "
        }
        for clave in sorted(ABREVIACIONES, key=len, reverse=True):
            texto = texto.replace(clave, ABREVIACIONES[clave])
        return texto

    def eliminar_parentesis_antes_de_con(self, texto):
        lineas = texto.splitlines()
        nuevas_lineas = []
        for linea in lineas:
            if " con " in linea:
                idx = linea.index(" con ")
                parte_antes = linea[:idx]
                parte_despues = linea[idx:]
                parte_antes = re.sub(r'\([^)]*\)', '', parte_antes)
                linea = parte_antes.rstrip() + parte_despues
            nuevas_lineas.append(linea)
        return "\n".join(nuevas_lineas)

    def procesar_parentesis(self, texto):
        def reemplazar(match):
            contenido = match.group(1)
            m = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2,4})', contenido)
            if m:
                dia, mes, anio_str = m.groups()
                dia = int(dia)
                mes = int(mes)
                anio = int(anio_str) if len(anio_str) == 4 else 2000 + int(anio_str)
                return f"({dia:02d}/{mes:02d}/{anio:04d})"
            return match.group(0)

        return re.sub(r"\(([^)]*)\)", reemplazar, texto)

    def eliminar_parentesis_sin_fechas(self, texto):
        def revisar_parentesis(match):
            contenido = match.group(1)
            if re.search(r'\b\d{1,2}/\d{1,2}/(\d{2}|\d{4})\b', contenido):
                return match.group(0)
            return ""
        return re.sub(r"\(([^)]*)\)", revisar_parentesis, texto)

    # -------------------------------------------------------------------------
    # 2. VALIDACIÓN (botón "Validar")
    # -------------------------------------------------------------------------
    def validar_contenido_completo(self, texto):
        """
        Recorre cada línea del texto, la parsea y hace validaciones.
        Si algo falla, ofrece un diálogo para editar o omitir la línea.
        Retorna el texto validado.
        """
        lineas = texto.splitlines()

        lineas_modificadas = []
        for i, linea in enumerate(lineas):
            # Conservar líneas de encabezado
            if "***" in linea or "APRONTES REALIZADOS" in linea:
                lineas_modificadas.append(linea)
                continue
                
            # Validar las líneas de aprontes
            while True:
                valido, linea_nueva, msg_error = self.validar_linea_apronte(linea)
                if valido:
                    # Todo OK => agregamos la versión final (que puede tener correcciones automáticas)
                    lineas_modificadas.append(linea_nueva)
                    break
                else:
                    # Hubo un problema => preguntar qué hacer
                    resp = QMessageBox.warning(
                        self,
                        "Validación de Aprontes",
                        f"Error en línea {i+1}:\n{msg_error}\n\n"
                        "¿Desea editar la línea (Sí) o omitir esta línea (No)?\n"
                        "Cancelar interrumpe la validación completa.",
                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                    )

                    if resp == QMessageBox.Yes:
                        # El usuario editará la línea manualmente
                        linea_editada, ok = QInputDialog.getMultiLineText(
                            self,
                            "Editar línea",
                            "Corrige la línea para que cumpla el formato:",
                            linea
                        )
                        if not ok:
                            # Si cierra o cancela el InputDialog => volvemos al mismo prompt
                            continue
                        # Reintentar validación con la línea corregida
                        linea = linea_editada
                        continue

                    elif resp == QMessageBox.No:
                        # Omitir la línea
                        lineas_modificadas.append(f"# LÍNEA OMITIDA: {linea}")
                        break
                    else:
                        # Cancel => abortar toda la validación
                        QMessageBox.information(self, "Validación cancelada", "Se interrumpió la validación.")
                        # Devolver el texto original sin validar
                        return texto

        # Si llegamos aquí, todas las líneas fueron validadas o omitidas
        texto_final = "\n".join(lineas_modificadas)
        return texto_final

    def validar_linea_apronte(self, linea):
        """
        Verifica que la línea cumpla la estructura,
        parsea sus campos y aplica validaciones (fecha futura, caballo, jinete, etc.).
        Devuelve: (True, linea_corregida, "") o (False, linea_parcial, "Mensaje de error")
        """
        data, error_parse = self.parsear_linea_apronte(linea)
        if not data:
            # Falla parse => devolvemos la línea tal cual
            return False, linea, f"No cumple el formato esperado. {error_parse}"

        caballo = data["caballo"]
        jinete = data["jinete"]
        distancia1 = data["distancia1"]
        tiempo1_quintos = data["tiempo1_quintos"]
        distancia2 = data["distancia2"]
        tiempo2_quintos = data["tiempo2_quintos"]
        pista = data["pista"]
        fecha_linea = data["fecha_linea"]
        calif = data["calificacion"]

        # 1) Fecha futura
        if fecha_linea:
            try:
                fecha_dt = datetime.datetime.strptime(fecha_linea, "%d/%m/%Y").date()
                if fecha_dt > datetime.date.today():
                    return False, linea, f"La fecha {fecha_linea} es mayor que hoy."
            except ValueError:
                return False, linea, f"Fecha inválida en la línea: {fecha_linea}"

        # 2) Caballo
        caballo_existe, caballo_final = self.verificar_caballo(caballo)
        if not caballo_existe and not caballo_final:
            return False, linea, f"Caballo '{caballo}' no existe y no se agregó."
        if caballo_final != caballo:
            # Reemplazamos en la línea. Para evitar reemplazos ambiguos,
            # podrías regenerar la línea con data. Aquí hacemos algo simple:
            linea = linea.replace(caballo, caballo_final, 1)
            caballo = caballo_final

        # 3) Jinete - ya fue normalizado durante la carga
        # No es necesario hacer nada aquí

        # 4) Distancia
        if distancia1 < 200 or distancia1 > 2200:
            return False, linea, f"La distancia {distancia1} está fuera del rango (200-2200)."

        # 5) Velocidad mínima
        segundos_totales = tiempo1_quintos * 0.2
        velocidad_kmh = 0
        if segundos_totales > 0:
            velocidad_kmh = (distancia1 / segundos_totales) * 3.6
        if velocidad_kmh > 60:
            return False, linea, f"Velocidad {velocidad_kmh:.1f} km/h es menor a 60."

        # 6) Calificación
        if calif:
            califs_validas = ["M", "R", "B", "MB", "E"]
            if calif not in califs_validas:
                return False, linea, f"La calificación '{calif}' no es válida."

        # Ok
        return True, linea, ""

    def parsear_linea_apronte(self, linea):
        """
        Ajustamos el regex para mayor flexibilidad. Ejemplo de línea:
          "JUVENTUD ROSADA con R MELGAREJO 1100 en 1'12\"3 , 200 en 12\"3 muy fác. pelo (05/02/2025) B"
        
        Notas:
         - Permitimos espacios extra.
         - Para el tiempo, aceptamos secuencias con dígitos, ', " y sin limitarnos a un patrón exacto.
         - La parte de "pista" la capturamos hasta encontrar fecha o calif opcionales.
        """
        # Regex explicada:
        # - (?P<caballo>[^0-9]+?) => toma todo hasta que aparezcan dígitos (heurística)
        # - \s+con\s+ => la palabra 'con' rodeada de espacios
        # - (?P<jinete>[^0-9]+?) => jinete hasta que tope con un número
        # - (?P<dist1>\d+)\s+en\s+(?P<tiempo1>[^,\s]+) => 1100 en 1'12"3
        # - la segunda distancia-tiempo es opcional => , 200 en 12"3
        # - (?P<pista>.*?) => capturamos el resto en "pista", pero ojo con la parte final
        # - (?:\((?P<fecha>\d{1,2}/\d{1,2}/\d{4})\))? => fecha opcional en paréntesis
        # - (?P<calif>[MRBmbE]+)? => calificación opcional
        # Se usan lookups para no comernos la fecha y la calif dentro de 'pista'.
        
        patron = re.compile(
            r"""
            ^\s*
            (?P<caballo>[^\d]+?)       # caballo, sin dígitos
            \s+con\s+
            (?P<jinete>[^\d]+?)        # jinete, sin dígitos
            \s+(?P<dist1>\d+)\s+en\s+(?P<tiempo1>[^\s,]+)
            (?:\s*,\s*(?P<dist2>\d+)\s+en\s+(?P<tiempo2>[^\s]+))?
            \s+(?P<resto>.*?)
            \s*$
            """,
            re.VERBOSE
        )

        m = patron.match(linea)
        if not m:
            return None, "No coincide con la estructura base (caballo con jinete dist1 en tiempo...)."

        # Extraemos lo que tenemos
        caballo   = m.group('caballo').strip()
        jinete    = m.group('jinete').strip()
        dist1_str = m.group('dist1')
        t1_str    = m.group('tiempo1')
        dist2_str = m.group('dist2') or ""
        t2_str    = m.group('tiempo2') or ""
        resto     = m.group('resto').strip()

        # Analizar 'resto' para detectar fecha opcional ( (dd/mm/yyyy) ) y calif final
        # Podrían estar o no. Para simplificar, lo hacemos con otra regex:
        # p.ej. "muy fác. pelo (05/02/2025) B"
        patron_final = re.compile(
            r"""
            ^(?P<pista>.*?)
            (?:\s*\((?P<fecha>\d{1,2}/\d{1,2}/\d{4})\))?
            \s*(?P<calif>[MRBmbE]+)?\s*$
            """,
            re.VERBOSE
        )
        m2 = patron_final.match(resto)
        if not m2:
            return None, "No se pudo extraer pista, fecha y/o calificación del resto."

        pista       = m2.group('pista').strip()
        fecha_linea = m2.group('fecha')
        calif       = (m2.group('calif') or "").upper()

        # Convertir distancias
        try:
            distancia1 = int(dist1_str)
        except ValueError:
            return None, f"Distancia principal inválida: {dist1_str}"

        tiempo1_quintos = self.parse_tiempo_quintos(t1_str)
        if tiempo1_quintos is None:
            return None, f"Tiempo principal inválido: {t1_str}"

        distancia2 = 0
        tiempo2_quintos = 0
        if dist2_str:
            try:
                distancia2 = int(dist2_str)
            except ValueError:
                return None, f"Distancia 2 inválida: {dist2_str}"

        if t2_str:
            t2_val = self.parse_tiempo_quintos(t2_str)
            if t2_val is None:
                return None, f"Tiempo 2 inválido: {t2_str}"
            tiempo2_quintos = t2_val

        data = {
            "caballo": caballo,
            "jinete": jinete,
            "distancia1": distancia1,
            "tiempo1_quintos": tiempo1_quintos,
            "distancia2": distancia2,
            "tiempo2_quintos": tiempo2_quintos,
            "pista": pista,
            "fecha_linea": fecha_linea,
            "calificacion": calif if calif else None
        }
        return data, None

    def parse_tiempo_quintos(self, t_str):
        """
        Convierte algo como "1'12\"3" en quintos de segundo.
        Acepta distintos patrones, p.ej. 1'12"3, 1'12''3, etc.
        """
        # Intentamos varios formatos:
        # Ejemplo 1: 1'12"3 => (\d+)'(\d+)"(\d+)
        # Ejemplo 2: 1'12''3 => (\d+)'(\d+)''(\d+)
        # como fallback, si no matchea, retornamos None.
        # En general, 1'12"3 => 1 min, 12 seg, 3 quintos => total 72.6 seg => 363 quintos
        patrones = [
            re.compile(r'^(\d+)[\' ](\d+)"(\d+)$'),        # 1'12"3
            re.compile(r'^(\d+)[\' ](\d+)\'\'(\d+)$'),     # 1'12''3
            # Añade más si tienes otras variantes
        ]

        for pat in patrones:
            m = pat.match(t_str.strip())
            if m:
                minutos = int(m.group(1))
                segundos = int(m.group(2))
                quintos = int(m.group(3))
                total_s = minutos*60 + segundos + quintos*0.2
                return int(round(total_s*5))

        # Si no coincide ningún patrón, probamos un parse súper básico
        # Por ejemplo, si alguien escribió "72.3" => interpretarlo como 72.3 seg => 361 quintos
        # Ajusta a tus necesidades.
        try:
            flotante = float(t_str.replace('"', '').replace("'", ""))
            return int(round(flotante*5))
        except:
            return None

    # -------------------------------------------------------------------------
    # 3. MÉTODOS PLACEHOLDER PARA VERIFICACIÓN EN BD
    # -------------------------------------------------------------------------
    def verificar_caballo(self, nombre_caballo):
        """
        Si no existe en BD, se pregunta si se corrige o se registra como debutante.
        Devuelve (existe, nombre_final).
        """
        c = self.buscar_caballo_por_nombre(nombre_caballo)
        if c:
            return True, nombre_caballo

        # Crear un mensaje personalizado
        msg = f"El caballo '{nombre_caballo}' no se encuentra."
        
        # Crear un cuadro de diálogo personalizado con botones específicos
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Caballo no encontrado")
        msgBox.setText(msg)
        msgBox.setInformativeText("¿Qué deseas hacer?")
        
        # Crear botones con textos personalizados
        btnCorregir = msgBox.addButton("Corregir el nombre", QMessageBox.ActionRole)
        btnDebutante = msgBox.addButton("Debutante", QMessageBox.ActionRole)
        btnCancelar = msgBox.addButton("Cancelar la validación", QMessageBox.RejectRole)
        
        msgBox.setDefaultButton(btnCorregir)
        msgBox.exec()
        
        clickedBtn = msgBox.clickedButton()
        
        if clickedBtn == btnCancelar:
            return False, ""
            
        elif clickedBtn == btnCorregir:
            # Proceso recursivo para corregir el nombre hasta encontrar un caballo válido
            return self.corregir_nombre_caballo(nombre_caballo)
            
        elif clickedBtn == btnDebutante:
            # Agregar nuevo caballo como debutante
            return self.agregar_caballo_debutante(nombre_caballo)
        
        return False, ""
        
    def corregir_nombre_caballo(self, nombre_original):
        """
        Procesa la corrección del nombre del caballo.
        Si el nombre corregido no existe, se vuelve a preguntar.
        """
        nuevo, ok = QInputDialog.getText(self, "Corregir caballo",
                                        "Nuevo nombre del caballo:",
                                        text=nombre_original)
        if not ok or not nuevo.strip():
            return False, ""
            
        nuevo = nuevo.strip()
        c = self.buscar_caballo_por_nombre(nuevo)
        
        if c:
            return True, nuevo
        else:
            # El nombre corregido tampoco existe, preguntar qué hacer
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Nombre no encontrado")
            msgBox.setText(f"El nombre corregido '{nuevo}' tampoco existe.")
            msgBox.setInformativeText("¿Qué deseas hacer?")
            
            btnReCorregir = msgBox.addButton("Corregir nuevamente", QMessageBox.ActionRole)
            btnDebutante = msgBox.addButton("Registrar como debutante", QMessageBox.ActionRole)
            btnCancelar = msgBox.addButton("Cancelar", QMessageBox.RejectRole)
            
            msgBox.setDefaultButton(btnReCorregir)
            msgBox.exec()
            
            clickedBtn = msgBox.clickedButton()
            
            if clickedBtn == btnCancelar:
                return False, ""
            elif clickedBtn == btnReCorregir:
                # Volver a intentar corregir el nombre (recursivamente)
                return self.corregir_nombre_caballo(nuevo)
            elif clickedBtn == btnDebutante:
                # Registrar como debutante
                return self.agregar_caballo_debutante(nuevo)
                
        return False, ""
        
    def agregar_caballo_debutante(self, nombre_caballo):
        """
        Recopila información para un caballo debutante y lo agrega a la base de datos.
        """
        datos_debut = self.dialogo_nuevo_caballo(nombre_caballo)
        if not datos_debut:
            return False, ""
            
        try:
            # Crear nueva instancia de Caballo y agregarla a la base de datos
            from models.models import Caballos
            
            nuevo_caballo = Caballos(
                nombre=datos_debut["nombre"],
                minusculas=datos_debut["minusculas"],
                breve=datos_debut["breve"],
                marcadorStart=datos_debut["marcadorStart"],
                # Valores por defecto para los campos obligatorios
                idPais=1,  # Perú por defecto
                idColor=14,  # Color por defecto
                idPadre=3689,  # Padre por defecto
                idMadre=3932,  # Madre por defecto
                idCriador=3561,  # Criador por defecto
                # Para los demás atributos se utilizan los valores predeterminados de la BD
            )
            
            self.session.add(nuevo_caballo)
            self.session.commit()
            
            QMessageBox.information(
                self, 
                "Caballo Registrado", 
                f"Se ha registrado el caballo debutante '{datos_debut['nombre']}' en la base de datos."
            )
            
            return False, datos_debut["nombre"]
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error al registrar caballo", 
                f"No se pudo registrar el caballo en la base de datos:\n{str(e)}"
            )
            self.session.rollback()
            return False, ""

    def dialogo_nuevo_caballo(self, nombre_caballo):
        minus_default = self.capitalizar_nombre(nombre_caballo)
        breve_default = minus_default
        marcador_default = minus_default

        minus_, ok = QInputDialog.getText(self, "Caballo debutante: minusculas",
                                          "Nombre en minúsculas:",
                                          text=minus_default)
        if not ok or not minus_.strip():
            return None
        breve_, ok = QInputDialog.getText(self, "Caballo debutante: breve",
                                          "Nombre abreviado:",
                                          text=breve_default)
        if not ok or not breve_.strip():
            return None
        marcador_, ok = QInputDialog.getText(self, "Caballo debutante: marcador",
                                             "Nombre marcador:",
                                             text=marcador_default)
        if not ok or not marcador_.strip():
            return None

        return {
            "nombre": nombre_caballo,
            "minusculas": minus_.strip(),
            "breve": breve_.strip(),
            "marcadorStart": marcador_.strip()
        }

    def normalizar_jinetes(self, texto):
        """
        Busca patrones de jinetes en el texto y normaliza sus nombres 
        según la información de la base de datos.
        Esta función se usa durante la carga del archivo.
        """
        # Patrón para detectar la estructura "con NOMBRE_JINETE"
        patron = re.compile(r'(\s+con\s+)([A-Z][A-Z\s]+)(\s+\d+\s+en\s+)')
        
        # Función para procesar cada coincidencia
        def reemplazar_jinete(match):
            prefijo = match.group(1)  # "con "
            jcp = match.group(2).strip()  # nombre del jinete en mayúsculas
            sufijo = match.group(3)  # " 1100 en "
            
            # Tratamiento especial para "aprendiz" y "galopador" (en cualquier variante de mayúsculas/minúsculas)
            if jcp.upper() == "APRENDIZ" or jcp.upper() == "GALOPADOR":
                return f"{prefijo}{jcp.lower()}{sufijo}"
                
            # Buscar el jinete en la base de datos
            jinete_normalizado = self.obtener_nombre_jinete(jcp)
            
            # Retornar la cadena reemplazada
            return f"{prefijo}{jinete_normalizado}{sufijo}"
        
        # Reemplazar todas las coincidencias en el texto
        texto = re.sub(patron, reemplazar_jinete, texto)
        
        # Buscar también los casos donde "aprendiz" o "galopador" podrían estar en minúsculas o mixtos
        # y normalizar a minúsculas sin preguntar
        patron_especial = re.compile(r'(\s+con\s+)(aprendiz|galopador|Aprendiz|Galopador|APRENDIZ|GALOPADOR)(\s+\d+\s+en\s+)', re.IGNORECASE)
        
        def normalizar_especiales(match):
            prefijo = match.group(1)
            palabra = match.group(2).lower()  # Convertir a minúsculas
            sufijo = match.group(3)
            return f"{prefijo}{palabra}{sufijo}"
            
        return re.sub(patron_especial, normalizar_especiales, texto)
    
    def obtener_nombre_jinete(self, jcp):
        """
        Busca un jinete por su código JCP y devuelve el nombre normalizado.
        Si no existe, muestra un diálogo para editarlo.
        """
        j = self.buscar_jinete_por_jcp(jcp)
        if j:
            # Si el jinete existe en BD, usar el valor del campo 'jinete'
            return j.jinete
            
        # Si no existe, mostrar diálogo para editar o marcar como aprendiz
        class JineteDialog(QtWidgets.QDialog):
            def __init__(self, parent=None, jcp="", sugerido=""):
                super().__init__(parent)
                self.setWindowTitle("Jinete no encontrado")
                self.setMinimumWidth(400)
                
                # Crear el layout
                layout = QtWidgets.QVBoxLayout()
                
                # Mensaje explicativo
                label = QtWidgets.QLabel(f"El jinete '{jcp}' no fue encontrado en la base de datos.")
                label.setWordWrap(True)
                layout.addWidget(label)
                
                # Instrucciones adicionales
                instrucciones = QtWidgets.QLabel("Por favor, edita el nombre del jinete o marca como aprendiz:")
                instrucciones.setWordWrap(True)
                layout.addWidget(instrucciones)
                
                # Campo de texto
                self.textEdit = QtWidgets.QLineEdit(sugerido)
                layout.addWidget(self.textEdit)
                
                # Botones
                btnLayout = QtWidgets.QHBoxLayout()
                
                self.btnOk = QtWidgets.QPushButton("Aceptar")
                self.btnOk.setDefault(True)
                self.btnOk.clicked.connect(self.accept)
                
                self.btnAprendiz = QtWidgets.QPushButton("Aprendiz")
                self.btnAprendiz.clicked.connect(self.marcar_aprendiz)
                
                self.btnCancel = QtWidgets.QPushButton("Cancelar")
                self.btnCancel.clicked.connect(self.reject)
                
                btnLayout.addWidget(self.btnOk)
                btnLayout.addWidget(self.btnAprendiz)
                btnLayout.addWidget(self.btnCancel)
                
                layout.addLayout(btnLayout)
                self.setLayout(layout)
                
                # Valor adicional para saber si se presionó el botón de aprendiz
                self.es_aprendiz = False
                
            def marcar_aprendiz(self):
                self.es_aprendiz = True
                self.accept()
                
            def get_text(self):
                return self.textEdit.text().strip()
                
            def is_aprendiz(self):
                return self.es_aprendiz

        # Usar el diálogo personalizado
        sugerido = self.capitalizar_nombre(jcp)
        dialog = JineteDialog(self, jcp, sugerido)
        
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            if dialog.is_aprendiz():
                # Si el usuario presiona "Aprendiz", usar "aprendiz" en minúsculas
                return "aprendiz"
            else:
                # Si el usuario edita y acepta, usar el texto editado
                nuevo = dialog.get_text()
                if not nuevo:
                    return jcp  # Si estaba vacío, mantener el original
                return nuevo
        else:
            # Si cancela, mantener el original
            return jcp

    def capitalizar_nombre(self, texto):
        palabras = texto.lower().split()
        return " ".join(p.capitalize() for p in palabras)

    def buscar_caballo_por_nombre(self, nombre):
        # print (self.session)
        if not self.session:
            return None
        return self.session.query(Caballos).filter_by(nombre=nombre).one_or_none()
        # return None

    def buscar_jinete_por_jcp(self, jcp):
        if not self.session:
            return None
        return self.session.query(Jinetes).filter_by(jcp=jcp).one_or_none()
        # return None

    # -------------------------------------------------------------------------
    # 4. GUARDAR ARCHIVO
    # -------------------------------------------------------------------------
    def guardar_archivo(self):
        item = self.ui.listArchivos.currentItem()
        if not item:
            QMessageBox.warning(self, "Selección", "No se ha seleccionado ningún archivo.")
            return

        contenido = self.ui.txtTexto.toPlainText()
        nombre_nuevo = self.ui.lblNombreNuevo.text()
        if not nombre_nuevo:
            QMessageBox.warning(self, "Error", "No se ha generado un nuevo nombre de archivo.")
            return

        # CheckBoxes
        carpetas = {
            "Estudie": self.ui.chkEstudie.isChecked(),
            "Cátedra": self.ui.chkCatedra.isChecked(),
            "Trabajo": self.ui.chkTrabajo.isChecked(),
            "Quispe": self.ui.chkQuispe.isChecked(),
            "Dato": self.ui.chkDato.isChecked(),
        }

        guardar_en_bd = False  # Flag para saber si debemos actualizar la BD
        guardado_exitoso = False
        ruta_trabajo = None
        
        for nombre_carpeta, activo in carpetas.items():
            if activo:
                ruta_destino = f"/Users/oscarorellana/Proyectos/colaboradores/{nombre_carpeta}"
                os.makedirs(ruta_destino, exist_ok=True)
                ruta_archivo = os.path.join(ruta_destino, nombre_nuevo)

                try:
                    with open(ruta_archivo, "w", encoding=self.obtener_codificacion()) as f:
                        f.write(contenido)
                    guardado_exitoso = True
                    
                    # Si se guardó en la carpeta "Trabajo", guardamos la ruta para consultar después
                    if nombre_carpeta == "Trabajo":
                        guardar_en_bd = True
                        ruta_trabajo = ruta_destino
                        
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error",
                        f"No se pudo guardar en {ruta_destino}:\n{str(e)}"
                    )

        if guardado_exitoso:
            if guardar_en_bd:
                # Preguntar al usuario si desea actualizar los aprontes ahora
                respuesta = QMessageBox.question(
                    self, 
                    "Actualizar Aprontes", 
                    "El archivo se ha guardado en la carpeta Trabajo. ¿Desea actualizar los aprontes en la base de datos ahora?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if respuesta == QMessageBox.Yes:
                    try:
                        # Actualizamos la base de datos con los aprontes
                        self.actualizar_aprontes_en_bd(contenido)
                        
                        # Registrar la acción en el archivo de tareas realizadas
                        self.registrar_tarea_realizada(ruta_trabajo, nombre_nuevo)
                        
                        QMessageBox.information(self, "Guardado", "Archivo guardado en las carpetas seleccionadas y actualizado en la base de datos.")
                    except Exception as e:
                        QMessageBox.warning(
                            self, "Advertencia",
                            f"El archivo se guardó, pero hubo un problema al actualizar la base de datos:\n{str(e)}"
                        )
                else:
                    QMessageBox.information(self, "Guardado", "Archivo guardado en las carpetas seleccionadas. La actualización de la base de datos no se realizó.")
            else:
                QMessageBox.information(self, "Guardado", "Archivo guardado en las carpetas seleccionadas.")

    def registrar_tarea_realizada(self, ruta_trabajo, nombre_archivo):
        """
        Registra la tarea de actualización en el archivo tareas_realizadas.txt
        
        Args:
            ruta_trabajo (str): Ruta de la carpeta Trabajo
            nombre_archivo (str): Nombre del archivo procesado
        """
        try:
            # Crear el archivo de tareas realizadas si no existe
            archivo_tareas = os.path.join(ruta_trabajo, "tareas_realizadas.txt")
            
            # Obtener la fecha y hora actual
            ahora = datetime.datetime.now()
            fecha_hora = ahora.strftime("%d/%m/%Y %H:%M:%S")
            
            # Crear el mensaje a registrar
            mensaje = f"[{fecha_hora}] Actualización de aprontes en BD para el archivo: {nombre_archivo}\n"
            
            # Abrir el archivo en modo append (crear si no existe)
            with open(archivo_tareas, "a", encoding=self.obtener_codificacion()) as f:
                f.write(mensaje)
                
        except Exception as e:
            QMessageBox.warning(
                self, 
                "Advertencia", 
                f"No se pudo registrar la tarea en el archivo de registro:\n{str(e)}"
            )
    
    # -------------------------------------------------------------------------
    # 5. OTRAS UTILIDADES
    # -------------------------------------------------------------------------
    def mostrar_menu_contextual(self, posicion):
        item = self.ui.listArchivos.itemAt(posicion)
        if not item:
            return

        menu = QMenu(self)
        vista_rapida = QAction("Vista rápida", self)
        vista_rapida.triggered.connect(lambda: self.vista_rapida_archivo(item.text()))
        menu.addAction(vista_rapida)
        menu.exec(QCursor.pos())

    def vista_rapida_archivo(self, nombre_archivo):
        ruta_archivo = os.path.join("/Users/oscarorellana/Proyectos/colaboradores/originales", nombre_archivo)
        try:
            with open(ruta_archivo, "r", encoding=self.obtener_codificacion()) as f:
                contenido = f.read()
                
            # Crear un diálogo mejorado para edición
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QPushButton
            
            class VistaRapidaDialog(QDialog):
                def __init__(self, parent=None, nombre_archivo="", contenido="", ruta_archivo="", codificacion="latin-1"):
                    super().__init__(parent)
                    self.setWindowTitle(f"Vista Rápida - {nombre_archivo}")
                    self.resize(700, 500)
                    self.ruta_archivo = ruta_archivo
                    self.codificacion = codificacion
                    
                    # Crear layout vertical para todo el diálogo
                    layout = QVBoxLayout(self)
                    
                    # Editor de texto
                    self.text_edit = QPlainTextEdit(self)
                    self.text_edit.setPlainText(contenido)
                    
                    # Fuente monoespaciada
                    font = QFont("Menlo", 12)
                    self.text_edit.setFont(font)
                    
                    # Añadir al layout (se expandirá cuando se redimensione)
                    layout.addWidget(self.text_edit)
                    
                    # Botones inferiores
                    btn_layout = QHBoxLayout()
                    
                    self.btn_guardar = QPushButton("Guardar")
                    self.btn_guardar.clicked.connect(self.guardar_cambios)
                    
                    self.btn_cerrar = QPushButton("Cerrar")
                    self.btn_cerrar.clicked.connect(self.reject)
                    
                    btn_layout.addWidget(self.btn_guardar)
                    btn_layout.addWidget(self.btn_cerrar)
                    
                    layout.addLayout(btn_layout)
                    
                    # Atajos de teclado
                    self.shortcut_guardar = QShortcut(QKeySequence("Ctrl+S"), self)
                    self.shortcut_guardar.activated.connect(self.guardar_cambios)
                    
                def guardar_cambios(self):
                    try:
                        contenido_nuevo = self.text_edit.toPlainText()
                        with open(self.ruta_archivo, "w", encoding=self.codificacion) as f:
                            f.write(contenido_nuevo)
                        QMessageBox.information(self, "Guardado", "Los cambios han sido guardados correctamente.")
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{str(e)}")
            
            # Crear y mostrar el diálogo
            dialogo = VistaRapidaDialog(
                self, 
                nombre_archivo=nombre_archivo, 
                contenido=contenido, 
                ruta_archivo=ruta_archivo,
                codificacion=self.obtener_codificacion()
            )
            
            dialogo.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo:\n{str(e)}")

    def obtener_codificacion(self):
        return "latin-1" if self.ui.radioANSI.isChecked() else "utf-8"

    def cargar_lista_archivos(self):
        carpeta_origen = "/Users/oscarorellana/Proyectos/colaboradores/originales"
        if not os.path.exists(carpeta_origen):
            QMessageBox.warning(self, "Error", "La carpeta de aprontes no existe.")
            return

        archivos = [f for f in os.listdir(carpeta_origen) if f.startswith("A") and f.endswith(".txt")]
        self.ui.listArchivos.clear()
        for archivo in archivos:
            self.ui.listArchivos.addItem(QListWidgetItem(archivo))

    def obtener_fecha_larga(self, anio, semana, dia):
        try:
            fecha = datetime.date.fromisocalendar(anio, semana, dia)
            dias = {1: "Lunes", 2: "Martes", 3: "Miércoles", 4: "Jueves", 5: "Viernes", 6: "Sábado", 7: "Domingo"}
            meses = {
                1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
                5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
                9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
            }
            return f"{dias[fecha.isoweekday()]} {fecha.day} de {meses[fecha.month]} de {fecha.year}"
        except ValueError:
            return "Fecha inválida"

    def generar_nombre_nuevo(self, nombre_original):
        if not nombre_original.startswith("A"):
            return nombre_original
        try:
            anio = int(nombre_original[1:5])
            semana = int(nombre_original[5:7])
            dia = int(nombre_original[7:8])
            fecha_larga = self.obtener_fecha_larga(anio, semana, dia)
            return f"Aprontes {anio}{semana}{dia} - {fecha_larga}.txt"
        except:
            return nombre_original
            
    # -------------------------------------------------------------------------
    # 6. ACTUALIZACIÓN DE LA BASE DE DATOS
    # -------------------------------------------------------------------------
    def actualizar_aprontes_en_bd(self, contenido):
        """
        Procesa el contenido del archivo y agrega registros a la tabla Aprontes.
        
        Args:
            contenido (str): Contenido completo del archivo procesado
        """
        lineas = contenido.splitlines()
        fecha_principal = None
        registros_creados = 0
        registros_actualizados = 0
        
        # Buscar la fecha principal en la primera línea que contiene "APRONTES REALIZADOS EL DIA"
        for linea in lineas:
            if "APRONTES REALIZADOS EL DIA" in linea:
                # Extraer la fecha del formato "APRONTES REALIZADOS EL DIA Domingo 25 de Febrero de 2024"
                try:
                    # Extraer la fecha en formato texto
                    partes = linea.split("APRONTES REALIZADOS EL DIA ")[1].strip()
                    
                    # Convertir la fecha textual a objeto datetime
                    dia_semana_texto = partes.split()[0]  # Domingo
                    dia = int(partes.split()[1])  # 25
                    mes_texto = partes.split("de ")[1].split()[0]  # Febrero
                    anio = int(partes.split("de ")[-1])  # 2024
                    
                    # Convertir mes texto a número
                    meses = {
                        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
                        "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
                        "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
                    }
                    mes = meses.get(mes_texto, 1)
                    
                    # Crear objeto date
                    fecha_principal = datetime.date(anio, mes, dia)
                except Exception as e:
                    QMessageBox.warning(
                        self, "Advertencia", 
                        f"No se pudo extraer la fecha principal del archivo. Se usará la fecha actual.\n{str(e)}"
                    )
                    fecha_principal = datetime.date.today()
                break
        
        # Si no se encontró ninguna fecha, usar la fecha actual
        if not fecha_principal:
            fecha_principal = datetime.date.today()
        
        # Procesar cada línea del archivo para convertirla en registro de apronte
        for linea in lineas:
            # Saltar líneas de encabezado y líneas comentadas
            if "***" in linea or "APRONTES REALIZADOS" in linea or linea.strip().startswith("#"):
                continue
            
            # Validar y parsear la línea
            valid, _, _ = self.validar_linea_apronte(linea)
            if not valid:
                continue
                
            data, _ = self.parsear_linea_apronte(linea)
            if not data:
                continue
            
            # Extraer los datos necesarios para el registro
            caballo_nombre = data["caballo"]
            jinete_nombre = data["jinete"]
            distancia1 = data["distancia1"]
            tiempo1_quintos = data["tiempo1_quintos"]
            distancia2 = data["distancia2"]
            tiempo2_quintos = data["tiempo2_quintos"]
            pista = data["pista"] 
            calificacion = data["calificacion"] if data["calificacion"] else ""
            
            # Si hay fecha específica en la línea, usarla en lugar de la fecha principal
            fecha_apronte = fecha_principal
            if data["fecha_linea"]:
                try:
                    dia, mes, anio = map(int, data["fecha_linea"].split("/"))
                    fecha_apronte = datetime.date(anio, mes, dia)
                except:
                    pass  # Si hay error, mantener la fecha principal
            
            # Buscar el id del caballo en la BD
            caballo = self.buscar_caballo_por_nombre(caballo_nombre)
            if not caballo:
                continue  # Si el caballo no existe, saltamos esta línea
            
            # Verificar si ya existe un registro para este caballo y fecha
            try:
                apronte_existente = self.session.query(AprontesModel).filter(
                    AprontesModel.fecha == fecha_apronte,
                    AprontesModel.idCaballo == caballo.idCaballo
                ).first()
                
                if apronte_existente:
                    # Actualizar el registro existente
                    apronte_existente.jinete = jinete_nombre
                    apronte_existente.distancia = distancia1
                    apronte_existente.tiempo = tiempo1_quintos
                    apronte_existente.disFin1 = distancia2
                    apronte_existente.tpoFin1 = tiempo2_quintos
                    apronte_existente.disFin2 = 0  # No tenemos información del segundo final
                    apronte_existente.tpoFin2 = 0  # No tenemos información del segundo final
                    apronte_existente.pista = pista
                    apronte_existente.calificacion = calificacion
                    registros_actualizados += 1
                else:
                    # Crear un nuevo registro
                    nuevo_apronte = AprontesModel(
                        fecha=fecha_apronte,
                        idCaballo=caballo.idCaballo,
                        jinete=jinete_nombre,
                        distancia=distancia1,
                        tiempo=tiempo1_quintos,
                        disFin1=distancia2,
                        tpoFin1=tiempo2_quintos,
                        disFin2=0,  # No tenemos información del segundo final
                        tpoFin2=0,  # No tenemos información del segundo final
                        pista=pista,
                        calificacion=calificacion
                    )
                    self.session.add(nuevo_apronte)
                    registros_creados += 1
                    
            except Exception as e:
                self.session.rollback()
                raise Exception(f"Error al procesar la línea '{linea}': {str(e)}")
        
        # Confirmar los cambios en la base de datos
        try:
            self.session.commit()
            QMessageBox.information(
                self, "Actualización BD", 
                f"Base de datos actualizada exitosamente.\n"
                f"Registros creados: {registros_creados}\n"
                f"Registros actualizados: {registros_actualizados}"
            )
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al guardar los cambios en la base de datos: {str(e)}")