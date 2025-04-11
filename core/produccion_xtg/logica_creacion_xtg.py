import os
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from db import SessionLocal
# Importar los módulos de generación de contenido
from core.produccion_xtg.xtg_prueba import generar_contenido_prueba
from core.produccion_xtg.xtg_estudie import generar_contenido_estudie

class CreacionXTG(QtWidgets.QWidget):
    """
    Ventana para crear archivos XTG.
    
    Esta implementación utiliza un enfoque modular procedimental,
    delegando la generación de contenido a módulos específicos para
    cada tipo de formato.
    """

    def __init__(self):
        super().__init__()
        self.cargar_ui()
        print("✅ Ventana de creación de XTG cargada correctamente.")

    def cargar_ui(self):
        """Carga el archivo .ui y asigna los widgets a self.ui"""
        loader = QUiLoader()
        ui_file = QFile("core/produccion_xtg/ui_creacion_xtg.ui")
        
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
        
        # Asignar la interfaz cargada como el layout de este widget
        self.setLayout(self.ui.layout())

        # Conexiones de interfaz
        self.ui.btnEstudie.clicked.connect(self.on_btnEstudie_clicked)
        self.ui.btnStart.clicked.connect(self.on_btnStart_clicked)
        self.ui.btnBurrero.clicked.connect(self.on_btnBurrero_clicked)
        self.ui.btnDato.clicked.connect(self.on_btnDato_clicked)
        self.ui.btnPrueba.clicked.connect(self.on_btnPrueba_clicked)

    # -------------------------------------------------------------------------
    # Métodos para manejar los botones
    # -------------------------------------------------------------------------
    def on_btnEstudie_clicked(self):
        """Maneja el clic en el botón 'Estudie su Polla'"""
        print("Botón 'Estudie su Polla' presionado")
        
        try:
            # Generar contenido usando el módulo xtg_estudie
            contenido = generar_contenido_estudie()
            self.ui.txtTexto.setPlainText(contenido)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar XTG Estudie: {str(e)}")
            print(f"❌ Error: {str(e)}")

    def on_btnStart_clicked(self):
        """Maneja el clic en el botón 'Start'"""
        print("Botón 'Start' presionado")
        QMessageBox.information(self, "Información", "Función no implementada aún")

    def on_btnBurrero_clicked(self):
        """Maneja el clic en el botón 'Burrero'"""
        print("Botón 'Burrero' presionado")
        QMessageBox.information(self, "Información", "Función no implementada aún")

    def on_btnDato_clicked(self):
        """Maneja el clic en el botón 'Dato'"""
        print("Botón 'Dato' presionado")
        QMessageBox.information(self, "Información", "Función no implementada aún")

    def on_btnPrueba_clicked(self):
        """Maneja el clic en el botón 'Prueba'"""
        print("Botón 'Prueba' presionado")
        
        try:
            # Generar contenido usando el módulo xtg_prueba
            contenido = generar_contenido_prueba()
            self.ui.txtTexto.setPlainText(contenido)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar XTG Prueba: {str(e)}")
            print(f"❌ Error: {str(e)}")
    