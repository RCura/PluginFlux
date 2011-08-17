# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from ui_control import ui_Control
import resources_rc
    
def testprint():
    print 'Le plugin s\'est bien lanc�'
    
def createTempLayer(layerType, layerName):
    """
    Cr�e une couche temporaire (stockage m�moire).
    layerType : 'POINT', 'LINESTRING', 'POLYGON'
    """
    
    tmpLayer = QgsVectorLayer(layerType, layerName, "memory")
    tmpLayer.updateExtents()
    QgsMapLayerRegistry().instance().addMapLayer(tmpLayer, True)
    return tmpLayer
     
            
def getMapCanvasLayerByName(self, layername):
    mapC = self.iface.mapCanvas()
    
    layers = mapC.layers()
    for i in range(mapC.layerCount()):
        if layers[i].name() == layername:
            if layers[i].isValid():
                return layers[i]
            else:
                return None
        else:
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
                   
            # Boucle pour cr�er le svg :
            while provider.nextFeature(feat):
                linesvg += '<polyline style="stroke:blue; stroke-width:10; fill:none; " points="'
                for ibis in range(len(feat.geometry().asPolyline())):
                    xfeat = feat.geometry().asPolyline()[ibis].x()
                    yfeat = feat.geometry().asPolyline()[ibis].y()
                    xsvg = ((xfeat - xmin) / (xmax - xmin)) * 1000
                    ysvg = ((ymax - yfeat) / (ymax - ymin)) * 1000
                    # Concat�nation des coords svg d'une ligne
                    linesvg += str(int(xsvg)) + "," + str(int(ysvg)) + " "
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

def createCP(self):
    mapC = self.iface.mapCanvas()
    baseLayer = mapC.currentLayer()
    # Si la couche est bien de type lin�aire,
    # On cr�e une couche ponctuelle CP.
    if (baseLayer.wkbType() == 2):
        layerName = baseLayer.name() + '_CP'
        # Si la couche existe d�j�, on la supprime
        existingLayer = getMapCanvasLayerByName(self, layerName)
        if existingLayer != None:
            QMessageBox.information(self.iface.mainWindow(),"Attention !",
                                'La couche existe d�j� et sera donc d�truite.')
            removeLayerFromQgsRegistry(existingLayer.getLayerID())
            
        layerNameID = 'ID_' + baseLayer.name()
        newLayer = createTempLayer('POINT', layerName)
        addAttributes(self, newLayer, idFieldName=layerNameID)
        completeAttributes(self, baseLayer, newLayer )
    # Sinon, on affiche un message d'erreur  
    else: 
        QMessageBox.information(self.iface.mainWindow(),"Erreur !",
                                'La cr�ation de courbes de B�zier requiert une couche lin�aire simple')

def addAttributes(self, layer, idFieldName="ID"):
    pr = layer.dataProvider()
    pr.addAttributes( [ QgsField(idFieldName, QVariant.String) ] )
    pr.addAttributes( [ QgsField("Xstart", QVariant.Double) ] )
    pr.addAttributes( [ QgsField("Ystart", QVariant.Double) ] )
    pr.addAttributes( [ QgsField("Xend", QVariant.Double) ] )
    pr.addAttributes( [ QgsField("Yend", QVariant.Double) ] )
    layer.startEditing()
    layer.commitChanges()

def completeAttributes(self, originLayer, destinationLayer):
    originPR = originLayer.dataProvider()
    destinationPR = destinationLayer.dataProvider()
    # Boucle sur les entit�s de la layer d'origine (� copier donc)
    allAttrs = originPR.attributeIndexes()
    originPR.select(allAttrs)
    feat = QgsFeature()
    
    while originPR.nextFeature(feat):
        ID = feat.attributeMap()[0].toString()
        Xstart = feat.geometry().asPolyline()[0].x()
        Ystart = feat.geometry().asPolyline()[0].y()
        Xend = feat.geometry().asPolyline()[1].x()
        Yend = feat.geometry().asPolyline()[1].y()
        XCP = (Xend + Xstart) / 2
        YCP = (Yend + Ystart) / 2
        newfeat = QgsFeature()
        newfeat.setGeometry( QgsGeometry.fromPoint(QgsPoint(XCP,YCP)) )
        newfeat.setAttributeMap(
        { 
        0 : ID,
        1 : Xstart,
        2 : Ystart,
        3 : Xend,
        4 : Yend
        }
        )
        destinationPR.addFeatures( [ newfeat ] )
        destinationLayer.commitChanges()
        destinationLayer.updateExtents()
    mapC = self.iface.mapCanvas()
    mapC.refresh()
    
