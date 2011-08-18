# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from ui_control import ui_Control
import resources
import tools

class PluginFlux:

  def __init__(self, iface):
    self.iface = iface

  def initGui(self):
    # create action that will start plugin configuration
    self.action = QAction(QIcon(":/icons/icon_plugin_flux.png"), "PluginFlux", self.iface.mainWindow())
    self.action.setWhatsThis("Configuration for test plugin")
    self.action.setStatusTip("This is status tip")

    # connect the action to the run method
    QObject.connect(self.action, SIGNAL("activated()"), self.run)

    # add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&PluginFlux", self.action)

  def unload(self):
    # remove the plugin menu item and icon
    self.iface.removePluginMenu("&PluginFlux",self.action)
    self.iface.removeToolBarIcon(self.action)

  def run(self):
    # create and show a configuration dialog or something similar
    flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
    self.pluginGui = ui_Control(self.iface.mainWindow(), flags)
    
    # On crée nos variables pour explorer les couches[...]
    mapC = self.iface.mapCanvas()
    layer = mapC.currentLayer()
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
    infoString = QString("Hello, Robin!")
    QMessageBox.information(self.iface.mainWindow(),"About",infoString)
    tools.testprint()
            

  def doExportSVG(self):
      
      tools.exportSVGLineaire(self)
      
  def startBezier(self):
      tools.createCP(self)
  
  def startBezier2(self):
      if self.pluginGui.cB_global.checkState() == 2:
          print "Coché"
          QMessageBox.information(self.iface.mainWindow(),"Erreur",QString('Fonction pas encore implémentée'))
      else:
          print "Décoché"
          tools.createBezier(self)   
          
  def doBezierSVG(self):
      print "Gogogogogo"
      tools.createBezierSVG(self)
      