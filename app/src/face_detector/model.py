import cv2
import serial
import os
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

    def face_identifier(self, frame): 
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)

        faces = self.face_cascade.detectMultiScale(frame_gray)

        return faces 


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
        return 0

    def update_dataset(self, user_data, frame, faces):
        if not os.path.isdir(f"data/user.{user_data['id']}"):
            os.makedirs(f"data/user.{user_data['id']}")
            self.curr_idx = 0
        if self.curr_idx < 100:
            for (x,y,w,h) in faces:
                cv2.imwrite(f"data/user.{user_data['id']}/user.{user_data['id']}.{self.curr_idx}.png", frame[y:y+h, x:x+w])
                self.curr_idx += 1
            return False
        else:
            return True

        
