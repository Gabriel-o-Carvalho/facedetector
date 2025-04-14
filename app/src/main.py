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
        return faces


    def handle_sign_up(self, frame=None, faces=None):
        if not self.view_app.sign_up:
            self.view_app.open_sign_up_dialog()
            
            if self.view_app.user_data is None:
                print("Operação foi cancelada, saindo do controller")
                self.view_app.sign_up = False
                return
            user = model.User(**self.view_app.user_data) 
            id = self.model_app.add_user_to_db(user)
            print(id)
            self.view_app.user_data["id"] = id
            self.view_app.sign_up = True
        else:
            if self.view_app.user_data is not None:
                isfull = self.model_app.update_dataset(self.view_app.user_data, frame, faces)
                if isfull:
                    self.view_app.sign_up = False
                    print("Data set concluído")
                    self.view_app.is_training = True
    def handle_remove_user(self):
        user_id = self.view_app.open_remove_dialog()
        if user_id is None:
            print("Operação Cancelada!")
        else:
            self.model_app.remove_user_from_db(user_id)
            self.model_app.train_model()
    def handle_access(self, id, enabled):
        self.model_app.add_access(id, enabled)

    def handle_training(self):
        print("Treinando o modelo...")
        self.model_app.train_model()
        print("Treinamento concluído!")
        self.view_app.is_training = False

    def handle_face_prediction(self, frame, face): 
        return self.model_app.predict(frame, face)




def main():
    controller = Controller()
    controller.start()
    
if __name__ == "__main__":
    main()
