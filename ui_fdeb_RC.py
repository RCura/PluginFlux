# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fdeb_RC.ui'
#
# Created: Thu Oct 13 18:06:14 2011
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
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 601, 581))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayoutWidget = QtGui.QWidget(self.tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 571, 42))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.LayerInformations = QtGui.QGridLayout(self.gridLayoutWidget)
        self.LayerInformations.setMargin(0)
        self.LayerInformations.setObjectName(_fromUtf8("LayerInformations"))
        self.layerName = QtGui.QLabel(self.gridLayoutWidget)
        self.layerName.setObjectName(_fromUtf8("layerName"))
        self.LayerInformations.addWidget(self.layerName, 0, 0, 1, 1)
        self.selectedLayer = QtGui.QLabel(self.gridLayoutWidget)
        self.selectedLayer.setText(_fromUtf8(""))
        self.selectedLayer.setObjectName(_fromUtf8("selectedLayer"))
        self.LayerInformations.addWidget(self.selectedLayer, 0, 1, 1, 1)
        self.featureCount = QtGui.QLabel(self.gridLayoutWidget)
        self.featureCount.setObjectName(_fromUtf8("featureCount"))
        self.LayerInformations.addWidget(self.featureCount, 1, 0, 1, 1)
        self.numFeatures = QtGui.QLabel(self.gridLayoutWidget)
        self.numFeatures.setText(_fromUtf8(""))
        self.numFeatures.setObjectName(_fromUtf8("numFeatures"))
        self.LayerInformations.addWidget(self.numFeatures, 1, 1, 1, 1)
        self.formLayoutWidget_2 = QtGui.QWidget(self.tab)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 470, 571, 71))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.ProgressBars = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.ProgressBars.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.ProgressBars.setMargin(0)
        self.ProgressBars.setObjectName(_fromUtf8("ProgressBars"))
        self.FDEBProgress = QtGui.QLabel(self.formLayoutWidget_2)
        self.FDEBProgress.setObjectName(_fromUtf8("FDEBProgress"))
        self.ProgressBars.setWidget(1, QtGui.QFormLayout.LabelRole, self.FDEBProgress)
        self.initProgressBar = QtGui.QProgressBar(self.formLayoutWidget_2)
        self.initProgressBar.setProperty(_fromUtf8("value"), 0)
        self.initProgressBar.setObjectName(_fromUtf8("initProgressBar"))
        self.ProgressBars.setWidget(0, QtGui.QFormLayout.FieldRole, self.initProgressBar)
        self.initProgress = QtGui.QLabel(self.formLayoutWidget_2)
        self.initProgress.setObjectName(_fromUtf8("initProgress"))
        self.ProgressBars.setWidget(0, QtGui.QFormLayout.LabelRole, self.initProgress)
        self.progressBar = QtGui.QProgressBar(self.formLayoutWidget_2)
        self.progressBar.setEnabled(True)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.BottomToTop)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.ProgressBars.setWidget(1, QtGui.QFormLayout.FieldRole, self.progressBar)
        self.Settings = QtGui.QGroupBox(self.tab)
        self.Settings.setGeometry(QtCore.QRect(10, 240, 571, 211))
        self.Settings.setObjectName(_fromUtf8("Settings"))
        self.AttractionSettings = QtGui.QGroupBox(self.Settings)
        self.AttractionSettings.setGeometry(QtCore.QRect(0, 140, 571, 70))
        self.AttractionSettings.setObjectName(_fromUtf8("AttractionSettings"))
        self.attractionStrength = QtGui.QSlider(self.AttractionSettings)
        self.attractionStrength.setGeometry(QtCore.QRect(0, 40, 571, 29))
        self.attractionStrength.setMinimum(0)
        self.attractionStrength.setMaximum(8)
        self.attractionStrength.setSingleStep(1)
        self.attractionStrength.setPageStep(2)
        self.attractionStrength.setProperty(_fromUtf8("value"), 4)
        self.attractionStrength.setSliderPosition(4)
        self.attractionStrength.setOrientation(QtCore.Qt.Horizontal)
        self.attractionStrength.setInvertedAppearance(True)
        self.attractionStrength.setInvertedControls(True)
        self.attractionStrength.setTickInterval(1)
        self.attractionStrength.setObjectName(_fromUtf8("attractionStrength"))
        self.Strong = QtGui.QLabel(self.AttractionSettings)
        self.Strong.setGeometry(QtCore.QRect(520, 30, 46, 17))
        self.Strong.setObjectName(_fromUtf8("Strong"))
        self.Weak = QtGui.QLabel(self.AttractionSettings)
        self.Weak.setGeometry(QtCore.QRect(0, 30, 39, 17))
        self.Weak.setObjectName(_fromUtf8("Weak"))
        self.Average = QtGui.QLabel(self.AttractionSettings)
        self.Average.setGeometry(QtCore.QRect(260, 30, 56, 17))
        self.Average.setObjectName(_fromUtf8("Average"))
        self.formLayoutWidget = QtGui.QWidget(self.Settings)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 30, 571, 101))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.BasicSettings = QtGui.QFormLayout(self.formLayoutWidget)
        self.BasicSettings.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.BasicSettings.setMargin(0)
        self.BasicSettings.setObjectName(_fromUtf8("BasicSettings"))
        self.compatibilityThreshold = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.compatibilityThreshold.setMaximum(1.0)
        self.compatibilityThreshold.setSingleStep(0.05)
        self.compatibilityThreshold.setProperty(_fromUtf8("value"), 0.9)
        self.compatibilityThreshold.setObjectName(_fromUtf8("compatibilityThreshold"))
        self.BasicSettings.setWidget(0, QtGui.QFormLayout.LabelRole, self.compatibilityThreshold)
        self.Compatibility = QtGui.QLabel(self.formLayoutWidget)
        self.Compatibility.setObjectName(_fromUtf8("Compatibility"))
        self.BasicSettings.setWidget(0, QtGui.QFormLayout.FieldRole, self.Compatibility)
        self.numCycles = QtGui.QSpinBox(self.formLayoutWidget)
        self.numCycles.setMinimum(1)
        self.numCycles.setMaximum(30)
        self.numCycles.setProperty(_fromUtf8("value"), 20)
        self.numCycles.setObjectName(_fromUtf8("numCycles"))
        self.BasicSettings.setWidget(1, QtGui.QFormLayout.LabelRole, self.numCycles)
        self.CyclesNb = QtGui.QLabel(self.formLayoutWidget)
        self.CyclesNb.setObjectName(_fromUtf8("CyclesNb"))
        self.BasicSettings.setWidget(1, QtGui.QFormLayout.FieldRole, self.CyclesNb)
        self.numSteps = QtGui.QSpinBox(self.formLayoutWidget)
        self.numSteps.setMaximum(300)
        self.numSteps.setSingleStep(10)
        self.numSteps.setProperty(_fromUtf8("value"), 100)
        self.numSteps.setObjectName(_fromUtf8("numSteps"))
        self.BasicSettings.setWidget(2, QtGui.QFormLayout.LabelRole, self.numSteps)
        self.Iterationnb = QtGui.QLabel(self.formLayoutWidget)
        self.Iterationnb.setObjectName(_fromUtf8("Iterationnb"))
        self.BasicSettings.setWidget(2, QtGui.QFormLayout.FieldRole, self.Iterationnb)
        self.WarningText = QtGui.QTextBrowser(self.tab)
        self.WarningText.setGeometry(QtCore.QRect(10, 60, 571, 171))
        self.WarningText.setObjectName(_fromUtf8("WarningText"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.HelpTab = QtGui.QWidget()
        self.HelpTab.setObjectName(_fromUtf8("HelpTab"))
        self.HelpTxt = QtGui.QTextBrowser(self.HelpTab)
        self.HelpTxt.setGeometry(QtCore.QRect(0, 0, 591, 551))
        self.HelpTxt.setObjectName(_fromUtf8("HelpTxt"))
        self.tabWidget.addTab(self.HelpTab, _fromUtf8(""))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pB_test, self.tabWidget)
        Dialog.setTabOrder(self.tabWidget, self.compatibilityThreshold)
        Dialog.setTabOrder(self.compatibilityThreshold, self.numCycles)
        Dialog.setTabOrder(self.numCycles, self.numSteps)
        Dialog.setTabOrder(self.numSteps, self.attractionStrength)
        Dialog.setTabOrder(self.attractionStrength, self.HelpTxt)
        Dialog.setTabOrder(self.HelpTxt, self.btnClose)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pB_test.setText(QtGui.QApplication.translate("Dialog", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.layerName.setText(QtGui.QApplication.translate("Dialog", "Selected Layer :", None, QtGui.QApplication.UnicodeUTF8))
        self.featureCount.setText(QtGui.QApplication.translate("Dialog", "Number of features in this layer :", None, QtGui.QApplication.UnicodeUTF8))
        self.FDEBProgress.setText(QtGui.QApplication.translate("Dialog", "FDEB Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.initProgress.setText(QtGui.QApplication.translate("Dialog", "Init Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setFormat(QtGui.QApplication.translate("Dialog", "%p%", None, QtGui.QApplication.UnicodeUTF8))
        self.Settings.setTitle(QtGui.QApplication.translate("Dialog", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.AttractionSettings.setTitle(QtGui.QApplication.translate("Dialog", "Attraction Strength", None, QtGui.QApplication.UnicodeUTF8))
        self.Strong.setText(QtGui.QApplication.translate("Dialog", "Strong", None, QtGui.QApplication.UnicodeUTF8))
        self.Weak.setText(QtGui.QApplication.translate("Dialog", "Weak", None, QtGui.QApplication.UnicodeUTF8))
        self.Average.setText(QtGui.QApplication.translate("Dialog", "Average", None, QtGui.QApplication.UnicodeUTF8))
        self.Compatibility.setText(QtGui.QApplication.translate("Dialog", "Compatibility Threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.CyclesNb.setText(QtGui.QApplication.translate("Dialog", "Number of cycles", None, QtGui.QApplication.UnicodeUTF8))
        self.Iterationnb.setText(QtGui.QApplication.translate("Dialog", "Number of iterations steps of first cycle", None, QtGui.QApplication.UnicodeUTF8))
        self.WarningText.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Force-Directed Edge Bundling (FDEB) is a way to bundle polylines, applying sort of an electro-magnetic attraction to the edges. This can help spotting patterns or big flows in a flow map, or can just be of an aesthetical interest. We recommend using default parameters first, and then, trying to adapt to your datas in order to get what you want to picture. Check Help tab for more informations</p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">BEWARE : Depending of the number of polylines and the power of the computer, running FDEB could be very time-consuming, so, even if QGIS might seems frozen for hours, it\'s still running.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.HelpTxt.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">FDEB is an algorithm developped by Danny Holten and Jarke J. van Wijk, you can find their original paper at this url : www.win.tue.nl/~dholten/papers/forcebundles_eurovis.pdf</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To conceive this plugin, we used the java jFlowMap tool, which includes an implementation of FDEB made by Ilya Boyandin and Enrico Bertini, and that can be reached here :</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">http://code.google.com/p/jflowmap/</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Keep in mind that all layers created by this plugin are temporary layers, saved in memory only. So, if you want to keep one of this layer, don\'t forget to save it, using the Save As menu when right-clicking on the layer.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Here are the parameters descriptions :</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Compatibility Threshold</span> :</p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For two lines to be attracted by each other, they got to match some criterias : the higher their compatibility score will be, more they\'ll be attracted. If two lines compatibility is bellow this threshold, they won\'t be attracted.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Number of cycles</span> :</p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Each cycle, one more point is added to every line, and those points are the ones who\'ll get closer to the other lines. Thus, the more cycles you put, the more precise your polylines will be.</p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Number of iterations steps of first cycle</span> :</p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Each cycle, one point is added. But this point moves by a small distance toward the most attractive points. Each iteration is a small step to this point : the more iterations you set, the more your points will move, and thus, the more your lines will get closer to each others.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Attraction Strength</span> :</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Compatible points are moved each steps by a small distance. This distance is computed on the line length, but also, it depends on the extent of your shapefile. Considering this, you may have to make this attraction strength weighter more or less valued, considering that you want your points to move by small or large distances.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.HelpTab), QtGui.QApplication.translate("Dialog", "Help", None, QtGui.QApplication.UnicodeUTF8))

