# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

from ui_control import ui_Control
import resources_rc

class Proto1:

  def __init__(self, iface):
    self.iface = iface

  def initGui(self):
    # create action that will start plugin configuration
    self.action = QAction(QIcon(":/icon.png"), "Proto1", self.iface.mainWindow())
    self.action.setWhatsThis("Configuration for test plugin")
    self.action.setStatusTip("This is status tip")

    # connect the action to the run method
    QObject.connect(self.action, SIGNAL("activated()"), self.run)

    # add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&Proto1", self.action)

  def unload(self):
    # remove the plugin menu item and icon
    self.iface.removePluginMenu("&Proto1",self.action)
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
        QObject.connect(self.pluginGui.pB_exportSVG, SIGNAL('clicked()'),self.doExportSVG)
        
        self.pluginGui.textEdit.setText(expText)
        self.pluginGui.show()

  def doClose(self):
    self.pluginGui.reject()

  def doShow(self):
    infoString = QString("Hello, Robin!")
    QMessageBox.information(self.iface.mainWindow(),"About",infoString)
    
  def doExportSVG(self):
    mapC = self.iface.mapCanvas()
    layer = mapC.currentLayer()
    if (layer.wkbType() == 2):    
        svgname = QFileDialog.getSaveFileName(None,
                                              "Choisir un nom de fichier et un repertoire",
                                              "~/output.svg",
                                              "*.svg"
                                              )
        if (svgname == ''):
            QMessageBox.information(self.iface.mainWindow(),"Erreur !",'On annule tout')
        else:
            provider = layer.dataProvider()
            allAttrs = provider.attributeIndexes()
            provider.select(allAttrs)
            feat = QgsFeature()
            
            
            xmin = layer.extent().xMinimum()
            xmax = layer.extent().xMaximum()
            ymin = layer.extent().yMinimum()
            ymax = layer.extent().yMaximum()
            
            linesvg = '<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?> \n' + \
            '<svg xmlns="http://www.w3.org/2000/svg"' + \
            ' width="1000" height="1000" version="1.1" x="test" xmlns:xlink="http://www.w3.org/1999/xlink"  >\n \n'
                   
            # Boucle pour créer le svg :
            provider.nextFeature(feat)
            for i in range(layer.featureCount()):
                linesvg += '<polyline style="stroke:blue; stroke-width:10; fill:none; " points="'
                for ibis in range(len(feat.geometry().asPolyline())):
                    xfeat = feat.geometry().asPolyline()[ibis].x()
                    yfeat = feat.geometry().asPolyline()[ibis].y()
                    xsvg = ((xfeat - xmin) / (xmax - xmin)) * 1000
                    ysvg = ((ymax - yfeat) / (ymax - ymin)) * 1000
                    # Concaténation des coords svg d'une ligne
                    linesvg += str(int(xsvg)) + "," + str(int(ysvg)) + " "
                provider.nextFeature(feat)
                # Fin de ligne
                linesvg += '"  />\n'
            # Fin du fichier svg    
            linesvg += '</svg>'
        
            text_file = open(svgname, "w")
            text_file.writelines(linesvg)
            text_file.close()
    else:
        QMessageBox.information(self.iface.mainWindow(),"Erreur !",
                                'L\'export SVG ne fonctionne que pour les shape de type lineaires')

