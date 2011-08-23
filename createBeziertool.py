# -*- coding: latin1 -*-

"""
Outil de création de courbes de Bezier, utilise les fonctions décrites dans createBezier.py
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

class CreateBezierTool():
    
    def __init__(self, plugin):
        plugin.testprint()
        abc = 12
        ## Save reference to the QGIS interface.
                         
    def initGui(self):
        ## Create action that will start plugin configuration.
        self.action = QAction(QIcon(":/icons/icon_Bezier.png"), "createBezier", self.iface.mainWindow())
        self.action.setCheckable(True)      
        
    
        ## Connect to signals for button behaviour.
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)
        
                   
        ## Add button to the plugin toolbar buttonn and add menu entry.
        self.iface.addPluginToMenu(self.action.tr("Nearest"), self.action)
        self.iface.addToolBarIcon(self.action)
              
    def run(self):
        mc = self.canvas
        layer = mc.currentLayer()

        self.tool = FeatureFinderTool(self.canvas)                 
        mc.setMapTool(self.tool)
        self.action.setChecked(True)      
        
        QObject.connect(self.tool, SIGNAL("featureFound(PyQt_PyObject)"), self.selectFeature)                
                   
    def selectFeature(self, result):
        layer = self.canvas.currentLayer()
        layer.removeSelection(False)
        layer.select(result[0],  False)
        self.canvas.refresh()
              
    def deactivate(self):
        self.action.setChecked(False)           

    def unload(self):
        self.iface.removePluginMenu(self.action.tr("Nearest"), self.action)
        self.iface.removeToolBarIcon(self.action)