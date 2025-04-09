import cv2
import serial


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
        pass

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
