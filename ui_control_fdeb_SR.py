from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_fdeb_SR import Ui_Dialog


class ui_Control_FDEB_SR(QDialog, Ui_Dialog):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
