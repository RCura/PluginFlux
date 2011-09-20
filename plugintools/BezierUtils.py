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
from CommonUtils import FlowUtils
from nearestfeaturetool import SelectNearestFeature


class BezierUtils:
    """ 
    Regroupe les outils/fonctions appelées dans les classes principales
    """
    
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
    
    def repartitionActions(self, selectedLayer, selectedFeature):
        # Si type de couche = Ligne ou (Point et CP)
        if ( (selectedLayer.wkbType() == 2) or \
            ( (selectedLayer.wkbType() == 1) and (selectedLayer.name().endsWith('_CP') == True) ) ):
            if (selectedLayer.wkbType() == 2): # Si ligne
                if (selectedLayer.name().endsWith('_Bezier') == True): # Si nom contient Bezier
                    # Selection du CP associé et mode edition
                    pass
                    print 2
                elif (FlowUtils(self.iface).isSimpleLineLayer(selectedLayer) == True): # Sinon, si ligne simple 
                    if (FlowUtils(self.iface).getMapCanvasLayerByName(str(selectedLayer.name())+'_CP') == None): # Si couche CP inexistante
                        # Création couche CP
                        # Création CP sur la ligne selectionnée
                        pass
                        print 3
                    else: # Si couche CP existante
                        CPcorrespondant = FlowUtils(self.iface).attachedCP(selectedLayer, selectedFeature)
                        if (CPcorrespondant == None): # Si CP sur ligne n'existe pas
                            # Creation CP + mode edition
                            pass
                            print 4
                        elif (CPcorrespondant[0].wkbType() != 1 ): # Si couche CP existe mais pas de type point
                           pass
                           print "erreur, cette couche ne correspond pas aux CP attendus"
                        else: # Si CP sur ligne existe
                            # Selection du CP + mode edition
                            pass
                            print 5
                else: # Ligne non simple, non Bezier.
                    pass
                    print "ligne non simple"
            elif ( (selectedLayer.wkbType() == 1) and (selectedLayer.name().endsWith('_CP') == True) ): # Si point CP
                    # Mode edition
                    pass
                    print 6
        else:
            # Message d'avertissement
            print "fail" 
        
            

        
