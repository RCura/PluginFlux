# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from ui_control import ui_Control
import resources_rc
    
def testprint():
    print 'Le plugin s\'est bien lancé'
    
def createTempLayer(layerType, layerName):
      tmpLayer = QgsVectorLayer(layerType, layerName, "memory")
      tmpLayer.updateExtents()
      QgsMapLayerRegistry().instance().addMapLayer(tmpLayer, True)
      return tmpLayer
      
# Pris dans l'extension cadTools   
def getLayerByName(layername):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.name() == layername:
            if layer.isValid():
                return layer
            else:
                print "Couche non valide"
                return None
        else:
            print 'Aucune couche ne porte ce nom'
            return None
            
def exportSVGLineaire(self):
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
