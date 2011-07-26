# -*- coding: utf-8 -*-
def name():
  return "PluginFlux"
def description():
  return "This plugin has no real use yet"
def qgisMinimumVersion(): 
  return "1.0" 
def version():
  return "Version 0.2"
def authorName():
  return "Robin"
def classFactory(iface):
  from plugin import PluginFlux
  return PluginFlux(iface)
