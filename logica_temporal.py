from PySide6.QtWidgets import QWidget
# from generated.ui_temporal import Ui_Temporal  # ✅ Importamos la interfaz generada

class Temporal(QWidget):
    """ 📌 Ventana de prueba para Resultados dentro de Semana Anterior """

    def __init__(self):
        super().__init__()
        # self.ui = Ui_Temporal()
        self.ui.setupUi(self)