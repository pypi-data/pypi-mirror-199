# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interactiveconsolewidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_InteractiveConsoleWidget(object):
    def setupUi(self, InteractiveConsoleWidget):
        if not InteractiveConsoleWidget.objectName():
            InteractiveConsoleWidget.setObjectName(u"InteractiveConsoleWidget")
        InteractiveConsoleWidget.resize(487, 530)
        self.verticalLayout = QVBoxLayout(InteractiveConsoleWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.outputPlainTextEdit = QPlainTextEdit(InteractiveConsoleWidget)
        self.outputPlainTextEdit.setObjectName(u"outputPlainTextEdit")

        self.verticalLayout.addWidget(self.outputPlainTextEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.promptLabel = QLabel(InteractiveConsoleWidget)
        self.promptLabel.setObjectName(u"promptLabel")

        self.horizontalLayout.addWidget(self.promptLabel)

        self.inputLineEdit = QLineEdit(InteractiveConsoleWidget)
        self.inputLineEdit.setObjectName(u"inputLineEdit")

        self.horizontalLayout.addWidget(self.inputLineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(InteractiveConsoleWidget)

        QMetaObject.connectSlotsByName(InteractiveConsoleWidget)
    # setupUi

    def retranslateUi(self, InteractiveConsoleWidget):
        InteractiveConsoleWidget.setWindowTitle(QCoreApplication.translate("InteractiveConsoleWidget", u"Interactive Console", None))
        self.promptLabel.setText(QCoreApplication.translate("InteractiveConsoleWidget", u">>> ", None))
    # retranslateUi

