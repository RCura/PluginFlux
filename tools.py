# -*- coding: latin1 -*-

"""
Bibliothèque de fonctions basiques
"""

# Import des libs PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import des libs Qgis
from qgis.core import *
from qgis.gui import *

# Import des resources Qt
import resources

# Import des libs du plugin
from ui_control import ui_Control



    
def testprint(self):
    print self
    print 'Le plugin s\'est bien lancé'
    
def createTempLayer(layerType, layerName):
    """
    Crée une couche temporaire (stockage mémoire).
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
                   
            # Boucle pour créer le svg :
            while provider.nextFeature(feat):
                linesvg += '<polyline style="stroke:blue; stroke-width:10; fill:none; " points="'
                for ibis in range(len(feat.geometry().asPolyline())):
                    xfeat = feat.geometry().asPolyline()[ibis].x()
                    yfeat = feat.geometry().asPolyline()[ibis].y()
                    # On multiplie par 900 (au lieu de 1000) pour réduire la taille des figurés,
                    # puis on les décalle de 50 depuis l'origine, pour avoir 50px de marge de chaque côté.
                    xsvg = (((xfeat - xmin) / (xmax - xmin)) * 900) + 50
                    ysvg = (((ymax - yfeat) / (ymax - ymin)) * 900) + 50
                    # Concaténation des coords svg d'une ligne
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
    if baseLayer.name().endsWith('_Bezier') == True:
        QMessageBox.information(self.iface.mainWindow(),"Attention !",
                                'Ne peut être réalisé sur des courbes de Bezier')
    else:
        # Si la couche est bien de type linéaire,
        # On crée une couche ponctuelle CP.
        if (baseLayer.wkbType() == 2):
            layerName = baseLayer.name() + '_CP'
            # Si la couche existe déjà, on la supprime
            existingLayer = getMapCanvasLayerByName(self, layerName)
            if existingLayer != None:
                QMessageBox.information(self.iface.mainWindow(),"Attention !",
                                    'La couche existe déjà et sera donc détruite.')
                removeLayerFromQgsRegistry(existingLayer.getLayerID())
                
            layerNameID = 'ID_' + baseLayer.name()
            newLayer = createTempLayer('POINT', layerName)
            addAttributes(self, newLayer, idFieldName=layerNameID)
            completeAttributes(self, baseLayer, newLayer )
        # Sinon, on affiche un message d'erreur  
        else: 
            QMessageBox.information(self.iface.mainWindow(),"Erreur !",
                                    'La création de courbes de Bézier requiert une couche linéaire simple')

def addAttributes(self, layer, idFieldName="ID"):
    pr = layer.dataProvider()
    pr.addAttributes( [ QgsField(idFieldName, QVariant.String) ] )
    pr.addAttributes( [ QgsField("Xstart", QVariant.Double) ] )
    pr.addAttributes( [ QgsField("Ystart", QVariant.Double) ] )
    pr.addAttributes( [ QgsField("Xend", QVariant.Double) ] )
    pr.addAttributes( [ QgsField("Yend", QVariant.Double) ] )
    layer.startEditing()
    layer.commitChanges()
    self.pluginGui.textEdit.setText('TEST 5687686567579')

def completeAttributes(self, originLayer, destinationLayer):
    originPR = originLayer.dataProvider()
    destinationPR = destinationLayer.dataProvider()
    # Boucle sur les entités de la layer d'origine (à copier donc)
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
    if CPLayer.name().endsWith('_CP') == False:
        QMessageBox.information(self.iface.mainWindow(),"Attention !",
                            'Vous devez sélectionner une couche de Points de Contrôles')
    else:
        BezierName = CPLayer.name().remove('_CP') + '_Bezier'
        existingLayer = getMapCanvasLayerByName(self, BezierName)
        if existingLayer != None:
            QMessageBox.information(self.iface.mainWindow(),"Attention !",
                                'La couche existe déjà et sera donc détruite.')
            removeLayerFromQgsRegistry(existingLayer.getLayerID())
        bezierLayer = createTempLayer('LINESTRING',BezierName)
        CPpr = CPLayer.dataProvider()
        bpr = bezierLayer.dataProvider()
        bpr.addAttributes([ QgsField('ID', QVariant.String) ] )
        bpr.addAttributes([ QgsField('xP0', QVariant.Double) ] )
        bpr.addAttributes([ QgsField('yP0', QVariant.Double) ] )
        bpr.addAttributes([ QgsField('xP1', QVariant.Double) ] )
        bpr.addAttributes([ QgsField('yP1', QVariant.Double) ] )
        bpr.addAttributes([ QgsField('xP2', QVariant.Double) ] )
        bpr.addAttributes([ QgsField('yP2', QVariant.Double) ] )
        bezierLayer.startEditing()
        bezierLayer.commitChanges()
        
        #On va lire la couche des Points de controle pour peupler la nouvelle couche
        allAttrs = CPpr.attributeIndexes()
        CPpr.select(allAttrs)
        feat = QgsFeature()
        while CPpr.nextFeature(feat):
            startPoint = QgsPoint(float(feat.attributeMap()[1].toString()),float(feat.attributeMap()[2].toString()))
            endPoint = QgsPoint(float(feat.attributeMap()[3].toString()), float(feat.attributeMap()[4].toString()))
            controlPoint = feat.geometry().asPoint()
            myfeat = createBezierLine(self, startPoint, controlPoint, endPoint)
            myfeat.setAttributeMap(
            { 
            0 : feat.attributeMap()[0].toString(),
            1 : startPoint.x(),
            2 : startPoint.y(),
            3 : controlPoint.x(),
            4 : controlPoint.y(),
            5 : endPoint.x(),
            6 : endPoint.y()
            }
            )
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
    
    # Calcul des points intermédiaires
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
    
    # On crée notre géometrie qu'on importera dans une nouvelle feature
    newFeat.setGeometry(QgsGeometry().fromPolyline(coords))

    # On supprime le rubberband
    rb.reset()
    return newFeat
        
def removeLayerFromQgsRegistry(layerID):
    mapR = QgsMapLayerRegistry().instance()
    mapR.removeMapLayer(layerID)
    
def convertToSVGCoordinates(coordType, coordMin, coordMax, coordValue):
    """
    On entre ici les valeurs (abcisse ou ordonnée) à convertir dans le système de coordonnés SVG
    coordType : x ou y
    coordMin : xmin ou ymin
    coordMax : xmax ou ymax
    coordValue : la valeur de x ou y à convertir
    """
    if coordType == 'x':
        convertedX = (((coordValue - coordMin) / (coordMax - coordMin)) * 900) + 50
        print convertedX
        print type(convertedX)
        return convertedX
    elif coordType == 'y':
        convertedY = (((coordMax - coordValue) / (coordMax - coordMin)) * 900 ) + 50
        return convertedY
    else:
        print "coordType doit être égal à 'x' ou 'y' uniquement"    
    
def createBezierSVG(self):
    mapC = self.iface.mapCanvas()
    layer = mapC.currentLayer()
    if (layer.wkbType() == 2) and (layer.name().endsWith('_Bezier') == True) :    
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
            
            pathsvg = '<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?> \n' + \
            '<svg xmlns="http://www.w3.org/2000/svg"' + \
            ' width="1000" height="1000" version="1.1" x="test" xmlns:xlink="http://www.w3.org/1999/xlink"  >\n \n'
                   
            # Boucle pour créer le svg :
            while provider.nextFeature(feat):
                pathsvg += '<path style="stroke:blue; stroke-width:10; fill:none; " d="M'
                x1 = convertToSVGCoordinates('x', xmin, xmax, feat.attributeMap()[1].toDouble()[0])
                y1 = convertToSVGCoordinates('y', ymin, ymax, feat.attributeMap()[2].toDouble()[0])
                x2 = convertToSVGCoordinates('x', xmin, xmax, feat.attributeMap()[3].toDouble()[0])
                y2 = convertToSVGCoordinates('y', ymin, ymax, feat.attributeMap()[4].toDouble()[0])
                x3 = convertToSVGCoordinates('x', xmin, xmax, feat.attributeMap()[5].toDouble()[0])
                y3 = convertToSVGCoordinates('y', ymin, ymax, feat.attributeMap()[6].toDouble()[0])
                # Concaténation des coords svg d'une ligne
                pathsvg += str(int(x1)) + "," + str(int(y1)) + " "
                pathsvg += "Q" + str(int(x2)) + "," + str(int(y2)) + " "
                pathsvg += str(int(x3)) + "," + str(int(y3))
                # Fin de ligne
                pathsvg += '"  />\n'
            # Fin du fichier svg    
            pathsvg += '</svg>'
        
            text_file = open(svgname, "w")
            text_file.writelines(pathsvg)
            text_file.close()
    else:
        QMessageBox.information(self.iface.mainWindow(),"Erreur !",
                                'L\'export SVG ne fonctionne que pour les shape type Bezier créés avec ce Plugin')



    