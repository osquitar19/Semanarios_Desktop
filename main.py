# main.py
import sys
from PySide6.QtWidgets import QApplication
from db import init_db
from core.main.logica_main_window import MainWindow

def main():
    # Inicializar la BD (opcional, crea tablas si no existen)
    init_db()

    # Lanzar la app de PySide6
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()