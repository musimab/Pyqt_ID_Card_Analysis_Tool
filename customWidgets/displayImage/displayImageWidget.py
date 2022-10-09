
from PyQt5.QtWidgets import (
    QWidget, QApplication,QDialogButtonBox, QDialog, QHeaderView,QVBoxLayout,
    QAction, QFileDialog, QTableWidgetItem, QMessageBox, QMenu, QScrollBar, QTabWidget, QSizePolicy, QDockWidget
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QCursor
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QSize,QEvent, pyqtSlot
from os import listdir
from os.path import isfile, join
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import (MultipleLocator, MaxNLocator, AutoMinorLocator)
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import cv2

class DisplayImageWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.figure = Figure(figsize =(8,4), constrained_layout=True)
        self.canvas = FigureCanvas(self.figure)
        ### Images ###
        self.orig_img = None
        self.rotated_img = None
        self.heatmap_img = None
        self.mask_img = None
        self.final_img = None
        self.face_img = None

        gs = self.figure.add_gridspec(3,5)
        self.ax1 = self.figure.add_subplot(gs[0,0])
        self.ax2 = self.figure.add_subplot(gs[0,1])
        self.ax3 = self.figure.add_subplot(gs[0,2])
        self.ax4 = self.figure.add_subplot(gs[0,3])
        self.ax5 = self.figure.add_subplot(gs[0,4])
        self.ax6 = self.figure.add_subplot(gs[1:,:-3])
        vertical_layout = QVBoxLayout()
        
        vertical_layout.addWidget(self.canvas)

        self.canvas.mpl_connect('button_press_event', self.draw_seperate_figure)
        
        self.setLayout(vertical_layout)
     
        
    
    def make_signal_slot_connections(self):
        pass

    @pyqtSlot(object, object)
    def displayOriginalImage(self, image, img_name):
        
        self.orig_img = image
        self.ax1.set_title(img_name)
        self.ax1.imshow(image)
        plt.show()
        self.ax1.set_axis_off()
        #self.show()
        
    @pyqtSlot(object, object)
    def displayRotatedImage(self, image, img_name):
        
        self.rotated_img = image
        self.ax2.set_title(img_name)
        self.ax2.imshow(image)
        plt.show()
        self.ax2.set_axis_off()
        self.canvas.draw()
    
    @pyqtSlot(object, object)
    def displayHeatMapImage(self, image, img_name):
        self.heatmap_img = image
        self.ax3.set_title(img_name)
        self.ax3.imshow(image)
        plt.show()
        self.ax3.set_axis_off()
        
    @pyqtSlot(object, object)
    def displayMaskImage(self, image, img_name):
        self.mask_img = image
        self.ax4.set_title(img_name)
        self.ax4.imshow(image)
        self.ax4.set_axis_off()
        plt.show()
        self.canvas.draw()

    @pyqtSlot(object, object)
    def displayFaceImage(self, image, img_name):
        self.face_img = image
        self.ax5.set_title(img_name)
        self.ax5.imshow(image)
        plt.show()
        self.ax5.set_axis_off()

    @pyqtSlot(object, object,object)
    def displayMatchedImage(self, image, img_name, new_bboxes):
        for box in new_bboxes:
            x1, w, y1, h = box
            cv2.rectangle(image, (x1, y1), (x1+w, y1+h), (0,0,255), 3)
            cX = round(int(x1) + w/2.0)
            cY = round(int(y1) + h/2.0)
            cv2.circle(image, (cX, cY), 7, (0, 255, 255), -1)

        self.final_img = image
        self.ax6.set_title(img_name)
        self.ax6.imshow(image)
        plt.show()
        self.ax6.set_axis_off()
        self.canvas.draw()
    
    
    """
    Show figure as a seperated image in matplotlib function
    """
    @pyqtSlot()
    def draw_seperate_figure(self, event):

        if event.inaxes and event.dblclick:
            
            plotIndex = self.canvas.figure.axes.index(event.inaxes)
            print("plotindex:", plotIndex)

            if plotIndex  == 0:
                fig, ax = plt.subplots(figsize=(16, 16))
                ax.imshow(self.orig_img)
                ax.set_axis_off()
                
            elif plotIndex  == 1:
                fig, ax = plt.subplots(figsize=(16, 16))
                ax.imshow(self.rotated_img)
                ax.set_axis_off()
            
            elif plotIndex  == 2:
                fig, ax = plt.subplots(figsize=(16, 16))
                ax.imshow(self.heatmap_img)
                ax.set_axis_off()
            
            elif plotIndex  == 3:
                fig, ax = plt.subplots(figsize=(16, 16))
                ax.imshow(self.mask_img)
                ax.set_axis_off()

            elif plotIndex  == 4:
                fig, ax = plt.subplots(figsize=(16, 16))
                ax.imshow(self.face_img)
                ax.set_axis_off()
            elif plotIndex  == 5:
                fig, ax = plt.subplots(figsize=(16, 16))
                ax.imshow(self.final_img)
                ax.set_axis_off()

        
        
        plt.show()
                
                

        
        

