import cv2

import numpy as np
import cv2
from ultralytics import YOLO
import random
#import EMAILSender


def startDetection(filename,mobilenumber):
    
    frame=cv2.imread("download//"+filename)
    model_pothole = YOLO("model/plant_identification_best.pt","v8") 
   
   
    detect_params_pothole = model_pothole.predict(source=[frame], conf=0.1, save=False)
       # detect_params_roadhumps = model_roadhump.predict(source=[frame], conf=0.1, save=False)
    class_list=["Apple_Leaf","Banana_Leaf","Brinjal_Leaf","Coconut_Leaf","Coriander_Leaf","Corn_Leaf",
                    "Cotton_Leaf","Kiwi_Leaf","Lemon_Leaf","Mango_Leaf","Neem_Leaf","Oak_Leaf","Papaya_Leaf",
                    "Peepal_Leaf","Potato_Leaf","Soyabean_Leaf","Strawberry_Leaf","Sweet_Potato_Leaf",
                    "Tamarind_Leaf","Tomato_Leaf"]
    for box in detect_params_pothole[0].boxes:
        clsID = box.cls.numpy()[0]
        conf = box.conf.numpy()[0]
        bb = box.xyxy.numpy()[0]
        
        x1 = int(bb[0])
        x2 = int(bb[2])
        y1 = int(bb[1])
        y2 = int(bb[3])
           
        
        value=round(conf, 3)
            #print("value ",value)
        if(value>0.1):
            text=class_list[int(clsID)]
            text_file_path="Leaf//"+text+"//"+"info.txt"
            print("Plant is "+text)
            print("text_file_path :"+text_file_path)
            with open(text_file_path, 'r') as file:
                file_content = file.read()
                
            import WhatsAPPSender
            imagepath="download//"+filename
            WhatsAPPSender.sendInfoWA(mobilenumber, imagepath, text, file_content)
            
            