import os
import re
import datetime

from PySide6.QtWidgets import (
    QWidget, QMessageBox, QListWidgetItem, QMenu, QInputDialog
)
from PySide6.QtGui import QCursor, QAction
from PySide6 import QtCore
from PySide6 import QtWidgets  # Importar QtWidgets explícitamente
from PySide6.QtUiTools import QUiLoader  # Importar QUiLoader para cargar el archivo .ui
from PySide6.QtCore import QFile  # Para manejar el archivo .ui

from db import SessionLocal
from models.models import Caballos, Studs, Preparadores, ReunionCaballos, ReunionCarreras, ErroresComunes

class PesosFisicos(QWidget):
    """Ventana para gestionar y procesar archivos de pesos físicos."""

    def __init__(self):
        super().__init__()
        self.cargar_ui()  # Cargar la interfaz desde el archivo .ui
        print("✅ Ventana de pesos físicos cargada correctamente.")  # Debug

        # Carpeta de archivos originales
        self.carpeta_originales = "/Users/oscarorellana/Proyectos/colaboradores/originales"
        
        # Inicialización de interfaz
        self.cargar_lista_archivos()
        
        # Conexiones de botones y eventos
        self.ui.listArchivos.itemClicked.connect(self.cargar_archivo)
        self.ui.btnCerrar.clicked.connect(self.cerrar_ventana)
        self.ui.btnGuardar.clicked.connect(self.guardar_archivo)
        self.ui.btnValidar.setVisible(False)  # Ocultamos el botón de validación por ahora
        
        # Menú contextual para la lista de archivos
        self.ui.listArchivos.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.listArchivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        
        # Crear sesión de base de datos
        self.session = SessionLocal()

    def closeEvent(self, event):
        """Controla el cierre de la ventana"""
        # Cerrar la sesión de base de datos
        if self.session:
            self.session.close()
            print("Sesión de base de datos cerrada")
        super().closeEvent(event)

    def cerrar_ventana(self):
        """Cierra la sesión de base de datos y oculta la ventana"""
        if self.session:
            self.session.close()
        self.hide()
        
    def cargar_lista_archivos(self):
        """Carga la lista de archivos de pesos físicos del directorio configurado"""
        # Usar una ruta configurable con valor por defecto
        base_path = os.getenv("COLABORADORES_PATH", os.path.expanduser("~/Proyectos/colaboradores"))
        carpeta_origen = os.path.join(base_path, "originales")
        
        self.ui.listArchivos.clear()
        
        # Verificar que la carpeta existe
        if not os.path.exists(carpeta_origen):
            QMessageBox.warning(self, "Error", "La carpeta de originales no existe.")
            return
            
        # Filtrar archivos que comienzan con "PK" (Pesos Físicos) y terminan con ".txt"
        archivos = [f for f in os.listdir(carpeta_origen) 
                   if f.startswith("PK") and f.endswith(".txt")]
        
        # Ordenar por fecha (más recientes primero)
        archivos.sort(reverse=True)
        
        # Agregar a la lista
        for archivo in archivos:
            self.ui.listArchivos.addItem(QListWidgetItem(archivo))
            
    def cargar_archivo(self, item):
        """Carga el contenido del archivo seleccionado en el TextEdit"""
        # Usar la misma lógica de ruta configurable
        base_path = os.getenv("COLABORADORES_PATH", os.path.expanduser("~/Proyectos/colaboradores"))
        ruta_archivo = os.path.join(base_path, "originales", item.text())
        
        try:
            # Determinar la codificación
            codificacion = "latin-1" if self.ui.radioANSI.isChecked() else "utf-8"
            
            # Leer el archivo
            with open(ruta_archivo, "r", encoding=codificacion) as f:
                lineas = f.readlines()
            
            # Eliminar líneas vacías pero mantener los espacios al inicio
            lineas = [ln for ln in lineas if ln.strip()]
            
            # Generar nombre nuevo basado en la fecha
            nuevo_nombre = self.generar_nombre_nuevo(item.text())
            self.ui.lblNombreNuevo.setText(nuevo_nombre)
            
            # Extraer la fecha formateada para la primera línea
            fecha_formateada = ""
            try:
                if item.text().startswith("PK") and len(item.text()) >= 9:
                    anio = int(item.text()[2:6])
                    semana = int(item.text()[6:8])
                    dia_semana = int(item.text()[8:9])
                    
                    # Calcular la fecha
                    fecha_obj = self.calcular_fecha_desde_nombre(anio, semana, dia_semana)
                    
                    # Obtener el nombre del día en español
                    dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
                    nombre_dia = dias[fecha_obj.weekday()]
                    
                    # Obtener el nombre del mes en español
                    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", 
                            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
                    nombre_mes = meses[fecha_obj.month - 1]
                    
                    # Formar la fecha para el encabezado
                    fecha_formateada = f"PESOS FISICOS DEL {nombre_dia} {fecha_obj.day} DE {nombre_mes} DE {fecha_obj.year}"
                else:
                    # Si no podemos extraer la fecha, usar la fecha actual
                    fecha_obj = datetime.date.today()
                    dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
                    nombre_dia = dias[fecha_obj.weekday()]
                    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", 
                            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
                    nombre_mes = meses[fecha_obj.month - 1]
                    fecha_formateada = f"PESOS FISICOS DEL {nombre_dia} {fecha_obj.day} DE {nombre_mes} DE {fecha_obj.year}"
            except Exception as e:
                print(f"Error al formatear fecha: {str(e)}")
                fecha_formateada = "PESOS FISICOS"
            
            # Establecer la primera línea con el formato correcto y fecha calculada
            if len(lineas) > 0:
                # Reemplazar la primera línea si ya existe una con "PESOS FÍSICOS"
                if any("PESOS F" in linea for linea in lineas[:3]):
                    for i, linea in enumerate(lineas[:3]):
                        if "PESOS F" in linea:
                            lineas[i] = fecha_formateada + "\n"
                            break
                else:
                    # Si no existe, insertarla al principio
                    lineas.insert(0, fecha_formateada + "\n")
                    
            # Recortar las líneas de separación a 125 guiones
            for i, linea in enumerate(lineas):
                if linea.strip().startswith("-"):
                    lineas[i] = "-" * 125 + "\n"
            
            # Validar el contenido con las nuevas reglas
            lineas = self.validar_contenido(lineas)
            
            # Mostrar contenido en el QTextEdit
            self.ui.txtTexto.setPlainText("".join(lineas))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo leer el archivo:\n{str(e)}")
            
    def guardar_archivo(self):
        """Guarda el contenido del TextEdit en las carpetas seleccionadas y actualiza la base de datos si es necesario"""
        # Verificar que hay un archivo seleccionado
        item = self.ui.listArchivos.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ningún archivo.")
            return
            
        # Obtener el texto
        contenido = self.ui.txtTexto.toPlainText()
        
        # Obtener el nombre nuevo
        nombre_nuevo = self.ui.lblNombreNuevo.text()
        if not nombre_nuevo:
            QMessageBox.warning(self, "Error", "No se ha generado un nuevo nombre de archivo.")
            return
        
        # Obtener el nombre original del archivo seleccionado
        nombre_original = item.text()
        
        # Verificar carpetas seleccionadas
        carpetas = {
            "Estudie": self.ui.chkEstudie.isChecked(),
            "Cátedra": self.ui.chkCatedra.isChecked(),
            "Trabajo": self.ui.chkTrabajo.isChecked(),
            "Quispe": self.ui.chkQuispe.isChecked(),
            "Dato": self.ui.chkDato.isChecked(),
        }
        
        # Determinar la codificación
        codificacion = "latin-1" if self.ui.radioANSI.isChecked() else "utf-8"
        
        # Guardar en cada carpeta seleccionada
        guardado_exitoso = False
        for nombre_carpeta, activo in carpetas.items():
            if activo:
                ruta_destino = f"/Users/oscarorellana/Proyectos/colaboradores/{nombre_carpeta}"
                os.makedirs(ruta_destino, exist_ok=True)
                ruta_archivo = os.path.join(ruta_destino, nombre_nuevo)
                
                try:
                    with open(ruta_archivo, "w", encoding=codificacion) as f:
                        f.write(contenido)
                    guardado_exitoso = True
                    
                    # Si es la carpeta Trabajo, actualizar la base de datos
                    if nombre_carpeta == "Trabajo":
                        self.actualizar_reunion_caballos(nombre_original, contenido)
                        
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error",
                        f"No se pudo guardar en {ruta_destino}:\n{str(e)}"
                    )
                    
        if guardado_exitoso:
            QMessageBox.information(self, "Guardado", "Archivo guardado correctamente en las carpetas seleccionadas.")
            
    def mostrar_menu_contextual(self, posicion):
        """Muestra un menú contextual para la lista de archivos"""
        item = self.ui.listArchivos.itemAt(posicion)
        if not item:
            return
            
        menu = QMenu(self)
        accion_vista_previa = QAction("Vista previa", self)
        accion_vista_previa.triggered.connect(lambda: self.vista_previa_archivo(item.text()))
        menu.addAction(accion_vista_previa)
        menu.exec(QCursor.pos())
        
    def vista_previa_archivo(self, nombre_archivo):
        """Muestra una vista previa del archivo en un diálogo que permite editar y guardar"""
        ruta_archivo = os.path.join(self.carpeta_originales, nombre_archivo)
        try:
            # Determinar la codificación
            codificacion = "latin-1" if self.ui.radioANSI.isChecked() else "utf-8"
            
            # Leer todo el contenido del archivo
            with open(ruta_archivo, "r", encoding=codificacion) as f:
                contenido = f.read()
                
            # Crear un diálogo personalizado para edición
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QPushButton
            from PySide6.QtGui import QFont, QShortcut, QKeySequence
            
            class VistaRapidaDialog(QDialog):
                def __init__(self, parent=None, nombre_archivo="", contenido="", ruta_archivo="", codificacion="latin-1"):
                    super().__init__(parent)
                    self.setWindowTitle(f"Vista Rápida - {nombre_archivo}")
                    self.resize(900, 700)
                    self.ruta_archivo = ruta_archivo
                    self.codificacion = codificacion
                    
                    # Crear layout vertical para todo el diálogo
                    layout = QVBoxLayout(self)
                    
                    # Editor de texto
                    self.text_edit = QPlainTextEdit(self)
                    self.text_edit.setPlainText(contenido)
                    
                    # Fuente monoespaciada
                    font = QFont("Menlo", 14)
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
                        QMessageBox.information(self, "Guardado", "Los cambios han sido guardados correctamente en el archivo original.")
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{str(e)}")
            
            # Crear y mostrar el diálogo
            dialogo = VistaRapidaDialog(
                self, 
                nombre_archivo=nombre_archivo, 
                contenido=contenido, 
                ruta_archivo=ruta_archivo,
                codificacion=codificacion
            )
            
            dialogo.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo para vista previa:\n{str(e)}")
            
    def validar_contenido(self, lineas):
        """
        Valida el contenido del archivo, verificando cada línea de caballo
        para asegurar que los datos existen en la base de datos.
        """
        fecha_principal = None
        carrera_actual = None
        referencia_actual = None
        en_carrera = False
        
        # Buscar la fecha principal del archivo
        for linea in lineas:
            if "PESOS F" in linea:
                fecha_principal = linea.strip()
                break
        
        # Recorrer todas las líneas y validar las que contienen caballos
        lineas_modificadas = lineas.copy()
        
        for i, linea in enumerate(lineas):
            # Verificar si es inicio de carrera
            if ("CARRERA" in linea and any(x in linea for x in ["PRIMERA", "SEGUNDA", "TERCERA", "CUARTA", "QUINTA"])) or linea.strip().startswith("REFERENCIA"):
                en_carrera = True
                carrera_actual = linea.strip()
                
                # Extraer número de referencia
                try:
                    match_referencia = re.search(r'REFERENCIA\s+(\d+)', linea)
                    if match_referencia:
                        referencia_actual = int(match_referencia.group(1))
                        print(f"Encontrada referencia: {referencia_actual}")
                except Exception as e:
                    print(f"Error al extraer referencia: {str(e)}")
                    pass
                continue
            
            # Si estamos en una carrera y encontramos un número al inicio, es una línea de caballo
            if en_carrera and re.match(r'^\s*\d+\s+', linea):
                # Obtener el nombre del caballo para mostrarlo en los diálogos de validación
                datos_linea = self.parsear_linea_caballo(linea)
                caballo_actual = ""
                if datos_linea:
                    caballo_actual = datos_linea["caballo"]
                
                # Agregar contexto para las validaciones (referencia y caballo)
                contexto = {
                    "referencia": referencia_actual,
                    "carrera": carrera_actual,
                    "caballo": caballo_actual
                }
                
                # Validar la línea de caballo y obtener la versión corregida
                linea_validada, cancelado = self.validar_linea_caballo(linea, contexto)
                
                # Si el usuario canceló la validación, detenemos el proceso
                if cancelado:
                    raise Exception("Proceso cancelado por el usuario")
                
                # Actualizar la línea en el arreglo
                if linea_validada:
                    lineas_modificadas[i] = linea_validada
                
                continue
                
            # Verificar líneas de separación que terminan una carrera
            if en_carrera and "----" in linea:
                en_carrera = False
                carrera_actual = None
                referencia_actual = None
        
        return lineas_modificadas
        
    def validar_linea_caballo(self, linea, contexto=None):
        """
        Valida una línea de caballo según los requerimientos.
        Retorna la línea validada y un indicador si se canceló el proceso.
        
        Args:
            linea: La línea a validar
            contexto: Diccionario con información de contexto (referencia, carrera, caballo)
        
        Posiciones fijas:
        Cajon: 1-9 (índices 0-8)
        Caballo: 10-34 (índices 9-33)
        Kilos: 35-61 (índices 34-60)
        Stud: 62-82 (índices 61-81)
        Preparador: 83-105 (índices 82-104)
        Jinete: 106-122 (índices 105-121)
        Peso: 123-125 (índices 122-124)
        """
        try:
            # Análisis detallado de la línea
            print(f"VALIDANDO LÍNEA: '{linea}'")
            print(f"LONGITUD: {len(linea)} caracteres")
            
            # Utilizar el método de parseo para extraer los campos
            datos = self.parsear_linea_caballo(linea)
            if not datos:
                return linea, False
            
            # Extraer campos del resultado de parseo
            espacios_iniciales = datos["espacios_iniciales"]
            cajon = datos["cajon"]
            caballo = datos["caballo"]  # Ya limpio sin paréntesis
            caballo_raw = datos["caballo_raw"]  # Con paréntesis si tenía
            kilos = datos["kilos"]
            stud = datos["stud"]
            preparador_jcp = datos["preparador"]
            jinete = datos["jinete"]
            peso = datos["peso"]
            
            # Mostrar campos extraídos para debug
            print(f"CAMPOS EXTRAÍDOS:")
            print(f"Espacios iniciales: '{espacios_iniciales}' (longitud: {len(espacios_iniciales)})")
            print(f"Cajón: '{cajon}'")
            print(f"Caballo (limpio): '{caballo}'")
            print(f"Caballo (original): '{caballo_raw}'")
            print(f"Kilos: '{kilos}'")
            print(f"Stud: '{stud}'")
            print(f"Preparador: '{preparador_jcp}'")
            print(f"Jinete: '{jinete}'")
            print(f"Peso: '{peso}'")
            
            # Preparar el texto de contexto para los diálogos
            info_contexto = ""
            if contexto:
                referencia = contexto.get("referencia", "")
                caballo_ctx = contexto.get("caballo", "")
                if referencia and caballo_ctx:
                    info_contexto = f" (Ref: {referencia}, Caballo: {caballo_ctx})"
            
            # 1. Validar nombre del caballo
            nombre_validado, cancelado = self.validar_caballo(caballo, info_contexto)
            if cancelado:
                return None, True
            
            # 2. Validar stud
            stud_validado, cancelado = self.validar_stud(stud, info_contexto)
            if cancelado:
                return None, True
                
            # 3. Validar preparador (usando jcp)
            preparador_validado, cancelado = self.validar_preparador(preparador_jcp, info_contexto)
            if cancelado:
                return None, True
                
            # 4. Validar peso físico
            peso_validado, cancelado = self.validar_peso(peso, info_contexto)
            if cancelado:
                return None, True
                
            # Verificar si hubo modificaciones
            modificaciones = []
            if nombre_validado != caballo:
                modificaciones.append(f"Caballo: '{caballo}' → '{nombre_validado}'")
            if stud_validado != stud:
                modificaciones.append(f"Stud: '{stud}' → '{stud_validado}'")
            if preparador_validado != preparador_jcp:
                modificaciones.append(f"Preparador: '{preparador_jcp}' → '{preparador_validado}'")
            if peso_validado != peso:
                modificaciones.append(f"Peso: '{peso}' → '{peso_validado}'")
                
            if modificaciones:
                print("⚠️ MODIFICACIONES DETECTADAS:")
                for mod in modificaciones:
                    print(f"- {mod}")
            
            # Siempre reconstruir la línea para garantizar la consistencia en el formato
            # Conservar los espacios iniciales exactos de la línea original
            nueva_linea = espacios_iniciales
            
            # Cajon: posiciones 1-9 (0-8 en Python)
            # Si no tenemos espacios iniciales, añadir el cajón con formato
            # Si ya tenemos espacios iniciales, añadir solo el número
            if len(espacios_iniciales) == 0:
                nueva_linea += f"{cajon:<9}"
            else:
                # El cajón ya tiene espacios, ajustamos para que ocupe todo el ancho
                # Primero quitamos los espacios iniciales de la longitud total
                espacio_restante = 9 - len(espacios_iniciales)
                if espacio_restante > 0:
                    nueva_linea += f"{cajon:<{espacio_restante}}"
                else:
                    nueva_linea += cajon
            
            # Caballo: posiciones 10-34 (9-33 en Python)
            nueva_linea += f"{nombre_validado:<25}"
            
            # Kilos: posiciones 35-61 (34-60 en Python)
            nueva_linea += f"{kilos:<27}"
            
            # Stud: posiciones 62-82 (61-81 en Python)
            nueva_linea += f"{stud_validado:<21}"
            
            # Preparador: posiciones 83-105 (82-104 en Python)
            nueva_linea += f"{preparador_validado:<23}"
            
            # Jinete: posiciones 106-122 (105-121 en Python)
            nueva_linea += f"{jinete:<17}"
            
            # Peso: posiciones 123-125 (122-124 en Python)
            nueva_linea += f"{peso_validado:>3}"
            
            # Asegurar salto de línea
            if not nueva_linea.endswith("\n"):
                nueva_linea += "\n"
            
            # Mostrar la línea generada para debug
            print(f"NUEVA LÍNEA: '{nueva_linea}'")
            
            return nueva_linea, False
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al validar línea: {str(e)}")
            print(f"ERROR AL VALIDAR LÍNEA: {str(e)}")
            return linea + "\n" if not linea.endswith("\n") else linea, False
    
    def validar_caballo(self, nombre_caballo, info_contexto=""):
        """
        Valida que el caballo exista en la base de datos.
        Retorna el nombre validado y un indicador si se canceló.
        
        Args:
            nombre_caballo: Nombre del caballo a validar
            info_contexto: Texto adicional para mostrar en el diálogo (referencia y caballo)
        """
        # Buscar el caballo en la base de datos
        caballo = self.session.query(Caballos).filter_by(nombre=nombre_caballo).first()
        
        # Si el caballo existe, retornar su nombre
        if caballo:
            return caballo.nombre, False
            
        # Si no existe, mostrar un diálogo para que el usuario lo corrija
        while True:
            # Mostrar diálogo con el nombre actual
            nuevo_nombre, ok = QInputDialog.getText(
                self, 
                f"Caballo no encontrado{info_contexto}", 
                f"El caballo '{nombre_caballo}' no existe en la base de datos.\nIngrese el nombre correcto:",
                text=nombre_caballo
            )
            
            if not ok:
                # El usuario canceló el diálogo
                return nombre_caballo, True
                
            # Verificar si el nuevo nombre existe
            caballo = self.session.query(Caballos).filter_by(nombre=nuevo_nombre).first()
            if caballo:
                # Si existe, retornar el nombre validado
                return caballo.nombre, False
            else:
                # Si no existe, mostrar un mensaje y volver a preguntar
                QMessageBox.warning(
                    self, 
                    f"Caballo no encontrado{info_contexto}", 
                    f"El caballo '{nuevo_nombre}' tampoco existe en la base de datos.\nPor favor, ingrese un nombre válido."
                )
    
    def validar_stud(self, nombre_stud, info_contexto=""):
        """
        Valida que el stud exista en la base de datos.
        Si está en la tabla de errores comunes, lo reemplaza.
        Retorna el nombre validado y un indicador si se canceló.
        
        Args:
            nombre_stud: Nombre del stud a validar
            info_contexto: Texto adicional para mostrar en el diálogo (referencia y caballo)
        """
        # Primero verificar si el stud existe directamente
        stud = self.session.query(Studs).filter_by(stud=nombre_stud).first()
        if stud:
            return stud.stud, False
            
        # Si no existe, buscar en la tabla de errores comunes
        error_comun = self.session.query(ErroresComunes).filter_by(texto_original=nombre_stud).first()
        if error_comun:
            # Verificar si el texto corregido existe como stud
            stud_corregido = self.session.query(Studs).filter_by(stud=error_comun.texto_corregido).first()
            if stud_corregido:
                return stud_corregido.stud, False
        
        # Si no está en errores comunes o el texto corregido no existe,
        # mostrar un diálogo para que el usuario lo corrija
        while True:
            # Mostrar diálogo con el nombre actual
            nuevo_nombre, ok = QInputDialog.getText(
                self, 
                f"Stud no encontrado{info_contexto}", 
                f"El stud '{nombre_stud}' no existe en la base de datos.\nIngrese el nombre correcto:",
                text=nombre_stud
            )
            
            if not ok:
                # El usuario canceló el diálogo
                return nombre_stud, True
                
            # Verificar si el nuevo nombre existe
            stud = self.session.query(Studs).filter_by(stud=nuevo_nombre).first()
            if stud:
                # Si existe, guardar la corrección en la tabla de errores comunes
                self.agregar_error_comun(nombre_stud, stud.stud)
                return stud.stud, False
            else:
                # Si no existe, mostrar un mensaje y volver a preguntar
                QMessageBox.warning(
                    self, 
                    f"Stud no encontrado{info_contexto}", 
                    f"El stud '{nuevo_nombre}' tampoco existe en la base de datos.\nPor favor, ingrese un nombre válido."
                )
    
    def validar_preparador(self, nombre_preparador, info_contexto=""):
        """
        Valida que el preparador exista en la base de datos.
        Si está en la tabla de errores comunes, lo reemplaza.
        Retorna el nombre validado (campo jcp) y un indicador si se canceló.
        
        Args:
            nombre_preparador: Nombre del preparador a validar
            info_contexto: Texto adicional para mostrar en el diálogo (referencia y caballo)
        """
        # Primero verificar si el preparador existe directamente
        preparador = self.session.query(Preparadores).filter_by(jcp=nombre_preparador).first()
        if preparador:
            # Devolvemos el campo jcp, NO el campo preparador
            return preparador.jcp, False
            
        # Si no existe, buscar en la tabla de errores comunes
        error_comun = self.session.query(ErroresComunes).filter_by(texto_original=nombre_preparador).first()
        if error_comun:
            # Verificar si el texto corregido existe como preparador
            preparador_corregido = self.session.query(Preparadores).filter_by(jcp=error_comun.texto_corregido).first()
            if preparador_corregido:
                # Devolvemos el campo jcp, NO el campo preparador
                return preparador_corregido.jcp, False
        
        # Si no está en errores comunes o el texto corregido no existe,
        # mostrar un diálogo para que el usuario lo corrija
        while True:
            # Mostrar diálogo con el nombre actual
            nuevo_nombre, ok = QInputDialog.getText(
                self, 
                f"Preparador no encontrado{info_contexto}", 
                f"El preparador '{nombre_preparador}' no existe en la base de datos.\nIngrese el nombre correcto:",
                text=nombre_preparador
            )
            
            if not ok:
                # El usuario canceló el diálogo
                return nombre_preparador, True
                
            # Verificar si el nuevo nombre existe
            preparador = self.session.query(Preparadores).filter_by(jcp=nuevo_nombre).first()
            if preparador:
                # Si existe, guardar la corrección en la tabla de errores comunes
                self.agregar_error_comun(nombre_preparador, preparador.jcp)
                # Devolvemos el campo jcp, NO el campo preparador
                return preparador.jcp, False
            else:
                # Si no existe, mostrar un mensaje y volver a preguntar
                QMessageBox.warning(
                    self, 
                    f"Preparador no encontrado{info_contexto}", 
                    f"El preparador '{nuevo_nombre}' tampoco existe en la base de datos.\nPor favor, ingrese un nombre válido."
                )
    
    def validar_peso(self, peso, info_contexto=""):
        """
        Valida que el peso físico esté en el rango permitido (300-560).
        Retorna el peso validado y un indicador si se canceló.
        
        Args:
            peso: Peso a validar
            info_contexto: Texto adicional para mostrar en el diálogo (referencia y caballo)
        """
        try:
            # Convertir a entero
            peso_int = int(peso)
            
            # Verificar si está en el rango permitido
            if 300 <= peso_int <= 560:
                return peso, False
                
            # Si no está en el rango, mostrar un diálogo para corregirlo
            while True:
                # Mostrar diálogo con el peso actual
                nuevo_peso, ok = QInputDialog.getText(
                    self, 
                    f"Peso físico inválido{info_contexto}", 
                    f"El peso físico '{peso}' debe estar entre 300 y 560.\nIngrese un peso válido:",
                    text=peso
                )
                
                if not ok:
                    # El usuario canceló el diálogo
                    return peso, True
                    
                try:
                    # Verificar si el nuevo peso está en el rango
                    peso_int = int(nuevo_peso)
                    if 300 <= peso_int <= 560:
                        return nuevo_peso, False
                    else:
                        # Si no está en el rango, mostrar un mensaje y volver a preguntar
                        QMessageBox.warning(
                            self, 
                            f"Peso físico inválido{info_contexto}", 
                            f"El peso físico '{nuevo_peso}' debe estar entre 300 y 560."
                        )
                except ValueError:
                    # Si no es un número, mostrar un mensaje y volver a preguntar
                    QMessageBox.warning(
                        self, 
                        f"Peso físico inválido{info_contexto}", 
                        f"El peso físico '{nuevo_peso}' debe ser un número entero."
                    )
        except ValueError:
            # Si el peso original no es un número, tratarlo como inválido
            return self.validar_peso("0", info_contexto)
    
    def agregar_error_comun(self, texto_original, texto_corregido):
        """Agrega un nuevo registro a la tabla de errores comunes."""
        try:
            # Verificar si ya existe
            error_existente = self.session.query(ErroresComunes).filter_by(texto_original=texto_original).first()
            
            if error_existente:
                # Actualizar el registro existente
                error_existente.texto_corregido = texto_corregido
            else:
                # Crear un nuevo registro
                nuevo_error = ErroresComunes(
                    texto_original=texto_original,
                    texto_corregido=texto_corregido
                )
                self.session.add(nuevo_error)
                
            # Guardar los cambios
            self.session.commit()
            
            print(f"Excepción agregada: '{texto_original}' → '{texto_corregido}'")
            
        except Exception as e:
            self.session.rollback()
            print(f"Error al agregar excepción: {str(e)}")
            
    def actualizar_reunion_caballos(self, nombre_archivo, contenido):
        """
        Actualiza la tabla ReunionCaballos con los pesos físicos y verifica cambios de Stud y Preparador.
        
        Args:
            nombre_archivo: Nombre original del archivo (PKYYYYSSW.txt)
            contenido: Contenido procesado del archivo con los pesos físicos
        """
        try:
            # Extraer la fecha del nombre del archivo
            if not nombre_archivo.startswith("PK") or len(nombre_archivo) < 9:
                QMessageBox.warning(self, "Advertencia", "No se pudo extraer la fecha del nombre del archivo.")
                return
                
            anio = int(nombre_archivo[2:6])
            semana = int(nombre_archivo[6:8])
            dia_semana = int(nombre_archivo[8:9])
            
            # Calcular la fecha usando el método específico
            fecha_obj = self.calcular_fecha_desde_nombre(anio, semana, dia_semana)
            fecha_sql = fecha_obj.strftime("%Y-%m-%d")  # Formato SQL: YYYY-MM-DD
            
            print(f"Fecha para actualización: {fecha_sql}")
            
            # Iniciar proceso de actualización
            QMessageBox.information(
                self, 
                "Actualizando BD", 
                f"Iniciando actualización de la tabla ReunionCaballos para la fecha {fecha_obj.strftime('%d/%m/%Y')}."
            )
            
            # Variables para estadísticas
            actualizados = 0
            cambios_stud = 0
            cambios_preparador = 0
            errores = 0
            
            # Parsear el contenido línea por línea
            lineas = contenido.splitlines()
            referencia_actual = None
            carrera_actual = None
            en_carrera = False
            
            for linea in lineas:
                # Verificar si es inicio de carrera
                if ("CARRERA" in linea and any(x in linea for x in ["PRIMERA", "SEGUNDA", "TERCERA", "CUARTA", "QUINTA"])) or linea.strip().startswith("REFERENCIA"):
                    en_carrera = True
                    carrera_actual = linea.strip()
                    
                    # Extraer número de referencia
                    try:
                        match_referencia = re.search(r'REFERENCIA\s+(\d+)', linea)
                        if match_referencia:
                            referencia_actual = int(match_referencia.group(1))
                            print(f"Procesando referencia: {referencia_actual}")
                    except Exception as e:
                        print(f"Error al extraer referencia: {str(e)}")
                    continue
                
                # Si estamos en una carrera y encontramos un número al inicio, es una línea de caballo
                if en_carrera and re.match(r'^\s*\d+\s+', linea) and referencia_actual:
                    try:
                        # Parsear la línea para obtener los datos del caballo
                        datos_linea = self.parsear_linea_caballo(linea)
                        if not datos_linea:
                            continue
                            
                        # Extraer los datos relevantes
                        caballo_nombre = datos_linea["caballo"]
                        stud_nombre = datos_linea["stud"]
                        preparador_nombre = datos_linea["preparador"]
                        peso_fisico = datos_linea["peso"]
                        
                        # Si el peso está vacío o no es un número, continuar con la siguiente línea
                        if not peso_fisico or not peso_fisico.isdigit():
                            continue
                            
                        # Convertir el peso a entero
                        peso_fisico_int = int(peso_fisico)
                        
                        # Obtener el idCaballo desde la tabla Caballos
                        caballo = self.session.query(Caballos).filter_by(nombre=caballo_nombre).first()
                        if not caballo:
                            print(f"Caballo no encontrado: {caballo_nombre}")
                            continue
                            
                        # Obtener el idStud desde la tabla Studs
                        stud = self.session.query(Studs).filter_by(stud=stud_nombre).first()
                        if not stud:
                            # Intentar buscar en errores comunes
                            error_comun = self.session.query(ErroresComunes).filter_by(texto_original=stud_nombre).first()
                            if error_comun:
                                stud = self.session.query(Studs).filter_by(stud=error_comun.texto_corregido).first()
                                
                        # Obtener el idPreparador desde la tabla Preparadores
                        preparador = self.session.query(Preparadores).filter_by(jcp=preparador_nombre).first()
                        if not preparador:
                            # Intentar buscar en errores comunes
                            error_comun = self.session.query(ErroresComunes).filter_by(texto_original=preparador_nombre).first()
                            if error_comun:
                                preparador = self.session.query(Preparadores).filter_by(jcp=error_comun.texto_corregido).first()
                        
                        # Buscar la entrada correspondiente en ReunionCaballos
                        
                        """
                        reunion_caballo = (
                            self.session.query(ReunionCaballos)
                            .join(ReunionCarreras, ReunionCaballos.idReunionCarrera == ReunionCarreras.idReunionCarrera)
                            .filter(
                                ReunionCarreras.fecha == fecha_sql,
                                ReunionCarreras.referencia == referencia_actual,
                                ReunionCaballos.idCaballo == caballo.idCaballo
                            )
                            .first()
                        )
                        """
                        reunion_caballo = (
                            self.session.query(ReunionCaballos)
                            .filter(
                                ReunionCaballos.fecha == fecha_sql,
                                ReunionCaballos.referencia == referencia_actual,
                                ReunionCaballos.idCaballo == caballo.idCaballo
                            )
                            .first()
                        )

                        if reunion_caballo:
                            # Actualizar el peso físico
                            reunion_caballo.pesoFisico = peso_fisico_int
                            actualizados += 1
                            
                            # Verificar cambios en Stud
                            if stud and reunion_caballo.idStud != stud.idStud:
                                stud_original = self.session.query(Studs).filter_by(idStud=reunion_caballo.idStud).first()
                                stud_original_nombre = stud_original.stud if stud_original else "Desconocido"
                                
                                print(f"Cambio de stud: {stud_original_nombre} -> {stud_nombre}")
                                reunion_caballo.idStud = stud.idStud
                                cambios_stud += 1
                                
                                # Mostrar mensaje de cambio
                                QMessageBox.information(
                                    self,
                                    "Cambio de Stud",
                                    f"Caballo: {caballo_nombre}, Ref: {referencia_actual}\n"
                                    f"Stud cambiado: {stud_original_nombre} → {stud_nombre}"
                                )
                            
                            # Verificar cambios en Preparador
                            if preparador and reunion_caballo.idPreparador != preparador.idPreparador:
                                prep_original = self.session.query(Preparadores).filter_by(idPreparador=reunion_caballo.idPreparador).first()
                                prep_original_nombre = prep_original.preparador if prep_original else "Desconocido"
                                
                                print(f"Cambio de preparador: {prep_original_nombre} -> {preparador.preparador}")
                                reunion_caballo.idPreparador = preparador.idPreparador
                                cambios_preparador += 1
                                
                                # Mostrar mensaje de cambio
                                QMessageBox.information(
                                    self,
                                    "Cambio de Preparador",
                                    f"Caballo: {caballo_nombre}, Ref: {referencia_actual}\n"
                                    f"Preparador cambiado: {prep_original_nombre} → {preparador.preparador}"
                                )
                            
                            # Commit para este caballo
                            self.session.commit()
                            
                        else:
                            print(f"No se encontró registro para {caballo_nombre} en referencia {referencia_actual}")
                    
                    except Exception as e:
                        self.session.rollback()
                        print(f"Error al procesar línea: {str(e)}")
                        errores += 1
                
                # Verificar líneas de separación que terminan una carrera
                if en_carrera and "----" in linea:
                    en_carrera = False
                    carrera_actual = None
                    referencia_actual = None
            
            # Mostrar resumen de la actualización
            if actualizados > 0 or cambios_stud > 0 or cambios_preparador > 0:
                QMessageBox.information(
                    self,
                    "Actualización Completada",
                    f"Se procesaron correctamente:\n"
                    f"- {actualizados} pesos físicos actualizados\n"
                    f"- {cambios_stud} cambios de stud\n"
                    f"- {cambios_preparador} cambios de preparador\n"
                    f"- {errores} errores durante el proceso"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Sin Actualizaciones",
                    f"No se encontraron registros para actualizar en la fecha {fecha_obj.strftime('%d/%m/%Y')}"
                )
                
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(
                self,
                "Error de Actualización",
                f"Ocurrió un error al actualizar la base de datos:\n{str(e)}"
            )
            print(f"Error general al actualizar la BD: {str(e)}")
            
    def parsear_contenido(self, lineas):
        """Analiza el contenido del archivo e identifica los datos de caballos (solo para debug)"""
        fecha_principal = None
        carrera_actual = None
        referencia_actual = None
        en_carrera = False
        
        # Buscar la fecha principal del archivo
        for linea in lineas:
            if "PESOS F" in linea:
                print(f"Encabezado: {linea.strip()}")
                fecha_principal = linea.strip()
                break
        
        # Contar estadísticas y parsear líneas de caballos
        caballos_count = 0
        carreras_count = 0
        
        # Recorrer todas las líneas
        for linea in lineas:
            # Verificar si es inicio de carrera
            if ("CARRERA" in linea and any(x in linea for x in ["PRIMERA", "SEGUNDA", "TERCERA", "CUARTA", "QUINTA"])) or linea.strip().startswith("REFERENCIA"):
                en_carrera = True
                carrera_actual = linea.strip()
                carreras_count += 1
                print(f"\n-- Carrera {carreras_count}: {carrera_actual}")
                
                # Extraer número de referencia
                try:
                    match_referencia = re.search(r'REFERENCIA\s+(\d+)', linea)
                    if match_referencia:
                        referencia_actual = int(match_referencia.group(1))
                        print(f"Referencia: {referencia_actual}")
                except:
                    print("No se pudo extraer la referencia de la carrera")
                continue
            
            # Si estamos en una carrera y encontramos un número al inicio, es una línea de caballo
            if en_carrera and re.match(r'^\s*\d+\s+', linea):
                caballos_count += 1
                self.parsear_linea_caballo(linea.rstrip())
                continue
                
            # Verificar líneas de separación que terminan una carrera
            if en_carrera and "----" in linea:
                en_carrera = False
                carrera_actual = None
                referencia_actual = None
                print("-- Fin de carrera")
                
        print(f"\nEstadísticas: {carreras_count} carreras, {caballos_count} caballos")
    
    def parsear_linea_caballo(self, linea):
        """
        Extrae información de cada línea de caballo usando posiciones fijas:
        Cajon: 1-9 (índices 0-8)
        Caballo: 10-34 (índices 9-33)
        Kilos: 35-61 (índices 34-60)
        Stud: 62-82 (índices 61-81)
        Preparador: 83-105 (índices 82-104)
        Jinete: 106-122 (índices 105-121)
        Peso: 123-125 (índices 122-124)
        """
        try:
            # Preservar los espacios iniciales exactos para mantener la alineación original
            espacios_iniciales = ""
            for c in linea:
                if c == ' ':
                    espacios_iniciales += ' '
                else:
                    break
            
            # Asegurar que la línea sea lo suficientemente larga para parsear todos los campos
            if len(linea) < 125:
                linea = linea.ljust(125)
            
            # Extraer cada campo según las posiciones fijas exactas
            cajon = linea[0:9].strip()
            caballo_raw = linea[9:34].strip()
            kilos = linea[34:61].strip()
            stud = linea[61:82].strip()
            preparador = linea[82:105].strip()
            jinete = linea[105:122].strip()
            peso = linea[122:125].strip() if len(linea) > 124 else ""
            
            # Limpiar nombre del caballo (quitar país en paréntesis)
            caballo = caballo_raw
            if "(" in caballo_raw and ")" in caballo_raw:
                inicio = caballo_raw.find("(")
                fin = caballo_raw.find(")")
                caballo = caballo_raw[:inicio].strip()
            
            # Imprimir información para depuración
            print(f"Línea: '{linea}'")
            print(f"Espacios iniciales: '{espacios_iniciales}' (longitud: {len(espacios_iniciales)})")
            print(f"Cajón: '{cajon}', Caballo: '{caballo}', Kilos: '{kilos}'")
            print(f"Stud: '{stud}', Preparador: '{preparador}', Jinete: '{jinete}', Peso: '{peso}'")
            
            return {
                "espacios_iniciales": espacios_iniciales,
                "cajon": cajon,
                "caballo": caballo,
                "caballo_raw": caballo_raw,
                "kilos": kilos,
                "stud": stud,
                "preparador": preparador,
                "jinete": jinete,
                "peso": peso
            }
            
        except Exception as e:
            print(f"Error al parsear línea: {str(e)}")
            return None
    
    def calcular_fecha_desde_nombre(self, anio, semana, dia_semana):
        """
        Calcula una fecha a partir del año, semana y día de la semana.
        
        Args:
            anio: Año (4 dígitos)
            semana: Número de semana (1-53)
            dia_semana: Día de la semana (1=lunes, 7=domingo)
            
        Returns:
            Objeto datetime.date con la fecha calculada
        """
        # Encontrar el primer día del año
        primer_dia_anio = datetime.date(anio, 1, 1)
        
        # Encontrar el primer lunes del año
        primer_dia_semana = primer_dia_anio.weekday()  # 0=lunes, 6=domingo
        dias_ajuste = primer_dia_semana  # Días hasta el lunes
        fecha_primer_lunes = primer_dia_anio - datetime.timedelta(days=dias_ajuste)
        
        # Si el primer día del año es lunes, es la semana 1
        # Si no, el primer lunes pertenece a la última semana del año anterior
        if primer_dia_semana != 0:  # Si no es lunes
            fecha_primer_lunes = fecha_primer_lunes + datetime.timedelta(weeks=1)
        
        # Calcular la fecha: primer lunes + semanas + días
        # Nota: semana-1 porque queremos 0-based para las semanas
        # dia_semana-1 porque 1=lunes, pero en timedelta 0=días
        fecha_obj = fecha_primer_lunes + datetime.timedelta(weeks=semana-1, days=dia_semana-1)
        
        return fecha_obj
    
    def generar_nombre_nuevo(self, nombre_original):
        """
        Genera un nuevo nombre basado en el nombre original.
        Si el formato es PKYYYYSSD.txt, lo convierte a:
        'Pesos Físicos YYYYSSW - Pesos físicos del DIA DD de MES de YYYY.txt'
        """
        if not nombre_original.startswith("PK"):
            return nombre_original
        
        try:
            anio = int(nombre_original[2:6])
            semana = int(nombre_original[6:8])
            dia_semana = int(nombre_original[8:9])
            
            # Calcular la fecha usando el método específico
            fecha_obj = self.calcular_fecha_desde_nombre(anio, semana, dia_semana)
            
            # Obtener día de la semana en español para el texto descriptivo
            dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            nombre_dia = dias_es[fecha_obj.weekday()]
            
            # Obtener nombre del mes en español
            meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            nombre_mes = meses_es[fecha_obj.month - 1]
            
            # Crear el identificador YYYYSSW (año+semana+día)
            # Usar la fecha original del archivo, no la calculada
            identificador = nombre_original[2:9]
            
            # Crear la descripción completa
            desc = f"Pesos físicos del {nombre_dia} {fecha_obj.day} de {nombre_mes} de {fecha_obj.year}"
            
            # Formato final: "Pesos Físicos 2024466 - Pesos físicos del Sábado 26 de Noviembre de 2024.txt"
            return f"Pesos Físicos {identificador} - {desc}.txt"
            
        except Exception as e:
            print(f"Error al generar nombre: {str(e)}")
            return nombre_original

    def cargar_ui(self):
        """Carga el archivo .ui y asigna los widgets a self.ui"""
        loader = QUiLoader()
        ui_file = QFile("core/edit_txt_pesos_fisicos/ui_pesos_fisicos.ui")  # Ruta actualizada
        
        if not ui_file.open(QFile.ReadOnly):
            error_msg = f"No se pudo abrir el archivo UI: {ui_file.errorString()}"
            print(error_msg)  # Mostrar el error en la consola
            QtWidgets.QMessageBox.critical(self, "Error", error_msg)  # Mostrar un mensaje de error
            return
        
        self.ui = loader.load(ui_file, self)  # Cargar la interfaz
        ui_file.close()
        
        if not self.ui:
            error_msg = "Error al cargar la interfaz desde el archivo .ui"
            print(error_msg)  # Mostrar el error en la consola
            QtWidgets.QMessageBox.critical(self, "Error", error_msg)  # Mostrar un mensaje de error
            return
        
        # Desactivar el "word wrap" en el QTextEdit
        self.ui.txtTexto.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        
        # Asignar la interfaz cargada como el layout de este widget
        self.setLayout(self.ui.layout())

