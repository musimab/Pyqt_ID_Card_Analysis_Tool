import cv2

from matplotlib import pyplot as plt
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,QDialogButtonBox, QDialog, 
    QAction, QFileDialog, QTableWidgetItem, QMessageBox, QMenu, QScrollBar, QTabWidget, QSizePolicy, QDockWidget
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QCursor
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QSize,pyqtSlot,QRunnable, QThreadPool


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
from faceDetectWorker import FaceDetectWorker
import concurrent.futures

class IdCardPhotoAnalyser(QMainWindow):


    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("Icon")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.threadOcr = QThread()

        self.threadpool = QThreadPool()
        

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
    
   
    def context_menu_method(self, pos):
        
        custom_menu = QMenu(self)

        clear_submenu = QMenu(custom_menu)

        #calculate_snr_menu_action = QAction("Calculate SNR", self)

        clear_submenu.setTitle("remove plots")
        custom_menu.addMenu(clear_submenu)
    
        #custom_menu.addAction(calculate_snr_menu_action)

        action_clear_all = QAction("clear all", self)

        clear_submenu.addAction(action_clear_all)
        #clear_submenu.addAction(action_clear_s)

        action_clear_all.triggered.connect(self.display_image_widget.clearAlldisplayedImages)

        pos = self.mapToGlobal(pos)
        custom_menu.move(pos)
        custom_menu.show() 

    def makeSignalSlotConnection(self):

        self.sample_image_selection_widget.sendImageNameandPath.connect(self.startFaceWorkerProcess)
        self.customContextMenuRequested.connect(self.context_menu_method)
    
    @pyqtSlot()
    def noFaceDetected(self):
        QMessageBox.about(self, "Warning", "No Face Detected")
    
    @pyqtSlot()
    def thread_complete(self):
        self.ui.statusbar.showMessage("Faceworker completed", 3000)

    def startOcrWorkerProcess(self, result_img):
        
        ############################ Start Ocr Worker Threading ################################

        ### Algorithm Parameters ####
        neighbor_box_distance = self.ocr_parameters_widget.get_neigbor_search_box_distance()
        
        ocr_method = self.ocr_parameters_widget.get_ocr_model()
        
        ORI_THRESH = 3 # Orientation angle threshold for skew correction
        
        use_cuda = "cuda" if torch.cuda.is_available() else "cpu"
        print("use cuda", use_cuda)
        self.ui.statusbar.showMessage(use_cuda )
        
        model = UnetModel(Res34BackBone(), use_cuda) # id card segmentation model
        nearestBox = NearestBox(distance_thresh = neighbor_box_distance, draw_line=False) # Box finder

        Image2Text = extract_words.ocr_factory(ocr_method = ocr_method, border_thresh=3, denoise = False) # ocr features
        #Image2Text =  OcrFactory().select_ocr_method(ocr_method = ocr_method, border_thresh=3, denoise = False)
        
        self.ocrWorker = OcrWorker(model, nearestBox,  Image2Text, result_img)
        self.ocrWorker.moveToThread(self.threadOcr)
        self.threadOcr.started.connect(self.ocrWorker.run)

        self.ocrWorker.ocr_finished_signal.connect(self.threadOcr.quit)
        self.ocrWorker.ocr_finished_signal.connect(self.ocrWorker.deleteLater)
        #self.threadOcr.finished.connect(self.threadOcr.deleteLater)

        self.ocrWorker.imshowHeatMapImage.connect(self.display_image_widget.displayHeatMapImage)
        self.ocrWorker.imshowMaskImage.connect(self.display_image_widget.displayMaskImage)
        self.ocrWorker.imshowMatchedImage.connect(self.display_image_widget.displayMatchedImage)
        self.ocrWorker.imshowAllBoxImage.connect(self.display_image_widget.displayAllBoxImage)
        self.ocrWorker.sendOcrOutput.connect(self.ocr_output_widget.receiveOcrOutputs)
        self.ocrWorker.sendNoFaceDetectedSignal.connect(self.noFaceDetected)
        self.ocrWorker.sendOrientationAngleSignal.connect(self.ocr_output_widget.receiveOrientationAngleofIdCard)
        
        message_to_ui = "ocr method: "+ str(ocr_method) 
        self.ui.statusbar.showMessage(message_to_ui,6000)
        self.threadOcr.start()
        
    
    @pyqtSlot(object, object)
    def startFaceWorkerProcess(self,data_path, data_item):
        
        face_recognition = self.ocr_parameters_widget.get_face_recognition_model()
        rotation_interval = self.ocr_parameters_widget.get_rotation_interval()
        face_detector = detect_face.face_factory(face_model = face_recognition)
        findFaceID = face_detector.get_face_detector()
        
        ############################# Start Face Detector Thread ####################
        img = cv2.imread(data_path)
        img1 = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)

        faceDetectWorker = FaceDetectWorker(findFaceID, img1, rotation_interval)
        faceDetectWorker.signals.result.connect(self.startOcrWorkerProcess)
        faceDetectWorker.signals.finished.connect(self.thread_complete)
        faceDetectWorker.signals.imshowOriginalImage.connect(self.display_image_widget.displayOriginalImage)
        faceDetectWorker.signals.imshowFaceImage.connect(self.display_image_widget.displayFaceImage)
        faceDetectWorker.signals.imshowRotatedImage.connect(self.display_image_widget.displayRotatedImage)
        faceDetectWorker.signals.imshowFaceImage.connect(self.ocr_output_widget.set_face_map_to_label)
        faceDetectWorker.signals.sendNoFaceDetectedSignal.connect(self.noFaceDetected)

        #faceDetectWorker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(faceDetectWorker)
        


app = QApplication([])
window = IdCardPhotoAnalyser()
window.show()
app.exec_()
