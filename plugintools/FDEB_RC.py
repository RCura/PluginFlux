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


    def calcEdgeCompatibility(self,i,j):
        C = 0.0
        
        #if (params.getUseSimpleCompatibilityMeasure()) {
        #    C = calcSimpleEdgeCompatibility(i, j);
        #} else {
        C = calcStandardEdgeCompatibility(i, j)
        #}

        assert (C >= 0 and C <= 1.0)
        # if (params.getBinaryCompatibility()) {
        #    if (C >= params.getEdgeCompatibilityThreshold()) {
        #        C = 1.0;
        #    } else {
        #        C = 0.0;
        #    }
        # }

        # if (params.getUseRepulsionForOppositeEdges()) {
        #    Vector2D p = Vector2D.valueOf(edgeStarts[i], edgeEnds[i]);
        #    Vector2D q = Vector2D.valueOf(edgeStarts[j], edgeEnds[j]);
        #    double cos = p.dot(q) / (p.length() * q.length());
        #    if (cos < 0) {
        #        C = -C;
        #    }
        # }
     
        return C
        
     def calcStandardEdgeCompatibility(self, i, j):
        # i and j are polylines
        if (isSelfLoop(i) or isSelfLoop(j)):
            return 0.0
        # i is a line with P0 and P1 as points
        # j is a line with P2 and P3 as points
        P0 = i.geometry().asPolyline()[0]
        P1 = i.geometry().asPolyline()[1]
        P2 = j.geometry().asPolyline()[0]
        P3 = j.geometry().asPolyline()[1]        
        
        # p and q are the vectorial coordinates of i and j
        p = QgsPoint((P1.x() - P0.x()), (P1.y() - P0.y()))
        q = QgsPoint((P3.x() - P2.x()), (P3.y() - P2.y()))
        # pm = Middle-point of i
        # qm = Middle-point of j
        pm = self.midpoint(P0, P1)
        qm = self.midpoint(P2, P3)        
        l_i = i.geometry.length()
        l_j = j.geometry().length()
        l_avg = (l_i + l_j) / 2

        # Angle compatibility
        Ca = 0.0
        # if (params.getDirectionAffectsCompatibility()) {
        #    Ca = (p.dot(q) / (p.length() * q.length()) + 1.0) / 2.0;
        #} else {
        # pq = Scalar product of p and q
        pq = p.x() * q.x() + p.y() * q.y()
        
        # Angle calculation
        Ca = abs(pq / (l_i * l_j ))
        #}
        if abs(Ca) < 1e-7:
            Ca = 0.0
        if (abs(abs(Ca) - 1.0) < 1e-7):
            Ca = 1.0

        # scale compatibility
        Cs = 2 / ( (l_avg / min(l_i, l_j)) + (max(l_i, l_j) / l_avg) )

        # position compatibility
        Cp = l_avg / (l_avg + sqrt(pm.distance(qm)))

        # visibility compatibility
        Cv = 0.0
        if (Ca * Cs * Cp > .9):
            # this compatibility measure is only applied if the edges are
            # (almost) parallel, equal in length and close together
            Cv = min(self.visibilityCompatibility(P0,P1,P2,P3), self.visibilityCompatibility(P2,P3,P0,P1))
        else:
            Cv = 1.0

        assert (Ca >= 0 and Ca <= 1)
        assert (Cs >= 0 and Cs <= 1)
        assert (Cp >= 0 and Cp <= 1)
        assert (Cv >= 0 and Cv <= 1)

#        if (params.getBinaryCompatibility()) {
#            double threshold = params.getEdgeCompatibilityThreshold();
#            Ca = Ca >= threshold ? 1.0 : 0.0;
#            Cs = Cs >= threshold ? 1.0 : 0.0;
#            Cp = Cp >= threshold ? 1.0 : 0.0;
#            Cv = Cv >= threshold ? 1.0 : 0.0;
#        }
        standardEdgeCompatibility = Ca * Cs * Cp * Cv
        return standardEdgeCompatibility

         