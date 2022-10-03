from abc import abstractmethod
import easyocr
import keras_ocr
import pytesseract
import cv2
import numpy as np
from matplotlib import pyplot as plt
import json
import os
from abc import ABC

"""
    There are 2 types of ocr methods. 
    Retrieves original image and target box coordinates 
    (id no, first name, last name, date of birth) 
    and saves txt outputs in json format
"""

CardInfo = {}



class JsonData:

    def __init__(self) -> None:
        
        self.text_output = {}
        self.data_path = 'test/predictions_json'
        self.dict_path = self.data_path +  '/data.json'
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def saveDict(self, dict_name):
        
        with open(self.dict_path, 'w', encoding='utf-8') as fp:
            json.dump(dict_name, fp, ensure_ascii = False)
    
    def loadDict(self):
        
        with open(self.dict_path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            print(data)
    

class Ocr(ABC):
    
    @abstractmethod
    def ocrOutput(self, img_name, img, bbox)->dict:
        """ Return text outputs"""
    
    @abstractmethod
    def cropRoi(self, img, bbox, denoise)->list:
        """ Returns image name list"""
    
    @abstractmethod
    def getonlyDigits(inp_str)->str:
        """ Return numbers in str format"""

    @abstractmethod
    def denoiseImage(img):
        """ Return opencv image"""

class OcrMethod(Ocr):

    def cropRoi(self, img, bbox, denoise):
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        id_infos= ["Tc", "Surname", "Name", "DateofBirth"]
        crop_img_names = []
        lw_thresh = 3
        up_thresh = 3
        for  info, box in zip(id_infos, bbox):
            x, w, y, h = box
            crop_img = img_rgb[y-lw_thresh :y+h+up_thresh, x-lw_thresh:x + w + up_thresh]
                
            if denoise:
                crop_img = self.denoiseImage(crop_img)
                
            if not os.path.exists("outputs/target_crops/"):
                os.makedirs("outputs/target_crops/")
            crop_name = "outputs/target_crops/" + str(info) +".jpg"
            plt.imsave(crop_name, crop_img)
            crop_img_names.append(crop_name) 

        return crop_img_names
        
    def getonlyDigits(self, inp_str):

        num = ""
        for c in inp_str:
            if c.isdigit():
                num = num + c
        return num
        
    def denoiseImage(self, img):
        
        img_denoise = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        imgGray = cv2.cvtColor(img_denoise , cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
        ret, imgf = cv2.threshold(imgBlur , 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #imgf contains Binary image
            
        kernel = np.ones((1,1), np.uint8)
        img_dilation = cv2.dilate( imgf, kernel, iterations=1)
        img_erosion = cv2.erode(img_dilation , kernel, iterations=1)

        return img_erosion   

class EasyOcr(OcrMethod):
    
    def __init__(self, border_thresh, denoise,) -> None:

        self.reader = easyocr.Reader(['tr','en'])
        self.denoise = denoise
        self.BORDER_THRSH = border_thresh
    
    def ocrOutput(self, img_name, img, bbox):
        """
        it saves the txt outputs as a json format
        """
        crop_img_names = self.cropRoi(img, bbox, self.denoise)
    
        id_infos= ["Tc", "Surname", "Name", "DateofBirth"]
        jsonData = JsonData()
        text_output = {"Tc":"", "Surname":"", "Name":"", "DateofBirth":""}
        for info, img  in zip(id_infos, crop_img_names):
            result = self.reader.readtext(img)
            if(len(result)):
                box, text, prob = result[0]
                text_output[info] = text.upper()
        
        text_output["DateofBirth"] = self.getonlyDigits(text_output["DateofBirth"])
       
        CardInfo[img_name] = text_output
        jsonData.saveDict(CardInfo)
        
        return text_output 

class TesseractOcr(OcrMethod):
    
    def __init__(self, border_thresh, denoise,) -> None:
        self.denoise = denoise
        self.BORDER_THRSH = border_thresh
        
    def ocrOutput(self, img_name, img, bbox):
        """
        it saves the txt outputs as a json format
        """
        crop_img_names = self.cropRoi(img, bbox, self.denoise)
        id_infos= ["Tc", "Surname", "Name", "DateofBirth"]
        jsonData = JsonData()        
        text_output = {"Tc":"", "Surname":"", "Name":"", "DateofBirth":""}
        for info, img  in zip(id_infos, crop_img_names):
            text = pytesseract.image_to_string(img)
            
            text_output[info] = text.upper()
        
        text_output["DateofBirth"] = self.getonlyDigits(text_output["DateofBirth"])
       
        CardInfo[img_name] = text_output
        jsonData.saveDict(CardInfo)
        
        return text_output

class OcrFactory:
    
    @staticmethod
    def select_ocr_method(ocr_method,  border_thresh = 3, denoise = False):
        
        if(ocr_method == "EasyOcr"):
            return EasyOcr(border_thresh, denoise)
        
        if(ocr_method == "TesseractOcr"):
            return TesseractOcr(border_thresh, denoise)
        print("Invalid Mehod")
        return -1


def ocr_factory(ocr_method = "EasyOcr", border_thresh = 3, denoise = False):
    
    ocr_factory = {
                    "EasyOcr": EasyOcr,
                    "TesseractOcr": TesseractOcr
                  }
    
    return ocr_factory[ocr_method](border_thresh, denoise) 

