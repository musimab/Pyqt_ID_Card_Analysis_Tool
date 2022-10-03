import cv2

from matplotlib import pyplot as plt
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,QDialogButtonBox, QDialog, 
    QAction, QFileDialog, QTableWidgetItem, QMessageBox, QMenu, QScrollBar, QTabWidget, QSizePolicy, QDockWidget
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QCursor
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QSize, QObject


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


class OcrWorker(QObject):
    ocr_finished_signal = pyqtSignal()
    imshowOriginalImage = pyqtSignal(object, object)
    imshowRotatedImage  = pyqtSignal(object, object)
    imshowHeatMapImage  = pyqtSignal(object, object)
    imshowMaskImage     = pyqtSignal(object, object)
    imshowMatchedImage  = pyqtSignal(object, object, object)
    sendOcrOutput = pyqtSignal(object)

    def __init__(self, segmentation_model, nearestBox ,face_detector,Image2Text, data_path):
        super().__init__()

        #self.sample_image_selection_widget = ImageSearchFolderWidget()
        self.display_image_widget = DisplayImageWidget()
        self.ocr_output_widget = OcrOutputWidget()
        self.ocr_parameters_widget = OcrParametersWidget()

        self.model = segmentation_model
        self.nearestBox = nearestBox
        self.face_detector = face_detector
        self.Image2Text = Image2Text
        self.data_path = data_path
        #self.makeSignalSlotConnection()
        
 

    def makeSignalSlotConnection(self):
        
        self.imshowOriginalImage.connect(self.display_image_widget.displayOriginalImage)
        self.imshowRotatedImage.connect(self.display_image_widget.displayRotatedImage)
        self.imshowHeatMapImage.connect(self.display_image_widget.displayHeatMapImage)
        self.imshowMaskImage.connect(self.display_image_widget.displayMaskImage)
        self.imshowMatchedImage.connect(self.display_image_widget.displayMatchedImage)
        self.sendOcrOutput.connect(self.ocr_output_widget.receiveOcrOutputs)

    def run(self):
        

        ### Algorithm Parameters ####
        neighbor_box_distance = 60
        face_recognition = 'ssd'
        ocr_method = 'EasyOcr'
        rotation_interval = 60
        ORI_THRESH = 3 # Orientation angle threshold for skew correction

        findFaceID = self.face_detector.get_face_detector()

        start = time.time()
        end = 0
        
            
        img = cv2.imread(self.data_path)
        img1 = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        print("Thread Image########################")
        
        self.imshowOriginalImage.emit(img1, "Original Image")
        
        final_img = findFaceID.changeOrientationUntilFaceFound(img1, rotation_interval)
            
        if(final_img is None):
            print(f"No face detected in identity card {1}")
            return 

        final_img = utlis.correctPerspective(final_img)

        self.imshowRotatedImage.emit(final_img, "Rotated Image")
        
        txt_heat_map, regions = utlis.createHeatMapAndBoxCoordinates(final_img)
            
        txt_heat_map = cv2.cvtColor(txt_heat_map, cv2.COLOR_BGR2RGB)

        ## Send Heatmap to mpl widget
        self.imshowHeatMapImage.emit(txt_heat_map, "Character Density Map")
            
        predicted_mask = self.model.predict(txt_heat_map)
        
        self.imshowMaskImage.emit(predicted_mask, "Mask Image")

        orientation_angle = utlis.findOrientationofLines(predicted_mask.copy())
        print("Orientation of Tc ID Card is {} ".format(orientation_angle))
            
        if ( abs(orientation_angle) > ORI_THRESH ):
                
            print("Absulute orientation_angle is greater than {}".format(ORI_THRESH)  )

            final_img = utlis.rotateImage(orientation_angle, final_img)

            txt_heat_map, regions = utlis.createHeatMapAndBoxCoordinates(final_img)
            txt_heat_map = cv2.cvtColor(txt_heat_map, cv2.COLOR_BGR2RGB)
            predicted_mask = self.model.predict(txt_heat_map)

        
        bbox_coordinates , box_centers = getBoxRegions(regions)
            
        mask_centers = getCenterOfMasks(predicted_mask)

        # centers ratio for 4 boxes
        centers_ratio_mask = getCenterRatios(predicted_mask, mask_centers) 

        # centers ratio for all boxes
        centers_ratio_all = getCenterRatios(final_img, box_centers) 
        
        matched_box_indexes = matchCenters(centers_ratio_mask , centers_ratio_all)
            
        new_bboxes = self.nearestBox.searchNearestBoundingBoxes(bbox_coordinates, matched_box_indexes, final_img)
        
        PersonInfo = self.Image2Text.ocrOutput(self.data_path, final_img, new_bboxes)

        self.sendOcrOutput.emit(PersonInfo)
        print(" ")
        for id, val in PersonInfo.items():
            print(id,':' ,val)
        print(" ")
        end = time.time()

        
        
        #utlis.displayMachedBoxes(final_img, new_bboxes)

        self.imshowMatchedImage.emit(final_img, "Final Image", new_bboxes)
            
        #utlis.displayAllBoxes(final_img, bbox_coordinates)
        

        self.ocr_finished_signal.emit()


