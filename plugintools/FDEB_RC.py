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
import math
import time as t
import pdb
from CommonUtils import FlowUtils

# FIXME : Les resultats peuvent �tre du grand n'importe-quoi
# Deplacements beaucoup trop importants
# Regarder l'histoire de seuil de d�placement (damping ?)
# SInon, mettre une limite, genre emp�cher que la ligne de fin
# ne fasse plus de 2(?) fois la taille de la ligne d'arriv�e

# TODO : Regarder les commentaires � l'appel de springForces (ligne 386)
# FIXME : Il y a un plantage quand on ne trouve aucun segment compatible


class FDEB_RC:
    """ 
    Classe principale de manipulation
    des flux pour appliquer
    l'algo FDEB.
    """
    
    def __init__(self, iface, myUI):
        self.fdebGUI_RC = myUI
        self.progress = 0
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.layer = self.canvas.currentLayer()
        # contient tous les points : Dim1 : Lignes / Dim2 : Points de la ligne
        self.edgePoints = [[]] 
        self.edgeLengths = []
        # tab de list de CompatibleEdge
        # private List<CompatibleEdge>[] compatibleEdgeLists
        self.compatibleEdgeLists = [[]]
        # tab obj Point
        self.edgeStarts = []
        self.edgeEnds = []
        
        self.edgeValues = []
        self.edgeValueMax = 0.0
        self.edgeValueMin = 0.0
        self.numEdges = 0
        self.cycle = 0
        # number of subdivision points (will increase with every cycle)
        self.P = 0
        # used to keep the double value to keep the stable increase rate
        self.Pdouble = 0.0
        # Step Size
        self.S = 0.0 
        # number of iteration steps performed during a cycle
        
        self.iteration = 0 # Just to know where we are.
        self.edgeCompatibilityThreshold = 0
        self.numCycle = 0
        self.I = 0
        self.maxLength = 0
        self.attractionStrength = 0

        
    def test(self):
        print "FDEB RC"
        #pyqtRemoveInputHook()
        #pdb.set_trace()
        self.numCycle = self.fdebGUI_RC.numCycles.value()
        self.bundle(self.numCycle)

    def bundle(self,numCycles):
        initStartTime = t.time()
        self.init()
        initEndTime = t.time()
        print "Initialisation lasted %s seconds"%(initEndTime - initStartTime)
        self.fdebGUI_RC.progressBar.setValue(0)
        cyclesStartTime = t.time()
        for i in range(numCycles):
            if (i == 0):
                self.progress = 10
            else:
                self.progress = (100 / numCycles) * i
            self.nextCycle()
            self.fdebGUI_RC.progressBar.setValue(self.progress)
        # On sort le updateLines de la boucle
        cyclesEndTime = t.time()
        print "Iteration through cycles took %s seconds"%(cyclesEndTime - cyclesStartTime)
        self.createLines()  
        self.progress = 100
        self.fdebGUI_RC.progressBar.setValue(self.progress)
        print "tout est termin�"
            

    def init(self):
        self.I = self.fdebGUI_RC.numSteps.value()
        myAttractionStrength = self.fdebGUI_RC.attractionStrength.value()
        self.attractionStrength = 10**(-(myAttractionStrength))
        #print self.attractionStrength
        #pyqtRemoveInputHook()
        #pdb.set_trace()
        self.edgeCompatibilityThreshold = self.fdebGUI_RC.compatibilityThreshold.value()
        #print "Threshold : %s / numCycles : %s / numSteps : %s"%(self.edgeCompatibilityThreshold, self.numCycle, self.I )
        self.numEdges = self.layer.featureCount()
        self.edgeLengths = [None] * self.numEdges
        self.edgeStarts = [None] * self.numEdges
        self.edgeEnds = [None] * self.numEdges
        xMin = self.layer.extent().xMinimum()
        xMax = self.layer.extent().xMaximum()
        yMin = self.layer.extent().yMinimum()
        yMax = self.layer.extent().yMaximum()
        self.maxLength = math.sqrt( (xMax-xMin)**2 + (yMax-yMin)**2 )
        evMin = float('-inf') # A conserver pour EdgeValueAffectsAttraction
        evMax = float('+inf') # Idem evMin
        # FIXME : A mettre en place avec les params.
        # /!\ Ce param�tre est tr�s important.
        # if (params.getEdgeValueAffectsAttraction()) {
        #   edgeValues = new double[numEdges];
        # }

        
        provider = self.layer.dataProvider()
        allAttrs = provider.attributeIndexes()
        provider.select(allAttrs)
        feat = QgsFeature()
        i = 0
        while provider.nextFeature(feat):

            # type Edge ou QgisLine
            lastEdge = len(feat.geometry().asPolyline()) - 1
            self.edgeStarts[i] = feat.geometry().asPolyline()[0]
            self.edgeEnds[i] = feat.geometry().asPolyline()[lastEdge]
            length = feat.geometry().length()
            
            if (abs(length) < (1e-7)):
                length = 0.0
            self.edgeLengths[i] = length
            # FIXME : A mettre en place avec les params.
            # /!\ Ce param�tre est tr�s important.
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
        
        # FIXME : A mettre en place avec les params.    
        # if (params.getEdgeValueAffectsAttraction()) {
        #  edgeValueMax = evMax;
        #  edgeValueMin = evMin;
        # }
        self.P = 1
        self.Pdouble = 1
        self.S = 1.0

        self.calcEdgeCompatibilityMeasures(self.numEdges)

        # ? pourquoi ici ? 
        self.cycle = 0

    def calcEdgeCompatibilityMeasures(self,numEdges):
        
        self.compatibleEdgeLists = [[None]] * numEdges
        numCompatible = 0
        initProgress = 0
        numCalcs = float(self.sommeSuite(range(numEdges)))
        for i in range(numEdges):
            initProgress =  (float(self.sommeSuite(range(i))) / numCalcs * 100) + 1
            # print "Calcul des compatibilit�s de %s / %s"%(i, numEdges)
            for j in range(i):
                C = self.calcEdgeCompatibility(i, j)
                if (abs(C) >= self.edgeCompatibilityThreshold):
                    self.compatibleEdgeLists[i].append([j,C])
                    self.compatibleEdgeLists[j].append([i,C])
                    numCompatible = numCompatible + 1
            self.fdebGUI_RC.initProgressBar.setValue(initProgress)
        self.fdebGUI_RC.initProgressBar.setValue(100)
    def calcEdgeCompatibility(self,i,j):
        C = 0.0
        
        # FIXME : A completer, la fonction est pr�te.
        #if (params.getUseSimpleCompatibilityMeasure()) {
        #    C = calcSimpleEdgeCompatibility(i, j);
        #} else {
        C = self.calcStandardEdgeCompatibility(i, j)
        #}

        assert (C >= 0 and C <= 1.0)
        # FIXME : Est-ce vraiment utile ?
        # if (params.getBinaryCompatibility()) {
        #    if (C >= params.getEdgeCompatibilityThreshold()) {
        #        C = 1.0;
        #    } else {
        #        C = 0.0;
        #    }
        # }
        
        # FIXME : On d�gage ?
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
        # i and j are integers
        # We transfer the Lines to i and j

        if (self.isSelfLoop(i) or self.isSelfLoop(j)):
            return 0.0
        id_i = i
        id_j = j
        i = QgsFeature()
        j = QgsFeature()
        provider = self.layer.dataProvider()
        provider.featureAtId(id_i, i)
        provider.featureAtId(id_j, j)    
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
        pm = self.midPoint(P0, P1)
        qm = self.midPoint(P2, P3)        
        l_i = i.geometry().length()
        l_j = j.geometry().length()
        l_avg = (l_i + l_j) / 2

        # Angle compatibility
        Ca = 0.0
        
        # FIXME :A int�grer dans le GUI.
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
        Cp = l_avg / (l_avg + math.sqrt(pm.sqrDist(qm)))

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

        # FIXME : Binary compatibility encore, on d�gage ?
