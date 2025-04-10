from face_detector import view
from face_detector import model
import cv2

class Controller:
    def __init__(self):
        self.model_app = model.Model() 
        self.view_app = view.App(self)
        
    def start(self):
        self.view_app.mainloop()
        
    def handle_face_detection(self, frame):
        faces = self.model_app.detect_face(frame)         
        self.view_app.set_face_coords(faces)


    def handle_sign_up(self, frame=None, faces=None):
        user_data = None
        if not self.view_app.sign_up:
            self.view_app.open_sign_up_dialog()
            
            if self.view_app.user_data is None:
                print("Operação foi cancelada, saindo do controller")
                self.view_app.sign_up = False
                return

            self.view_app.sign_up = True
        
            self.view_app.user_data["id"] = self.model_app.add_user_to_db(user_data)

        else:
            isfull = self.model_app.update_dataset(self.view_app.user_data, frame, faces)
            if isfull:
                self.view_app.sign_up = False
                print("Data set concluído")


def main():
    controller = Controller()
    controller.start()

if __name__ == "__main__":
    main()
