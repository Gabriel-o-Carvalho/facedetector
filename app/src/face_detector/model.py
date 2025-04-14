from os.path import isfile
import cv2
import serial
import os
import numpy as np
from PIL import Image
# TODO: Implement User class
class User:
    def __init__(self, id, name):
        pass

# TODO: Implement Access class
class Access:
    def __init__(self, schedule, blocked):
        pass

# TODO: FaceDetectionDB class
class FaceDetectionDB:
    def __init__(self):
        pass
        
    def add_user(self, user):
        pass

    def add_access(self):
        pass

    def remove_user(self):
        pass

class FaceDetectorModel:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier()
        self.face_cascade.load("app/models/haarcascade_hand.xml") 

        self.classifier = cv2.face.LBPHFaceRecognizer_create()
        
        if os.path.isfile("data/classifier.xml"):
           self.classifier.read("data/classifier.xml")
            
    def face_identifier(self, frame): 
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)

        faces = self.face_cascade.detectMultiScale(frame_gray)

        return faces

    def train(self):
        faces = []
        ids = []
        data_dir = "data/"
        for dir in os.listdir(data_dir):
            print("Dir é: ", dir)
            dir_path = os.path.join(data_dir,dir)
            if os.path.isdir(dir_path):
                for image_file in os.listdir(dir_path):
                    img = Image.open(os.path.join(dir_path, image_file)).convert("L")
                    imageNp=np.array(img, "uint8")
                    id=int(os.path.split(dir)[1].split(".")[1])
                    
                    faces.append(imageNp)
                    ids.append(id)

        ids = np.array(ids)

        self.classifier.train(faces, ids)
        self.classifier.write(f"{data_dir}/classifier.xml")
        
    def predict(self, face):

        return self.classifier.predict(face)

# TODO: Implement Locker class
class Locker:
    def __init__(self, port, baud_rate):
        pass

    def connect(self):
        pass

    def enable_access(self):
        pass

    def block_access(self):
        pass 


class Model:
    def __init__(self):
        self.db = FaceDetectionDB()
        self.locker = Locker("/dev/ttyUSB0", 9600)
        self.face_model = FaceDetectorModel()
        self.curr_idx = 0

    def detect_face(self, frame):
        return self.face_model.face_identifier(frame) 


    def add_user_to_db(self, user_data): 
        return 2

    def update_dataset(self, user_data, frame, faces):
        if not os.path.isdir(f"data/user.{user_data['id']}"):
            os.makedirs(f"data/user.{user_data['id']}")
            self.curr_idx = 0

        if self.curr_idx < 250:
            for (x,y,w,h) in faces:
                cv2.imwrite(f"data/user.{user_data['id']}/user.{user_data['id']}.{self.curr_idx}.png", frame[y:y+h, x:x+w])
                self.curr_idx += 1
            return False
        else:
            return True

    def train_model(self):
        self.face_model.train()

    def predict(self, frame, face):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (x,y,w,h) = face
        return self.face_model.predict(frame[y:y+h,x:x+w])
