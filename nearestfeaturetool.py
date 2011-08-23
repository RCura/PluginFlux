# -*- coding: latin1 -*-

"""
Outil de selection de la feature la plus proche du clic, dans l'ensemble des couches affichées.
Based on Stefan Ziegler Nearest Plugin, thanks to him.
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
import tools

class SelectNearestFeature(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self,canvas)
        self.canvas = canvas
        
        self.index = None

        ## Our own fancy cursor.
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                  "      c None",
                                  ".     c #FF0000",
                                  "+     c #FFFFFF",
                                  "                ",
                                  "       +.+      ",
                                  "      ++.++     ",
                                  "     +.....+    ",
                                  "    +.     .+   ",
                                  "   +.   .   .+  ",
                                  "  +.    .    .+ ",
                                  " ++.    .    .++",
                                  " ... ...+... ...",
                                  " ++.    .    .++",
                                  "  +.    .    .+ ",
                                  "   +.   .   .+  ",
                                  "   ++.     .+   ",
                                  "    ++.....+    ",
                                  "      ++.++     ",
                                  "       +.+      "]))
                                  
    def canvasPressEvent(self,event):
        pass
  
    def canvasMoveEvent(self,event):
        pass
  
    def canvasReleaseEvent(self,event):
        layer = self.canvas.currentLayer()
        clickedCoords = self.toLayerCoordinates( layer, event.pos() )
        bestLayer, bestFeatureID = self.findNearestFeature(clickedCoords)
        self.emit( SIGNAL( "featureFound(PyQt_PyObject)" ), [bestLayer, bestFeatureID] )
            
    def activate(self):
        self.canvas.setCursor(self.cursor)
  
    def deactivate(self):
        pass

    def isZoomTool(self):
        return False
  
    def isTransient(self):
        return False
    
    def isEditTool(self):
        return True
        
                    
    def findNearestFeature(self, clickedcoords):
        layers = self.canvas.layers()
        minDist = float('inf')
        for i in range(len(layers)): 
            myLayer = layers[i]
            if type(myLayer) != QgsVectorLayer:
                break
             
            provider = myLayer.dataProvider()
            allAttr = provider.attributeIndexes()
            provider.select(allAttr)
            feat = QgsFeature()         
            sindex = QgsSpatialIndex()
            myclick = QgsGeometry.fromPoint(clickedcoords)
            otherfeat = QgsFeature()
             
            if myLayer.geometryType == 0:
                while provider.nextFeature(feat):
                    sindex.insertFeature(feat)    
                    nearest = sindex.nearestNeighbor(clickedcoords, 1)
                    myLayer.featureAtId(nearest[0], otherfeat, True, True)
                    currentDistance = myclick.distance( otherfeat.geometry() )
                    if currentDistance < minDist:
                        minDist = currentDistance
                        minId = nearest[0]
                        minLayer = myLayer
            else:
                while provider.nextFeature(feat):
                    myLayer.featureAtId(feat.id(), otherfeat, True, True)
                    currentDistance = myclick.distance( otherfeat.geometry() )
                    if currentDistance < minDist:
                        minDist = currentDistance
                        minId = feat.id()
                        minLayer = myLayer
        return minLayer, minId 