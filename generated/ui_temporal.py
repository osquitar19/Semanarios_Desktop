# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_temporaljZPMUp.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

class Ui_Temporal(object):
    def setupUi(self, Temporal):
        if not Temporal.objectName():
            Temporal.setObjectName(u"Temporal")
        Temporal.resize(1001, 675)
        self.label = QLabel(Temporal)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(230, 210, 531, 201))
        font = QFont()
        font.setFamilies([u"American Typewriter"])
        font.setPointSize(72)
        self.label.setFont(font)

        self.retranslateUi(Temporal)

        QMetaObject.connectSlotsByName(Temporal)
    # setupUi

    def retranslateUi(self, Temporal):
        Temporal.setWindowTitle(QCoreApplication.translate("Temporal", u"TEMPORAL", None))
        self.label.setText(QCoreApplication.translate("Temporal", u"TextLabel", None))
    # retranslateUi

