# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'consoleeditorwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from opencmiss.zincwidgets.interactiveconsolewidget import InteractiveConsoleWidget


class Ui_ConsoleEditorWidget(object):
    def setupUi(self, ConsoleEditorWidget):
        if not ConsoleEditorWidget.objectName():
            ConsoleEditorWidget.setObjectName(u"ConsoleEditorWidget")
        ConsoleEditorWidget.resize(452, 533)
        self.gridLayout = QGridLayout(ConsoleEditorWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.interactiveConsoleWidget = InteractiveConsoleWidget(ConsoleEditorWidget)
        self.interactiveConsoleWidget.setObjectName(u"interactiveConsoleWidget")

        self.gridLayout.addWidget(self.interactiveConsoleWidget, 0, 0, 1, 1)


        self.retranslateUi(ConsoleEditorWidget)

        QMetaObject.connectSlotsByName(ConsoleEditorWidget)
    # setupUi

    def retranslateUi(self, ConsoleEditorWidget):
        ConsoleEditorWidget.setWindowTitle(QCoreApplication.translate("ConsoleEditorWidget", u"Interactive console", None))
    # retranslateUi

