# -*- coding: latin1 -*-

"""
/***************************************************************************
PluginFlux
A QGIS plugin dedicated to Flow Mapping.
Offers some tools for flow mapping, like Clustering, great-circles flows, 
Bezier curves, SVG export.
Developed by Robin Cura on behalf of Geographie-cités geography laboratory.
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
- Soucis dans le passage de MapTools : Fonctionne avec la main,  mais pas avec les zooms+/-


"""

# Import des libs PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import des libs Qgis
from qgis.core import *
from qgis.gui import *

# Import des resources Qt
import resources

import webbrowser, os
import os.path, sys

# Set up current path.
currentPath = os.path.dirname( __file__ )

# Import des libs du plugin
from ui_control import ui_Control

from plugintools.CommonUtils import FlowUtils
from plugintools.nearestfeaturetool import SelectNearestFeature
from plugintools.BezierUtils import BezierUtils

class PluginFlux:
    """
    Classe principale du plugin, définit l'interface et les actions.
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
            
        QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivateBezier) # Si un autre outil est selectionné
        QObject.connect(self.BezierTool, SIGNAL("triggered()"), self.runBezier) # Chargement de l'outil Bezier
        
        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addToolBarIcon(self.BezierTool)
        self.iface.addPluginToMenu("&PluginFlux", self.action)
        self.iface.addPluginToMenu("&PluginFlux", self.BezierTool)
    
    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&PluginFlux",self.action)
        self.iface.removeToolBarIcon(self.action)
        # on enleve aussi l'outil Bezier
        self.iface.removePluginMenu("&PluginFlux", self.BezierTool)
        self.iface.removeToolBarIcon(self.BezierTool)
    
    def run(self):
        # create and show a configuration dialog or something similar
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint   # QgisGui.ModalDialogFlags 
        self.pluginGui = ui_Control(self.iface.mainWindow(), flags)
        self.pluginGui.setWindowTitle('PluginFlux - Version pre-alpha')
            
        # On crée nos variables pour explorer les couches[...]
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
            print "Coché"
            QMessageBox.information(self.iface.mainWindow(),"Erreur",QString('Fonction pas encore implémentée'))
        else:
            print "Décoché"
            FlowUtils(self.iface).createBezier()   
              
    def doBezierSVG(self):
        FlowUtils(self.iface).createBezierSVG()
      
          
          
    def runBezier(self):
        if self.canvas.layerCount() != 0:
            self.tool = SelectNearestFeature(self.canvas)                 
            self.canvas.setMapTool(self.tool)
            self.BezierTool.setChecked(True)      
            QObject.connect(self.tool, SIGNAL("featureFound(PyQt_PyObject)"), self.selectFeature)
        else:
            QMessageBox.information(self.iface.mainWindow(),"Erreur",QString('Aucune couche n\'est chargée'))
            self.BezierTool.setChecked(False)
        
    def selectFeature(self, result):
        layer = result[0]
        idfeature = result[1]
        for i in range(self.canvas.layerCount()):
            displayedLayer = self.canvas.layers()[i]
            displayedLayer.removeSelection(False)
        layer.select(idfeature, False)
        self.canvas.refresh()
        # Maintenant, on appelle, dans BezierUtils, les fonctions qui vont permettre d'agir depuis la selection
        BezierUtils(self.iface).repartitionActions(layer, idfeature)
        
        
    
    def deactivateBezier(self):
        self.BezierTool.setChecked(False)
        for i in range(self.canvas.layerCount()):
            displayedLayer = self.canvas.layers()[i]
            displayedLayer.removeSelection(False)
        self.canvas.refresh()