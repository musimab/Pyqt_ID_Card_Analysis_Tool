import cv2

from matplotlib import pyplot as plt
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,QDialogButtonBox, QDialog, 
    QAction, QFileDialog, QTableWidgetItem, QMessageBox, QMenu, QScrollBar, QTabWidget, QSizePolicy, QDockWidget
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QCursor
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QSize


from main_window_ui import Ui_MainWindow
from customWidgets.imageSearchFolder.imageSearchFolderWidget import ImageSearchFolderWidget
from customWidgets.displayImage.displayImageWidget import DisplayImageWidget
from customWidgets.IdCardOutput.ocrOutputWidget import OcrOutputWidget
from customWidgets.algorithmParameters.ocrParametersWidget import OcrParametersWidget


from identityCardRecognition import utlis
import numpy as np
import torch
from identityCardRecognition.find_nearest_box import NearestBox
from identityCardRecognition.pytorch_unet.unet_predict import UnetModel
from identityCardRecognition.pytorch_unet.unet_predict import Res34BackBone
from identityCardRecognition.extract_words import OcrFactory
from identityCardRecognition import extract_words
import os
import time
import argparse
from identityCardRecognition import detect_face
from ocrWorker import OcrWorker

class IdCardPhotoAnalyser(QMainWindow):


    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("Icon")
        self.threadOcr = QThread()

        self.sample_image_selection_widget = ImageSearchFolderWidget()
        self.display_image_widget = DisplayImageWidget()
        self.ocr_output_widget = OcrOutputWidget()
        self.ocr_parameters_widget = OcrParametersWidget()

        self.setCentralWidget(self.display_image_widget)
       

        self.addImageSearchFolderDockWidget()
        self.addOcrOutputDockWidget()
        self.makeSignalSlotConnection()
        self.show()

    
    def addImageSearchFolderDockWidget(self):
        sample_image_selection_dockwidget = QDockWidget("Sample Image Selection", self)
        sample_image_selection_dockwidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        sample_image_selection_dockwidget.setWidget(self.sample_image_selection_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea,sample_image_selection_dockwidget)
    
    def addOcrOutputDockWidget(self):

        parameters_widget_tab = QTabWidget()

        parameters_widget_tab.addTab(self.ocr_output_widget, "Ocr Results")
        parameters_widget_tab.addTab(self.ocr_parameters_widget, "Ocr Parameters")
        parameters_widget_tab.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding))
        
        ocr_result_dockwidget = QDockWidget("Algorithm Parameters", self)
        ocr_result_dockwidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        ocr_result_dockwidget.setWidget(parameters_widget_tab)

        self.addDockWidget(Qt.RightDockWidgetArea, ocr_result_dockwidget)

    def makeSignalSlotConnection(self):

        self.sample_image_selection_widget.sendImageNameandPath.connect(self.getDataPathandItem)
       
    
    def getDataPathandItem(self,data_path, data_item):
        
        
        ### Algorithm Parameters ####
        neighbor_box_distance = 60
        face_recognition = 'ssd'
        ocr_method = 'EasyOcr'
        rotation_interval = 60
        ORI_THRESH = 3 # Orientation angle threshold for skew correction
        
        use_cuda = "cuda" if torch.cuda.is_available() else "cpu"
        
        model = UnetModel(Res34BackBone(), use_cuda)
        nearestBox = NearestBox(distance_thresh = neighbor_box_distance, draw_line=False)
        face_detector = detect_face.face_factory(face_model = face_recognition)
        findFaceID = face_detector.get_face_detector()
        #Image2Text = extract_words.ocr_factory(ocr_method = args.ocr_method, border_thresh=3, denoise = False)
        Image2Text =  OcrFactory().select_ocr_method(ocr_method = ocr_method, border_thresh=3, denoise = False)
        
        start = time.time()
        end = 0
        ############################ Start Threading ################################3
        
        self.ocrWorker = OcrWorker(model, nearestBox, face_detector,Image2Text, data_path)
        self.ocrWorker.moveToThread(self.threadOcr)

        self.threadOcr.started.connect(self.ocrWorker.run)

        self.ocrWorker.ocr_finished_signal.connect(self.threadOcr.quit)
        self.ocrWorker.ocr_finished_signal.connect(self.ocrWorker.deleteLater)
        #self.threadOcr.finished.connect(self.threadOcr.deleteLater)

        self.ocrWorker.imshowOriginalImage.connect(self.display_image_widget.displayOriginalImage)
        self.ocrWorker.imshowRotatedImage.connect(self.display_image_widget.displayRotatedImage)
        self.ocrWorker.imshowHeatMapImage.connect(self.display_image_widget.displayHeatMapImage)
        self.ocrWorker.imshowMaskImage.connect(self.display_image_widget.displayMaskImage)
        self.ocrWorker.imshowMatchedImage.connect(self.display_image_widget.displayMatchedImage)
        self.ocrWorker.sendOcrOutput.connect(self.ocr_output_widget.receiveOcrOutputs)
        
        self.threadOcr.start()
        



app = QApplication([])
window = IdCardPhotoAnalyser()
window.show()
app.exec_()