#        if (params.getBinaryCompatibility()) {
#            double threshold = params.getEdgeCompatibilityThreshold();
#            Ca = Ca >= threshold ? 1.0 : 0.0;
#            Cs = Cs >= threshold ? 1.0 : 0.0;
#            Cp = Cp >= threshold ? 1.0 : 0.0;
#            Cv = Cv >= threshold ? 1.0 : 0.0;
#        }
        #print "Ca : %s / Cs : %s / Cp : %s / Cv : %s"%(Ca, Cs, Cp, Cv)
        standardEdgeCompatibility = Ca * Cs * Cp * Cv
        return standardEdgeCompatibility

    def isSelfLoop(self,edgeIdx):
        return self.edgeLengths[edgeIdx] == 0.0
        
    def calcSimpleEdgeCompatibility(self,i, j):
        if (self.isSelfLoop(i) or self.isSelfLoop(j)):
            return 0.0
        l_avg = (self.edgeLengths[i] + self.edgeLengths[j]) / 2
        simpleEdgeCompatibility = (l_avg / (l_avg + math.sqrt(self.edgeStarts[i].sqrDist(self.edgeStarts[j])) + math.sqrt(self.edgeEnds[i].sqrDist(self.edgeEnds[j]))))
        return simpleEdgeCompatibility
        
    def visibilityCompatibility(self, p0, p1, q0, q1):
        # Renvoie les points i0 et i1, projetee de q0 et q1 sur une ligne en continuit� de P0 - P1
        i0 = self.projectPointToLine(p0, p1, q0)
        i1 = self.projectPointToLine(p0, p1, q1)
        # Calcul le point milieu Pm de la ligne P0-P1, et im point milieu de la ligne projete 
        # correspondant aux point I0 I1  
        im = self.midPoint(i0, i1);
        pm = self.midPoint(p0, p1);
        Cv = max(0,(1 - 2 * math.sqrt(pm.sqrDist(im)) / math.sqrt(i0.sqrDist(i1))))
        return Cv
        
        
    def projectPointToLine(self, line1, line2, point) :
  
        x1 = line1.x()
        y1 = line1.y()
        x2 = line2.x()
        y2 = line2.y()
        x = point.x()
        y = point.y()

        L = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
        r = ((y1-y)*(y1-y2) - (x1-x)*(x2-x1)) / (L * L)
        projectedPoint = QgsPoint(x1 + r * (x2-x1), y1 + r * (y2-y1))
        return projectedPoint
        
    def midPoint(self,P0,P1):
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
        
        #pyqtRemoveInputHook()
        #pdb.set_trace()

        #FIXME : A passer en parametre par la suite
        
        
        subdivisionPointsCycleIncreaseRate = 1.3 # Non param�trable dans jFlowMap
        stepDampingFactor = 0.5

        # Set parameters for the next cycle
        # FIXME : Bizarre ...
        if (self.cycle > 0):
            Pdouble = Pdouble * subdivisionPointsCycleIncreaseRate
            P = int(round(Pdouble))
            S = S * (1.0 - stepDampingFactor)
            I = (I * 2) / 3
            
        self.addSubdivisionPoints(P)
            
        # Perform simulation steps

        # init tableau multi-dimensionnel
        tmpEdgePoints = [None] * self.numEdges
        for i in range(len(tmpEdgePoints)):
            tmpEdgePoints[i] = [None] * P
        
        step = 0
        self.iteration = 0
        while (step < I):
            self.iteration = step
            pe = 0
            while (pe < self.numEdges): 
                tmpEdgePoints[pe] = self.computeEdges(pe,tmpEdgePoints[pe],P,S)
                pe = pe + 1 
                # end while pe

            self.copy(tmpEdgePoints, self.edgePoints)
            step = step + 1
            #end step + 1

        # update params only in case of success (i.e. no exception)
        self.P = P
        self.Pdouble = Pdouble
        self.S = S
        self.I = I
        self.cycle = self.cycle + 1

    def computeEdges(self,pe,subTmpEdgePoints,P,S):

        K = 1.0

        # if (isSelfLoop(pe)) {
        #    continue;     // ignore self-loops
        #    }
                
        # final value
        numOfSegments = P + 1
        if ((self.edgeLengths[pe] == 0) or (numOfSegments == 0)):
            k_p = 2
        else:
            k_p = K / (self.edgeLengths[pe] * numOfSegments)
                
        i = 0
        #print "P = " + str(P)
        while (i < P):
            # FIXME : A REVOIR !!! 
            # springForces prend un temps �norme
            # Il doit y avoir un probleme qqpart
            # C'est du calcul simple normalement
            # Essayer de r�duire les acc�s aux points en mettant tout �a en tableau.
            # Tester ce qui prend vraiment la majorit� du temps � l'interieur.
            subTmpEdgePoints = self.springForces(i,S,pe,P,k_p,subTmpEdgePoints)
            i = i + 1
            # print "Cycle : %s / Iteration : %s/%s / pe : %s / k_p: %s" %(self.cycle, self.iteration, self.I, pe, k_p)

        return subTmpEdgePoints

    def springForces(self,i,S,pe,P,k_p,newP):

        useInverseQuadraticModel = False
        repulsionAmount = 1.0
        edgeValueAffectsAttraction = False

        # newP = tmpEdgePoints[pe]
        # p et newP = Point[]
        p = self.edgePoints[pe]

        # List<CompatibleEdge> compatible = compatibleEdgeLists[pe];
        compatible = self.compatibleEdgeLists[pe]
        # spring forces
        p_i = p[i]
        
        if (i == 0):
            p_prev = self.edgeStarts[pe]
        else:
            p_prev = p[i - 1]

        if (i == (P - 1) ):
            p_next = self.edgeEnds[pe] 
        else:
            p_next = p[i + 1]
        if ( (p_prev == None ) or (p_i == None) or (p_next == None) or (p_i == None) ):
            pyqtRemoveInputHook()
            pdb.set_trace()
        Fsi_x = (p_prev.x() - p_i.x()) + (p_next.x() - p_i.x())
        Fsi_y = (p_prev.y() - p_i.y()) + (p_next.y() - p_i.y())
        
        #print "abs (k_p) + " + str(k_p)
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

            if (ce == None):
                ci = ci + 1
                # print "ci > " + str(ci)
                continue

            qe = ce[0] #final value, on recupere un attribut Idx du point ...
            C = ce[1] #final value, idem on recupere un attribut C du point
            q_i = self.edgePoints[qe][i] # q_i = point

            v_x = q_i.x() - p_i.x()
            v_y = q_i.y() - p_i.y()

            # print "v_x = " + str(v_x)
            # print "v_x = " + str(v_x)
            if (abs(v_x) > 1e-7  or abs(v_y) > 1e-7):  # zero vector has no direction
                d = math.sqrt(v_x * v_x + v_y * v_y)  # shouldn't be zero
                m = 0.0
                    
                if (useInverseQuadraticModel):
                    m = (C / d) / (d * d)
                else:
                    #m = (C / d**2)
                    # FIXME : C'est ici que je teste les formules pour adapter d
                    d_weighted = d / (self.maxLength * self.attractionStrength)
                    m = C / d_weighted**2
                    # => Comme les coords de jFlowMap sont entre -100 et +100,
                    # on adapte : Diagonale de l'extent / diagonale max jflowmap
                    #print "C : %s , d : %s, m : %s, maxLength : %s, sqrt : %s"%(C, d, m, self.maxLength, math.sqrt(200**2 + 200**2))
                    # print "m equqal > " + str(m)
 
                if (C < 0):  # means that repulsion is enabled
                    m = m * repulsionAmount
                                 
                if (edgeValueAffectsAttraction):
                    coeff = 1.0 + max(-1.0, (self.edgeValues[qe] - self.edgeValues[pe])/(self.edgeValueMax + self.edgeValueMin))
                    m = m * coeff
                                 
                if (abs(m * S) > 1.0):
                    # // this condition is to reduce the "hairy" effect:
                    # // a point shouldn't be moved farther than to the
                    # // point which attracts it
                    m = self.signum(m) / S
                    # TODO : this force difference shouldn't be neglected
                    # instead it should make it more difficult to move the
                    # point from it's current position: this should reduce
                    # the effect even more
                            
                v_x = v_x * m
                v_y = v_y * m
                Fei_x = Fei_x + v_x
                Fei_y = Fei_y + v_y
            # pyqtRemoveInputHook()
            # pdb.set_trace()                                 
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
        return newP

    # http://download.oracle.com/javase/1,5,0/docs/api/java/lang/Math.html#signum(float)
    def signum(self, int):
        if(int < 0): return -1
        elif(int > 0): return 1
        else: return int

    def copy(self,src, dest):

        if (len(src) != len(dest)) : raise Exception("Src and dest array sizes mismatch")
            
        i = 0
        for i in range(len(src)):
            j = 0
            for j in range(len(src[i])):
                ps = src[i][j]
                if (ps == None):
                    dest[i][j] = None
                else:
                    dest[i][j] = QgsPoint(ps.x(), ps.y())

    def addSubdivisionPoints(self,P):

        prevP = 0
    
        if (self.edgePoints == None  or  len(self.edgePoints) == 0):
            prevP = 0
        else:
            prevP = len(self.edgePoints[0])
        
        # print "prevP = " + str(prevP)

        # bigger array for subdivision points of the next cycle
        # Point[][] newEdgePoints = new Point[numEdges][P];
        newEdgePoints = [[None]] * self.numEdges
        for i in range(len(newEdgePoints)):
            newEdgePoints[i] = [None] * P

        # Add subdivision points
        # i < len(newEdgePoints)
        for i in range(len(newEdgePoints)):
            if (self.isSelfLoop(i)):
                continue   # ignore self-loops
                    
            newPoints = newEdgePoints[i]

            if (self.cycle == 0):
                assert(P == 1)
                newPoints[0] = self.midPoint(self.edgeStarts[i], self.edgeEnds[i])
            else:
                # List<Point> points = new ArrayList<Point>(Arrays.asList(edgePoints[i]));
                points = []
                points = self.edgePoints[i][:]
                points.insert(0, self.edgeStarts[i])
                points.append(self.edgeEnds[i])
                
                polylineLen = 0
                segmentLen = [None] * (prevP + 1)
                        
                # j < prevP +1
                for j in range(prevP + 1):
                    segLen = math.sqrt(points[j].sqrDist(points[j + 1]))
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
        

        self.edgePoints = newEdgePoints

    """
    Returns a point on a segment between the two points
    @param alpha Between 0 and 1
    """
    def between(self, a, b, alpha):
        return QgsPoint(a.x() + (b.x() - a.x()) * alpha,a.y() + (b.y() - a.y()) * alpha)
  
  
