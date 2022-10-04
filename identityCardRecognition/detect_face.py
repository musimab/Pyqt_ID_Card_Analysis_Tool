from abc import abstractmethod
import cv2
import numpy as np
import dlib
from matplotlib import pyplot as plt
from abc import ABC

class FaceDetector(ABC):

    @abstractmethod
    def changeOrientationUntilFaceFound(self, image, rot_interval):
        pass

    @abstractmethod
    def findFace(self,img):
        pass
    
    def rotate_bound(self,image, angle):
        # grab the dimensions of the image and then determine the
        # centre
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        # perform the actual rotation and return the image
        return cv2.warpAffine(image, M, (nW, nH))

    @abstractmethod
    def cropFace(self, image):
        pass


class DlibFaceDetector(FaceDetector):
    def __init__(self) -> None:
        super().__init__()
        self.predictor = dlib.shape_predictor("identityCardRecognition/model/shape_predictor_68_face_landmarks.dat")      
        self.detector = dlib.get_frontal_face_detector()

    def changeOrientationUntilFaceFound(self, image, rot_interval):
        
        img = image.copy()
        angle_max = 0

        for angle in range(0,360, rot_interval):
            
            img_rotated = self.rotate_bound(img, angle)
            is_face_available = self.findFace(img_rotated)
            
            if(is_face_available):
                return img_rotated
        

        return None

    def findFace(self, image):
        
        faces = self.detector(image)
        num_of_faces = len(faces)
        print("Dlib Number of Faces:", num_of_faces )
        if(num_of_faces):
            return True
        return False
    
    def cropFace(self, image):
        rects = self.detector(image)
        for bbox in rects:
            x1 = bbox.left()
            y1 = bbox.top()
            x2 = bbox.right()
            y2 = bbox.bottom()

        return image[y1 :y2, x1:x2]
    

class SsdFaceDetector(FaceDetector):
    def __init__(self) -> None:
        super().__init__()
        modelFile = "identityCardRecognition/model/res10_300x300_ssd_iter_140000.caffemodel"
        configFile = "identityCardRecognition/model/deploy.prototxt.txt"
        self.FaceNet = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    
    def changeOrientationUntilFaceFound(self,image, rot_interval):
        """
        It takes the image and sends it to the face detection model 
        by rotating it at 15 degree intervals and returning the original image 
        according to that angle which has the highest probability of faces in the image.
        """
        img = image.copy()
        face_conf = []
        
        
        for angle in range(0, 360, rot_interval):
            img_rotated = self.rotate_bound(img, angle)
            confidence_score = self.findFace(img_rotated)
            face_conf.append((confidence_score, angle))
            

        face_confidence = np.array(face_conf)
        face_arg_max = np.argmax(face_confidence, axis=0)
        angle_max = face_confidence[face_arg_max[0]][1]

        rotated_img = self.rotate_bound(image, angle_max)
        
        return rotated_img
    
    def findFace(self,img):
        
        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
        (300, 300), (104.0, 117.0, 123.0))
        
        self.FaceNet.setInput(blob)
        faces = self.FaceNet.forward()
        
        for i in range(faces.shape[2]):
            confidence = faces[0, 0, i, 2]
            if confidence > 0.6:
                # compute the (x, y)-coordinates of the bounding box for the object
                box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                
                #print("Confidence:", confidence)
                return confidence
            return 0
    
    def cropFace(self, img):
        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
        (300, 300), (104.0, 117.0, 123.0))
        
        self.FaceNet.setInput(blob)
        faces = self.FaceNet.forward()
        
        for i in range(faces.shape[2]):
            confidence = faces[0, 0, i, 2]
            if confidence > 0.6:
                # compute the (x, y)-coordinates of the bounding box for the object
                box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")
                
                #print("Confidence:", confidence)
            
            return img[y1:y2, x1:x2]
        
        return None
    
    
class HaarFaceDetector(FaceDetector):
    def __init__(self) -> None:
        super().__init__()
        self.  face_cascade = cv2.CascadeClassifier('identityCardRecognition/model/haarcascade_frontalface_default.xml')

    
    def changeOrientationUntilFaceFound(self,image, rot_interval):
        img = image.copy()

        for angle in range(0,360, rot_interval):
            
            img_rotated = self.rotate_bound(img, angle)
            is_face_available = self.findFace(img_rotated)
            
            if(is_face_available):
                return img_rotated
        

        return None

    def findFace(self,img):
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        num_of_faces = len(faces)
            
        if(num_of_faces ):
            print("Haar Number of Faces:", num_of_faces)
            return True
        
        return False
    
    def cropFace(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if(not len(rects)):
            return 
        (x, y, w, h)  = rects
        
        return img[y:y+h, x:x+w]
        
            
        


class FaceFactory(ABC):
    
    @abstractmethod
    def get_face_detector(self) -> FaceDetector:
        """ Returns new face detector """

class DlibModel(FaceFactory):
    
    def get_face_detector(self) -> FaceDetector:
        return DlibFaceDetector()

class SsdModel(FaceFactory):
    
    def get_face_detector(self) -> FaceDetector:
        return SsdFaceDetector()

class HaarModel(FaceFactory):
    
    def get_face_detector(self) -> FaceDetector:
        return HaarFaceDetector()


def face_factory(face_model = "ssd")->FaceFactory:
    """Constructs an face detector factory based on the user's preference."""
    
    factories = {
        "dlib": DlibModel(),
        "ssd" : SsdModel(),
        "haar": HaarModel()
    }
    return factories[face_model]

