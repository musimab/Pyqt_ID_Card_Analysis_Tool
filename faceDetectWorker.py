from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QObject, QRunnable, QThreadPool,pyqtSlot, pyqtSignal

import time
import traceback, sys
from identityCardRecognition.detect_face import FaceFactory
from identityCardRecognition import utlis

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    - finished: No data
    - error:`tuple` (exctype, value, traceback.format_exc() )
    - result: `object` data returned from processing, anything
    - progress: `tuple` indicating progress metadata
    '''
    finished = pyqtSignal()
    result = pyqtSignal(object)
    imshowOriginalImage = pyqtSignal(object, object)
    imshowFaceImage     = pyqtSignal(object, object)
    sendNoFaceDetectedSignal = pyqtSignal()
    #progress = pyqtSignal(tuple)


class FaceDetectWorker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    '''
    def __init__(self, face_detector,  img1, rotation_interval):
        super(FaceDetectWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = face_detector
        self.img  = img1
        self.rotation_interval = rotation_interval
        #self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        #self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them

        self.signals.imshowOriginalImage.emit(self.img, "original image")
        
        result = self.fn.changeOrientationUntilFaceFound(self.img, self.rotation_interval)
        if(result is None):
            self.signals.finished.emit() 
            self.signals.sendNoFaceDetectedSignal.emit()
            return
        final_img = utlis.correctPerspective(result)
        
        self.signals.result.emit(final_img)  # Return the result of the processing

        face_cord_in =  self.fn.cropFace(final_img)
        self.signals.imshowFaceImage.emit(face_cord_in, "Face")
        
        self.signals.finished.emit()  # Done
