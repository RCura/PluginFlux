# -*- coding: latin1 -*-

"""
/***************************************************************************
PluginFlux
A QGIS plugin dedicated to Flow Mapping.
Offers some tools for flow mapping, like Clustering, great-circles flows, 
Bezier curves, SVG export.
Developed by Robin Cura on behalf of Geographie-cit�s geography laboratory.
http://www.parisgeo.cnrs.fr/

                             -------------------
begin                : 2011-07-11
copyright            : (C) 2011 by Robin Cura
email                : robin.cura@gmail.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

BUGS:


TODO :
- Comportement OK
- Ajout des manipulations


"""

# Import des libs PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import des libs Qgis
from qgis.core import *
from qgis.gui import *

# Import des resources Qt
import resources

import os
import os.path
import pdb

# Set up current path.
currentPath = os.path.dirname( __file__ )

# Import des libs du plugin
from ui_control import ui_Control
from ui_control_fdeb import ui_Control_FDEB
from ui_control_fdeb_RC import ui_Control_FDEB_RC
from ui_control_fdeb_SR import ui_Control_FDEB_SR

from plugintools.CommonUtils import FlowUtils
from plugintools.nearestfeaturetool import SelectNearestFeature
from plugintools.BezierUtils import BezierUtils
from plugintools.FDEB import FDEB
from plugintools.FDEB_RC import FDEB_RC
from plugintools.FDEB_SR import FDEB_SR

