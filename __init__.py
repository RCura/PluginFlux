# -*- coding: utf-8 -*-
def name():
  return "Proto1"
def description():
  return "This plugin has no real use yet"
def qgisMinimumVersion(): 
  return "1.0" 
def version():
  return "Version 0.3"
def authorName():
  return "Robin"
def classFactory(iface):
  from plugin import Proto1
  return Proto1(iface)
