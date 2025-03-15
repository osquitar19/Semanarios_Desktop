# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowTDxQQS.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QMenuBar, QSizePolicy, QStackedWidget,
    QStatusBar, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1960, 1313)
        MainWindow.setMinimumSize(QSize(1187, 906))
        self.mainContainer = QWidget(MainWindow)
        self.mainContainer.setObjectName(u"mainContainer")
        self.horizontalLayout = QHBoxLayout(self.mainContainer)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.treeMenu = QTreeWidget(self.mainContainer)
        __qtreewidgetitem = QTreeWidgetItem(self.treeMenu)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.treeMenu)
        QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem2 = QTreeWidgetItem(self.treeMenu)
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3 = QTreeWidgetItem(self.treeMenu)
        QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem3)
        __qtreewidgetitem4 = QTreeWidgetItem(self.treeMenu)
        QTreeWidgetItem(__qtreewidgetitem4)
        QTreeWidgetItem(__qtreewidgetitem4)
        self.treeMenu.setObjectName(u"treeMenu")
        self.treeMenu.setMaximumSize(QSize(200, 16777215))
        self.treeMenu.setHeaderHidden(True)
        self.treeMenu.setColumnCount(1)

        self.horizontalLayout.addWidget(self.treeMenu)

        self.mainStackedWidget = QStackedWidget(self.mainContainer)
        self.mainStackedWidget.setObjectName(u"mainStackedWidget")
        self.emptyPage = QWidget()
        self.emptyPage.setObjectName(u"emptyPage")
        self.verticalLayout = QVBoxLayout(self.emptyPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.emptyLabel = QLabel(self.emptyPage)
        self.emptyLabel.setObjectName(u"emptyLabel")

        self.verticalLayout.addWidget(self.emptyLabel)

        self.mainStackedWidget.addWidget(self.emptyPage)

        self.horizontalLayout.addWidget(self.mainStackedWidget)

        MainWindow.setCentralWidget(self.mainContainer)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1960, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Semanarios \u00a9 2025 Oscar Orellana Casas", None))
        ___qtreewidgetitem = self.treeMenu.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"1", None));

        __sortingEnabled = self.treeMenu.isSortingEnabled()
        self.treeMenu.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeMenu.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Semana actual", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"Programas", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"Apuestas", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"Debutantes", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem1.child(3)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"Comentarios", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem1.child(4)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"Cambios de carreras", None));
        ___qtreewidgetitem7 = self.treeMenu.topLevelItem(1)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("MainWindow", u"Semana anterior", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem7.child(0)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("MainWindow", u"Resultados", None));
        ___qtreewidgetitem9 = self.treeMenu.topLevelItem(2)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("MainWindow", u"Edici\u00f3n de texto", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem9.child(0)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("MainWindow", u"Programas", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem9.child(1)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("MainWindow", u"Resultados", None));
        ___qtreewidgetitem12 = ___qtreewidgetitem9.child(2)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("MainWindow", u"Aprontes", None));
        ___qtreewidgetitem13 = ___qtreewidgetitem9.child(3)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("MainWindow", u"Pesos f\u00edsicos", None));
        ___qtreewidgetitem14 = self.treeMenu.topLevelItem(3)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("MainWindow", u"Producci\u00f3n", None));
        ___qtreewidgetitem15 = ___qtreewidgetitem14.child(0)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("MainWindow", u"Programas", None));
        ___qtreewidgetitem16 = ___qtreewidgetitem14.child(1)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("MainWindow", u"Resultados", None));
        ___qtreewidgetitem17 = ___qtreewidgetitem14.child(2)
        ___qtreewidgetitem17.setText(0, QCoreApplication.translate("MainWindow", u"Estad\u00edsticas", None));
        ___qtreewidgetitem18 = self.treeMenu.topLevelItem(4)
        ___qtreewidgetitem18.setText(0, QCoreApplication.translate("MainWindow", u"Utilidades", None));
        ___qtreewidgetitem19 = ___qtreewidgetitem18.child(0)
        ___qtreewidgetitem19.setText(0, QCoreApplication.translate("MainWindow", u"Importaci\u00f3n", None));
        ___qtreewidgetitem20 = ___qtreewidgetitem18.child(1)
        ___qtreewidgetitem20.setText(0, QCoreApplication.translate("MainWindow", u"Actividades", None));
        self.treeMenu.setSortingEnabled(__sortingEnabled)

        self.treeMenu.setProperty(u"headerLabels", [
            QCoreApplication.translate("MainWindow", u"Men\u00fa", None)])
        self.emptyLabel.setText(QCoreApplication.translate("MainWindow", u"Contenido de la p\u00e1gina", None))
    # retranslateUi

