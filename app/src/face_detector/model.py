import cv2
import serial
import os
import mysql.connector
import base64
import cv2
import time

# TODO: Implement User class
class User:
    def __init__(self, id, name, cpf, tipo, cadastro_valido_ate):
        self.id = id
        self.name = name
        self.cpf = cpf
        self.tipo = tipo
        self.cadastro_valido_ate = cadastro_valido_ate

# TODO: Implement Access class
class Access:
    def __init__(self, usuario_id, autorizado, imagem_base64, timestamp=None):
        self.usuario_id = usuario_id  # pode ser None se for não autorizado
        self.autorizado = autorizado
        self.imagem_base64 = imagem_base64
        self.timestamp = timestamp
        # timestamp ficou none por essa atibuição fica a cargo do banco de dados definir

# TODO: FaceDetectionDB class
import mysql.connector

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

    def add_user(self, user):
               # O campo 'cadastro_valido_ate' deve estar no formato 'YYYY-MM-DD'
        # Os tipos de cadastro são: Aluno, Professor, Técnico, Terceirizado ou Visitante
        query = """
        INSERT INTO usuarios (nome, CPF, tipo, cadastro_valido_ate)
        VALUES (%s, %s, %s, %s)
        """
        values = (user.name, user.cpf, user.tipo, user.cadastro_valido_ate)
        self.cursor.execute(query, values)
        self.conexao.commit()
        return self.cursor.lastrowid  # retorna o id do novo usuário

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

    def frame_to_base64(frame):
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode('utf-8')

        