class PluginFlux:
    """
    Classe principale du plugin, d�finit l'interface et les actions.
    """
    
    def __init__(self, iface):   
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
    
    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(QIcon(":/icons/icon_plugin_flux.png"), "PluginFlux", self.iface.mainWindow())
        self.action.setWhatsThis("Configuration for test plugin")
        self.action.setStatusTip("This is status tip")
        
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("activated()"), self.run)
            
        # on ajoute l'outil Bezier
        self.BezierTool = QAction(QIcon(":/icons/icon_Bezier.png"), "BezierTool", self.iface.mainWindow())
        self.BezierTool.setCheckable(True)
        self.BezierTool.setWhatsThis("Outil de construction de courbes de Bezier")
            
        QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivateBezier) # Si un autre outil est selectionn�
        QObject.connect(self.BezierTool, SIGNAL("triggered()"), self.runBezier) # Chargement de l'outil Bezier
        
        # On ajoute la fenetre FDEB Global
        self.fdeb = QAction(QIcon(":/icons/icon_FDEB.png"), "FDEB", self.iface.mainWindow())
        self.fdeb.setWhatsThis("Outil de bundling des liens selon FDEB")
        self.fdeb.setStatusTip("Lancer la configuration de FDEB")
        
        QObject.connect(self.fdeb, SIGNAL("activated()"), self.runFDEB)
        
        # On ajoute la fenetre FDEB RC
        self.fdeb_RC = QAction(QIcon(":/icons/icon_FDEB_RC.png"), "FDEB", self.iface.mainWindow())
        self.fdeb_RC.setWhatsThis("Outil de bundling des liens selon FDEB")
        self.fdeb_RC.setStatusTip("Lancer la configuration de FDEB")
        
        QObject.connect(self.fdeb_RC, SIGNAL("activated()"), self.runFDEB_RC)
        
        # On ajoute la fenetre FDEB SR
        self.fdeb_SR = QAction(QIcon(":/icons/icon_FDEB_SR.png"), "FDEB", self.iface.mainWindow())
        self.fdeb_SR.setWhatsThis("Outil de bundling des liens selon FDEB")
        self.fdeb_SR.setStatusTip("Lancer la configuration de FDEB")
        
        QObject.connect(self.fdeb_SR, SIGNAL("activated()"), self.runFDEB_SR)
        
        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addToolBarIcon(self.BezierTool)
        self.iface.addToolBarIcon(self.fdeb)
        self.iface.addToolBarIcon(self.fdeb_RC)
        self.iface.addToolBarIcon(self.fdeb_SR)
        
        self.iface.addPluginToMenu("&PluginFlux", self.action)
        self.iface.addPluginToMenu("&PluginFlux", self.BezierTool)
        self.iface.addPluginToMenu("&PluginFlux", self.fdeb)
        self.iface.addPluginToMenu("&PluginFlux", self.fdeb_RC)
        self.iface.addPluginToMenu("&PluginFlux", self.fdeb_SR)
    
    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&PluginFlux",self.action)
        self.iface.removeToolBarIcon(self.action)
        # on enleve aussi l'outil Bezier
        self.iface.removePluginMenu("&PluginFlux", self.BezierTool)
        self.iface.removeToolBarIcon(self.BezierTool)
        # Et FDEB
        self.iface.removePluginMenu("PluginFlux", self.fdeb)
        self.iface.removeToolBarIcon(self.fdeb)
        self.iface.removePluginMenu("PluginFlux", self.fdeb_RC)
        self.iface.removeToolBarIcon(self.fdeb_RC)
        self.iface.removePluginMenu("PluginFlux", self.fdeb_SR)
        self.iface.removeToolBarIcon(self.fdeb_SR)
    
    def run(self):
        # create and show a configuration dialog or something similar
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint   # QgisGui.ModalDialogFlags 
        self.pluginGui = ui_Control(self.iface.mainWindow(), flags)
        self.pluginGui.setWindowTitle('PluginFlux - Version pre-alpha')
            
        # On cr�e nos variables pour explorer les couches[...]
        layer = self.canvas.currentLayer()
        if (layer == None):
            QMessageBox.information(self.iface.mainWindow(),"About","Aucune couche n'est chargee")
        else:  
            # On sort quelques infos
            lyname = layer.name()
            fcount = str(layer.featureCount())
            
            expText = "Voila le nom de la couche selectionnee : \n" + \
                    lyname + "\n" + \
                    "Cette couche comporte : " + fcount + " entitees \n"
            
            #INSERT EVERY SIGNAL CONECTION HERE!
            QObject.connect(self.pluginGui.btnClose, SIGNAL('clicked()'), self.doClose)
            QObject.connect(self.pluginGui.btnShowMsgBox, SIGNAL('clicked()'),self.doShow)
            QObject.connect(self.pluginGui.pB_exportSVG, SIGNAL('clicked()'), self.doExportSVG)
            QObject.connect(self.pluginGui.pB_Bezier, SIGNAL('clicked()'), self.startBezier)
            QObject.connect(self.pluginGui.pB_Bezier2, SIGNAL('clicked()'), self.startBezier2)
            QObject.connect(self.pluginGui.pB_exportSVGBezier, SIGNAL('clicked()'), self.doBezierSVG)
            self.pluginGui.textEdit.setText(expText)
            self.pluginGui.show()
    
    def doClose(self):
        self.pluginGui.reject()
    
    def doShow(self):
        infoString = QString("Hello, Robin !!!")
        QMessageBox.information(self.iface.mainWindow(),"About",infoString)
    
    def doExportSVG(self):
        FlowUtils(self.iface).exportSVGLineaire()
      
    def startBezier(self):
        FlowUtils(self.iface).createCP()
      
    def startBezier2(self):
        if self.pluginGui.cB_global.checkState() == 2:
            print "Coch�"
            QMessageBox.information(self.iface.mainWindow(),"Erreur",QString('Fonction pas encore impl�ment�e'))
        else:
            print "D�coch�"
            FlowUtils(self.iface).createBezier()   
              
    def doBezierSVG(self):
        FlowUtils(self.iface).createBezierSVG()

          
    def runBezier(self):
        if self.canvas.layerCount() != 0:
            self.tool = SelectNearestFeature(self.canvas)                 
            self.canvas.setMapTool(self.tool)
            self.BezierTool.setChecked(True)      
            self.tool.featureFound.connect(self.selectFeature)
        else:
            QMessageBox.information(self.iface.mainWindow(),"Erreur",QString('Aucune couche n\'est charg�e'))
            self.BezierTool.setChecked(False)
        
    def selectFeature(self, result):
        layer = result[0]
        idfeature = result[1]
        for i in range(self.canvas.layerCount()):
            displayedLayer = self.canvas.layers()[i]
            displayedLayer.removeSelection(False)
        layer.select(idfeature, False)
        self.canvas.refresh()
        
        BezierUtils(self.iface).repartitionActions(layer, idfeature)
        
    
    def deactivateBezier(self):
        self.BezierTool.setChecked(False)
        for i in range(self.canvas.layerCount()):
            displayedLayer = self.canvas.layers()[i]
            displayedLayer.removeSelection(False)
        self.canvas.refresh()
        
    def runFDEB(self):
            # create and show a configuration dialog or something similar
            flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint   # QgisGui.ModalDialogFlags 
            self.fdebGUI = ui_Control_FDEB(self.iface.mainWindow(), flags)
            self.fdebGUI.setWindowTitle('FDEB - Version d\'Int�gration')
            QObject.connect(self.fdebGUI.btnClose, SIGNAL('clicked()'), self.closeFDEB)
            QObject.connect(self.fdebGUI.pB_test, SIGNAL('clicked()'), self.launchFDEB)
            self.fdebGUI.textEdit.setText("Test de texte.....")
            self.fdebGUI.show()
    
    def closeFDEB(self):
        self.fdebGUI.reject()
        
    def launchFDEB(self):
        FDEB(self.iface).test()
        
    def runFDEB_RC(self):
        # create and show a configuration dialog or something similar
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint   # QgisGui.ModalDialogFlags 
        self.fdebGUI_RC = ui_Control_FDEB_RC(self.iface.mainWindow(), flags)
        self.fdebGUI_RC.setWindowTitle('FDEB - Version de RC')
        QObject.connect(self.fdebGUI_RC.btnClose, SIGNAL('clicked()'), self.closeFDEB_RC)
        QObject.connect(self.fdebGUI_RC.pB_test, SIGNAL('clicked()'), self.launchFDEB_RC)
        self.fdebGUI_RC.textEdit.setText("Test de texte..... Pour Robin")
        self.fdebGUI_RC.show()
    
    def closeFDEB_RC(self):
        self.fdebGUI_RC.reject()
        
    def launchFDEB_RC(self):
        FDEB_RC(self.iface).test()
        
    def runFDEB_SR(self):
        # create and show a configuration dialog or something similar
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint   # QgisGui.ModalDialogFlags 
        self.fdebGUI_SR = ui_Control_FDEB_SR(self.iface.mainWindow(), flags)
        self.fdebGUI_SR.setWindowTitle('FDEB - Version de SR')
        QObject.connect(self.fdebGUI_SR.btnClose, SIGNAL('clicked()'), self.closeFDEB_SR)
        QObject.connect(self.fdebGUI_SR.pB_test, SIGNAL('clicked()'), self.launchFDEB_SR)
        self.fdebGUI_SR.textEdit.setText("Test de texte..... Pour S�bastien")
        self.fdebGUI_SR.show()
    
    def closeFDEB_SR(self):
        self.fdebGUI_SR.reject()
        
    def launchFDEB_SR(self):
        FDEB_SR(self.iface).test()
        
