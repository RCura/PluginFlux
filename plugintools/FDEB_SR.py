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
                 
    

    def __init__(self):
        print "init"
        # tab obj Point
        edgePoints = [][] 
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
        
    def bundle(self,numCycles):
        init()

    def init(self):
        mapC = self.iface.mapCanvas()
        myLayer = mapC.currentLayer()
        numEdges = myLayer.featureCount()
        edgeLengths = [None] * numEdges
        edgeStarts = [None] * numEdges
        edgeEnds = [None] * numEdges
        evMin = float(-inf)
        evMax = float(+inf)
        # if (params.getEdgeValueAffectsAttraction()) {
        #   edgeValues = new double[numEdges];
        # }


        for i in range(numEdges):
            # type Edge ou QgisLine
            edge = #Recuperer l'ensemble des aretes du graphe
            edgeStarts[i] = Recuperer le Point de depart de cette ligne
            edgeEnds[i] = Recuperer le Point de fin de cette ligne
            length = #taille de l'arrete = distance point de depart Ã  point d'arrivÃ©e
            
            if (abs(length) < 1e-7):
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
   

        # if (params.getEdgeValueAffectsAttraction()) {
        #  edgeValueMax = evMax;
        #  edgeValueMin = evMin;
        # }
        I = 100
        P = 1
        Pdouble = 1
        S = 1.0

        calcEdgeCompatibilityMeasures(numEdges)

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


    # private static class CompatibleEdge {
    #
    #      public CompatibleEdge(int edgeIdx, double c) {
    #          this.edgeIdx = edgeIdx;
    #          C = c;
    #      }
    #      final int edgeIdx;
    #      final double C;
    #  }

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
    
    #Renvoi un boolean
    def isSelfLoop(self,edgeIdx):
        return edgeLengths[edgeIdx] == 0.0
    
    def calcSimpleEdgeCompatibility(self,i, j):
        if (isSelfLoop(i) or isSelfLoop(j)):
            return 0.0

        l_avg = (edgeLengths[i] + edgeLengths[j]) / 2
        return (l_avg / (l_avg + sqrt(edgeStarts[i].sqrDist(edgeStarts[j])) + sqrt(edgeEnds[i].sqrDist(edgeEnds[j]))))

    def visibilityCompatibility(self, p0, p1, q0, q1):
        # Renvoie les points i0 et i1, projetee de q0 et q1 sur une ligne en continuité de P0 - P1
        i0 = self.projectPointToLine(p0, p1, q0)
        i1 = self.projectPointToLine(p0, p1, q1)
        # Calcul le point milieu Pm de la ligne P0-P1, et im point milieu de la ligne projete 
        # correspondant aux point I0 I1  
        im = self.midPoint(i0, i1);
        pm = self.midPoint(p0, p1);

        return max(0,(1 - 2 * sqrt(pm.sqrDist(im)) / sqrt(i0.sqrDist(i1))))
 
    def projectPointToLine(self, line1, line2, point) :
  
        x1 = line1.x()
        y1 = line1.y()
        x2 = line2.x()
        y2 = line2.y()
        x = point.x()
        y = point.y()

        L = sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
        r = ((y1-y)*(y1-y2) - (x1-x)*(x2-x1)) / (L * L)

        return QgsPoint(x1 + r * (x2-x1), y1 + r * (y2-y1))
    
 
    def midPoint(P0,P1):

        Xstart = P0.x() 
        Ystart = P0.y()
        Xend = P1.x()
        Yend = P1.y()
        XCP = (Xend + Xstart) / 2
        YCP = (Yend + Ystart) / 2
        
        return QgsPoint(XCP,YCP)
