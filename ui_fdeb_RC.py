# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fdeb_RC.ui'
#
# Created: Mon Oct 10 17:33:49 2011
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
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 571, 151))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setGeometry(QtCore.QRect(490, 590, 91, 31))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.pB_test = QtGui.QPushButton(Dialog)
        self.pB_test.setGeometry(QtCore.QRect(10, 590, 111, 31))
        self.pB_test.setObjectName(_fromUtf8("pB_test"))
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(10, 550, 571, 23))
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.BottomToTop)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

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
        self.pB_test.setText(QtGui.QApplication.translate("Dialog", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setFormat(QtGui.QApplication.translate("Dialog", "%p%", None, QtGui.QApplication.UnicodeUTF8))

