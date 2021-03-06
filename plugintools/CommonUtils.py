# -*- coding: latin1 -*-

"""
Biblioth�que de fonctions basiques
"""

# Import des libs PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import des libs Qgis
from qgis.core import *
from qgis.gui import *
import pdb


class FlowUtils:
    """ 
    Regroupe les outils/fonctions appel�es dans les classes principales
    """
    
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
                 
    def createTempLayer(self, layerType, layerName):
        """
        Cr�e une couche temporaire (stockage m�moire).
        layerType : 'POINT', 'LINESTRING', 'POLYGON'
        """
        
        tmpLayer = QgsVectorLayer(layerType, layerName, "memory")
        tmpLayer.updateExtents()
        QgsMapLayerRegistry().instance().addMapLayer(tmpLayer, True)
        return tmpLayer
          
    def getMapCanvasLayerByName(self, layername):
        layers = self.canvas.layers()  
        for i in range(self.canvas.layerCount()):
            if layers[i].name() == layername:
                if layers[i].isValid():
                    return layers[i]
        return None            
                    
    def exportSVGLineaire(self):
        layer = self.canvas.currentLayer()
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
                        # On multiplie par 900 (au lieu de 1000) pour r�duire la taille des figur�s,
                        # puis on les d�calle de 50 depuis l'origine, pour avoir 50px de marge de chaque c�t�.
                        xsvg = (((xfeat - xmin) / (xmax - xmin)) * 900) + 50
                        ysvg = (((ymax - yfeat) / (ymax - ymin)) * 900) + 50
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
        baseLayer = self.canvas.currentLayer()
        if baseLayer.name().endsWith('_Bezier') == True:
            QMessageBox.information(self.iface.mainWindow(),"Attention !",
                                    'Ne peut �tre r�alis� sur des courbes de Bezier')
        else:
            # Si la couche est bien de type lin�aire,
            # On cr�e une couche ponctuelle CP.
            if (baseLayer.wkbType() == 2):
                layerName = baseLayer.name() + '_CP'
                # Si la couche existe d�j�, on la supprime
                existingLayer = self.getMapCanvasLayerByName(layerName)
                if existingLayer != None:
                    QMessageBox.information(self.iface.mainWindow(),"Attention !",
                                        'La couche existe d�j� et sera donc d�truite.')
                    self.removeLayerFromQgsRegistry(existingLayer.getLayerID())
                    
                layerNameID = 'ID'
                newLayer = self.createTempLayer('POINT', layerName)
                self.addAttributes(newLayer, idFieldName=layerNameID)
                self.completeAttributes(baseLayer, newLayer )
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
        self.canvas.refresh()
        
    def createBezier(self):
        #Defs
        CPLayer = self.canvas.currentLayer()
        
        #Creation nouvelle couche
        if CPLayer.name().endsWith('_CP') == False:
            QMessageBox.information(self.iface.mainWindow(),"Attention !",
                                'Vous devez s�lectionner une couche de Points de Contr�les')
        else:
            BezierName = CPLayer.name().remove('_CP') + '_Bezier'
            existingLayer = self.getMapCanvasLayerByName(BezierName)
            if existingLayer != None:
                QMessageBox.information(self.iface.mainWindow(),"Attention !",
                                    'La couche existe d�j� et sera donc d�truite.')
                self.removeLayerFromQgsRegistry(existingLayer.getLayerID())
            bezierLayer = self.createTempLayer('LINESTRING',BezierName)
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
                myfeat = self.createBezierLine(startPoint, controlPoint, endPoint)
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
            self.canvas.refresh()        
        
    def createBezierLine(self, startPoint, controlPoint, endPoint, nbSegments=30):
        # Creation d'un rubberband
        rb = QgsRubberBand(self.canvas,  True)
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
            
    def removeLayerFromQgsRegistry(self, layerID):
        mapR = QgsMapLayerRegistry().instance()
        mapR.removeMapLayer(layerID)
        
    def convertToSVGCoordinates(self, coordType, coordMin, coordMax, coordValue):
        """
        On entre ici les valeurs (abcisse ou ordonn�e) � convertir dans le syst�me de coordonn�s SVG
        coordType : x ou y
        coordMin : xmin ou ymin
        coordMax : xmax ou ymax
        coordValue : la valeur de x ou y � convertir
        """
        if coordType == 'x':
            convertedX = (((coordValue - coordMin) / (coordMax - coordMin)) * 900) + 50
            return convertedX
        elif coordType == 'y':
            convertedY = (((coordMax - coordValue) / (coordMax - coordMin)) * 900 ) + 50
            return convertedY
        else:
            print "coordType doit �tre �gal � 'x' ou 'y' uniquement"    
        
    def createBezierSVG(self):
        layer = self.canvas.currentLayer()
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
                       
                # Boucle pour cr�er le svg :
                while provider.nextFeature(feat):
                    pathsvg += '<path style="stroke:blue; stroke-width:10; fill:none; " d="M'
                    x1 = self.convertToSVGCoordinates('x', xmin, xmax, feat.attributeMap()[1].toDouble()[0])
                    y1 = self.convertToSVGCoordinates('y', ymin, ymax, feat.attributeMap()[2].toDouble()[0])
                    x2 = self.convertToSVGCoordinates('x', xmin, xmax, feat.attributeMap()[3].toDouble()[0])
                    y2 = self.convertToSVGCoordinates('y', ymin, ymax, feat.attributeMap()[4].toDouble()[0])
                    x3 = self.convertToSVGCoordinates('x', xmin, xmax, feat.attributeMap()[5].toDouble()[0])
                    y3 = self.convertToSVGCoordinates('y', ymin, ymax, feat.attributeMap()[6].toDouble()[0])
                    # Concat�nation des coords svg d'une ligne
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
                                    'L\'export SVG ne fonctionne que pour les shape type Bezier cr��s avec ce Plugin')


    def isSimpleLineLayer(self, layer):
        provider = layer.dataProvider()
        allAttrs = provider.attributeIndexes()
        provider.select(allAttrs)
        feat = QgsFeature()
        isSimple = True
        while provider.nextFeature(feat):
            if (len(feat.geometry().asPolyline()) > 2):
                return False
        return True
    

    def getFieldNbByName(self, layer, fieldName):
        provider = layer.dataProvider()
        provider.select(provider.attributeIndexes())
        for i in range(len(provider.fields())):
            if (str(provider.fields()[i].name()) == fieldName):
                return i
        # Pas de fieldname correspondant
        return None
        
    def attachedCP(self, layer, myIdFeature):
        """
        S'execute sur une couche de type ligne simple :
        Cherche s'il existe un CP correspondant � l'entit� ligne selectionn�e
        returns None s'il n'y en a pas, returns layer + myIdFeature s'il y a.
        """
        CPLayerName = str(layer.name()) + '_CP'
        CPLayer = self.getMapCanvasLayerByName(CPLayerName)
        CPpr = CPLayer.dataProvider()
        CPpr.select(CPpr.attributeIndexes())
        feat = QgsFeature()
        myfield = int(self.getFieldNbByName(CPLayer, "ID"))
        while CPpr.nextFeature(feat):
            featId = str(feat.attributeMap()[myfield].toString())
            if ( featId == str(myIdFeature) ):
                return CPLayer, myIdFeature, feat
        return None
    
        
 