import sys
import os
import shutil
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QDir

class UIConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de UI a PY")
        self.setGeometry(100, 100, 500, 400)
        
        self.initUI()
    
    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        
        # Lista de archivos .ui
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        layout.addWidget(self.listWidget)
        
        # Botón para actualizar lista
        self.btnActualizar = QtWidgets.QPushButton("Actualizar lista")
        self.btnActualizar.clicked.connect(self.listar_archivos_ui)
        layout.addWidget(self.btnActualizar)
        
        # Botón para convertir
        self.btnConvertir = QtWidgets.QPushButton("Convertir seleccionados")
        self.btnConvertir.clicked.connect(self.convertir_seleccionados)
        layout.addWidget(self.btnConvertir)
        
        # Widget central
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        
        # Cargar archivos inicialmente
        self.listar_archivos_ui()
    
    def listar_archivos_ui(self):
        """Lista los archivos .ui en la carpeta ui."""
        self.listWidget.clear()
        carpeta_ui = os.path.join(os.getcwd(), "ui")
        if not os.path.exists(carpeta_ui):
            QMessageBox.warning(self, "Error", "No se encontró la carpeta 'ui'.")
            return
        
        archivos_ui = [f for f in os.listdir(carpeta_ui) if f.endswith(".ui")]
        self.listWidget.addItems(archivos_ui)
    
    def convertir_seleccionados(self):
        """Convierte los archivos seleccionados de .ui a .py."""
        seleccionados = self.listWidget.selectedItems()
        if not seleccionados:
            QMessageBox.warning(self, "Atención", "No hay archivos seleccionados.")
            return
        
        carpeta_ui = os.path.join(os.getcwd(), "ui")
        carpeta_generated = os.path.join(os.getcwd(), "generated")
        os.makedirs(carpeta_generated, exist_ok=True)
        
        for item in seleccionados:
            archivo_ui = item.text()
            ruta_ui = os.path.join(carpeta_ui, archivo_ui)
            archivo_py = archivo_ui.replace(".ui", ".py")
            ruta_py = os.path.join(carpeta_generated, archivo_py)
            
            # Copia de seguridad si el archivo ya existe
            if os.path.exists(ruta_py):
                ruta_backup = ruta_py + ".bak"
                shutil.copy2(ruta_py, ruta_backup)
            
            # Conversión usando pyside6-uic
            os.system(f"pyside6-uic {ruta_ui} -o {ruta_py}")
        
        QMessageBox.information(self, "Éxito", "Conversión completada.")
        self.listar_archivos_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = UIConverterApp()
    ventana.show()
    sys.exit(app.exec())
