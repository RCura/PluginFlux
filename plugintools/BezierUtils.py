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
        pass
        # Si type de couche = Ligne ou (Point et CP)
        if ( (selectedLayer.wkbType() == 2) or \
            ( (selectedLayer.wkbType() == 1) and (selectedLayer.name().endsWith('_CP') == True) ) ):
                pass
                # Si ligne :
                if (selectedLayer.wkbType() == 2):
                    # Si nom contient Bezier
                    if (selectedLayer.name().endsWith('_CP') == True):
                        # Selection du CP associé et mode edition
                        pass
                    # Sinon, si ligne simple :    
                    elif (test ligne simple):
                        # Si couche CP inexistante :
                            if (FlowUtils(self.iface).getMapCanvasLayerByName(selectedLayer.name()+'_CP') == None):
                                # Création couche CP
                                # Création CP sur la ligne selectionnée
                                pass
                            # Si couche CP existante :     
                            else:
                                # Si CP sur ligne n'existe pas :
                                if (testCPsurligne):
                                    # Creation CP + mode edition
                                    pass
                                # Si CP sur ligne existe :
                                else:
                                    # Selection du CP + mode edition
                                    pass
                # Si point CP
                elif (testPointCP):
                    # Mode edition
                    pass
        # Sinon :
        else:
            # Message d'avertissement
            print "fail" 
        
            

        
        