def getCenterRatios(img, centers):
    """
    Calculates the position of the centers of all boxes 
    in the ID card image and Unet Mask relative to the width and height of the image 
    and returns these ratios as a numpy array.
    """
    if(len(img.shape) == 2):
        img_h, img_w = img.shape
        ratios = np.zeros_like(centers, dtype=np.float32)
        for i, center in enumerate(centers):
            ratios[i] = (center[0]/img_w, center[1]/img_h)
        return ratios
    else :
        img_h, img_w,_ = img.shape
        ratios = np.zeros_like(centers, dtype=np.float32)
        for i, center in enumerate(centers):
            ratios[i] = (center[0]/img_w, center[1]/img_h)
        return ratios


def matchCenters(ratios1, ratios2):
    """
    It takes the ratio of the centers of the regions 
    included in the mask and CRAFT result on the image 
    and maps them according to the absolute distance. 
    Returns the index of the centers with the lowest absolute difference accordingly
    """

    bbb0 = np.zeros_like(ratios2)
    bbb1 = np.zeros_like(ratios2)
    bbb2 = np.zeros_like(ratios2)
    bbb3 = np.zeros_like(ratios2)

    for i , r2 in enumerate(ratios2):
        bbb0[i] = abs(ratios1[0] - r2)
        bbb1[i] = abs(ratios1[1] - r2)
        bbb2[i] = abs(ratios1[2] - r2)
        bbb3[i] = abs(ratios1[3] - r2)

    sum_b0 = np.sum(bbb0, axis = 1)
    sum_b0 = np.reshape(sum_b0, (-1, 1))
    arg_min_b0 = np.argmin(sum_b0, axis=0)

    sum_b1 = np.sum(bbb1, axis = 1)
    sum_b1 = np.reshape(sum_b1, (-1, 1))
    arg_min_b1 = np.argmin(sum_b1, axis=0)

    sum_b2 = np.sum(bbb2, axis = 1)
    sum_b2 = np.reshape(sum_b2, (-1, 1))
    arg_min_b2 = np.argmin(sum_b2, axis=0)

    sum_b3 = np.sum(bbb3, axis = 1)
    sum_b3 = np.reshape(sum_b3, (-1, 1))
    arg_min_b3 = np.argmin(sum_b3, axis=0)

    return np.squeeze(arg_min_b0), np.squeeze(arg_min_b1), np.squeeze(arg_min_b2),np.squeeze(arg_min_b3)         



def getCenterOfMasks(thresh):
    """
    Find centers of 4 boxes in mask from top to bottom with unet model output and return them
    """
    
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by size from smallest to largest
    contours = sorted(contours, key = cv2.contourArea, reverse=False)
    
    contours = contours[-4:] # get the 4 largest contours

    #print("size of cnt", [cv2.contourArea(cnt) for cnt in contours])
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    
    # Sort the 4 largest regions from top to bottom so that we filter the relevant regions
    (cnts, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes),key=lambda b:b[1][1], reverse=False))
    
    detected_centers = []
 
    for contour in cnts:
        (x,y,w,h) = cv2.boundingRect(contour)
        #cv2.rectangle(thresh, (x,y), (x+w,y+h), (255, 0, 0), 2)
        cX = round(int(x) + w/2.0)
        cY = round(int(y) + h/2.0)
        detected_centers.append((cX, cY))
        #cv2.circle(thresh, (cX, cY), 7, (255, 0, 0), -1)

    return np.array(detected_centers)


def getBoxRegions(regions):
    """
    The coordinates of the texts on the id card are converted 
    to x, w, y, h type and the centers and coordinates of these boxes are returned.
    """
    boxes = []
    centers = []
    for box_region in regions:

        x1,y1, x2, y2, x3, y3, x4, y4 = np.int0(box_region.reshape(-1))
        x = min(x1, x3)
        y = min(y1, y2)
        w = abs(min(x1,x3) - max(x2, x4))
        h = abs(min(y1,y2) - max(y3, y4))

        cX = round(int(x) + w/2.0)
        cY = round(int(y) + h/2.0)
        centers.append((cX, cY))
        bbox = (int(x), w, int(y), h)
        boxes.append(bbox)

    #print("number of detected boxes", len(boxes))
    return np.array(boxes), np.array(centers)



