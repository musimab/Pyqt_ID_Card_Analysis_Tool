
from PyQt5.QtWidgets import (
    QWidget, QApplication,QDialogButtonBox, QDialog, QHeaderView,
    QAction, QFileDialog, QTableWidgetItem, QMessageBox, QMenu, QScrollBar, QTabWidget, QSizePolicy, QDockWidget
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QCursor
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QSize
from os import listdir
from os.path import isfile, join

from customWidgets.IdCardOutput.ocroutputwidget_python import Ui_Form


class OcrOutputWidget(QWidget):
    returned = pyqtSignal(str)
    changed = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.make_signal_slot_connections()
        
    
    def make_signal_slot_connections(self):
        pass

    def receiveOcrOutputs(self,PersonInfo):

        self.ui.lineEdit_tcno.setText(PersonInfo["Tc"])
        self.ui.lineEdit_name.setText(PersonInfo["Name"])
        self.ui.lineEdit_surname.setText(PersonInfo["Surname"])
        self.ui.lineEdit_date_of_birth.setText(PersonInfo["DateofBirth"])

