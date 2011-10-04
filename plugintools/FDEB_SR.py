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

    def __init__(self):
        print "init"

    def bundle(self,numCycles):
        init()

    def init(self):

        # numEdges = flowMapGraph.getGraph().getEdgeCount()
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
            length = #taille de l'arrete = distance point de depart à point d'arrivée
            
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
    
    def double calcSimpleEdgeCompatibility(self,i, j):
        if (isSelfLoop(i) or isSelfLoop(j)):
            return 0.0

        l_avg = (edgeLengths[i] + edgeLengths[j]) / 2
        # return l_avg / (l_avg + edgeStarts[i].distanceTo(edgeStarts[j]) + edgeEnds[i].distanceTo(edgeEnds[j]))

    def double calcStandardEdgeCompatibility(self, i, j):
        
        if (isSelfLoop(i) or isSelfLoop(j)):
            return 0.0

        Vector2D p = Vector2D.valueOf(edgeStarts[i], edgeEnds[i]);
        Vector2D q = Vector2D.valueOf(edgeStarts[j], edgeEnds[j]);
        Point pm = GeomUtils.midpoint(edgeStarts[i], edgeEnds[i]);
        Point qm = GeomUtils.midpoint(edgeStarts[j], edgeEnds[j]);
        double l_avg = (edgeLengths[i] + edgeLengths[j]) / 2;

        // angle compatibility
        double Ca;
        if (params.getDirectionAffectsCompatibility()) {
            Ca = (p.dot(q) / (p.length() * q.length()) + 1.0) / 2.0;
        } else {
            Ca = Math.abs(p.dot(q) / (p.length() * q.length()));
        }
        if (Math.abs(Ca) < EPS) {
            Ca = 0.0;
        }     // this led to errors (when Ca == -1e-12)
        if (Math.abs(Math.abs(Ca) - 1.0) < EPS) {
            Ca = 1.0;
        }

        // scale compatibility
        double Cs = 2 / ((l_avg / Math.min(edgeLengths[i], edgeLengths[j]))
                + (Math.max(edgeLengths[i], edgeLengths[j]) / l_avg));

        // position compatibility
        double Cp = l_avg / (l_avg + pm.distanceTo(qm));

        // visibility compatibility
        double Cv;
        if (Ca * Cs * Cp > .9) {
            // this compatibility measure is only applied if the edges are
            // (almost) parallel, equal in length and close together
            Cv = Math.min(
                    visibilityCompatibility(edgeStarts[i], edgeEnds[i], edgeStarts[j], edgeEnds[j]),
                    visibilityCompatibility(edgeStarts[j], edgeEnds[j], edgeStarts[i], edgeEnds[i]));
        } else {
            Cv = 1.0;
        }

        assert (Ca >= 0 && Ca <= 1);
        assert (Cs >= 0 && Cs <= 1);
        assert (Cp >= 0 && Cp <= 1);
        assert (Cv >= 0 && Cv <= 1);

        if (params.getBinaryCompatibility()) {
            double threshold = params.getEdgeCompatibilityThreshold();
            Ca = Ca >= threshold ? 1.0 : 0.0;
            Cs = Cs >= threshold ? 1.0 : 0.0;
            Cp = Cp >= threshold ? 1.0 : 0.0;
            Cv = Cv >= threshold ? 1.0 : 0.0;
        }

        return Ca * Cs * Cp * Cv;
    }
