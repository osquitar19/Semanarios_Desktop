import sys
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader  # Importar QUiLoader para cargar el archivo .ui
from PySide6.QtCore import QFile, QDir  # Para manejar el archivo .ui y rutas
from PySide6.QtWidgets import QMessageBox  # Importar QMessageBox para mostrar mensajes

# 📌 Importamos las clases de cada módulo desde sus nuevas ubicaciones
from core.edit_txt_aprontes.logica_aprontes import Aprontes
from core.edit_txt_resultados.logica_resultados import Resultados
from core.edit_txt_pesos_fisicos.logica_pesos_fisicos import PesosFisicos
from core.produccion_xtg.logica_creacion_xtg import CreacionXTG  # Cambiado de Programas a CreacionXTG

class MainWindow(QtWidgets.QMainWindow):
    """ Ventana principal que administra la navegación entre módulos """

    def __init__(self):
        super().__init__()
        self.cargar_ui()  # Cargar la interfaz desde el archivo .ui
        print("✅ Ventana principal cargada correctamente.")  # Debug

        # Conectar el menú lateral con la navegación
        self.ui.treeMenu.itemClicked.connect(self.on_item_clicked)

        # Placeholder para mantener la referencia de ventanas cargadas
        self.modulos_abiertos = {}  # 📌 Guardará las instancias de cada ventana

    def cargar_ui(self):
        """Carga el archivo .ui y asigna los widgets a self.ui"""
        loader = QUiLoader()
        ui_file = QFile("core/main/ui_main_window.ui")  # Ruta actualizada
        
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
        
        # Asignar el widget central (mainContainer) al QMainWindow
        self.setCentralWidget(self.ui.mainContainer)
        
        # Establecer el tamaño de la ventana principal según el archivo .ui
        self.resize(1960, 1313)  # Tamaño definido en el archivo .ui

    def on_item_clicked(self, item, column):
        """ 📌 Cambia entre ventanas según el ítem seleccionado """
        nombre_item = item.text(column)

        # Diccionario de módulos disponibles
        modulos = {
            "Aprontes": Aprontes,          # Edición de texto > Aprontes
            "Pesos físicos": PesosFisicos, # Edición de texto > Pesos físicos
        }
        
        # Obtener el texto del elemento padre para diferenciar secciones con el mismo nombre
        parent_text = ""
        parent = item.parent()
        if parent:
            parent_text = parent.text(0)
            
        # Manejo especial para ítems con el mismo nombre en diferentes secciones
        if nombre_item == "Resultados" and parent_text == "Edición de texto":
            self.cargar_modulo(nombre_item, Resultados)
            return
        elif nombre_item == "Programas" and parent_text == "Producción":
            self.cargar_modulo(nombre_item, CreacionXTG)  # Actualizado para usar CreacionXTG
            return
        if nombre_item in modulos:
            self.cargar_modulo(nombre_item, modulos[nombre_item])

    def cargar_modulo(self, nombre, clase_ventana):
        """ 📌 Carga dinámicamente una ventana dentro del contenedor """
        if nombre in self.modulos_abiertos:
            # Si ya está abierta, simplemente la mostramos
            self.ui.mainStackedWidget.setCurrentWidget(self.modulos_abiertos[nombre])
        else:
            # Si no está abierta, la creamos y la agregamos al contenedor
            nueva_ventana = clase_ventana()
            self.modulos_abiertos[nombre] = nueva_ventana
            self.ui.mainStackedWidget.addWidget(nueva_ventana)
            self.ui.mainStackedWidget.setCurrentWidget(nueva_ventana)

    def resizeEvent(self, event):
        """Actualiza el tamaño de los módulos hijos"""
        super().resizeEvent(event)
        
        # Ajustar tamaño del contenedor principal
        self.ui.mainContainer.resize(self.size())
        
        # Ajustar cada módulo cargado
        for modulo in self.modulos_abiertos.values():
            modulo.resize(self.ui.mainStackedWidget.size())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())