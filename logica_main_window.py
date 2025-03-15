import sys
from PySide6 import QtWidgets
from generated.ui_main_window import Ui_MainWindow  # Importa la UI generada

# 📌 Importamos las clases de cada módulo
from logica_aprontes import Aprontes
from logica_temporal import Temporal  # ✅ Importamos la nueva ventana
from logica_programas import Programas  # ✅ Importamos módulos de Edición de texto
from logica_resultados import Resultados  # ✅ Importamos módulos de Edición de texto
from logica_pesos_fisicos import PesosFisicos  # ✅ Importamos módulos de Edición de texto
# ⚠️ Cuando se agreguen más módulos, se importan aquí sus clases

class MainWindow(QtWidgets.QMainWindow):
    """ Ventana principal que administra la navegación entre módulos """

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print("✅ Ventana principal cargada correctamente.")  # Debug

        # Conectar el menú lateral con la navegación
        self.ui.treeMenu.itemClicked.connect(self.on_item_clicked)

        # Placeholder para mantener la referencia de ventanas cargadas
        self.modulos_abiertos = {}  # 📌 Guardará las instancias de cada ventana

    def on_item_clicked(self, item, column):
        """ 📌 Cambia entre ventanas según el ítem seleccionado """
        nombre_item = item.text(column)

        # Diccionario de módulos disponibles
        modulos = {
            "Aprontes": Aprontes,  # Edición de texto > Aprontes
            "Programas": Programas,  # Edición de texto > Programas
            "Pesos físicos": PesosFisicos,  # Edición de texto > Pesos físicos
        }
        
        # Obtener el texto del elemento padre para diferenciar secciones con el mismo nombre
        parent_text = ""
        parent = item.parent()
        if parent:
            parent_text = parent.text(0)
            
        # Manejo especial para ítems con el mismo nombre en diferentes secciones
        if nombre_item == "Resultados":
            if parent_text == "Semana anterior":
                self.cargar_modulo(nombre_item, Temporal)
                return
            elif parent_text == "Edición de texto":
                self.cargar_modulo(nombre_item, Resultados)
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())