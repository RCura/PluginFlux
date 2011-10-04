# -*- coding: latin1 -*-

"""
Bibliotheque de fonctions basiques
"""

# Import des libs PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import des libs Qgis
from qgis.core import *
from qgis.gui import *
import pdb



class FDEB_SR:
    """ 
    Classe principale de manipulation
    des flux pour appliquer
    l'algo FDEB.
    """
    
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        
    def test(self):
        print "FDEB SR"
                 
    # tab obj Point
    edgePoints = [[]] 
    # tab Numerique Double
    edgeLengths = []
    # tab de list de CompatibleEdge
    # private List<CompatibleEdge>[] compatibleEdgeLists
  
    # tab obj Point
    edgeStarts = []
    edgeEnds = []

    # tab Numerique Double
    edgeValues = []
  
    # Val numerique Double
    edgeValueMax = 0.0
    edgeValueMin = 0.0
    # Val numerique Int
    numEdges = 0
    cycle = 0
   
    # number of subdivision points (will increase with every cycle)
    P = 0
    # used to keep the double value to keep the stable increase rate
    Pdouble = 0.0
    # Step Size
    S = 0.0 
    # number of iteration steps performed during a cycle
    I = 0

    def __init__(self):
        print "init"

    def bundle(self,numCycles):
        init()

    def init(self):
        myLayer = self.canvas.currentLayer()
        numEdges = myLayer.featureCount()
        edgeLengths = [None] * numEdges
        edgeStarts = [None] * numEdges
        edgeEnds = [None] * numEdges
        evMin = float('-inf')
        evMax = float('+inf')
        # if (params.getEdgeValueAffectsAttraction()) {
        #   edgeValues = new double[numEdges];
        # }

        
        provider = myLayer.dataProvider()
        allAttrs = provider.attributeIndexes()
        provider.select(allAttrs)
        feat = QgsFeature()
        i = 0
        while provider.nextFeature(feat):
            # type Edge ou QgisLine
            edge = feat
            edgeStarts[i] = feat.geometry().asPolyline()[0]
            edgeEnds[i] = feat.geometry().asPolyline()[1]
            length = feat.geometry().length()
            
            if (abs(length) < (1e-7)):
                length = 0.0
            edgeLengths[i] = length
            # if (params.getEdgeValueAffectsAttraction()) {
            #  double value = flowMapGraph.getEdgeWeight(edge, params.getEdgeWeightAttr());
            #  edgeValues[i] = value;
            #  if (value > evMax) {
            #    evMax = value;
            #  }
            #  if (value < evMin) {
            #    evMin = value;
            #  }
            # }
            i += 1
        # if (params.getEdgeValueAffectsAttraction()) {
        #  edgeValueMax = evMax;
        #  edgeValueMin = evMin;
        # }
        I = 100
        P = 1
        Pdouble = 1
        S = 1.0

        self.calcEdgeCompatibilityMeasures(numEdges)

        # ? pourquoi ici ? 
        cycle = 0

    def calcEdgeCompatibilityMeasures(self,numEdges):
        
        compatibleEdgeLists = [None] * numEdges

        for i in range(numEdges):
            compatibleEdgeLists[i] = #new ArrayList<CompatibleEdge>();
            
        numTotal = 0
        numCompatible = 0
        Csum = 0.0
        edgeCompatibilityThreshold = 0.60
  
        for i in range(numEdges):
            for j in range(i):
                
                C = calcEdgeCompatibility(i, j)
                if (abs(C) >= edgeCompatibilityThreshold):
                    compatibleEdgeLists[i] = #(new CompatibleEdge(j, C));
                    compatibleEdgeLists[j] = #(new CompatibleEdge(i, C));
                    numCompatible = numCompatible + 1
                    
                Csum =  CSum + abs(C)
                numTotal = numTotal + 1
