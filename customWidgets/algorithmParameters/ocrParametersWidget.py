
from PyQt5.QtWidgets import (
    QWidget, QApplication,QDialogButtonBox, QDialog, QHeaderView,
    QAction, QFileDialog, QTableWidgetItem, QMessageBox, QMenu, QScrollBar, QTabWidget, QSizePolicy, QDockWidget
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QCursor, QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QSize
from os import listdir
from os.path import isfile, join

from customWidgets.algorithmParameters.ocrParametersWidget_python import Ui_Form

import cv2

class OcrParametersWidget(QWidget):
    returned = pyqtSignal(str)
    changed = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.make_signal_slot_connections()
        self.init_face_recognition_models()
        self.init_ocr_models()
        self.init_segmentation_models()
        self.set_neigbor_search_box_distance()
        self.set_rotation_interval()
    
    def make_signal_slot_connections(self):
        pass

    def init_face_recognition_models(self):
        face_models = ["dlib", "haar", "ssd"]
        self.ui.comboBox_face_detection_model.addItems( face_models )
    
    def init_segmentation_models(self):
        seg_models = ["Unet"]
        self.ui.comboBox_id_card_seg_model.addItems(seg_models)

    def init_ocr_models(self):
        ocr_models = ['EasyOcr', 'TesseractOcr']
        self.ui.comboBox_ocr_model.addItems(ocr_models)
    
    def set_rotation_interval(self):
        self.ui.lineEdit_rotation_interval.setValidator(QIntValidator())
        self.ui.lineEdit_rotation_interval.setText("60")
    
    def set_neigbor_search_box_distance(self):
        self.ui.lineEdit_neighor_box_distance.setValidator(QIntValidator())
        self.ui.lineEdit_neighor_box_distance.setText("60")
    
    def get_rotation_interval(self):
        return int(self.ui.lineEdit_rotation_interval.text())
    
    def get_neigbor_search_box_distance(self):
        return int(self.ui.lineEdit_neighor_box_distance.text())
    
    def get_face_recognition_model(self):
        return str(self.ui.comboBox_face_detection_model.currentText())
    
    def get_ocr_model(self):
        return str(self.ui.comboBox_ocr_model.currentText())


