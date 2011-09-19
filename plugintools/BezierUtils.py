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
            if (selectedLayer.wkbType() == 2): # Si ligne
                if (selectedLayer.name().endsWith('_Bezier') == True): # Si nom contient Bezier
                    # Selection du CP associé et mode edition
                    pass
                elif (FlowUtils(self.iface).isSimpleLineLayer(selectedLayer) == True): # Sinon, si ligne simple 
                    if (FlowUtils(self.iface).getMapCanvasLayerByName(selectedLayer.name()+'_CP') == None): # Si couche CP inexistante
                        # Création couche CP
                        # Création CP sur la ligne selectionnée
                        pass
                    else: # Si couche CP existante
                        CPcorrespondant = FlowUtils(self.iface).attachedCP(selectedLayer, selectedFeature)
                        if (CPcorrespondant == None): # Si CP sur ligne n'existe pas
                            # Creation CP + mode edition
                            pass
                        else: # Si CP sur ligne existe
                            # Selection du CP + mode edition
                            pass
            elif ( (selectedLayer.wkbType() == 1) and (selectedLayer.name().endsWith('_CP') == True) ): # Si point CP
                    # Mode edition
                    pass
        else:
            # Message d'avertissement
            print "fail" 
        
            

        
        