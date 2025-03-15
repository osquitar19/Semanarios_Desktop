import os
import re
import datetime

from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QWidget, QMessageBox, QInputDialog, QListWidgetItem, QMenu,
    QAction, QPlainTextEdit, QDialog
)
from PySide6.QtGui import QCursor
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader

# Ejemplo de modelo
# from data.models import Caballos, Jinetes

class AprontesWidget(QWidget):
    def __init__(self, session=None, parent=None):
        super().__init__(parent)
        self.session = session

        # 1) Cargar el archivo UI
        loader = QUiLoader()
        ui_file_path = os.path.join(os.path.dirname(__file__), "ui_aprontes.ui")
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QIODevice.ReadOnly):
            raise IOError(f"No se puede abrir {ui_file_path}: {ui_file.errorString()}")

        self.ui = loader.load(ui_file, self)  # 'self' como padre
        ui_file.close()

        # 2) Ajustar layout principal
        #    Hacemos que "self.ui" sea el layout interno en este QWidget
        #    Podríamos hacer un layout, o directamente un setLayout si la raíz
        #    del .ui era un QWidget con layouts.
        #    Para simplificar, si self.ui no es QMainWindow, asignamos a layout:
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.ui)

        # 3) Conectar señales
        self.ui.btnCerrar.clicked.connect(self.close)
        self.ui.btnGuardar.clicked.connect(self.guardar_archivo)
        self.ui.btnValidar.clicked.connect(self.validar_aprontes)
        self.ui.listArchivos.itemClicked.connect(self.cargar_archivo_seleccionado)
        self.ui.listArchivos.setContextMenuPolicy(QtWidgets.Qt.CustomContextMenu)
        self.ui.listArchivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)

        # 4) Invocar lo que quieras al iniciar
        self.cargar_lista_archivos()
        self.ui.lblNombreNuevo.setText("")

    def cargar_archivo_seleccionado(self, item):
        """Carga el contenido del archivo seleccionado en txtTexto
           y genera un nombre nuevo sugerido."""
        carpeta = "/Users/oscarorellana/Proyectos/colaboradores/originales"
        ruta = os.path.join(carpeta, item.text())
        try:
            with open(ruta, "r", encoding=self.obtener_codificacion()) as f:
                contenido = f.read()
            self.ui.txtTexto.setPlainText(contenido)
            # Generar nombre nuevo
            nombre_nuevo = self.generar_nombre_nuevo(item.text())
            self.ui.lblNombreNuevo.setText(nombre_nuevo)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo:\n{str(e)}")

    def validar_aprontes(self):
        lineas = self.ui.txtTexto.toPlainText().splitlines()
        lineas_modificadas = []
        i = 0
        while i < len(lineas):
            linea = lineas[i]
            ok, linea_corregida, msg_error = self.validar_linea_apronte(linea)

            if ok:
                # Aceptamos y guardamos
                lineas_modificadas.append(linea_corregida)
                i += 1
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
                    linea_editada, ok2 = QInputDialog.getMultiLineText(
                        self,
                        "Editar línea",
                        "Corrige la línea para que cumpla el formato:",
                        linea
                    )
                    if not ok2:
                        # Si cierra o cancela el InputDialog => volvemos al mismo prompt
                        continue
                    # Reintentar validación con la línea corregida
                    linea = linea_editada
                    continue

                elif resp == QMessageBox.No:
                    # Omitir la línea
                    lineas_modificadas.append(f"# LÍNEA OMITIDA: {linea}")
                    i += 1
                else:
                    # Cancel => abortar toda la validación
                    QMessageBox.information(self, "Validación cancelada", "Se interrumpió la validación.")
                    return

        # Si salimos del bucle, todas las líneas se validaron u omitieron
        texto_final = "\n".join(lineas_modificadas)
        self.ui.txtTexto.setPlainText(texto_final)
        QMessageBox.information(self, "Validación completada",
                                "Las líneas han sido validadas u omitidas.")

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
            # Reemplazamos en la línea...
            linea = linea.replace(caballo, caballo_final, 1)
            caballo = caballo_final

        # 3) Jinete
        jinete_existe, jinete_final = self.verificar_jinete(jinete)
        if not jinete_existe:
            linea = linea.replace(jinete, jinete_final, 1)
            jinete = jinete_final

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

        caballo   = m.group('caballo').strip()
        jinete    = m.group('jinete').strip()
        dist1_str = m.group('dist1')
        t1_str    = m.group('tiempo1')
        dist2_str = m.group('dist2') or ""
        t2_str    = m.group('tiempo2') or ""
        resto     = m.group('resto').strip()

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
        patrones = [
            re.compile(r'^(\\d+)[\\\' ](\\d+)"(\\d+)$'),      # 1'12"3
            re.compile(r'^(\\d+)[\\\' ](\\d+)\\\'\\\'(\\d+)$'), # 1'12''3
        ]
        for pat in patrones:
            m = pat.match(t_str.strip())
            if m:
                minutos = int(m.group(1))
                segundos = int(m.group(2))
                quintos = int(m.group(3))
                total_s = minutos*60 + segundos + quintos*0.2
                return int(round(total_s*5))

        # Fallback: intenta float
        try:
            flotante = float(t_str.replace('"', '').replace("'", ""))
            return int(round(flotante*5))
        except:
            return None

    # -----------------------
    #  VERIFICACIÓN EN BD
    # -----------------------
    def verificar_caballo(self, nombre_caballo):
        c = self.buscar_caballo_por_nombre(nombre_caballo)
        if c:
            return True, nombre_caballo

        msg = (
            f"El caballo '{nombre_caballo}' no se encuentra.\\n"
            "¿Deseas corregir el nombre (Sí) o declararlo debutante (No)?\\n"
            "Cancelar interrumpe la validación."
        )
        resp = QMessageBox.question(
            self, "Caballo no encontrado", msg,
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if resp == QMessageBox.Cancel:
            return False, ""

        elif resp == QMessageBox.Yes:
            nuevo, ok = QInputDialog.getText(
                self, "Corregir caballo",
                "Nuevo nombre del caballo:",
                text=nombre_caballo
            )
            if not ok or not nuevo.strip():
                return False, ""
            c2 = self.buscar_caballo_por_nombre(nuevo.strip())
            if c2:
                return True, nuevo.strip()
            else:
                return False, ""
        else:
            # Debutante
            datos_debut = self.dialogo_nuevo_caballo(nombre_caballo)
            if not datos_debut:
                return False, ""
            return False, datos_debut["nombre"]

    def dialogo_nuevo_caballo(self, nombre_caballo):
        minus_default = self.capitalizar_nombre(nombre_caballo)
        breve_default = minus_default
        marcador_default = minus_default

        minus_, ok = QInputDialog.getText(
            self, "Caballo debutante: minusculas",
            "Nombre en minúsculas:",
            text=minus_default
        )
        if not ok or not minus_.strip():
            return None
        breve_, ok = QInputDialog.getText(
            self, "Caballo debutante: breve",
            "Nombre abreviado:",
            text=breve_default
        )
        if not ok or not breve_.strip():
            return None
        marcador_, ok = QInputDialog.getText(
            self, "Caballo debutante: marcador",
            "Nombre marcador:",
            text=marcador_default
        )
        if not ok or not marcador_.strip():
            return None

        return {
            "nombre": nombre_caballo,
            "minusculas": minus_.strip(),
            "breve": breve_.strip(),
            "marcadorStart": marcador_.strip()
        }

    def verificar_jinete(self, jcp):
        j = self.buscar_jinete_por_jcp(jcp)
        if j:
            return True, jcp

        sugerido = self.capitalizar_nombre(jcp)
        nuevo, ok = QInputDialog.getText(
            self, "Jinete no encontrado",
            "Editar nombre del jinete:",
            text=sugerido
        )
        if not ok or not nuevo.strip():
            return False, jcp
        return False, nuevo.strip()

    def capitalizar_nombre(self, texto):
        palabras = texto.lower().split()
        return " ".join(p.capitalize() for p in palabras)

    def buscar_caballo_por_nombre(self, nombre):
        if not self.session:
            return None
        # Ejemplo: return self.session.query(Caballos).filter_by(nombre=nombre).one_or_none()
        return None

    def buscar_jinete_por_jcp(self, jcp):
        if not self.session:
            return None
        # Ejemplo: return self.session.query(Jinetes).filter_by(jcp=jcp).one_or_none()
        return None

    # -----------------------
    #  GUARDAR ARCHIVO
    # -----------------------
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

        carpetas = {
            "Estudie": self.ui.chkEstudie.isChecked(),
            "Cátedra": self.ui.chkCatedra.isChecked(),
            "Trabajo": self.ui.chkTrabajo.isChecked(),
            "Quispe":  self.ui.chkQuispe.isChecked(),
            "Dato":    self.ui.chkDato.isChecked(),
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

    # -----------------------
    #  OTRAS UTILIDADES
    # -----------------------
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