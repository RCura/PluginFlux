# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Tue Oct  4 12:25:41 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(594, 627)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 571, 451))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setGeometry(QtCore.QRect(490, 590, 91, 31))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.btnShowMsgBox = QtGui.QPushButton(Dialog)
        self.btnShowMsgBox.setGeometry(QtCore.QRect(356, 590, 121, 31))
        self.btnShowMsgBox.setObjectName(_fromUtf8("btnShowMsgBox"))
        self.pB_exportSVG = QtGui.QPushButton(Dialog)
        self.pB_exportSVG.setGeometry(QtCore.QRect(220, 590, 111, 31))
        self.pB_exportSVG.setObjectName(_fromUtf8("pB_exportSVG"))
        self.pB_Bezier = QtGui.QPushButton(Dialog)
        self.pB_Bezier.setGeometry(QtCore.QRect(480, 470, 101, 31))
        self.pB_Bezier.setObjectName(_fromUtf8("pB_Bezier"))
        self.pB_Bezier2 = QtGui.QPushButton(Dialog)
        self.pB_Bezier2.setGeometry(QtCore.QRect(480, 510, 101, 31))
        self.pB_Bezier2.setObjectName(_fromUtf8("pB_Bezier2"))
        self.cB_global = QtGui.QCheckBox(Dialog)
        self.cB_global.setGeometry(QtCore.QRect(40, 480, 97, 22))
        self.cB_global.setObjectName(_fromUtf8("cB_global"))
        self.pB_exportSVGBezier = QtGui.QPushButton(Dialog)
        self.pB_exportSVGBezier.setGeometry(QtCore.QRect(30, 520, 161, 27))
        self.pB_exportSVGBezier.setObjectName(_fromUtf8("pB_exportSVGBezier"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.btnShowMsgBox.setText(QtGui.QApplication.translate("Dialog", "Show MsgBox", None, QtGui.QApplication.UnicodeUTF8))
        self.pB_exportSVG.setText(QtGui.QApplication.translate("Dialog", "ExportSVG", None, QtGui.QApplication.UnicodeUTF8))
        self.pB_Bezier.setText(QtGui.QApplication.translate("Dialog", "Créer CP", None, QtGui.QApplication.UnicodeUTF8))
        self.pB_Bezier2.setText(QtGui.QApplication.translate("Dialog", "CréerBezier", None, QtGui.QApplication.UnicodeUTF8))
        self.cB_global.setText(QtGui.QApplication.translate("Dialog", "Global ?", None, QtGui.QApplication.UnicodeUTF8))
        self.pB_exportSVGBezier.setText(QtGui.QApplication.translate("Dialog", "ExportSVG_Bezier", None, QtGui.QApplication.UnicodeUTF8))

