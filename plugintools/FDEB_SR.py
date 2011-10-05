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
        simpleEdgeCompatibility = (l_avg / (l_avg + sqrt(edgeStarts[i].sqrDist(edgeStarts[j])) + sqrt(edgeEnds[i].sqrDist(edgeEnds[j]))))
        return simpleEdgeCompatibility

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

   
    def nextCycle(self):
        
        Pdouble = self.Pdouble
        P = self.P
        S = self.S
        I = self.I
        
        # A passer en parametre par la suite
        useInverseQuadraticModel = False
        K = 1.0
        repulsionAmount = 1.0
        edgeValueAffectsAttraction = False
        subdivisionPointsCycleIncreaseRate = 1.3
        stepDampingFactor = 0.5

        # Set parameters for the next cycle
        # Bizarre ...
        if (cycle > 0):
            Pdouble = Pdouble * params.subdivisionPointsCycleIncreaseRate
            P = Int(round(Pdouble))
            S = S * (1.0 - stepDampingFactor)
            I = (I * 2) / 3
    
            
        self.addSubdivisionPoints(P)
            
        # Perform simulation steps

        # init tableau multi-dimensionnel
        # Point[][] tmpEdgePoints = new Point[numEdges][P];
        tmpEdgePoints = [None] * numEdges
        for i in tmpEdgePoints:
            tmpEdgePoints[i] = [None] * P
        
        step = 0
        while (step < I):
            
            pe = 0
            while (pe < numEdges): 
               
                #p et newP = Point[]
                p = edgePoints[pe]
                newP = tmpEdgePoints[pe]

                # if (isSelfLoop(pe)) {
                #    continue;     // ignore self-loops
                #    }
                
                # final value
                numOfSegments = P + 1
                
                k_p = K / (edgeLengths[pe] * numOfSegments);
                
                # List<CompatibleEdge> compatible = compatibleEdgeLists[pe];
                compatible = compatibleEdgeLists[pe]
                
                i = 0
                while (i < P):
                    # spring forces
                    p_i = p[i]

                    if (i == 0):
                        p_prev = edgeStarts[pe]
                    else:
                        p_prev = p[i - 1]

                    if (i = P - 1 ):
                        p_next = edgeEnds[pe] 
                    else:
                        p_next = p[i + 1]

                    Fsi_x = (p_prev.x() - p_i.x()) + (p_next.x() - p_i.x())
                    Fsi_y = (p_prev.y() - p_i.y()) + (p_next.y() - p_i.y())
                    
                    if (abs(k_p) < 1.0):
                        Fsi_x = Fsi_x * k_p
                        Fsi_y = Fsi_y * k_p
        
                    # attracting electrostatic forces (for each other compatible edge)
                    Fei_x = 0
                    Fei_y = 0

                    size = len(compatible)
                    ci = 0

                    while(ci < size):
                        ce = compatible[ci]
                        
                        qe = ce.edgeIdx #final value, on recupere un attribut Idx du point ...
                        C = ce.C #final value, idem on recupere un attribut C du point
                        q_i = edgePoints[qe][i] # q_i = point 
                         
                        v_x = q_i.x() - p_i.x();
                        v_y = q_i.y() - p_i.y();
                         
                        if (abs(v_x) > 1e-7  or abs(v_y) > 1e-7):  # zero vector has no direction
                             
                            d = sqrt(v_x * v_x + v_y * v_y)  # shouldn't be zero
                            m = 0.0

                            if (useInverseQuadraticModel):
                                m = (C / d) / (d * d)
                            else:
                                m = (C / d) / d
                                 
                            if (C < 0):  # means that repulsion is enabled
                                m = m * repulsionAmount
                                 
                            if (edgeValueAffectsAttraction):
                                coeff = 1.0 + max(-1.0, (edgeValues[qe] - edgeValues[pe])/(edgeValueMax + edgeValueMin))
                                m = m * coeff
                                 
                            if (abs(m * S) > 1.0):
                              #// this condition is to reduce the "hairy" effect:
                              #// a point shouldn't be moved farther than to the
                              #// point which attracts it
                                m = self.signum(m) / S
                              # TODO: this force difference shouldn't be neglected
                              # instead it should make it more difficult to move the
                              # point from it's current position: this should reduce
                              # the effect even more
                                 
                            v_x = v_w * m
                            v_y = v_y * m
                            Fei_x = Fei_x + v_x
                            Fei_y = Fei_y + v_y
                             
                            ci = ci + 1
                            # end while ci
    
                    Fpi_x = Fsi_x + Fei_x
                    Fpi_y = Fsi_y + Fei_y

                    # np est un Point
                    np = newP[i]
                    if (np == None):
                        np = QgsPoint(p[i].x(), p[i].y())
                         
                    np = QgsPoint(np.x() + Fpi_x * S, np.y() + Fpi_y * S)
                    newP[i] = np
                    i = i +1
                    #end while i

                pe = pe + 1 
                # end while pe

            self.copy(tmpEdgePoints, edgePoints);
            
            step = step + 1
            #end step + 1

            # update params only in case of success (i.e. no exception)
            self.P = P
            self.Pdouble = Pdouble
            self.S = S
            self.I = I
            cycle = cycle +1

    # http://download.oracle.com/javase/1,5,0/docs/api/java/lang/Math.html#signum(float)
    def signum(self, int):
        if(int < 0): return -1;
        elif(int > 0): return 1;
        else: return int;

    def copy(self,src, dest):

        if (len(src) != len(dest)) : raise Exception("Src and dest array sizes mismatch")
            
        i = 0
        for i in range(len(src)):
            j = 0
            for j in range(len(src[i])):
                ps = src[i][j]
                if (ps == null):
                    dest[i][j] = null
                else:
                    dest[i][j] = QgsPoint(ps.x(), ps.y())
    

    def addSubdivisionPoints(P):

        prevP = 0
    
        if (edgePoints == null  or  edgePoints.length == 0):
            prevP = 0
        else:
            prevP = len(edgePoints[0])

        # bigger array for subdivision points of the next cycle
        # Point[][] newEdgePoints = new Point[numEdges][P];
        newEdgePoints = [None] * numEdges
        for i in newEdgePoints:
            newEdgePoints[i] = [None] * P

        # Add subdivision points
        # i < len(newEdgePoints)
        for i in range len(newEdgePoints):
            if (self.isSelfLoop(i)):
                continue   # ignore self-loops
                    
            newPoints = newEdgePoints[i]
            if (cycle == 0):
                assert(P == 1)
                newPoints[0] = self.midpoint(edgeStarts[i], edgeEnds[i])
            else:
                # List<Point> points = new ArrayList<Point>(Arrays.asList(edgePoints[i]));
                points = edgePoints[i]
                points.insert(0, edgeStarts[i])
                points.append(edgeEnds[i])

                polylineLen = 0
                segmentLen = [None] * (prevP + 1)
                        
                # j < prevP +1
                for j in range(prevP + 1):
                    segLen = sqr(points[j].sqrDist(points[j + 1]))
                    segmentLen[j] = segLen
                    polylineLen = polylineLen + segLen
                            
                L = polylineLen / (P + 1)
                curSegment = 0
                prevSegmentsLen = 0
                # Recupere points
                p = points[0]
                nextP = points[1]

                # j < P
                for j in range(P): 
                    while (segmentLen[curSegment] < L * (j + 1) - prevSegmentsLen):
                        prevSegmentsLen = prevSegmentsLen + segmentLen[curSegment]
                        curSegment = curSegment + 1
                        p = points[curSegment]
                        nextP = points[curSegment + 1]
                                
                    d = L * (j + 1) - prevSegmentsLen
                    newPoints[j] = self.between(p, nextP, d / segmentLen[curSegment])
        
        edgePoints = newEdgePoints

    """
    Returns a point on a segment between the two points
    @param alpha Between 0 and 1
    """
    def between(self, a, b, alpha):
        return QgsPoint(a.x() + (b.x() - a.x()) * alpha,a.y() + (b.y() - a.y()) * alpha)
  
