# -*- coding: utf-8 -*-

################################################################################
## Form generated for Resultados UI
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QRadioButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_Resultados(object):
    def setupUi(self, Resultados):
        if not Resultados.objectName():
            Resultados.setObjectName(u"Resultados")
        Resultados.resize(1647, 1028)
        self.txtTexto = QTextEdit(Resultados)
        self.txtTexto.setObjectName(u"txtTexto")
        self.txtTexto.setGeometry(QRect(290, 120, 1351, 1161))
        font = QFont()
        font.setFamilies([u"Menlo"])
        font.setPointSize(14)
        self.txtTexto.setFont(font)
        self.chkEstudie = QCheckBox(Resultados)
        self.chkEstudie.setObjectName(u"chkEstudie")
        self.chkEstudie.setGeometry(QRect(300, 60, 85, 16))
        self.chkEstudie.setChecked(True)
        self.chkDato = QCheckBox(Resultados)
        self.chkDato.setObjectName(u"chkDato")
        self.chkDato.setGeometry(QRect(620, 60, 85, 16))
        self.chkDato.setChecked(True)
        self.chkCatedra = QCheckBox(Resultados)
        self.chkCatedra.setObjectName(u"chkCatedra")
        self.chkCatedra.setGeometry(QRect(380, 60, 85, 16))
        self.chkCatedra.setChecked(True)
        self.chkQuispe = QCheckBox(Resultados)
        self.chkQuispe.setObjectName(u"chkQuispe")
        self.chkQuispe.setGeometry(QRect(540, 60, 85, 16))
        self.chkQuispe.setChecked(True)
        self.chkTrabajo = QCheckBox(Resultados)
        self.chkTrabajo.setObjectName(u"chkTrabajo")
        self.chkTrabajo.setGeometry(QRect(460, 60, 85, 16))
        self.chkTrabajo.setChecked(True)
        self.lblArchivos = QLabel(Resultados)
        self.lblArchivos.setObjectName(u"lblArchivos")
        self.lblArchivos.setGeometry(QRect(50, 100, 231, 20))
        self.lblArchivos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblNombreNuevo = QLabel(Resultados)
        self.lblNombreNuevo.setObjectName(u"lblNombreNuevo")
        self.lblNombreNuevo.setGeometry(QRect(290, 100, 1351, 16))
        self.lblNombreNuevo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btnGuardar = QPushButton(Resultados)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setGeometry(QRect(60, 50, 221, 31))
        self.listArchivos = QListWidget(Resultados)
        self.listArchivos.setObjectName(u"listArchivos")
        self.listArchivos.setGeometry(QRect(55, 120, 221, 341))
        self.frame = QFrame(Resultados)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(730, 30, 81, 71))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.radioANSI = QRadioButton(self.frame)
        self.radioANSI.setObjectName(u"radioANSI")
        self.radioANSI.setGeometry(QRect(10, 10, 61, 20))
        self.radioANSI.setChecked(True)
        self.radioUTF = QRadioButton(self.frame)
        self.radioUTF.setObjectName(u"radioUTF")
        self.radioUTF.setGeometry(QRect(10, 40, 61, 20))
        self.btnCerrar = QPushButton(Resultados)
        self.btnCerrar.setObjectName(u"btnCerrar")
        self.btnCerrar.setGeometry(QRect(60, 0, 221, 32))
        self.btnValidar = QPushButton(Resultados)
        self.btnValidar.setObjectName(u"btnValidar")
        self.btnValidar.setGeometry(QRect(1400, 10, 221, 32))

        self.retranslateUi(Resultados)

        QMetaObject.connectSlotsByName(Resultados)
    # setupUi

    def retranslateUi(self, Resultados):
        Resultados.setWindowTitle(QCoreApplication.translate("Resultados", u"Edici\u00f3n de Resultados", None))
        self.txtTexto.setHtml(QCoreApplication.translate("Resultados", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Menlo'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt;\"><br /></p></body></html>", None))
        self.chkEstudie.setText(QCoreApplication.translate("Resultados", u"Estudie", None))
        self.chkDato.setText(QCoreApplication.translate("Resultados", u"Dato", None))
        self.chkCatedra.setText(QCoreApplication.translate("Resultados", u"C\u00e1tedra", None))
        self.chkQuispe.setText(QCoreApplication.translate("Resultados", u"Quispe", None))
        self.chkTrabajo.setText(QCoreApplication.translate("Resultados", u"Trabajo", None))
        self.lblArchivos.setText(QCoreApplication.translate("Resultados", u"Resultados disponibles", None))
        self.lblNombreNuevo.setText(QCoreApplication.translate("Resultados", u"Nombre nuevo", None))
        self.btnGuardar.setText(QCoreApplication.translate("Resultados", u"Guardar", None))
        self.radioANSI.setText(QCoreApplication.translate("Resultados", u"ANSI", None))
        self.radioUTF.setText(QCoreApplication.translate("Resultados", u"UTF-8", None))
        self.btnCerrar.setText(QCoreApplication.translate("Resultados", u"Cerrar", None))
        self.btnValidar.setText(QCoreApplication.translate("Resultados", u"Validar resultados", None))
    # retranslateUi