# TODO : On ne doit pas organiser les fonctions de "sortie" comme eux
# => On n'a pas l'affichage sous forme de graphes � g�rer
# => Nous, on doit simplement injecter dans nos features leurs nouvelles g�om�trie
    def addEdgeEnds(self):
        for i in range(len(self.edgePoints)):
            if (self.isSelfLoop(i)):
                continue   # ignore self-loops
            else:
                self.edgePoints[i].insert(0, self.edgeStarts[i])
                self.edgePoints[i].append(self.edgeEnds[i])
                 
            
    def createLines(self):
        self.addEdgeEnds()
        newLayerName = "%s_FDEB"%self.layer.name()
        oldLayer = self.layer
        newLayer = FlowUtils(self.iface).createTempLayer("LINESTRING", newLayerName)
        self.layer = newLayer
        oldProvider = oldLayer.dataProvider()
        newProvider = newLayer.dataProvider()
        allAttrs = oldProvider.attributeIndexes()
        oldProvider.select(allAttrs)
        oldFeat = QgsFeature()
        i = 0
        for i in range(len(oldProvider.fields())):
            newProvider.addAttributes([oldProvider.fields()[i]])
        i = 0
        while oldProvider.nextFeature(oldFeat):
            newLayer.startEditing()
            # Create and fill the rubberband
            rb = QgsRubberBand(self.canvas,  True)     
            j = 0
            for j in range(len(self.edgePoints[i])):
                rb.addPoint(self.edgePoints[i][j])
            # Create the geometry list
            coords = []
            for k in range(rb.numberOfVertices()):
                coords.append(rb.getPoint(0,k))
            
            # Set geometry and attributes to new Feature
            newFeat = QgsFeature()
            newFeat.setGeometry(QgsGeometry.fromPolyline(coords))
            newFeat.setAttributeMap(oldFeat.attributeMap())
            newProvider.addFeatures([newFeat])
            newLayer.commitChanges()
            newLayer.updateExtents()
            rb.reset()
            i = i + 1
        newLayer.setUsingRendererV2(True)
        print "SymboV2 : oldLayer : %s / newLayer : %s"%(oldLayer.isUsingRendererV2(),newLayer.isUsingRendererV2() )
        print newLayer.hasCompatibleSymbology(oldLayer)
        print newLayer.copySymbologySettings(oldLayer)
        self.canvas.refresh()
        
        
    def sommeSuite(self, liste):
        def addition(x,y): return x+y
        return reduce(addition, liste, 0)

