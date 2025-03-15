import os
import re
import datetime

from PySide6.QtWidgets import (
    QWidget, QMessageBox, QListWidgetItem, QMenu, QInputDialog
)
from PySide6.QtGui import QCursor, QAction
from PySide6 import QtCore, QtWidgets

from generated.ui_programas import Ui_Programas
from db import SessionLocal  # Para crear sesiones
from models.models import Caballos  # Solo los modelos necesitados
from models.models import Jinetes  # Solo los modelos necesitados

class Programas(QWidget):
    """Ventana para gestionar y procesar archivos de programas."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_Programas()
        self.ui.setupUi(self)

        # Conexiones de interfaz
        self.cargar_lista_archivos()
        self.ui.listArchivos.itemClicked.connect(self.cargar_archivo)
        self.ui.btnGuardar.clicked.connect(self.guardar_archivo)
        self.ui.btnValidar.clicked.connect(self.validar_programas)

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
            if len(nombre_archivo) >= 8 and nombre_archivo[0] == "P":
                # Ej: P20231231.txt => P + año(4) + semana(2) + dia(1)
                anio = int(nombre_archivo[1:5])
                semana = int(nombre_archivo[5:7])
                dia_semana = int(nombre_archivo[7:8])
                fecha_larga = self.obtener_fecha_larga(anio, semana, dia_semana)

            # Reemplazar la línea "PROGRAMAS DEL DIA ..." con la fecha nueva (si existe)
            if fecha_larga:
                for i, ln in enumerate(lineas):
                    if ln.startswith("PROGRAMAS DEL DIA"):
                        lineas[i] = f"PROGRAMAS DEL DIA {fecha_larga}"

            # Unir en un texto único y aplicar transformaciones
            texto = "\n".join(lineas)
            texto = self.transformar_contenido(texto)

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
        Aplica transformaciones específicas para programas:
         - abreviaciones
         - formateo de texto
         - otras transformaciones requeridas
        """
        # Aquí deberías implementar las transformaciones específicas para programas
        # Como ejemplo, aplicamos solo una función simple
        texto = self.aplicar_abreviaciones(texto)
        return texto

    def aplicar_abreviaciones(self, texto):
        ABREVIACIONES = {
            # Aquí se pueden definir abreviaciones específicas para programas
            "metros": "m.",
            "kilogramos": "kg.",
            ",": " , "
        }
        for clave in sorted(ABREVIACIONES, key=len, reverse=True):
            texto = texto.replace(clave, ABREVIACIONES[clave])
        return texto

    # -------------------------------------------------------------------------
    # 2. VALIDACIÓN
    # -------------------------------------------------------------------------
    def validar_programas(self):
        """
        Implementación básica de validación para programas.
        Esto es un ejemplo y debe adaptarse a las necesidades específicas.
        """
        contenido = self.ui.txtTexto.toPlainText()
        # Aquí implementarías la lógica de validación
        
        QMessageBox.information(self, "Validación completada",
                             "Los programas han sido validados correctamente.")

    # -------------------------------------------------------------------------
    # 3. GUARDAR ARCHIVO
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

        guardado_exitoso = False
        for nombre_carpeta, activo in carpetas.items():
            if activo:
                ruta_destino = f"/Users/oscarorellana/Proyectos/colaboradores/{nombre_carpeta}"
                os.makedirs(ruta_destino, exist_ok=True)
                ruta_archivo = os.path.join(ruta_destino, nombre_nuevo)

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
        ruta_archivo = os.path.join("/Users/oscarorellana/Proyectos/colaboradores/originales", nombre_archivo)
        try:
            with open(ruta_archivo, "r", encoding=self.obtener_codificacion()) as f:
                contenido = f.read()
            dialogo = QtWidgets.QDialog(self)
            dialogo.setWindowTitle(f"Vista Rápida - {nombre_archivo}")
            dialogo.resize(600, 400)

            text_edit = QtWidgets.QPlainTextEdit(dialogo)
            text_edit.setPlainText(contenido)
            text_edit.setReadOnly(True)
            text_edit.setGeometry(10, 10, 580, 380)

            dialogo.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo:\n{str(e)}")

    def obtener_codificacion(self):
        return "latin-1" if self.ui.radioANSI.isChecked() else "utf-8"

    def cargar_lista_archivos(self):
        carpeta_origen = "/Users/oscarorellana/Proyectos/colaboradores/originales"
        if not os.path.exists(carpeta_origen):
            QMessageBox.warning(self, "Error", "La carpeta de programas no existe.")
            return

        # Filtramos archivos que empiezan con P pero no con PK para evitar mostrar archivos de pesos físicos
        archivos = [f for f in os.listdir(carpeta_origen) if f.startswith("P") and not f.startswith("PK") and f.endswith(".txt")]
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
        if not nombre_original.startswith("P"):
            return nombre_original
        try:
            anio = int(nombre_original[1:5])
            semana = int(nombre_original[5:7])
            dia = int(nombre_original[7:8])
            fecha_larga = self.obtener_fecha_larga(anio, semana, dia)
            return f"Programas {anio}{semana}{dia} - {fecha_larga}.txt"
        except:
            return nombre_original