from face_detector import view
from face_detector import model
import cv2

class Controller:
    def __init__(self):
        self.model = model.Model() 
        self.view_app = view.App(self)
        
    def start(self):
        self.view_app.mainloop()
        
    def handle_face_detection(self, frame):
        faces = self.model.detect_face(frame)         
        self.view_app.set_face_coords(faces)
    def handle_sign_up(self):
        self.view_app.open_sign_up_dialog()
def main():
    controller = Controller()
    controller.start()

if __name__ == "__main__":
    main()
