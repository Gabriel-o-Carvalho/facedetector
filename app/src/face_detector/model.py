import cv2
import serial
import os
import numpy as np
from PIL import Image
import mysql.connector
import cv2
import shutil
# TODO: Implement User class
class User:
    def __init__(self, id, name, cpf, type, valid):
        self.id = id
        self.name = name
        self.cpf = cpf
        self.type = type
        self.valid = valid

# TODO: Implement Access class
class Access:
    def __init__(self, usuario_id, autorizado, imagem_base64, timestamp=None):
        self.usuario_id = usuario_id  # pode ser None se for não autorizado
        self.autorizado = autorizado
        self.imagem_base64 = imagem_base64
        self.timestamp = timestamp
        # timestamp ficou none por essa atibuição fica a cargo do banco de dados definir

# TODO: FaceDetectionDB class

class FaceDetectionDB:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            database="controle_acesso_dee"
        )
        self.cursor = self.conexao.cursor() 
        self.user_list = {}
        
        query = """
        SELECT id, nome FROM usuarios 
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for line in result:
            self.user_list[str(line[0])] = line[1]

    def add_user(self, user):
               # O campo 'cadastro_valido_ate' deve estar no formato 'YYYY-MM-DD'
        # Os tipos de cadastro são: Aluno, Professor, Técnico, Terceirizado ou Visitante
        query = """
        INSERT INTO usuarios (nome, CPF, tipo, cadastro_valido_ate)
        VALUES (%s, %s, %s, %s)
        """
        values = (user.name, user.cpf, user.type, user.valid)
        self.cursor.execute(query, values)
        id = self.cursor.lastrowid
        print("O novo id é:",id)
        self.user_list[str(id)] = user.name
        self.conexao.commit()
        return id # retorna o id do novo usuário
    
    def remove_user(self, user):
        query = """
        DELETE FROM usuarios WHERE id = %s
        """
        self.cursor.execute(query, user.id)
        self.cursor.commit()

    def add_access(self, access):
        query = """
        INSERT INTO log_acesso (usuario_id, autorizado, imagem_base64, timestamp)
        VALUES (%s, %s, %s, NOW())
        """
        self.cursor.execute(query, (access.usuario_id, access.autorizado, access.imagem_base64))
        self.conexao.commit()

    def remove_user(self, user_id):
        self.cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        self.conexao.commit()
        del self.user_list[user_id]

    
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
        self.classifier = cv2.face.LBPHFaceRecognizer_create()
        self.classifier.train(faces, ids)
        self.classifier.write(f"{data_dir}/classifier.xml")
        
    def predict(self, face):

        return self.classifier.predict(face)

# TODO: Implement Locker class
class Locker:
    def __init__(self, port="COM4", baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.arduino = None

    def connect(self):
        self.arduino = serial.Serial(self.port, self.baud_rate, timeout=5)
    
    def enable_access(self):
        if self.arduino and self.arduino.isOpen():
            self.arduino.write(b'1')
    
    def block_access(self):
        if self.arduino and self.arduino.isOpen():
            self.arduino.write(b'0')
            print("Acesso negado: usuário não reconhecido.")

class Model:
    def __init__(self):
        self.db = FaceDetectionDB()
        self.locker = Locker("/dev/ttyUSB0", 9600)
        self.face_model = FaceDetectorModel()
        self.curr_idx = 0

    def detect_face(self, frame):
        return self.face_model.face_identifier(frame) 

    def add_user_to_db(self, user_data): 
        return self.db.add_user(user_data)  
    

    def remove_user_from_db(self, user_id):
        self.db.remove_user(user_id)     
        shutil.rmtree(f"data/user.{user_id}")


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
        id, pred = self.face_model.predict(frame[y:y+h,x:x+w])
     
        name = self.db.user_list[str(id)]
        return name, pred
        

