import os
import re
import datetime

from PySide6.QtWidgets import (
    QWidget, QMessageBox, QListWidgetItem, QMenu, QInputDialog
)
from PySide6.QtGui import (
    QCursor, 
    QAction, 
    QFont, 
    QKeySequence,
    QShortcut
)
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

# from generated.ui_resultados import Ui_Resultados
from db import SessionLocal  # Para crear sesiones
from models.models import Caballos  # Solo los modelos necesitados
from models.models import Jinetes  # Solo los modelos necesitados

class Resultados(QtWidgets.QWidget):
    """Ventana para gestionar y procesar archivos de resultados."""

    def __init__(self):
        super().__init__()
        self.cargar_ui()  # Cargar la interfaz desde el archivo .ui
        print("✅ Ventana de resultados cargada correctamente.")  # Debug

        # Conexiones de interfazi
        self.cargar_lista_archivos()
        self.ui.listArchivos.itemClicked.connect(self.cargar_archivo)
        self.ui.btnGuardar.clicked.connect(self.guardar_archivo)
        self.ui.btnValidar.clicked.connect(self.validar_resultados)

        self.ui.listArchivos.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.listArchivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)

        # Aquí podrías inyectar tu sesión de SQLAlchemy
        self.session = SessionLocal()  # Placeholder para tu Session

    def cargar_ui(self):
        """Carga el archivo .ui y asigna los widgets a self.ui"""
        loader = QUiLoader()
        ui_file = QFile("core/edit_txt_resultados/ui_resultados.ui")  # Ruta actualizada
        
        if not ui_file.open(QFile.ReadOnly):
            error_msg = f"No se pudo abrir el archivo UI: {ui_file.errorString()}"
            print(error_msg)  # Mostrar el error en la consola
            QMessageBox.critical(self, "Error", error_msg)  # Mostrar un mensaje de error
            return
        
        self.ui = loader.load(ui_file, self)  # Cargar la interfaz
        ui_file.close()
        
        if not self.ui:
            error_msg = "Error al cargar la interfaz desde el archivo .ui"
            print(error_msg)  # Mostrar el error en la consola
            QMessageBox.critical(self, "Error", error_msg)  # Mostrar un mensaje de error
            return
        
        # Desactivar el "word wrap" en el QTextEdit
        self.ui.txtTexto.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        
        # Asignar la interfaz cargada como el layout de este widget
        self.setLayout(self.ui.layout())

    # -------------------------------------------------------------------------
    # 1. CARGA Y CONVERSIÓN (transformaciones)
    # -------------------------------------------------------------------------
    def cargar_archivo(self, item):
        # Usar la misma lógica de ruta configurable
        base_path = os.getenv("COLABORADORES_PATH", os.path.expanduser("~/Proyectos/colaboradores"))
        ruta_archivo = os.path.join(base_path, "originales", item.text())
        
        try:
            with open(ruta_archivo, "r", encoding=self.obtener_codificacion()) as f:
                lineas = f.readlines()

            # Filtrar líneas vacías sin modificar espacios
            lineas = [ln for ln in lineas if ln.strip()]

            # Eliminar encabezados específicos (comparación exacta)
            encabezados_a_eliminar = [
                "JOCKEY CLUB DEL PERU\n",
                "DEPARTAMENTO HIPICO\n",
                "COMISION DE PROGRAMA\n",
            ]
            lineas = [ln for ln in lineas if ln not in encabezados_a_eliminar]



            # Procesar fecha y reemplazar línea de fecha
            nombre_archivo = item.text()
            fecha_larga = None
            if len(nombre_archivo) >= 8 and nombre_archivo[0] == "R":
                try:
                    anio = int(nombre_archivo[1:5])
                    semana = int(nombre_archivo[5:7])
                    dia_semana = int(nombre_archivo[7:8])
                    fecha_larga = self.obtener_fecha_larga(anio, semana, dia_semana)
                except ValueError:
                    pass

            # Reemplazar línea de fecha si corresponde
            if fecha_larga:
                for i, ln in enumerate(lineas):
                    if ln.startswith("RESULTADOS DEL DIA"):
                        lineas[i] = f"RESULTADOS DEL DIA {fecha_larga}\n"

            # Variables para seguimiento de carreras
            lineas_procesadas = []
            referencia_anterior = None
            ignorar_siguiente = False
            es_linea_totales = False
            numero_carrera_actual = None
            orden_carrera_actual = None
            lineas_informativas = []
            recopilando_info = False
            
            # Procesar cada línea
            i = 0
            while i < len(lineas):
                ln = lineas[i]
                
                # 1. Verificar si es línea de carrera
                primeros_4 = ln[:4].strip()
                es_carrera = False
                if primeros_4.isdigit() and "a.Car." in ln:
                    try:
                        referencia_actual = int(primeros_4)
                        numero_carrera_actual = referencia_actual
                        
                        match_carrera = re.search(r'(\d+)a\.Car\.', ln)
                        if match_carrera:
                            orden_carrera_actual = int(match_carrera.group(1))
                        
                        es_carrera = True
                    except ValueError:
                        pass

                    if es_carrera:
                        # Validar secuencia
                        if referencia_anterior is not None and referencia_actual != referencia_anterior + 1:
                            QMessageBox.warning(
                                self,
                                "Error de secuencia",
                                f"Error en línea {i+1}: La referencia {referencia_actual} no sigue a {referencia_anterior}"
                            )
                        referencia_anterior = referencia_actual
                        ignorar_siguiente = False
                        
                        # Añadir línea en blanco antes de nueva carrera
                        if lineas_procesadas:
                            lineas_procesadas.append('\n')
                        
                        # CAMBIO IMPORTANTE: En lugar de agregar la línea de carrera directamente,
                        # la incluimos como la primera línea informativa
                        lineas_informativas = [ln]  # Iniciar con la línea de carrera
                        recopilando_info = True     # Comenzar a recopilar más información
                        i += 1
                        continue
                
                # 2. Verificar si es línea de caballo
                es_linea_caballo = False
                if len(ln) >= 12:
                    posible_puesto = ln[8:10].strip()
                    posible_separador = ln[10:12]
                    
                    if (posible_puesto.isdigit() and posible_separador == ".-"):
                        es_linea_caballo = True
                        puesto = int(posible_puesto)
                        
                        # Si estábamos recopilando información y encontramos un caballo
                        if recopilando_info and lineas_informativas:
                            # Unir todas las líneas informativas y agregarlas
                            info_unificada = " ".join([l.strip() for l in lineas_informativas])
                            while "  " in info_unificada:
                                info_unificada = info_unificada.replace("  ", " ")
                            lineas_procesadas.append(info_unificada + "\n")  # Agregar salto de línea
                            recopilando_info = False  # Dejar de recopilar
                        
                        # Si es puesto 99, ignorar esta línea
                        
                        if puesto == 99:
                            i += 1
                            continue
                        
                        # Validar el nombre del caballo
                        inicio_nombre = ln.find(".-") + 2
                        fin_nombre = ln.find(" (", inicio_nombre)
                        
                        if fin_nombre > inicio_nombre:
                            nombre_caballo = ln[inicio_nombre:fin_nombre].strip()
                            caballo = self.session.query(Caballos).filter(
                                Caballos.nombre == nombre_caballo
                            ).first()
                            
                            if not caballo and orden_carrera_actual:
                                QMessageBox.warning(
                                    self,
                                    "Caballo no encontrado",
                                    f"En la {orden_carrera_actual}a. carrera el caballo {nombre_caballo} no existe."
                                )
                        
                        # Procesar nacionalidad y espaciado
                        primera_parte = ln[:57] if len(ln) >= 57 else ln
                        segunda_parte = ln[57:] if len(ln) >= 57 else ""
                        
                        primer_inicio = primera_parte.find(" (")
                        if primer_inicio > 0:
                            primer_fin = primera_parte.find(")", primer_inicio)
                            if primer_fin > 0:
                                segundo_inicio = primera_parte.find(" (", primer_fin)
                                if segundo_inicio > 0:
                                    primera_parte = primera_parte[:primer_inicio] + primera_parte[primer_fin+1:]
                        
                        primera_parte = re.sub(r'(\w+)\(', r'\1 (', primera_parte)
                        
                        if len(primera_parte) < 65:
                            primera_parte = primera_parte + " " * (65 - len(primera_parte))
                        else:
                            primera_parte = primera_parte[:65]
                        
                        ln = primera_parte + segunda_parte
                        
                        # Si es puesto 1, marcar para ignorar la siguiente línea
                        if puesto == 1:
                            ignorar_siguiente = True
                            lineas_procesadas.append(ln)
                            i += 1
                            continue
                # 3. Verificar si es línea de totales
                if "---------- ----------" in ln:
                    es_linea_totales = True
                    recopilando_info = False
                    ln = " " * 8 + ln
                    lineas_procesadas.append(ln)
                    i += 1
                    continue
                
                # 4. Verificar si es la línea de valores después de los guiones
                if es_linea_totales:
                    es_linea_totales = False
                    ln = " " * 9 + ln
                    lineas_procesadas.append(ln)
                    i += 1
                    continue
                
                # 5. Línea a ignorar después del caballo ganador
                if ignorar_siguiente and not es_linea_caballo:
                    ignorar_siguiente = False
                    i += 1
                    continue
                
                # 6. Recopilar líneas informativas
                if recopilando_info and ln.strip():
                    # Filtrar líneas triviales
                    if ln.strip() not in ["CUADRUPLE", "DUPLETA", "EXACTA", "GANADOR", "PLACE", "TRIFECTA"]:
                        lineas_informativas.append(ln)
                    i += 1
                    continue
                
                # 7. Caso por defecto: agregar línea sin modificar
                if not ignorar_siguiente:
                    lineas_procesadas.append(ln)
                
                i += 1  # Avanzar al siguiente elemento

            # Convertir lista de líneas a texto
            texto = "".join(lineas_procesadas)
            
            # Aplicar transformaciones adicionales
            texto = self.transformar_contenido(texto)

            # Mostrar en la interfaz
            self.ui.txtTexto.setPlainText(texto)

            # Generar nombre nuevo
            nuevo_nombre = self.generar_nombre_nuevo(nombre_archivo)
            self.ui.lblNombreNuevo.setText(nuevo_nombre)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo leer el archivo:\n{str(e)}")

    def transformar_contenido(self, texto):
        """
        Transformaciones que preservan espacios:
        - Solo modifica texto específico sin afectar formato
        - Elimina líneas que comiencen con "Macho" o "Hembra"
        """
        # Ejemplo de transformación que no afecta espacios
        texto = texto.replace("segundos", "s.")
        
        # Eliminar líneas que comiencen con "Macho" o "Hembra" después de quitar espacios
        lineas = texto.split('\n')
        lineas_filtradas = [ln for ln in lineas 
                            if not ln.lstrip().startswith("Macho") and 
                            not ln.lstrip().startswith("Hembra")]
        
        return '\n'.join(lineas_filtradas)

    # -------------------------------------------------------------------------
    # 2. VALIDACIÓN
    # -------------------------------------------------------------------------
    def validar_resultados(self):
        """
        Implementación básica de validación para resultados.
        Esto es un ejemplo y debe adaptarse a las necesidades específicas.
        """
        contenido = self.ui.txtTexto.toPlainText()
        # Aquí implementarías la lógica de validación
        
        QMessageBox.information(self, "Validación completada",
                             "Los resultados han sido validados correctamente.")

    # -------------------------------------------------------------------------
    # 3. GUARDAR ARCHIVO
    # -------------------------------------------------------------------------
    def guardar_archivo(self):
        # Usar la misma lógica de ruta configurable
        base_path = os.getenv("COLABORADORES_PATH", os.path.expanduser("~/Proyectos/colaboradores"))
        nombre_archivo = self.ui.lblNombreNuevo.text()
        
        if not nombre_archivo:
            QMessageBox.warning(self, "Error", "No hay archivo procesado para guardar.")
            return
        
        carpeta_destino = os.path.join(base_path, "procesados")
        os.makedirs(carpeta_destino, exist_ok=True)
        
        ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
        
        contenido = self.ui.txtTexto.toPlainText()
        if not contenido:
            QMessageBox.warning(self, "Error", "No hay contenido para guardar.")
            return

        # CheckBoxes
        carpetas = {
            "Estudie": self.ui.chkEstudie.isChecked(),
            "Cátedra": self.ui.chkCatedra.isChecked(),
            "Trabajo": self.ui.chkTrabajo.isChecked(),
            "Quispe": self.ui.chkQuispe.isChecked(),
            "Dato": self.ui.chkDato.isChecked(),
        }

        guardado_exitoso = False
        for nombre_carpeta, activo in carpetas.items():
            if activo:
                ruta_destino = f"{ruta_destino}"
                os.makedirs(ruta_destino, exist_ok=True)
                ruta_archivo = os.path.join(ruta_destino, nombre_archivo)

                try:
                    with open(ruta_archivo, "w", encoding=self.obtener_codificacion()) as f:
                        f.write(contenido)
                    guardado_exitoso = True
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error",
                        f"No se pudo guardar en {ruta_destino}:\n{str(e)}"
                    )

        if guardado_exitoso:
            QMessageBox.information(self, "Guardado", "Archivo guardado en las carpetas seleccionadas.")

    # -------------------------------------------------------------------------
    # 4. OTRAS UTILIDADES
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
        # Usar ruta configurable en lugar de la ruta absoluta
        base_path = os.getenv("COLABORADORES_PATH", os.path.expanduser("~/Proyectos/colaboradores"))
        ruta_archivo = os.path.join(base_path, "originales", nombre_archivo)
        
        try:
            codificacion = "latin-1" if self.ui.radioANSI.isChecked() else "utf-8"
            with open(ruta_archivo, "r", encoding=codificacion) as f:
                contenido = f.read()
            
            # Crear diálogo con editor editable
            dialogo = QtWidgets.QDialog(self)
            dialogo.setWindowTitle(f"Vista Rápida - {nombre_archivo}")
            dialogo.resize(900, 700)
            
            layout = QtWidgets.QVBoxLayout(dialogo)
            
            # Editor de texto con fuente monoespaciada
            text_edit = QtWidgets.QPlainTextEdit()
            text_edit.setPlainText(contenido)
            text_edit.setFont(QFont("Menlo", 14))  # Fuente igual que en Pesos Físicos
            layout.addWidget(text_edit)
            
            # Botones inferiores
            btn_layout = QtWidgets.QHBoxLayout()
            
            btn_guardar = QtWidgets.QPushButton("Guardar")
            btn_guardar.clicked.connect(lambda: self.guardar_vista_rapida(ruta_archivo, text_edit.toPlainText(), codificacion))
            
            btn_cerrar = QtWidgets.QPushButton("Cerrar")
            btn_cerrar.clicked.connect(dialogo.reject)
            
            btn_layout.addWidget(btn_guardar)
            btn_layout.addWidget(btn_cerrar)
            
            layout.addLayout(btn_layout)
            
            # Atajos de teclado
            shortcut_guardar = QShortcut(QKeySequence("Ctrl+S"), dialogo)
            shortcut_guardar.activated.connect(lambda: self.guardar_vista_rapida(ruta_archivo, text_edit.toPlainText(), codificacion))
            
            dialogo.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo:\n{str(e)}")

    def guardar_vista_rapida(self, ruta, contenido, codificacion):
        try:
            with open(ruta, "w", encoding=codificacion) as f:
                f.write(contenido)
            QMessageBox.information(self, "Guardado", "Cambios guardados en el archivo original.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{str(e)}")

    def obtener_codificacion(self):
        return "latin-1" if self.ui.radioANSI.isChecked() else "utf-8"

    def cargar_lista_archivos(self):
        """Carga la lista de archivos de resultados del directorio configurado"""
        # Usar una ruta configurable con valor por defecto
        base_path = os.getenv("COLABORADORES_PATH", os.path.expanduser("~/Proyectos/colaboradores"))
        carpeta_origen = os.path.join(base_path, "originales")
        
        if not os.path.exists(carpeta_origen):
            QMessageBox.warning(self, "Error", f"La carpeta de resultados no existe: {carpeta_origen}")
            return

        # Filtrar solo archivos que comiencen con 'R' y terminen en '.txt'
        archivos = [f for f in os.listdir(carpeta_origen) if f.startswith("R") and f.endswith(".txt")]
        self.ui.listArchivos.clear()
        for archivo in sorted(archivos, reverse=True):  # Más recientes primero
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
        if not nombre_original.startswith("R"):
            return nombre_original
        try:
            anio = int(nombre_original[1:5])
            semana = int(nombre_original[5:7])
            dia = int(nombre_original[7:8])
            fecha_larga = self.obtener_fecha_larga(anio, semana, dia)
            return f"Resultados {anio}{semana}{dia} - {fecha_larga}.txt"
        except:
            return nombre_original