def createBezier(self):
    #Defs
    mapC = self.iface.mapCanvas()
    CPLayer = mapC.currentLayer()
    
    #Creation nouvelle couche
    BezierName = CPLayer.name().remove('_CP') + '_Bezier'
    existingLayer = getMapCanvasLayerByName(self, BezierName)
    if existingLayer != None:
        QMessageBox.information(self.iface.mainWindow(),"Attention !",
                            'La couche existe d�j� et sera donc d�truite.')
        removeLayerFromQgsRegistry(existingLayer.getLayerID())
    bezierLayer = createTempLayer('LINESTRING',BezierName)
    CPpr = CPLayer.dataProvider()
    bpr = bezierLayer.dataProvider()
    bpr.addAttributes( [ QgsField('ID', QVariant.String) ] )
    bezierLayer.startEditing()
    bezierLayer.commitChanges()
    
    #On va lire la couche des Points de controle pour peupler la nouvelle couche
    allAttrs = CPpr.attributeIndexes()
    CPpr.select(allAttrs)
    feat = QgsFeature()
    i = 1
    while CPpr.nextFeature(feat):
        startPoint = QgsPoint(float(feat.attributeMap()[1].toString()),float(feat.attributeMap()[2].toString()))
        endPoint = QgsPoint(float(feat.attributeMap()[3].toString()), float(feat.attributeMap()[4].toString()))
        controlPoint = feat.geometry().asPoint()
        myfeat = createBezierLine(self, startPoint, controlPoint, endPoint)
        myfeat.addAttribute(0,feat.attributeMap()[0].toString())
        bpr.addFeatures( [ myfeat ] )
        bezierLayer.commitChanges()
        bezierLayer.updateExtents()
    mapC.refresh()        
    
def createBezierLine(self, startPoint, controlPoint, endPoint, nbSegments=20):
    # Creation d'un rubberband
    mapC = self.iface.mapCanvas()
    rb = QgsRubberBand(mapC,  True)
    # Creation du LineString
    newFeat = QgsFeature()    
    
    # Calcul des points interm�diaires
    tstep = 1.0 / nbSegments
    t = 0.0
    for i in range(nbSegments + 1):
        x = ((1-t)**2) * startPoint.x() + ((2*t)*(1-t)) * controlPoint.x() + (t**2)*endPoint.x()
        y = ((1-t)**2) * startPoint.y() + ((2*t)*(1-t)) * controlPoint.y() + (t**2)*endPoint.y()
        rb.addPoint(QgsPoint(x,y))
        t += tstep
    # Conversion du rubberband en LineString    
    coords = []
    
    for i in range(rb.numberOfVertices()):
        coords.append(rb.getPoint(0, i))
    
    # On cr�e notre g�ometrie qu'on importera dans une nouvelle feature
    newFeat.setGeometry(QgsGeometry().fromPolyline(coords))

    # On supprime le rubberband
    rb.reset()
    return newFeat
        
def removeLayerFromQgsRegistry(layerID):
    mapR = QgsMapLayerRegistry().instance()
    mapR.removeMapLayer(layerID)
    
def createBezierSVG(self):
    mapC = self.iface.mapCanvas()
    layer = mapC.currentLayer()
    if (layer.wkbType() == 2):    
        svgname = QFileDialog.getSaveFileName(None,
                                              "Choisir un nom de fichier et un repertoire",
                                              "~/BezierOutput.svg",
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
                   
            # Boucle pour cr�er le svg :
            while provider.nextFeature(feat):
                linesvg += '<polyline style="stroke:blue; stroke-width:10; fill:none; " points="'
                for ibis in range(len(feat.geometry().asPolyline())):
                    xfeat = feat.geometry().asPolyline()[ibis].x()
                    yfeat = feat.geometry().asPolyline()[ibis].y()
                    xsvg = ((xfeat - xmin) / (xmax - xmin)) * 1000
                    ysvg = ((ymax - yfeat) / (ymax - ymin)) * 1000
                    # Concat�nation des coords svg d'une ligne
                    linesvg += str(int(xsvg)) + "," + str(int(ysvg)) + " "
                # Fin de ligne
                linesvg += '"  />\n'
            # Fin du fichier svg    
            linesvg += '</svg>'
        
            text_file = open(svgname, "w")
            text_file.writelines(linesvg)
            text_file.close()
    else:
        QMessageBox.information(self.iface.mainWindow(),"Erreur !",
                                'L\'export SVG ne fonctionne que pour les shape type Bezier cr��s avec ce Plugin')


    