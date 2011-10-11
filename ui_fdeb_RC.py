# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fdeb_RC.ui'
#
# Created: Tue Oct 11 18:34:33 2011
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
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 430, 571, 100))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.compatibilityThreshold = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.compatibilityThreshold.setMaximum(1.0)
        self.compatibilityThreshold.setSingleStep(0.05)
        self.compatibilityThreshold.setProperty(_fromUtf8("value"), 0.8)
        self.compatibilityThreshold.setObjectName(_fromUtf8("compatibilityThreshold"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.compatibilityThreshold)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label)
        self.numCycles = QtGui.QSpinBox(self.formLayoutWidget)
        self.numCycles.setMinimum(1)
        self.numCycles.setMaximum(30)
        self.numCycles.setProperty(_fromUtf8("value"), 5)
        self.numCycles.setObjectName(_fromUtf8("numCycles"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.numCycles)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_2)
        self.numSteps = QtGui.QSpinBox(self.formLayoutWidget)
        self.numSteps.setMaximum(300)
        self.numSteps.setSingleStep(10)
        self.numSteps.setProperty(_fromUtf8("value"), 100)
        self.numSteps.setObjectName(_fromUtf8("numSteps"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.numSteps)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.label_3)
        self.gridLayoutWidget = QtGui.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 30, 521, 121))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.selectedLayer = QtGui.QLabel(self.gridLayoutWidget)
        self.selectedLayer.setText(_fromUtf8(""))
        self.selectedLayer.setObjectName(_fromUtf8("selectedLayer"))
        self.gridLayout.addWidget(self.selectedLayer, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.numFeatures = QtGui.QLabel(self.gridLayoutWidget)
        self.numFeatures.setText(_fromUtf8(""))
        self.numFeatures.setObjectName(_fromUtf8("numFeatures"))
        self.gridLayout.addWidget(self.numFeatures, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pB_test.setText(QtGui.QApplication.translate("Dialog", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setFormat(QtGui.QApplication.translate("Dialog", "%p%", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Compatibility Threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Number of cycles", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Number of iterations steps of first cycle", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Selected Layer :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Number of features in this layer :", None, QtGui.QApplication.UnicodeUTF8))

