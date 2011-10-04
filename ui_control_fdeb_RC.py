from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_fdeb_RC import Ui_Dialog


class ui_Control_FDEB_RC(QDialog, Ui_Dialog):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
